import random
import time

class PatientFeaturePreprocessor:
    def __init__(self):
        self.mean_glucose = 0.0
        self.std_dev_glucose = 1.0
        self.diagnosis_vocabulary = set()

    def fit(self, raw_patient_data_list):
        all_glucose_levels = []
        for patient_data in raw_patient_data_list:
            all_glucose_levels.append(patient_data['glucose_level'])
            for diagnosis in patient_data['diagnoses']:
                self.diagnosis_vocabulary.add(diagnosis)
        
        if all_glucose_levels:
            self.mean_glucose = sum(all_glucose_levels) / len(all_glucose_levels)
            self.std_dev_glucose = (sum((x - self.mean_glucose) ** 2 for x in all_glucose_levels) / len(all_glucose_levels)) ** 0.5
        
        if self.std_dev_glucose == 0: # Avoid division by zero if all glucose levels are identical
            self.std_dev_glucose = 1.0

    def transform(self, raw_patient_data):
        # Age binning
        age = raw_patient_data['age']
        age_bin_young = 1 if age < 30 else 0
        age_bin_middle = 1 if 30 <= age < 60 else 0
        age_bin_old = 1 if age >= 60 else 0

        # Glucose normalization (Z-score)
        normalized_glucose = (raw_patient_data['glucose_level'] - self.mean_glucose) / self.std_dev_glucose

        # One-hot encoding for diagnoses
        diagnosis_features = {f'diag_{d}': (1 if d in raw_patient_data['diagnoses'] else 0) for d in self.diagnosis_vocabulary}
        
        # Combine features
        processed_features = {
            'patient_id': raw_patient_data['patient_id'],
            'age_young': age_bin_young,
            'age_middle': age_bin_middle,
            'age_old': age_bin_old,
            'normalized_glucose': normalized_glucose,
            **diagnosis_features
        }
        return processed_features

class PatientRiskAssessment:
    def __init__(self, patient_id, risk_score, risk_level, contributing_factors):
        self.patient_id = patient_id
        self.risk_score = risk_score
        self.risk_level = risk_level
        self.contributing_factors = contributing_factors

    def __str__(self):
        return f"Patient {self.patient_id}: Risk Score {self.risk_score:.2f} ({self.risk_level}). Factors: {', '.join(self.contributing_factors)}"

# --- Simulation of Training Pipeline ---
print("--- Training Pipeline Simulation ---")

# Raw historical patient data
historical_patients_raw = [
    {'patient_id': 'P001', 'age': 25, 'glucose_level': 90, 'diagnoses': ['None']},
    {'patient_id': 'P002', 'age': 45, 'glucose_level': 130, 'diagnoses': ['Hypertension', 'Diabetes']},
    {'patient_id': 'P003', 'age': 70, 'glucose_level': 105, 'diagnoses': ['HeartDisease']},
    {'patient_id': 'P004', 'age': 55, 'glucose_level': 115, 'diagnoses': ['Hypertension']},
    {'patient_id': 'P005', 'age': 35, 'glucose_level': 95, 'diagnoses': ['None']},
    {'patient_id': 'P006', 'age': 62, 'glucose_level': 140, 'diagnoses': ['Diabetes', 'KidneyDisease']},
]

# Initialize and fit the shared preprocessor on training data
preprocessor = PatientFeaturePreprocessor()
preprocessor.fit(historical_patients_raw)

# Process training data using the shared logic
train_processed_features = [preprocessor.transform(p) for p in historical_patients_raw]

print("Processed features for training data:")
for feature in train_processed_features:
    print(feature)

# Simulate model training (simplified)
class MockRiskModel:
    def predict_risk(self, features):
        score = 0.0
        factors = []
        if features.get('age_old', 0) == 1: score += 0.3; factors.append('Age_old')
        if features.get('age_middle', 0) == 1: score += 0.1; factors.append('Age_middle')
        if features['normalized_glucose'] > 0.5: score += 0.4; factors.append('High_Glucose')
        if features.get('diag_Diabetes', 0) == 1: score += 0.5; factors.append('Diabetes')
        if features.get('diag_Hypertension', 0) == 1: score += 0.3; factors.append('Hypertension')
        if features.get('diag_HeartDisease', 0) == 1: score += 0.6; factors.append('HeartDisease')

        risk_level = "Low"
        if score > 0.8: risk_level = "High"
        elif score > 0.4: risk_level = "Medium"
        
        return min(score, 1.0), risk_level, factors if factors else ['No significant factors identified']

mock_risk_model = MockRiskModel()

print("\n--- Serving Pipeline Simulation ---")

# Raw data for a new patient in a live setting
new_patient_raw = {'patient_id': 'P007', 'age': 58, 'glucose_level': 125, 'diagnoses': ['Hypertension']}

# Process new patient data using the *same* shared preprocessor instance
new_patient_processed = preprocessor.transform(new_patient_raw)

print("Processed features for new patient:")
print(new_patient_processed)

# Simulate model inference and present results
risk_score, risk_level, contributing_factors = mock_risk_model.predict_risk(new_patient_processed)
assessment = PatientRiskAssessment(new_patient_raw['patient_id'], risk_score, risk_level, contributing_factors)
print(f"\n{assessment}")

# Another new patient example
new_patient_raw_2 = {'patient_id': 'P008', 'age': 72, 'glucose_level': 150, 'diagnoses': ['Diabetes', 'HeartDisease']}
new_patient_processed_2 = preprocessor.transform(new_patient_raw_2)
risk_score_2, risk_level_2, contributing_factors_2 = mock_risk_model.predict_risk(new_patient_processed_2)
assessment_2 = PatientRiskAssessment(new_patient_raw_2['patient_id'], risk_score_2, risk_level_2, contributing_factors_2)
print(f"\n{assessment_2}")
