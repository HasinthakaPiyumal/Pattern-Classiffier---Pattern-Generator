import random

class Patient:
    def __init__(self, name, patient_id, allergies=None, existing_medications=None):
        self.name = name
        self.patient_id = patient_id
        self.allergies = allergies if allergies else []
        self.existing_medications = existing_medications if existing_medications else []

    def __str__(self):
        return f"Patient: {self.name} (ID: {self.patient_id}), Allergies: {', '.join(self.allergies) if self.allergies else 'None'}, On Meds: {', '.join(self.existing_medications) if self.existing_medications else 'None'}"

class TreatmentPlan:
    def __init__(self, patient: Patient, diagnosis, proposed_medications, proposed_procedures):
        self.patient = patient
        self.diagnosis = diagnosis
        self.proposed_medications = proposed_medications
        self.proposed_procedures = proposed_procedures
        self.is_safe = False
        self.safety_warnings = []

    def __str__(self):
        meds_str = ', '.join([f"{m['name']} ({m['dosage']})" for m in self.proposed_medications])
        procs_str = ', '.join(self.proposed_procedures)
        return (f"Treatment Plan for {self.patient.name} (Diagnosis: {self.diagnosis})\n"
                f"  Meds: {meds_str if meds_str else 'None'}\n"
                f"  Procedures: {procs_str if procs_str else 'None'}\n"
                f"  Safety Status: {'SAFE' if self.is_safe else 'UNSAFE'}\n"
                f"  Warnings: {', '.join(self.safety_warnings) if self.safety_warnings else 'None'}")

class TreatmentPlanGenerator:
    def generate_plan(self, patient: Patient, diagnosis):
        print(f"Generator: Creating a treatment plan for {patient.name} with diagnosis '{diagnosis}'...")
        proposed_meds = []
        proposed_procedures = []

        if diagnosis == "Flu":
            proposed_meds.append({"name": "Oseltamivir", "dosage": "75mg BID"})
            proposed_meds.append({"name": "Acetaminophen", "dosage": "500mg PRN"})
        elif diagnosis == "Hypertension":
            proposed_meds.append({"name": "Lisinopril", "dosage": "10mg QD"})
            proposed_procedures.append("Blood Pressure Monitoring")
        elif diagnosis == "Allergic Reaction":
            proposed_meds.append({"name": "Diphenhydramine", "dosage": "25mg PRN"})
        else:
            proposed_meds.append({"name": "Placebo", "dosage": "1 tablet QD"}) # Default for unknown
            proposed_procedures.append("Observation")

        return TreatmentPlan(patient, diagnosis, proposed_meds, proposed_procedures)

class MedicalSafetyReviewer:
    DRUG_INTERACTIONS = {
        ("Oseltamivir", "Lisinopril"): "Monitor for kidney function",
        ("Diphenhydramine", "Lisinopril"): "May cause additive hypotension"
    }

    def evaluate_plan(self, plan: TreatmentPlan):
        print(f"SafetyReviewer: Evaluating treatment plan for {plan.patient.name}...")
        plan.safety_warnings = [] # Reset warnings

        # Check for allergies
        for med in plan.proposed_medications:
            if med['name'] in plan.patient.allergies:
                plan.safety_warnings.append(f"Allergy Alert: Patient is allergic to {med['name']}")
                print(f"  - Warning: Allergy to {med['name']}")

        # Check for drug interactions (with proposed and existing meds)
        all_meds = [m['name'] for m in plan.proposed_medications] + plan.patient.existing_medications
        for i in range(len(all_meds)):
            for j in range(i + 1, len(all_meds)):
                med1, med2 = sorted((all_meds[i], all_meds[j])) # Standardize order for lookup
                if (med1, med2) in self.DRUG_INTERACTIONS:
                    interaction_info = self.DRUG_INTERACTIONS[(med1, med2)]
                    plan.safety_warnings.append(f"Drug Interaction: {med1} + {med2} ({interaction_info})")
                    print(f"  - Warning: Drug interaction between {med1} and {med2}")

        # Simplified check for dosage limits (e.g., Acetaminophen combined with existing meds)
        for med in plan.proposed_medications:
            if "Acetaminophen" == med['name'] and "500mg" in med['dosage']:
                if any("Acetaminophen" in existing_med for existing_med in plan.patient.existing_medications):
                    plan.safety_warnings.append(f"Dosage Alert: {med['name']} combined with existing meds might exceed daily limit.")
                    print(f"  - Warning: {med['name']} dosage might be too high combined with existing meds.")

        if len(plan.safety_warnings) > 0:
            print(f"SafetyReviewer: Plan for {plan.patient.name} has safety concerns.")
            plan.is_safe = False
            return False
        else:
            print(f"SafetyReviewer: Plan for {plan.patient.name} appears safe.")
            plan.is_safe = True
            return True

class HospitalSystem:
    def __init__(self):
        self.plan_generator = TreatmentPlanGenerator()
        self.safety_reviewer = MedicalSafetyReviewer()
        self.approved_plans = []

    def propose_and_validate_treatment(self, patient: Patient, diagnosis: str):
        plan = self.plan_generator.generate_plan(patient, diagnosis)
        is_safe = self.safety_reviewer.evaluate_plan(plan)
        if is_safe:
            self.approved_plans.append(plan)
            print(f"System: Treatment plan for {patient.name} APPROVED and added to patient records.")
        else:
            print(f"System: Treatment plan for {patient.name} REJECTED or requires revision due to safety warnings.")
        print(plan)
        print("-" * 50)

if __name__ == "__main__":
    hospital = HospitalSystem()

    patient1 = Patient("Alice Smith", "P001", allergies=["Penicillin"])
    patient2 = Patient("Bob Johnson", "P002", existing_medications=["Lisinopril"])
    patient3 = Patient("Charlie Brown", "P003", allergies=["Diphenhydramine"])
    patient4 = Patient("Diana Prince", "P004")

    hospital.propose_and_validate_treatment(patient1, "Flu")
    hospital.propose_and_validate_treatment(patient2, "Flu") # Interaction: Oseltamivir + Lisinopril
    hospital.propose_and_validate_treatment(patient3, "Allergic Reaction") # Allergy to Diphenhydramine
    hospital.propose_and_validate_treatment(patient4, "Hypertension")