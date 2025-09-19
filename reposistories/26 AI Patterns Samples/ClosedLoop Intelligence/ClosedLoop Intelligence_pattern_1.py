import random

class TreatmentAdvisor:
    def __init__(self, treatments):
        self.treatments = treatments
        self.treatment_effectiveness = {name: {'impact': 0.5, 'risk': 0.1} for name in treatments}
        self.patient_history = {}

    def assess_patient(self, patient_id, current_metrics):
        
        suggestions = []
        if current_metrics['blood_sugar'] > 180:
            suggestions.append({'treatment': 'DrugX', 'action': 'increase_dose', 'amount': 10})
        if current_metrics['blood_pressure'] > 140:
            suggestions.append({'treatment': 'DrugY', 'action': 'increase_dose', 'amount': 5})
        if current_metrics['activity_level'] < 3:
            suggestions.append({'treatment': 'DietY', 'action': 'increase_intensity', 'amount': 1})
            
        sorted_effective_treatments = sorted(self.treatment_effectiveness.items(), 
                                             key=lambda item: item[1]['impact'] - item[1]['risk'], reverse=True)
        if not suggestions and sorted_effective_treatments:
            top_treatment = sorted_effective_treatments[0][0]
            suggestions.append({'treatment': top_treatment, 'action': 'maintain_current'})

        print(f"ML Advisor suggests for patient {patient_id}: {suggestions}")
        return suggestions

    def get_patient_outcome(self, patient_id, suggested_plan, actual_plan):
        
        outcome_score = 0
        for item in actual_plan:
            treatment_name = item['treatment']
            if treatment_name in self.treatment_effectiveness:
                outcome_score += self.treatment_effectiveness[treatment_name]['impact'] * (1 if 'increase' in item['action'] else 0.5)
                outcome_score -= self.treatment_effectiveness[treatment_name]['risk'] * (1 if 'increase' in item['action'] else 0.5)
        
        outcome_score += random.uniform(-0.1, 0.1)
        
        if outcome_score > 0.6:
            return {'status': 'improved', 'delta_metrics': {'blood_sugar': -20, 'blood_pressure': -5, 'activity_level': 1}}
        elif outcome_score < 0.3:
            return {'status': 'deteriorated', 'delta_metrics': {'blood_sugar': +15, 'blood_pressure': +3, 'activity_level': -0.5}}
        else:
            return {'status': 'stable', 'delta_metrics': {'blood_sugar': 0, 'blood_pressure': 0, 'activity_level': 0}}

    def learn_from_outcome(self, patient_id, suggested_plan, actual_plan, outcome):
        print(f"Learning from outcome for patient {patient_id}: {outcome['status']}")
        for item in actual_plan:
            treatment_name = item['treatment']
            if treatment_name in self.treatment_effectiveness:
                if outcome['status'] == 'improved':
                    self.treatment_effectiveness[treatment_name]['impact'] = min(1.0, self.treatment_effectiveness[treatment_name]['impact'] + 0.05)
                    self.treatment_effectiveness[treatment_name]['risk'] = max(0.0, self.treatment_effectiveness[treatment_name]['risk'] - 0.01)
                elif outcome['status'] == 'deteriorated':
                    self.treatment_effectiveness[treatment_name]['impact'] = max(0.0, self.treatment_effectiveness[treatment_name]['impact'] - 0.05)
                    self.treatment_effectiveness[treatment_name]['risk'] = min(1.0, self.treatment_effectiveness[treatment_name]['risk'] + 0.02)
        print(f"Updated treatment effectiveness: {self.treatment_effectiveness}")


def simulate_doctor_action(patient_id, suggested_plan):
    
    actual_plan = list(suggested_plan)
    
    if random.random() < 0.2:
        if actual_plan:
            modified_item = random.choice(actual_plan)
            print(f"Doctor for {patient_id} modified: {modified_item['treatment']} - {modified_item['action']} -> {'no_change' if 'increase' in modified_item['action'] else 'increase'}")
            if 'increase' in modified_item['action']:
                modified_item['action'] = 'maintain_current'
            else:
                modified_item['action'] = 'increase_dose'
    
    print(f"Doctor for {patient_id} approves plan: {actual_plan}")
    return actual_plan

def get_initial_patient_metrics():
    return {
        'blood_sugar': random.randint(150, 200),
        'blood_pressure': random.randint(130, 150),
        'activity_level': random.randint(1, 5)
    }

available_treatments = {
    'DrugX': {'type': 'medication'}, 
    'DrugY': {'type': 'medication'}, 
    'DietY': {'type': 'lifestyle'}, 
    'ExerciseZ': {'type': 'lifestyle'}
}
advisor = TreatmentAdvisor(available_treatments)

patient_id = "patient_001"
current_patient_metrics = get_initial_patient_metrics()
print(f"--- Starting Healthcare Treatment Adjustment Loop for {patient_id} ---")
print(f"Initial patient metrics: {current_patient_metrics}")

for i in range(4):
    print(f"\n--- Week {i+1} ---")
    
    suggested_plan = advisor.assess_patient(patient_id, current_patient_metrics)
    
    actual_plan = simulate_doctor_action(patient_id, suggested_plan)
    
    outcome = advisor.get_patient_outcome(patient_id, suggested_plan, actual_plan)
    print(f"Simulated patient outcome: {outcome['status']}")
    
    for metric, delta in outcome['delta_metrics'].items():
        current_patient_metrics[metric] += delta
        current_patient_metrics[metric] = max(0, current_patient_metrics[metric])
    print(f"Patient metrics after week {i+1}: {current_patient_metrics}")
    
    advisor.learn_from_outcome(patient_id, suggested_plan, actual_plan, outcome)
    
print("\n--- Healthcare Treatment Adjustment Loop Finished ---")