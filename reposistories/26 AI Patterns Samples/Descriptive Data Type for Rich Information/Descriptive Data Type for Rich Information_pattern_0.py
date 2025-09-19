
class DiseaseRisk:
    def __init__(self, value: float, disease_name: str, model_id: str, confidence_score: float, unit: str = 'probability'):
        if not (0.0 <= value <= 1.0):
            raise ValueError("Risk value must be between 0 and 1.")
        if not (0.0 <= confidence_score <= 1.0):
            raise ValueError("Confidence score must be between 0 and 1.")
        self.value = value
        self.disease_name = disease_name
        self.model_id = model_id
        self.confidence_score = confidence_score
        self.unit = unit

    def __repr__(self):
        return (f"DiseaseRisk(disease='{self.disease_name}', value={self.value:.4f}, "
                f"unit='{self.unit}', model='{self.model_id}', confidence={self.confidence_score:.2f})")

    def is_high_risk(self, threshold: float = 0.7):
        return self.value >= threshold

def simulate_risk_prediction(patient_id: str, features: dict) -> DiseaseRisk:
    if 'genetics_marker_A' in features and features['genetics_marker_A'] > 0.8:
        risk_val = 0.92
        conf_score = 0.95
    elif 'age' in features and features['age'] > 60 and features.get('smoker', False):
        risk_val = 0.78
        conf_score = 0.88
    else:
        risk_val = 0.35
        conf_score = 0.75
    
    return DiseaseRisk(
        value=risk_val,
        disease_name="Cardiovascular Disease",
        model_id="CardioRiskNet_v3.2",
        confidence_score=conf_score
    )

if __name__ == "__main__":
    print("--- Healthcare System: Disease Risk Prediction ---")

    patient_data_1 = {"patient_id": "P001", "age": 55, "smoker": True, "bmi": 28.5}
    patient_data_2 = {"patient_id": "P002", "age": 70, "smoker": False, "genetics_marker_A": 0.9}
    patient_data_3 = {"patient_id": "P003", "age": 30, "smoker": False, "bmi": 22.1}

    risk_p1 = simulate_risk_prediction("P001", patient_data_1)
    risk_p2 = simulate_risk_prediction("P002", patient_data_2)
    risk_p3 = simulate_risk_prediction("P003", patient_data_3)

    print(f"\nPatient P001 Risk: {risk_p1}")
    print(f"Is P001 high risk (threshold 0.7)? {risk_p1.is_high_risk()}")

    print(f"\nPatient P002 Risk: {risk_p2}")
    print(f"Is P002 high risk (threshold 0.7)? {risk_p2.is_high_risk()}")

    print(f"\nPatient P003 Risk: {risk_p3}")
    print(f"Is P003 high risk (threshold 0.7)? {risk_p3.is_high_risk()}")

    print("\n--- Clinical Decision Support ---")
    patients_risks = [risk_p1, risk_p2, risk_p3]
    for i, risk in enumerate(patients_risks):
        if risk.is_high_risk(threshold=0.75):
            print(f"Alert: Patient {i+1} has HIGH risk for {risk.disease_name} ({risk.value:.2f}). "
                  f"Model {risk.model_id} reports confidence {risk.confidence_score:.2f}. Recommend further tests.")
        else:
            print(f"Patient {i+1} has moderate/low risk for {risk.disease_name} ({risk.value:.2f}). "
                  f"Model {risk.model_id} reports confidence {risk.confidence_score:.2f}. Continue monitoring.")

    try:
        invalid_risk = DiseaseRisk(1.2, "Invalid Disease", "M1", 0.9)
    except ValueError as e:
        print(f"\nAttempted to create invalid risk: {e}")
