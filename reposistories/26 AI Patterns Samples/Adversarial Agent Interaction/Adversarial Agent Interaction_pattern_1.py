import random

class Patient:
    def __init__(self, patient_id, allergies, existing_conditions):
        self.patient_id = patient_id
        self.allergies = set(allergies)
        self.existing_conditions = set(existing_conditions)

    def __str__(self):
        return f"Patient ID: {self.patient_id}, Allergies: {', '.join(self.allergies) if self.allergies else 'None'}, Conditions: {', '.join(self.existing_conditions) if self.existing_conditions else 'None'}"

class TreatmentPlan:
    def __init__(self, patient_id, medications, dosages, procedures):
        self.patient_id = patient_id
        self.medications = medications
        self.dosages = dosages
        self.procedures = procedures
        self.status = "proposed"
        self.issues = []

    def __str__(self):
        meds_str = ", ".join([f"{m} ({d})" for m, d in zip(self.medications, self.dosages)])
        procs_str = ", ".join(self.procedures)
        return f"Patient: {self.patient_id}\n  Medications: {meds_str if meds_str else 'None'}\n  Procedures: {procs_str if procs_str else 'None'}\n  Status: {self.status}"

class TreatmentPlanGenerator:
    def __init__(self, available_meds, available_procs, patients):
        self.available_meds = available_meds
        self.available_procs = available_procs
        self.patients = patients

    def generate_plan(self, patient):
        num_meds = random.randint(0, 3)
        medications = random.sample(self.available_meds, k=min(num_meds, len(self.available_meds)))
        dosages = [random.choice(["10mg BID", "20mg QD", "5mg TID"]) for _ in medications]

        num_procs = random.randint(0, 2)
        procedures = random.sample(self.available_procs, k=min(num_procs, len(self.available_procs)))

        return TreatmentPlan(patient.patient_id, medications, dosages, procedures)

class SafetyEfficacyReviewer:
    def __init__(self, drug_interactions, contraindications, max_dosages):
        self.drug_interactions = drug_interactions
        self.contraindications = contraindications
        self.max_dosages = max_dosages

    def evaluate(self, plan, patient):
        issues = []

        for med in plan.medications:
            if med in patient.allergies:
                issues.append(f"Allergy Alert: Patient is allergic to {med}.")

        for i, med1 in enumerate(plan.medications):
            for j, med2 in enumerate(plan.medications):
                if i != j and med1 in self.drug_interactions and med2 in self.drug_interactions[med1]:
                    issues.append(f"Drug Interaction Alert: {med1} and {med2} should not be co-administered.")

        for condition in patient.existing_conditions:
            if condition in self.contraindications:
                for contraindicated_med in self.contraindications[condition]:
                    if contraindicated_med in plan.medications:
                        issues.append(f"Contraindication Alert: {contraindicated_med} is contraindicated for {condition}.")
        
        for med, dosage_str in zip(plan.medications, plan.dosages):
            if med in self.max_dosages:
                try:
                    dose_value = int(dosage_str.split('mg')[0])
                    if dose_value > self.max_dosages[med]:
                        issues.append(f"Dosage Alert: {med} ({dosage_str}) exceeds recommended max ({self.max_dosages[med]}mg).")
                except ValueError:
                    pass

        if issues:
            return False, issues
        return True, ["No issues found. Plan is safe and effective."]

if __name__ == "__main__":
    available_meds = ["Aspirin", "Ibuprofen", "Amoxicillin", "Metformin", "Insulin", "Lisinopril"]
    available_procs = ["Blood Test", "X-Ray", "MRI", "Physical Therapy"]

    patients = [
        Patient("P001", ["Aspirin"], ["Hypertension"]),
        Patient("P002", [], ["Diabetes"]),
        Patient("P003", ["Ibuprofen"], []),
        Patient("P004", [], ["Asthma"]),
    ]

    drug_interactions = {
        "Aspirin": ["Ibuprofen"],
        "Metformin": ["Insulin"],
    }
    contraindications = {
        "Asthma": ["Aspirin", "Ibuprofen"],
        "Hypertension": ["Ibuprofen"],
    }
    max_dosages = {
        "Amoxicillin": 500,
        "Ibuprofen": 400,
    }

    plan_generator = TreatmentPlanGenerator(available_meds, available_procs, patients)
    reviewer = SafetyEfficacyReviewer(drug_interactions, contraindications, max_dosages)

    print("--- Simulating Treatment Plan Generation and Safety Review ---")

    test_cases = [
        ("P001", ["Aspirin", "Lisinopril"], ["100mg QD", "10mg QD"], ["Blood Test"]),
        ("P002", ["Metformin", "Insulin"], ["500mg BID", "10 units QD"], []),
        ("P004", ["Ibuprofen"], ["200mg TID"], ["X-Ray"]),
        ("P003", ["Amoxicillin"], ["600mg BID"], []),
        ("P001", ["Lisinopril"], ["10mg QD"], ["MRI"]),
    ]

    for p_id, meds, doses, procs in test_cases:
        patient = next(p for p in patients if p.patient_id == p_id)
        
        plan = TreatmentPlan(patient.patient_id, meds, doses, procs)
        
        print(f"\nReviewing Plan for {patient.patient_id}:")
        print(patient)
        print(plan)

        is_safe, issues = reviewer.evaluate(plan, patient)
        plan.issues = issues
        
        if is_safe:
            plan.status = "approved"
            print("  Safeguard (Safety & Efficacy Reviewer): APPROVED")
        else:
            plan.status = "rejected"
            print("  Safeguard (Safety & Efficacy Reviewer) REJECTED. Issues found:")
        
        for issue in plan.issues:
            print(f"    - {issue}")
        print(f"  Final Plan Status: {plan.status}")
