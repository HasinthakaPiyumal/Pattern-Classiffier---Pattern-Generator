import random
import time

class PatientAdmission:
    def __init__(self, patient_id, age, primary_diagnosis_group, num_prev_admissions, length_of_stay_days):
        self.patient_id = patient_id
        self.age = age
        self.primary_diagnosis_group = primary_diagnosis_group
        self.num_prev_admissions = num_prev_admissions
        self.length_of_stay_days = length_of_stay_days
        self.initial_risk = "UNKNOWN"
        self.detailed_probability = 0.0
        self.recommended_interventions = []

    def __str__(self):
        return (f"ID:{self.patient_id}, Age:{self.age}, Diag:{self.primary_diagnosis_group}, "
                f"Risk(L):{self.initial_risk}, Prob(C):{self.detailed_probability:.2f}, "
                f"Intv(C):{', '.join(self.recommended_interventions) or 'None'}")

class LightweightEHRModel:
    def assess_risk(self, admission: PatientAdmission) -> str:
        print(f"[{admission.patient_id}] Phase 1 (EHR Client): Assessing...")
        risk = "LOW"
        if admission.age >= 70 or admission.num_prev_admissions >= 2:
            risk = "MEDIUM"
        if admission.age >= 80 and admission.num_prev_admissions >= 3 and admission.primary_diagnosis_group in ["Cardiac", "Respiratory"]:
            risk = "HIGH"
        
        admission.initial_risk = risk
        time.sleep(0.03)
        print(f"[{admission.patient_id}] Phase 1 (EHR Client): Result - Initial Risk:{risk}")
        return risk

class ComplexCloudAnalyticsModel:
    def predict_and_recommend(self, admission: PatientAdmission):
        print(f"[{admission.patient_id}] Phase 2 (Cloud Analytics): Predicting & Recommending...")
        
        base_prob = 0.05
        interventions = []

        if admission.age >= 75: base_prob += 0.15
        if admission.num_prev_admissions >= 3: base_prob += 0.2
        if admission.length_of_stay_days > 10: base_prob += 0.1
        if admission.primary_diagnosis_group == "Cardiac":
            base_prob += 0.15
            interventions.append("Cardiac Rehab")
        if admission.primary_diagnosis_group == "Respiratory":
            base_prob += 0.12
            interventions.append("Pulmonary F/U")
        
        if admission.initial_risk == "HIGH": base_prob += 0.25
        elif admission.initial_risk == "MEDIUM": base_prob += 0.1
            
        if random.random() < 0.1:
            base_prob += 0.2
            interventions.append("Social Worker")

        admission.detailed_probability = min(1.0, base_prob + random.uniform(0, 0.1))
        
        if admission.detailed_probability >= 0.4:
            interventions.append("Home Health")
        if admission.detailed_probability >= 0.6:
            interventions.append("Early F/U Appt")

        admission.recommended_interventions = list(set(interventions))
        
        time.sleep(random.uniform(1.0, 3.0))
        print(f"[{admission.patient_id}] Phase 2 (Cloud Analytics): Result - Prob:{admission.detailed_probability:.2f}, Intv:{admission.recommended_interventions}")

def process_patient_discharge(admission: PatientAdmission, client_model: LightweightEHRModel, cloud_model: ComplexCloudAnalyticsModel):
    print(f"\n--- Processing Discharge for {admission.patient_id} ---")
    
    initial_risk = client_model.assess_risk(admission)
    
    if initial_risk in ["MEDIUM", "HIGH"] or admission.length_of_stay_days > 14:
        print(f"[{admission.patient_id}] Triggering Phase 2.")
        cloud_model.predict_and_recommend(admission)
    else:
        print(f"[{admission.patient_id}] Phase 2 skipped.")
        admission.detailed_probability = 0.05 + random.uniform(0, 0.05)
        admission.recommended_interventions = ["Standard Discharge"]

    print(f"Final assessment: {admission}")

if __name__ == "__main__":
    ehr_client = LightweightEHRModel()
    cloud_analytics = ComplexCloudAnalyticsModel()

    patient_admissions = [
        PatientAdmission("P001", 65, "Orthopedic", 0, 5),
        PatientAdmission("P002", 78, "Cardiac", 1, 7),
        PatientAdmission("P003", 82, "Respiratory", 3, 15),
        PatientAdmission("P004", 55, "Gastrointestinal", 0, 3),
        PatientAdmission("P005", 70, "Neurological", 2, 12),
    ]

    for admission in patient_admissions:
        process_patient_discharge(admission, ehr_client, cloud_analytics)
