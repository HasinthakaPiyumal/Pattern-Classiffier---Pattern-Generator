import random
import time

class ProductRecommendationModel:
    def __init__(self, version):
        self.version = version
        self.latency_ms = random.randint(50, 200)

    def predict(self, user_id):
        time.sleep(self.latency_ms / 1000.0)
        recommended_products = [f"product_{random.randint(100, 999)}" for _ in range(3)]
        return {
            "model_version": self.version,
            "user_id": user_id,
            "recommendations": recommended_products,
            "latency_ms": self.latency_ms
        }

class ECommerceCanaryDeployer:
    def __init__(self, primary_model, canary_model, canary_traffic_percentage):
        self.primary_model = primary_model
        self.canary_model = canary_model
        self.canary_traffic_percentage = canary_traffic_percentage
        self.primary_requests = 0
        self.canary_requests = 0
        self.canary_success_metrics = []
        self.canary_latencies = []

    def route_request(self, user_id):
        if random.uniform(0, 100) < self.canary_traffic_percentage:
            self.canary_requests += 1
            result = self.canary_model.predict(user_id)
            self._monitor_canary(result)
            return result
        else:
            self.primary_requests += 1
            return self.primary_model.predict(user_id)

    def _monitor_canary(self, result):
        simulated_success = random.uniform(0.05, 0.15)
        self.canary_success_metrics.append(simulated_success)
        self.canary_latencies.append(result["latency_ms"])

    def get_monitoring_report(self):
        avg_canary_success = sum(self.canary_success_metrics) / len(self.canary_success_metrics) if self.canary_success_metrics else 0
        avg_canary_latency = sum(self.canary_latencies) / len(self.canary_latencies) if self.canary_latencies else 0
        return {
            "primary_requests": self.primary_requests,
            "canary_requests": self.canary_requests,
            "avg_canary_success_metric": avg_canary_success,
            "avg_canary_latency_ms": avg_canary_latency
        }

    def evaluate_canary(self):
        report = self.get_monitoring_report()
        
        target_success_metric = 0.10
        max_acceptable_latency = 180

        if report["canary_requests"] < 100:
            return "INSUFFICIENT_DATA"

        if report["avg_canary_success_metric"] >= target_success_metric * 0.9 and \
           report["avg_canary_latency_ms"] <= max_acceptable_latency:
            return "PROMOTE"
        else:
            return "ROLLBACK"

if __name__ == "__main__":
    print("E-commerce Product Recommendation Canary Deployment Simulation")
    print("Goal: Safely deploy a new recommendation engine (v1.1) to improve sales without impacting user experience.")

    primary_model = ProductRecommendationModel(version="v1.0_stable")
    canary_model = ProductRecommendationModel(version="v1.1_canary")

    canary_traffic_percentage = 5
    deployer = ECommerceCanaryDeployer(primary_model, canary_model, canary_traffic_percentage)

    print(f"Initiating canary deployment for v1.1 with {canary_traffic_percentage}% of live traffic.")

    for i in range(500):
        user_id = f"user_{i}"
        recommendation = deployer.route_request(user_id)
        time.sleep(0.01)

        if (i + 1) % 100 == 0:
            report = deployer.get_monitoring_report()
            print(f"\n--- Monitoring Report after {i+1} user requests ---")
            print(f"Primary recommendations served: {report['primary_requests']}, Canary recommendations served: {report['canary_requests']}")
            print(f"Avg Canary Success Metric (e.g., Click-Through Rate): {report['avg_canary_success_metric']:.2%}")
            print(f"Avg Canary Latency: {report['avg_canary_latency_ms']:.2f} ms")

            decision = deployer.evaluate_canary()
            print(f"Canary Evaluation Decision: {decision}")

            if decision == "PROMOTE":
                print("\nCanary model (v1.1) performs well! It's meeting performance and quality expectations. Gradual traffic increase or full promotion initiated.")
                break
            elif decision == "ROLLBACK":
                print("\nCanary model (v1.1) shows issues (e.g., lower engagement, higher latency). Rolling back to v1.0 and investigating.")
                break
            elif decision == "INSUFFICIENT_DATA":
                print("Still gathering sufficient user interaction data for a confident decision on v1.1.")

    if deployer.evaluate_canary() == "INSUFFICIENT_DATA":
        print("\nCanary deployment for v1.1 ended without a final decision due to insufficient data.")