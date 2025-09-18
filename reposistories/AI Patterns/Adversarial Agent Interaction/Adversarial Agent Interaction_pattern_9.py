import random

class Patient:
    def __init__(self, patient_id, allergies, existing_medications):
        self.patient_id = patient_id
        self.allergies = set(allergies)
        self.existing_medications = set(existing_medications)

    def __str__(self):
        return f"Patient {self.patient_id} | Allergies: {', '.join(self.allergies) if self.allergies else 'None'} | Meds: {', '.join(self.existing_medications) if self.existing_medications else 'None'}"

class TreatmentPlan:
    def __init__(self, patient_id, proposed_medications, dosage_mg):
        self.patient_id = patient_id
        self.proposed_medications = set(proposed_medications)
        self.dosage_mg = dosage_mg # Simplified: dosage for one of the meds

    def __str__(self):
        return f"Plan for Patient {self.patient_id} | Proposed Meds: {', '.join(self.proposed_medications)} | Dosage: {self.dosage_mg}mg"

class TreatmentPlanGeneratorAgent:
    def generate_plan(self, patient):
        all_meds = ["Aspirin", "Ibuprofen", "Amoxicillin", "Metformin", "Insulin", "Penicillin"]
        num_proposed = random.randint(1, 3)
        proposed_meds = random.sample(all_meds, num_proposed)
        dosage = random.randint(100, 1000) # Example dosage
        return TreatmentPlan(patient.patient_id, proposed_meds, dosage)

class ClinicalSafetyAuditorAgent:
    def __init__(self):
        self.known_allergens = {"Penicillin": "Penicillin", "Aspirin": "Aspirin"}
        self.severe_drug_interactions = {
            ("Aspirin", "Ibuprofen"): "Increased bleeding risk",
            ("Metformin", "Insulin"): "Risk of severe hypoglycemia"
        }
        self.max_single_dose_mg = {"Ibuprofen": 800, "Aspirin": 500} # Example max doses

    def audit_plan(self, patient, plan):
        issues_found = False
        reasons = []

        for med in plan.proposed_medications:
            if med in patient.allergies:
                issues_found = True
                reasons.append(f"Allergy conflict: Patient allergic to {med}")

        for proposed_med in plan.proposed_medications:
            for existing_med in patient.existing_medications:
                if (proposed_med, existing_med) in self.severe_drug_interactions or \
                   (existing_med, proposed_med) in self.severe_drug_interactions:
                    issues_found = True
                    reason = self.severe_drug_interactions.get((proposed_med, existing_med), self.severe_drug_interactions.get((existing_med, proposed_med)))
                    reasons.append(f"Severe drug interaction: {proposed_med} with {existing_med} ({reason})")
        
        for med in plan.proposed_medications:
            if med in self.max_single_dose_mg and plan.dosage_mg > self.max_single_dose_mg[med]:
                issues_found = True
                reasons.append(f"Dosage exceeds limit for {med}: {plan.dosage_mg}mg > {self.max_single_dose_mg[med]}mg")

        return issues_found, reasons

if __name__ == "__main__":
    generator = TreatmentPlanGeneratorAgent()
    auditor = ClinicalSafetyAuditorAgent()

    print("--- Simulating Healthcare Treatment Plan Validation (Real-world: Clinical decision support systems) ---")

    # Scenario 1: Safe plan (simulation pattern)
    patient1 = Patient("P001", [], ["Metformin"])
    plan1 = TreatmentPlan("P001", ["Amoxicillin"], 250)
    print(f"\n{patient1}\nProposed: {plan1}")
    issues, reasons = auditor.audit_plan(patient1, plan1)
    if issues:
        print(f"  ALERT: Issues found! Reasons: {', '.join(reasons)}")
    else:
        print("  Plan deemed safe.")

    # Scenario 2: Allergy conflict (simulation pattern)
    patient2 = Patient("P002", ["Penicillin"], ["Aspirin"])
    plan2 = TreatmentPlan("P002", ["Penicillin", "Ibuprofen"], 400)
    print(f"\n{patient2}\nProposed: {plan2}")
    issues, reasons = auditor.audit_plan(patient2, plan2)
    if issues:
        print(f"  ALERT: Issues found! Reasons: {', '.join(reasons)}")
    else:
        print("  Plan deemed safe.")

    # Scenario 3: Drug interaction (simulation pattern)
    patient3 = Patient("P003", [], ["Insulin"])
    plan3 = TreatmentPlan("P003", ["Metformin"], 500)
    print(f"\n{patient3}\nProposed: {plan3}")
    issues, reasons = auditor.audit_plan(patient3, plan3)
    if issues:
        print(f"  ALERT: Issues found! Reasons: {', '.join(reasons)}")
    else:
        print("  Plan deemed safe.")
    
    # Scenario 4: Dosage exceedance (simulation pattern)
    patient4 = Patient("P004", [], [])
    plan4 = TreatmentPlan("P004", ["Ibuprofen"], 900)
    print(f"\n{patient4}\nProposed: {plan4}")
    issues, reasons = auditor.audit_plan(patient4, plan4)
    if issues:
        print(f"  ALERT: Issues found! Reasons: {', '.join(reasons)}")
    else:
        print("  Plan deemed safe.")
