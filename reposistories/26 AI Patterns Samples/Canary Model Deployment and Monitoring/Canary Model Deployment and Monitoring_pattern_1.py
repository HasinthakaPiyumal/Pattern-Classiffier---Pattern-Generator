import random
import time

class PatientRiskPredictionModel:
    def __init__(self, version):
        self.version = version
        self.base_accuracy = 0.85 if "stable" in version else 0.88
        self.prediction_time_ms = random.randint(100, 300)

    def predict(self, patient_data):
        time.sleep(self.prediction_time_ms / 1000.0)
        risk_score = random.uniform(0.1, 0.9)
        prediction = "HIGH_RISK" if risk_score > 0.5 else "LOW_RISK"
        return {
            "model_version": self.version,
            "patient_id": patient_data["id"],
            "prediction": prediction,
            "risk_score": risk_score,
            "prediction_time_ms": self.prediction_time_ms
        }

class HealthcareCanaryDeployer:
    def __init__(self, primary_model, canary_model, canary_traffic_percentage):
        self.primary_model = primary_model
        self.canary_model = canary_model
        self.canary_traffic_percentage = canary_traffic_percentage
        self.primary_requests = 0
        self.canary_requests = 0
        self.canary_discrepancies = 0
        self.canary_latencies = []
        self.canary_predictions = []
        self.primary_predictions_for_comparison = []

    def route_request(self, patient_data):
        primary_result = self.primary_model.predict(patient_data)
        self.primary_predictions_for_comparison.append(primary_result)

        if random.uniform(0, 100) < self.canary_traffic_percentage:
            self.canary_requests += 1
            canary_result = self.canary_model.predict(patient_data)
            self._monitor_canary(primary_result, canary_result)
            return canary_result
        else:
            self.primary_requests += 1
            return primary_result

    def _monitor_canary(self, primary_result, canary_result):
        self.canary_latencies.append(canary_result["prediction_time_ms"])
        self.canary_predictions.append(canary_result)

        if primary_result["prediction"] != canary_result["prediction"]:
            self.canary_discrepancies += 1

    def get_monitoring_report(self):
        avg_canary_latency = sum(self.canary_latencies) / len(self.canary_latencies) if self.canary_latencies else 0
        discrepancy_rate = (self.canary_discrepancies / self.canary_requests) * 100 if self.canary_requests > 0 else 0
        return {
            "primary_requests": self.primary_requests,
            "canary_requests": self.canary_requests,
            "canary_discrepancy_rate_vs_primary": discrepancy_rate,
            "avg_canary_latency_ms": avg_canary_latency
        }

    def evaluate_canary(self):
        report = self.get_monitoring_report()
        
        max_acceptable_discrepancy_rate = 5
        max_acceptable_latency = 250

        if report["canary_requests"] < 50:
            return "INSUFFICIENT_DATA"

        if report["canary_discrepancy_rate_vs_primary"] <= max_acceptable_discrepancy_rate and \
           report["avg_canary_latency_ms"] <= max_acceptable_latency:
            return "PROMOTE"
        else:
            return "ROLLBACK"

if __name__ == "__main__":
    print("Healthcare Patient Risk Prediction Canary Deployment Simulation")
    print("Goal: Safely introduce a new patient readmission risk prediction model (v2.1) to ensure no misclassifications before full rollout.")

    primary_model = PatientRiskPredictionModel(version="v2.0_stable")
    canary_model = PatientRiskPredictionModel(version="v2.1_canary")

    canary_traffic_percentage = 10
    deployer = HealthcareCanaryDeployer(primary_model, canary_model, canary_traffic_percentage)

    print(f"Initiating canary deployment for v2.1 with {canary_traffic_percentage}% of patient data requests.")

    for i in range(300):
        patient_data = {"id": f"patient_{i}", "features": [random.random() for _ in range(10)]}
        result = deployer.route_request(patient_data)
        time.sleep(0.02)

        if (i + 1) % 50 == 0:
            report = deployer.get_monitoring_report()
            print(f"\n--- Monitoring Report after {i+1} patient requests ---")
            print(f"Primary model requests: {report['primary_requests']}, Canary model requests: {report['canary_requests']}")
            print(f"Canary Discrepancy Rate vs Primary: {report['canary_discrepancy_rate_vs_primary']:.2f}%")
            print(f"Avg Canary Latency: {report['avg_canary_latency_ms']:.2f} ms")

            decision = deployer.evaluate_canary()
            print(f"Canary Evaluation Decision: {decision}")

            if decision == "PROMOTE":
                print("\nCanary model (v2.1) performs acceptably! It maintains accuracy and meets latency requirements. Considering wider rollout.")
                break
            elif decision == "ROLLBACK":
                print("\nCanary model (v2.1) shows significant discrepancies or performance issues. Rolling back to v2.0 to prevent patient impact.")
                break
            elif decision == "INSUFFICIENT_DATA":
                print("Still gathering sufficient patient data for a confident decision on v2.1.")

    if deployer.evaluate_canary() == "INSUFFICIENT_DATA":
        print("\nCanary deployment for v2.1 ended without a final decision due to insufficient data.")