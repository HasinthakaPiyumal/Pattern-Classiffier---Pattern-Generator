import random
import time

class ReadmissionRiskModel:
    def __init__(self):
        self._model_loaded = True

    def predict(self, patient_features: dict) -> float:
        if not self._model_loaded:
            raise RuntimeError("ML model not loaded.")
        
        time.sleep(0.06)
        
        age = patient_features.get("age", 50)
        num_previous_admissions = patient_features.get("num_previous_admissions", 0)
        chronic_conditions = patient_features.get("chronic_conditions", 0)
        last_discharge_summary = patient_features.get("last_discharge_summary", "stable")
        
        risk_score = 0.1
        if age > 70:
            risk_score += 0.2
        if num_previous_admissions > 2:
            risk_score += 0.3
        if chronic_conditions > 1:
            risk_score += 0.25
        if last_discharge_summary == "critical":
            risk_score += 0.4
        
        risk_score += random.uniform(-0.04, 0.04)
        return min(max(risk_score, 0.0), 1.0)

class PatientDataStore:
    def get_patient_medical_history(self, patient_id: str) -> dict:
        time.sleep(0.03)
        return {
            "age": random.randint(30, 90),
            "num_previous_admissions": random.randint(0, 5),
            "chronic_conditions": random.randint(0, 3),
            "last_discharge_summary": random.choice(["stable", "unstable", "critical"]),
            "allergies": ["penicillin"] if random.random() < 0.2 else []
        }

    def get_clinical_guidelines(self, condition: str) -> dict:
        time.sleep(0.01)
        return {"standard_treatment": f"Treatment for {condition}", "follow_up_frequency": "monthly"}

class PatientCareService:
    def __init__(self, risk_model: ReadmissionRiskModel, data_store: PatientDataStore):
        self.risk_model = risk_model
        self.data_store = data_store
        self.HIGH_RISK_THRESHOLD = 0.6

    def admit_patient(self, patient_id: str, admitting_condition: str) -> dict:
        medical_history = self.data_store.get_patient_medical_history(patient_id)
        
        ml_features = {
            "age": medical_history.get("age"),
            "num_previous_admissions": medical_history.get("num_previous_admissions"),
            "chronic_conditions": medical_history.get("chronic_conditions"),
            "last_discharge_summary": medical_history.get("last_discharge_summary")
        }

        readmission_risk_score = self.risk_model.predict(ml_features)

        care_plan_recommendation = "Standard care plan."
        admission_status = "Admitted"
        follow_up_plan = "Regular follow-up."

        if readmission_risk_score >= self.HIGH_RISK_THRESHOLD:
            care_plan_recommendation = "Enhanced care plan: Include daily check-ins, social worker consultation, and home health referral."
            follow_up_plan = "Weekly follow-up for 1 month, then bi-weekly."
            admission_status = "Admitted (High Risk)"
        elif medical_history.get("allergies"):
            care_plan_recommendation += f" Special attention needed for allergies: {', '.join(medical_history['allergies'])}."
        
        guidelines = self.data_store.get_clinical_guidelines(admitting_condition)
        care_plan_recommendation += f" Based on guidelines for {admitting_condition}: {guidelines['standard_treatment']}."
        
        return {
            "patient_id": patient_id,
            "admitting_condition": admitting_condition,
            "admission_status": admission_status,
            "readmission_risk_score": readmission_risk_score,
            "care_plan_recommendation": care_plan_recommendation,
            "follow_up_plan": follow_up_plan
        }

def main_healthcare_app():
    risk_model = ReadmissionRiskModel()
    data_store = PatientDataStore()
    patient_service = PatientCareService(risk_model, data_store)

    patients_to_admit = [
        {"patient_id": "P001", "condition": "Pneumonia"},
        {"patient_id": "P002", "condition": "Heart Failure"},
        {"patient_id": "P003", "condition": "Appendicitis"},
        {"patient_id": "P004", "condition": "Diabetes Management"},
        {"patient_id": "P005", "condition": "Stroke Recovery"}
    ]

    for patient_admission_request in patients_to_admit:
        result = patient_service.admit_patient(
            patient_admission_request["patient_id"],
            patient_admission_request["condition"]
        )
        time.sleep(0.1)

if __name__ == '__main__':
    main_healthcare_app()