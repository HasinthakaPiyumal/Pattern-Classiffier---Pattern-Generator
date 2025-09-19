import random

class SimulatedLLMHealthcare:
    def __init__(self):
        self.knowledge_base = {
            "fever,cough": ("Influenza", "Patient presents with fever and cough, classic symptoms of influenza. Rule out common cold due to fever severity."),
            "headache,stiff neck": ("Meningitis", "Severe headache and stiff neck are red flags for meningitis. Consider immediate medical attention."),
        }
        self.accuracy_score = 0.6

    def generate_rationale_and_diagnosis(self, symptoms):
        symptoms_key = ",".join(sorted(symptoms))
        if symptoms_key in self.knowledge_base and random.random() < self.accuracy_score:
            diagnosis, rationale = self.knowledge_base[symptoms_key]
            return rationale, diagnosis
        else:
            possible_diagnoses = ["Common Cold", "Influenza", "Meningitis", "Migraine", "Allergy", "Viral Infection", "Tension Headache"]
            
            if "fever" in symptoms and "cough" in symptoms:
                diagnosis = "Influenza" if random.random() < 0.7 else "Common Cold"
                rationale = f"Based on {symptoms_key}, considering viral infection. Further tests needed for definitive diagnosis."
            elif "headache" in symptoms and "stiff neck" in symptoms:
                diagnosis = "Meningitis" if random.random() < 0.8 else random.choice(["Migraine", "Tension Headache"])
                rationale = f"Severe symptoms like {symptoms_key} suggest serious neurological issues. Urgent investigation advised."
            elif "headache" in symptoms:
                diagnosis = "Migraine" if random.random() < 0.6 else "Tension Headache"
                rationale = f"Headache is primary symptom. Exploring neurological causes or stress-related factors."
            else:
                diagnosis = random.choice(possible_diagnoses)
                rationale = f"General symptoms like {symptoms_key}. Initial assessment suggests {diagnosis}."
            return rationale, diagnosis

    def fine_tune(self, symptoms, rationale, diagnosis):
        symptoms_key = ",".join(sorted(symptoms))
        if symptoms_key not in self.knowledge_base:
            self.knowledge_base[symptoms_key] = (diagnosis, rationale)
            self.accuracy_score = min(1.0, self.accuracy_score + 0.05)

def get_ground_truth_diagnosis(symptoms):
    symptoms_key = ",".join(sorted(symptoms))
    if symptoms_key == "cough,fever":
        return "Influenza"
    if symptoms_key == "headache,stiff neck":
        return "Meningitis"
    if symptoms_key == "runny nose,sneeze":
        return "Common Cold"
    if symptoms_key == "fatigue,muscle aches":
        return "Viral Infection"
    if symptoms_key == "fever,sore throat":
        return "Streptococcal Pharyngitis"
    return "Unknown"

def simulate_healthcare_star_pattern():
    llm = SimulatedLLMHealthcare()
    patient_cases = [
        ["fever", "cough"],
        ["headache", "stiff neck"],
        ["runny nose", "sneeze"],
        ["fatigue", "muscle aches"],
        ["fever", "sore throat"]
    ]
    
    for _ in range(5): 
        for case_symptoms in patient_cases:
            ground_truth = get_ground_truth_diagnosis(case_symptoms)
            if ground_truth == "Unknown":
                continue
            
            rationale, predicted_diagnosis = llm.generate_rationale_and_diagnosis(case_symptoms)
            
            if predicted_diagnosis == ground_truth:
                llm.fine_tune(case_symptoms, rationale, predicted_diagnosis)

simulate_healthcare_star_pattern()