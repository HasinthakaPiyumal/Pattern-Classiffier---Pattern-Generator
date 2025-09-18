import random

class Patient:
    def __init__(self, patient_id, allergies, existing_meds, diagnosis):
        self.patient_id = patient_id
        self.allergies = allergies
        self.existing_meds = existing_meds
        self.diagnosis = diagnosis
        self.proposed_treatment = None
        self.final_treatment = None
        self.review_issues = []

class TreatmentPlan:
    def __init__(self, patient_id, medications, procedures):
        self.patient_id = patient_id
        self.medications = medications
        self.procedures = procedures
        self.is_valid = True
        self.issues = []

class DiagnosisAndTreatmentAgent:
    def generate_plan(self, patient: Patient):
        meds = []
        procs = []
        if patient.diagnosis == "Type 2 Diabetes":
            meds.append("Metformin")
            procs.append("Dietary Counseling")
            if random.random() < 0.2:
                meds.append("Insulin Glargine")
        elif patient.diagnosis == "Hypertension":
            meds.append("Lisinopril")
            procs.append("Blood Pressure Monitoring")
            if random.random() < 0.1:
                meds.append("Ibuprofen")
        else:
            meds.append("General Pain Reliever")
            procs.append("Rest")

        plan = TreatmentPlan(patient.patient_id, meds, procs)
        patient.proposed_treatment = plan
        print(f"Agent generated plan for {patient.patient_id}: Meds={plan.medications}, Procs={plan.procedures}")
        return plan

class PatientSafetyReviewAgent:
    def review_plan(self, patient: Patient, plan: TreatmentPlan):
        issues_found = []

        for med in plan.medications:
            if med in patient.allergies:
                issues_found.append(f"Allergy alert: Patient allergic to {med}.")

        for med_new in plan.medications:
            for med_existing in patient.existing_meds:
                if (med_new == "Ibuprofen" and med_existing == "Lisinopril") or \
                   (med_new == "Insulin Glargine" and med_existing == "Metformin" and patient.diagnosis != "Type 2 Diabetes"):
                    issues_found.append(f"Potential drug interaction: {med_new} with {med_existing}.")

        if "Ibuprofen" in plan.medications and patient.diagnosis == "Hypertension":
            issues_found.append("Contraindication: Ibuprofen can worsen hypertension.")
        if "Insulin Glargine" in plan.medications and patient.diagnosis != "Type 2 Diabetes":
            issues_found.append("Warning: Insulin Glargine might be inappropriate for non-diabetic diagnosis.")

        if issues_found:
            plan.is_valid = False
            plan.issues = issues_found
            patient.review_issues = issues_found
            patient.final_treatment = "Rejected/Needs Revision"
            print(f"Review Agent found issues for {patient.patient_id}: {', '.join(issues_found)}")
        else:
            plan.is_valid = True
            patient.final_treatment = "Approved"
            print(f"Review Agent approved plan for {patient.patient_id}.")
        return plan

if __name__ == "__main__":
    patients_data = [
        Patient("P001", ["Penicillin"], ["Aspirin"], "Type 2 Diabetes"),
        Patient("P002", [], ["Lisinopril"], "Hypertension"),
        Patient("P003", ["Metformin"], ["Omeprazole"], "Type 2 Diabetes"),
        Patient("P004", [], [], "Common Cold"),
        Patient("P005", [], ["Lisinopril"], "Hypertension")
    ]

    treatment_agent = DiagnosisAndTreatmentAgent()
    safety_agent = PatientSafetyReviewAgent()

    for patient in patients_data:
        print(f"\n--- Processing Patient {patient.patient_id} ({patient.diagnosis}) ---")
        proposed_plan = treatment_agent.generate_plan(patient)
        final_plan = safety_agent.review_plan(patient, proposed_plan)

        print(f"Final Treatment Status for {patient.patient_id}: {patient.final_treatment}")
        if not final_plan.is_valid:
            print(f"  Issues: {', '.join(final_plan.issues)}")
        else:
            print(f"  Approved Medications: {final_plan.medications}, Procedures: {final_plan.procedures}")