import random

class TreatmentPlanGenerator:
    def __init__(self, available_medications, available_therapies):
        self.available_medications = available_medications
        self.available_therapies = available_therapies

    def generate_plans(self, patient_condition, num_candidates=5):
        candidate_plans = []
        for _ in range(num_candidates):
            medication = random.choice(self.available_medications)
            therapy = random.choice(self.available_therapies)
            plan = {'medication': medication, 'therapy': therapy}
            candidate_plans.append(plan)
        return candidate_plans

class TreatmentPlanRewardModel:
    def __init__(self, patient_data):
        self.patient_data = patient_data

    def score_plan(self, plan):
        score = 0
        if self.patient_data['severity'] == 'moderate':
            if plan['medication']['type'] == 'standard':
                score += 0.6
            elif plan['medication']['type'] == 'advanced':
                score += 0.8
        elif self.patient_data['severity'] == 'severe':
            if plan['medication']['type'] == 'standard':
                score += 0.4
            elif plan['medication']['type'] == 'advanced':
                score += 0.9

        if self.patient_data['has_allergies'] and plan['medication']['allergy_risk']:
            score -= 0.3
        if plan['medication']['side_effects_level'] == 'high':
            score -= 0.2
        if plan['therapy']['intensity'] == 'high' and self.patient_data['age'] > 60:
            score -= 0.1

        score -= (plan['medication']['cost'] + plan['therapy']['cost']) * 0.01

        score += random.uniform(-0.05, 0.05)
        return score

available_meds = [
    {'name': 'MedA', 'type': 'standard', 'cost': 50, 'side_effects_level': 'low', 'allergy_risk': False},
    {'name': 'MedB', 'type': 'advanced', 'cost': 150, 'side_effects_level': 'moderate', 'allergy_risk': True},
    {'name': 'MedC', 'type': 'standard', 'cost': 70, 'side_effects_level': 'low', 'allergy_risk': True},
    {'name': 'MedD', 'type': 'advanced', 'cost': 200, 'side_effects_level': 'high', 'allergy_risk': False},
]

available_therapies = [
    {'name': 'TherapyX', 'intensity': 'low', 'cost': 80},
    {'name': 'TherapyY', 'intensity': 'moderate', 'cost': 120},
    {'name': 'TherapyZ', 'intensity': 'high', 'cost': 180},
]

current_patient_id = 'patient_456'
patient_clinical_data = {'age': 55, 'has_allergies': True, 'severity': 'moderate'}
patient_condition = 'chronic_pain'

if __name__ == "__main__":
    plan_generator = TreatmentPlanGenerator(available_meds, available_therapies)
    num_candidates_to_generate = 8
    candidate_treatment_plans = plan_generator.generate_plans(patient_condition, num_candidates_to_generate)

    reward_model = TreatmentPlanRewardModel(patient_clinical_data)
    scored_candidates = []
    for plan in candidate_treatment_plans:
        score = reward_model.score_plan(plan)
        scored_candidates.append({'plan': plan, 'score': score})

    best_treatment_plan = max(scored_candidates, key=lambda x: x['score'])
    final_output = {
        "medication": best_treatment_plan['plan']['medication']['name'],
        "therapy": best_treatment_plan['plan']['therapy']['name'],
        "score": best_treatment_plan['score']
    }
