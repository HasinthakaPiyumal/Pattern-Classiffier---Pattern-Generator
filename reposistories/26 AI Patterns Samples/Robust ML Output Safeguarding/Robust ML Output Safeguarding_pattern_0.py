import random

class MLDiagnosisModel:
    """Simulates an ML model for medical diagnosis."""
    def predict(self, patient_data):
        # In a real scenario, this would be a complex ML inference.
        # For simulation, we'll generate a random diagnosis and confidence.
        symptoms = patient_data.get('symptoms', [])
        lab_results = patient_data.get('lab_results', {})
        age = patient_data.get('age', 30)

        # Simple heuristic for simulation
        if "severe_chest_pain" in symptoms and lab_results.get("troponin") is not None and lab_results.get("troponin") > 0.1:
            diagnosis = "Acute Myocardial Infarction"
            confidence = random.uniform(0.85, 0.99)
        elif "fever" in symptoms and "cough" in symptoms:
            diagnosis = "Viral Infection"
            confidence = random.uniform(0.6, 0.9)
        else:
            diagnosis = "Healthy"
            confidence = random.uniform(0.5, 0.95)

        # Introduce some instability for demonstration
        if random.random() < 0.1: # 10% chance of a slightly off prediction
            diagnosis = random.choice(["Misdiagnosis A", "Misdiagnosis B"])
            confidence = random.uniform(0.4, 0.7)

        return diagnosis, confidence

class MedicalDiagnosisSafeguard:
    """Encapsulates the ML model with deterministic rule-based safeguards."""
    def __init__(self, ml_model):
        self.ml_model = ml_model

    def _apply_deterministic_rules(self, ml_diagnosis, ml_confidence, patient_data):
        final_decision = ml_diagnosis
        action = "ML Recommendation"

        # Rule 1: Low ML confidence requires human review
        if ml_confidence < 0.7:
            action = "Escalate to Human Physician Review (Low Confidence)"
            final_decision = f"Review needed for: {ml_diagnosis}"
            return final_decision, action

        # Rule 2: Specific lab markers override ML for critical conditions
        if patient_data.get("lab_results", {}).get("critical_marker_X") == "positive":
            if ml_diagnosis != "Critical Disease Alpha":
                action = "Override ML: Confirm Critical Disease Alpha (Deterministic Rule)"
                final_decision = "Critical Disease Alpha"
                return final_decision, action

        # Rule 3: High-risk diagnosis with moderate confidence requires secondary confirmation
        if ml_diagnosis in ["Acute Myocardial Infarction", "Stroke"] and ml_confidence < 0.9:
            action = f"Escalate to Specialist & Secondary Diagnostic (High Risk, Moderate Confidence)"
            final_decision = f"Confirm {ml_diagnosis}"
            return final_decision, action

        # Rule 4: Age-specific override (e.g., certain conditions are rare/impossible in infants)
        if patient_data.get('age', 0) < 2 and ml_diagnosis == "Adult-Onset Diabetes":
            action = "Override ML: Unlikely for Age Group (Deterministic Rule)"
            final_decision = "Further investigation, unlikely Adult-Onset Diabetes"
            return final_decision, action

        return final_decision, action

    def get_safe_diagnosis(self, patient_data):
        ml_diagnosis, ml_confidence = self.ml_model.predict(patient_data)
        final_diagnosis, action = self._apply_deterministic_rules(ml_diagnosis, ml_confidence, patient_data)

        # Real-world usage simulation
        print(f"--- Patient ID: {patient_data.get('id', 'N/A')} ---")
        print(f"ML Predicted Diagnosis: {ml_diagnosis} (Confidence: {ml_confidence:.2f})")
        print(f"Safeguard Decision: {final_diagnosis}")
        print(f"Action Taken: {action}\n")
        return final_diagnosis, action

# Real-world usage simulation
if __name__ == "__main__":
    ml_model = MLDiagnosisModel()
    safeguarded_system = MedicalDiagnosisSafeguard(ml_model)

    # Scenario 1: ML low confidence
    patient1 = {"id": "P001", "symptoms": ["fatigue"], "lab_results": {"blood_pressure": "normal"}, "age": 45}
    safeguarded_system.get_safe_diagnosis(patient1)

    # Scenario 2: Critical marker override
    patient2 = {"id": "P002", "symptoms": ["mild_cough"], "lab_results": {"critical_marker_X": "positive", "troponin": 0.05}, "age": 60}
    safeguarded_system.get_safe_diagnosis(patient2)

    # Scenario 3: High risk, moderate confidence (simulated by ML model output)
    patient3 = {"id": "P003", "symptoms": ["severe_chest_pain"], "lab_results": {"troponin": 0.2}, "age": 70}
    safeguarded_system.get_safe_diagnosis(patient3)

    # Scenario 4: ML gives a "safe" diagnosis with high confidence
    patient4 = {"id": "P004", "symptoms": ["headache"], "lab_results": {"blood_count": "normal"}, "age": 30}
    safeguarded_system.get_safe_diagnosis(patient4)

    # Scenario 5: Age-specific override
    patient5 = {"id": "P005", "symptoms": ["thirst"], "lab_results": {"sugar_level": "high"}, "age": 1}
    safeguarded_system.get_safe_diagnosis(patient5)

    # Example of a "misdiagnosis" from the ML model simulation being caught
    print("--- Testing ML instability catch ---")
    for _ in range(3): # Run a few times to potentially hit the random misdiagnosis
        patient_instability = {"id": "P_INST", "symptoms": ["mild_cold"], "lab_results": {}, "age": 25}
        safeguarded_system.get_safe_diagnosis(patient_instability)
