import random

class PatientDiagnosis:
    def __init__(self, patient_id, symptoms, proposed_diagnosis, proposed_treatment):
        self.patient_id = patient_id
        self.symptoms = symptoms
        self.proposed_diagnosis = proposed_diagnosis
        self.proposed_treatment = proposed_treatment

    def __str__(self):
        return f"PatientDiagnosis(ID:{self.patient_id}, Diag:'{self.proposed_diagnosis}', Treat:'{self.proposed_treatment}')"

class DiagnosticAI:
    COMMON_SYMPTOMS = ['fever', 'cough', 'fatigue', 'headache', 'nausea', 'rash', 'dizziness']
    COMMON_DIAGNOSES = ['Common Cold', 'Influenza', 'Migraine', 'Allergy', 'Gastroenteritis', 'Dermatitis']
    COMMON_TREATMENTS = ['Rest and Fluids', 'Painkillers', 'Antihistamines', 'Antibiotics', 'Antivirals', 'Topical Cream']

    def generate_diagnosis(self, patient_id):
        num_symptoms = random.randint(1, 3)
        symptoms = random.sample(self.COMMON_SYMPTOMS, num_symptoms)
        
        diagnosis = random.choice(self.COMMON_DIAGNOSES)
        treatment = random.choice(self.COMMON_TREATMENTS)

        # Simulate some edge cases for validation
        if 'rash' in symptoms and 'Dermatitis' not in diagnosis: # Mismatch
            diagnosis = random.choice(['Common Cold', 'Influenza'])
            treatment = 'Painkillers'
        if 'fever' in symptoms and random.random() < 0.2: # Potentially serious
            diagnosis = random.choice(['Influenza', 'Bacterial Infection'])
            treatment = random.choice(['Antivirals', 'Antibiotics'])

        print(f"[DiagnosticAI] Generated preliminary diagnosis for Patient {patient_id}.")
        return PatientDiagnosis(patient_id, symptoms, diagnosis, treatment)

class TreatmentPlanValidator:
    KNOWN_ALLERGIES = {'P002': ['Painkillers'], 'P004': ['Antibiotics']}
    MEDICAL_GUIDELINES = {
        'Common Cold': {'min_treatment': 'Rest and Fluids', 'avoid': ['Antibiotics']},
        'Influenza': {'min_treatment': 'Antivirals', 'avoid': []},
        'Migraine': {'min_treatment': 'Painkillers', 'avoid': []},
        'Allergy': {'min_treatment': 'Antihistamines', 'avoid': []},
        'Dermatitis': {'min_treatment': 'Topical Cream', 'avoid': []}
    }

    def validate_plan(self, diagnosis):
        print(f"[Validator] Validating treatment plan for {diagnosis.patient_id}...")
        issues = []

        # Rule 1: Check for drug allergies
        if diagnosis.patient_id in self.KNOWN_ALLERGIES:
            allergies = self.KNOWN_ALLERGIES[diagnosis.patient_id]
            if diagnosis.proposed_treatment in allergies:
                issues.append(f"High severity: Patient {diagnosis.patient_id} is allergic to '{diagnosis.proposed_treatment}'.")

        # Rule 2: Check against medical guidelines for diagnosis
        guideline = self.MEDICAL_GUIDELINES.get(diagnosis.proposed_diagnosis)
        if guideline:
            if diagnosis.proposed_treatment != guideline['min_treatment'] and random.random() < 0.5: # Simulate some flexibility or minor deviations
                 issues.append(f"Medium severity: Proposed treatment '{diagnosis.proposed_treatment}' deviates from standard guideline '{guideline['min_treatment']}' for '{diagnosis.proposed_diagnosis}'.")
            if diagnosis.proposed_treatment in guideline.get('avoid', []):
                issues.append(f"High severity: Proposed treatment '{diagnosis.proposed_treatment}' is specifically contraindicated for '{diagnosis.proposed_diagnosis}'.")
        else:
            issues.append(f"Low severity: Diagnosis '{diagnosis.proposed_diagnosis}' not found in standard guidelines. Requires manual review.")

        # Rule 3: Basic symptom-diagnosis consistency (simplified)
        if 'rash' in diagnosis.symptoms and diagnosis.proposed_diagnosis not in ['Dermatitis', 'Allergy']:
            issues.append(f"Medium severity: Patient has 'rash' but diagnosis is '{diagnosis.proposed_diagnosis}'. Potential mismatch.")

        if not issues:
            print(f"[Validator] Treatment plan for {diagnosis.patient_id} is approved. No critical issues found.")
            return True, "Approved"
        else:
            print(f"[Validator] Treatment plan for {diagnosis.patient_id} flagged with issues:")
            for issue in issues:
                print(f"  - {issue}")
            return False, issues

# --- Simulation ---
if __name__ == "__main__":
    diag_ai = DiagnosticAI()
    validator = TreatmentPlanValidator()

    print("\n--- Running Medical Diagnosis and Treatment Validation ---")
    patient_ids = [f"P{str(i).zfill(3)}" for i in range(1, 6)]
    for pid in patient_ids:
        print(f"\nProcessing Patient {pid}...")
        preliminary_diagnosis = diag_ai.generate_diagnosis(pid)
        print(f"Generated: {preliminary_diagnosis}")
        approved, feedback = validator.validate_plan(preliminary_diagnosis)
        print(f"Validation Result for Patient {pid}: {'APPROVED' if approved else 'REJECTED'}\n")

    # Test a specific allergy case
    print("\n--- Testing specific allergy scenario (P002 is allergic to Painkillers) ---")
    patient_with_allergy = PatientDiagnosis('P002', ['headache'], 'Migraine', 'Painkillers')
    print(f"[DiagnosticAI] Generated specific case: {patient_with_allergy}")
    approved, feedback = validator.validate_plan(patient_with_allergy)
    print(f"Validation Result for P002 (Allergy Test): {'APPROVED' if approved else 'REJECTED'}\n")
