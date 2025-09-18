import random

class AITreatmentPlanGenerator:
    def generate_plan(self, patient_id, diagnosis):
        medications = random.sample(["Aspirin", "Ibuprofen", "Amoxicillin", "Metformin", "Insulin", "Lisinopril"], k=random.randint(1, 3))
        dosage = {med: f"{random.randint(50, 500)}mg" for med in medications}
        procedures = random.sample(["Blood Test", "X-Ray", "MRI", "Physical Therapy", "ECG"], k=random.randint(0, 2))
        print(f"AI generating treatment plan for patient {patient_id} with diagnosis '{diagnosis}'.")
        return {"patient_id": patient_id, "diagnosis": diagnosis, "medications": medications, "dosage": dosage, "procedures": procedures}

class MedicalComplianceChecker:
    def evaluate_plan(self, plan, patient_allergies, known_interactions):
        print(f"  Safeguard: Checking treatment plan for patient {plan['patient_id']}...")
        issues = []

        for med in plan["medications"]:
            if med in patient_allergies:
                issues.append(f"Medication '{med}' is an allergen for the patient.")
            for existing_med, interacting_meds in known_interactions.items():
                if med == existing_med:
                    for other_med in plan["medications"]:
                        if other_med in interacting_meds:
                            issues.append(f"Potential interaction between '{med}' and '{other_med}'.")
        
        if not plan["medications"] and "severe" in plan["diagnosis"].lower():
            issues.append("No medications prescribed for a severe diagnosis.")

        if issues:
            print(f"  Safeguard: Treatment plan flagged with issues: {', '.join(issues)}")
            return {"status": "rejected", "issues": issues}
        else:
            print("  Safeguard: Treatment plan approved, no immediate issues found.")
            return {"status": "approved", "issues": []}

if __name__ == "__main__":
    generator = AITreatmentPlanGenerator()
    safeguard = MedicalComplianceChecker()

    patient_data = [
        {"patient_id": "P001", "diagnosis": "Hypertension", "allergies": ["Aspirin"], "interactions": {"Metformin": ["Insulin"]}},
        {"patient_id": "P002", "diagnosis": "Common Cold", "allergies": [], "interactions": {}},
        {"patient_id": "P003", "diagnosis": "Severe Infection", "allergies": [], "interactions": {"Amoxicillin": ["Metformin"]}},
        {"patient_id": "P004", "diagnosis": "Diabetes", "allergies": [], "interactions": {"Metformin": ["Insulin"], "Insulin": ["Metformin"]}},
    ]

    for data in patient_data:
        print("-" * 30)
        generated_plan = generator.generate_plan(data["patient_id"], data["diagnosis"])
        
        if data["patient_id"] == "P001": 
            generated_plan["medications"] = ["Aspirin", "Metformin"]
            generated_plan["dosage"] = {"Aspirin": "100mg", "Metformin": "500mg"}
        if data["patient_id"] == "P003": 
             generated_plan["medications"] = ["Amoxicillin", "Metformin"]
             generated_plan["dosage"] = {"Amoxicillin": "250mg", "Metformin": "500mg"}
        if data["patient_id"] == "P004": 
             generated_plan["medications"] = ["Metformin", "Insulin"]
             generated_plan["dosage"] = {"Metformin": "500mg", "Insulin": "10 units"}

        result = safeguard.evaluate_plan(generated_plan, data["allergies"], data["interactions"])
        if result["status"] == "approved":
            print(f"Plan for patient {generated_plan['patient_id']} approved. Medications: {', '.join(generated_plan['medications'])}")
        else:
            print(f"Plan for patient {generated_plan['patient_id']} rejected. Issues: {', '.join(result['issues'])}")