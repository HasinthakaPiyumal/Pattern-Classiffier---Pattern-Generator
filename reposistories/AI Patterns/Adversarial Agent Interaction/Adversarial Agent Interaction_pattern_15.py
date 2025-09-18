import random

class AIDiagnosisProposer:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.symptoms_db = {
            "fever_cough": {"diagnosis": "Flu", "treatment": {"medication": "Oseltamivir", "dosage": "75mg BID", "duration": "5 days"}},
            "headache_nausea": {"diagnosis": "Migraine", "treatment": {"medication": "Sumatriptan", "dosage": "50mg PRN", "duration": "as needed"}},
            "chest_pain": {"diagnosis": "Possible Angina", "treatment": {"medication": "Nitroglycerin", "dosage": "0.4mg SL", "duration": "as needed"}},
            "rash_itch": {"diagnosis": "Allergic Reaction", "treatment": {"medication": "Diphenhydramine", "dosage": "25mg TID", "duration": "3 days"}}
        }

    def propose_diagnosis_and_treatment(self, symptoms):
        diagnosis_info = self.symptoms_db.get(symptoms, {"diagnosis": "Unspecified Condition", "treatment": {"medication": "Supportive Care", "dosage": "N/A", "duration": "N/A"}})
        return {
            "patient_id": self.patient_id,
            "symptoms": symptoms,
            "diagnosis": diagnosis_info["diagnosis"],
            "treatment": diagnosis_info["treatment"]
        }

class TreatmentSafetyValidator:
    def __init__(self, patient_allergies=None, known_contraindications=None):
        self.patient_allergies = patient_allergies if patient_allergies is not None else []
        self.known_contraindications = known_contraindications if known_contraindications is not None else {
            "Oseltamivir": ["Asthma", "Kidney Failure"],
            "Sumatriptan": ["Heart Disease", "High Blood Pressure"],
            "Nitroglycerin": ["Sildenafil"]
        }
        self.max_dosage_limits = {"Oseltamivir": 75, "Sumatriptan": 100, "Diphenhydramine": 50}

    def evaluate_treatment_plan(self, proposed_plan):
        patient_id = proposed_plan["patient_id"]
        diagnosis = proposed_plan["diagnosis"]
        treatment = proposed_plan["treatment"]
        medication = treatment.get("medication")
        dosage_str = treatment.get("dosage", "")

        if diagnosis == "Unspecified Condition":
            return False, "Diagnosis is too vague, requires further investigation."

        if medication in self.patient_allergies:
            return False, f"Patient {patient_id} has a known allergy to {medication}."

        if medication and medication in self.known_contraindications:
            if diagnosis in self.known_contraindications[medication]:
                return False, f"Contraindication: {medication} is contraindicated for {diagnosis}."

        if medication and medication in self.max_dosage_limits:
            try:
                dosage_value = float("".join(filter(str.isdigit, dosage_str)))
                if dosage_value > self.max_dosage_limits[medication]:
                    return False, f"Dosage for {medication} ({dosage_value}mg) exceeds maximum recommended limit ({self.max_dosage_limits[medication]}mg)."
            except ValueError:
                pass

        return True, "Treatment plan appears safe and valid."

if __name__ == "__main__":
    patient_id_1 = "P001"
    patient_allergies_1 = ["Penicillin"]
    proposer_1 = AIDiagnosisProposer(patient_id_1)
    validator_1 = TreatmentSafetyValidator(patient_allergies=patient_allergies_1)

    plan_1 = proposer_1.propose_diagnosis_and_treatment("fever_cough")
    print(f"Proposed plan: {plan_1}")
    is_safe, reason = validator_1.evaluate_treatment_plan(plan_1)
    print(f"TreatmentSafetyValidator: Status: {'SAFE' if is_safe else 'REJECTED'} - {reason}\n")

    patient_id_2 = "P002"
    patient_allergies_2 = ["Oseltamivir"]
    proposer_2 = AIDiagnosisProposer(patient_id_2)
    validator_2 = TreatmentSafetyValidator(patient_allergies=patient_allergies_2)
    plan_2 = proposer_2.propose_diagnosis_and_treatment("fever_cough")
    print(f"Proposed plan: {plan_2}")
    is_safe, reason = validator_2.evaluate_treatment_plan(plan_2)
    print(f"TreatmentSafetyValidator: Status: {'SAFE' if is_safe else 'REJECTED'} - {reason}\n")

    patient_id_3 = "P003"
    proposer_3 = AIDiagnosisProposer(patient_id_3)
    validator_3 = TreatmentSafetyValidator()
    plan_3 = proposer_3.propose_diagnosis_and_treatment("headache_nausea")
    plan_3["treatment"]["medication"] = "Sumatriptan"
    plan_3["treatment"]["dosage"] = "150mg PRN"
    print(f"Proposed plan: {plan_3}")
    is_safe, reason = validator_3.evaluate_treatment_plan(plan_3)
    print(f"TreatmentSafetyValidator: Status: {'SAFE' if is_safe else 'REJECTED'} - {reason}\n")

    patient_id_4 = "P004"
    proposer_4 = AIDiagnosisProposer(patient_id_4)
    validator_4 = TreatmentSafetyValidator()
    plan_4 = proposer_4.propose_diagnosis_and_treatment("unknown_symptom_set")
    print(f"Proposed plan: {plan_4}")
    is_safe, reason = validator_4.evaluate_treatment_plan(plan_4)
    print(f"TreatmentSafetyValidator: Status: {'SAFE' if is_safe else 'REJECTED'} - {reason}\n")