class Patient:
    def __init__(self, name, allergies, conditions):
        self.name = name
        self.allergies = set(allergies)
        self.conditions = set(conditions)

class Medication:
    def __init__(self, name, interactions, contraindications):
        self.name = name
        self.interactions = set(interactions)
        self.contraindications = set(contraindications)

class TreatmentPlan:
    def __init__(self, patient, medications):
        self.patient = patient
        self.medications = medications
        self.status = "PROPOSED"

    def __repr__(self):
        med_names = ", ".join([m.name for m in self.medications])
        return f"TreatmentPlan for {self.patient.name} with meds: [{med_names}] (Status: {self.status})"

class TreatmentPlanGenerator:
    def generate_plan(self, patient, suggested_medications_names):
        print(f"TreatmentPlanGenerator: Generating a plan for {patient.name} with suggested medications: {', '.join(suggested_medications_names)}")
        all_available_meds = {
            "Aspirin": Medication("Aspirin", {"Warfarin"}, {"Asthma", "Ulcers"}),
            "Warfarin": Medication("Warfarin", {"Aspirin"}, {"BleedingDisorder"}),
            "Penicillin": Medication("Penicillin", {}, {"PenicillinAllergy"}),
            "Paracetamol": Medication("Paracetamol", {}, {}),
            "Amoxicillin": Medication("Amoxicillin", {}, {"PenicillinAllergy"})
        }
        medications = [all_available_meds[name] for name in suggested_medications_names if name in all_available_meds]
        return TreatmentPlan(patient, medications)

class DrugInteractionChecker:
    def evaluate_plan(self, plan):
        issues = []

        for med in plan.medications:
            if med.name in plan.patient.allergies:
                issues.append(f"Patient is allergic to {med.name}.")

        for med in plan.medications:
            for contra in med.contraindications:
                if contra in plan.patient.conditions:
                    issues.append(f"{med.name} is contraindicated for patient's condition: {contra}.")

        for i, med1 in enumerate(plan.medications):
            for j, med2 in enumerate(plan.medications):
                if i < j and med1.name in med2.interactions:
                    issues.append(f"Potential interaction between {med1.name} and {med2.name}.")
                if i < j and med2.name in med1.interactions:
                    issues.append(f"Potential interaction between {med2.name} and {med1.name}.")

        if issues:
            plan.status = "REJECTED_UNSAFE"
            print(f"DrugInteractionChecker: !!! Detected safety issues for {plan.patient.name}'s plan. Issues: {'; '.join(issues)}")
            return False, issues
        else:
            plan.status = "APPROVED_SAFE"
            print(f"DrugInteractionChecker: Treatment plan for {plan.patient.name} appears safe. Approved.")
            return True, []

if __name__ == "__main__":
    plan_generator = TreatmentPlanGenerator()
    interaction_checker = DrugInteractionChecker()

    patient1 = Patient("Alice", ["PenicillinAllergy"], ["Asthma"])
    patient2 = Patient("Bob", [], ["BleedingDisorder"])
    patient3 = Patient("Charlie", [], [])

    plans_to_check = [
        (patient1, ["Amoxicillin", "Aspirin"]),
        (patient2, ["Warfarin", "Aspirin"]),
        (patient3, ["Paracetamol"]),
    ]

    for patient, meds in plans_to_check:
        proposed_plan = plan_generator.generate_plan(patient, meds)
        is_safe, reasons = interaction_checker.evaluate_plan(proposed_plan)
        print("-" * 30)