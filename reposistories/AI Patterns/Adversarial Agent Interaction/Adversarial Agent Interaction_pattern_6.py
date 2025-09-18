import random

class PatientData:
    def __init__(self, patient_id, age, symptoms, existing_conditions, medications):
        self.patient_id = patient_id
        self.age = age
        self.symptoms = symptoms
        self.existing_conditions = existing_conditions
        self.medications = medications

    def __repr__(self):
        return f"Patient(ID: {self.patient_id}, Age: {self.age}, Symptoms: {', '.join(self.symptoms)}, Conditions: {', '.join(self.existing_conditions)}, Meds: {', '.join(self.medications)})"

class Diagnosis:
    def __init__(self, patient_id, proposed_diagnosis, recommended_treatment):
        self.patient_id = patient_id
        self.proposed_diagnosis = proposed_diagnosis
        self.recommended_treatment = recommended_treatment

    def __repr__(self):
        return f"Diagnosis(Patient: {self.patient_id}, Diagnosis: {self.proposed_diagnosis}, Treatment: {self.recommended_treatment})"

class DiagnosisGenerator:
    def generate_diagnosis(self, patient_data):
        if "fever" in patient_data.symptoms and "cough" in patient_data.symptoms:
            if patient_data.age < 10 and "rash" in patient_data.symptoms:
                return Diagnosis(patient_data.patient_id, "Childhood Viral Infection", "Rest, Hydration, Symptomatic relief")
            return Diagnosis(patient_data.patient_id, "Common Cold/Flu", "Rest, Hydration, Antivirals (if flu suspected)")
        elif "chest pain" in patient_data.symptoms and patient_data.age > 50:
            return Diagnosis(patient_data.patient_id, "Potential Cardiac Event", "Immediate Hospitalization, ECG, Blood tests")
        elif "headache" in patient_data.symptoms and "nausea" in patient_data.symptoms:
            return Diagnosis(patient_data.patient_id, "Migraine", "Pain relievers, Dark room, Hydration")
        return Diagnosis(patient_data.patient_id, "Undetermined Ailment", "Further Diagnostics Recommended")

class MedicalReviewBoard:
    def __init__(self):
        self.drug_interactions = {
            ("Anticoagulant", "NSAID"): "Increased bleeding risk",
            ("Diuretic", "Lithium"): "Increased lithium toxicity",
            ("Antidepressant", "MAOI"): "Serotonin syndrome risk"
        }
        self.contraindications = {
            "Pregnancy": ["X-ray", "Certain antibiotics"],
            "Kidney Failure": ["High dose NSAIDs", "Certain contrast dyes"]
        }
        self.diagnosis_guidelines = {
            "Common Cold/Flu": {"symptoms": ["fever", "cough"], "min_age": 0},
            "Potential Cardiac Event": {"symptoms": ["chest pain"], "min_age": 40},
            "Migraine": {"symptoms": ["headache", "nausea"], "min_age": 10}
        }

    def evaluate_diagnosis(self, patient_data, diagnosis):
        issues = []

        if diagnosis.proposed_diagnosis in self.diagnosis_guidelines:
            required_symptoms = self.diagnosis_guidelines[diagnosis.proposed_diagnosis].get("symptoms", [])
            if not all(symptom in patient_data.symptoms for symptom in required_symptoms):
                issues.append(f"Diagnosis '{diagnosis.proposed_diagnosis}' inconsistent with patient symptoms.")
            min_age = self.diagnosis_guidelines[diagnosis.proposed_diagnosis].get("min_age", 0)
            if patient_data.age < min_age:
                issues.append(f"Diagnosis '{diagnosis.proposed_diagnosis}' inappropriate for patient's age ({patient_data.age} < {min_age}).")

        for i, med1 in enumerate(patient_data.medications):
            for j, med2 in enumerate(patient_data.medications):
                if i >= j: continue
                interaction = self.drug_interactions.get((med1, med2)) or self.drug_interactions.get((med2, med1))
                if interaction:
                    issues.append(f"Potential drug interaction between {med1} and {med2}: {interaction}.")

        for condition in patient_data.existing_conditions:
            if condition in self.contraindications:
                for contraindicated_item in self.contraindications[condition]:
                    if contraindicated_item in diagnosis.recommended_treatment:
                        issues.append(f"Treatment '{contraindicated_item}' contraindicated for patient with '{condition}'.")
                    elif contraindicated_item in patient_data.medications:
                        issues.append(f"Patient with '{condition}' is on contraindicated medication '{contraindicated_item}'.")

        if issues:
            return False, issues
        else:
            return True, ["Diagnosis appears sound and safe."]

if __name__ == "__main__":
    generator = DiagnosisGenerator()
    reviewer = MedicalReviewBoard()

    patient_scenarios = [
        PatientData("P001", 35, ["fever", "cough", "fatigue"], [], []),
        PatientData("P002", 62, ["chest pain", "shortness of breath"], ["Hypertension"], ["Aspirin"]),
        PatientData("P003", 28, ["headache", "nausea", "light sensitivity"], ["Migraine History"], ["Sumatriptan"]),
        PatientData("P004", 7, ["fever", "cough", "rash"], [], []),
        PatientData("P005", 55, ["dizziness"], ["Kidney Failure"], ["High dose NSAID"]),
        PatientData("P006", 40, ["fever"], ["Hypertension"], ["Anticoagulant", "NSAID"])
    ]

    print("--- Simulating Medical Diagnosis and Review ---")
    for i, patient in enumerate(patient_scenarios):
        print(f"\n--- Scenario {i+1} ---")
        print(f"Patient Data: {patient}")
        
        generated_diagnosis = generator.generate_diagnosis(patient)
        print(f"Generated: {generated_diagnosis}")
        
        is_safe, findings = reviewer.evaluate_diagnosis(patient, generated_diagnosis)
        
        if is_safe:
            print("  Review Status: Approved")
        else:
            print("  Review Status: Flagged for further review")
        for finding in findings:
            print(f"    - {finding}")