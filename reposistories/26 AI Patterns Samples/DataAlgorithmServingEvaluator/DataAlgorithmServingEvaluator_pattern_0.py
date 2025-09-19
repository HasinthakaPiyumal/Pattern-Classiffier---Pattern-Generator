import random

class PatientRecordDataSource:
    def fetch_patient_data(self, patient_id):
        print(f"DataSource: Fetching raw data for patient {patient_id}...")
        data = {
            'patient_id': patient_id,
            'age': random.randint(30, 80),
            'gender': random.choice(['Male', 'Female']),
            'blood_pressure_systolic': random.randint(100, 180),
            'blood_pressure_diastolic': random.randint(60, 110),
            'cholesterol_ldl': random.randint(80, 200),
            'has_diabetes': random.choice([True, False]),
            'actual_disease_outcome': random.choice([True, False])
        }
        print(f"DataSource: Fetched data: {data}")
        return data

class MedicalFeaturePreparator:
    def prepare_features(self, raw_data):
        print("DataPreparator: Preparing medical features...")
        prepared_features = {
            'age_normalized': raw_data['age'] / 100.0,
            'is_male': 1 if raw_data['gender'] == 'Male' else 0,
            'bp_ratio': raw_data['blood_pressure_systolic'] / raw_data['blood_pressure_diastolic'],
            'cholesterol_level': raw_data['cholesterol_ldl'],
            'diabetes_status': 1 if raw_data['has_diabetes'] else 0
        }
        print(f"DataPreparator: Prepared features: {prepared_features}")
        return prepared_features

class DiseaseRiskPredictor:
    def __init__(self):
        print("Algorithm (Serving): Initializing Disease Risk Predictor model...")
        self.model_weights = {
            'age_normalized': 0.1,
            'is_male': 0.05,
            'bp_ratio': 0.2,
            'cholesterol_level': 0.005,
            'diabetes_status': 0.3
        }
        self.intercept = -0.5

    def predict_risk(self, features):
        print("Algorithm (Serving): Predicting disease risk...")
        score = self.intercept
        for feature, weight in self.model_weights.items():
            if feature in features:
                score += features[feature] * weight
        
        risk_probability = 1 / (1 + (2.71828 ** -score))
        print(f"Algorithm (Serving): Predicted risk probability: {risk_probability:.2f}")
        return risk_probability

class RiskPredictionEvaluator:
    def evaluate_prediction(self, predicted_risk, actual_outcome_true):
        print("Algorithm (Evaluator): Evaluating prediction...")
        predicted_outcome = predicted_risk > 0.5
        
        if predicted_outcome == actual_outcome_true:
            evaluation_result = "Correct"
        else:
            evaluation_result = "Incorrect"
        
        print(f"Evaluator: Predicted: {predicted_outcome}, Actual: {actual_outcome_true} -> Result: {evaluation_result}")
        return evaluation_result

def run_healthcare_prediction_system(patient_id):
    print("\n--- Running Healthcare Patient Risk Prediction System ---")
    data_source = PatientRecordDataSource()
    raw_patient_data = data_source.fetch_patient_data(patient_id)
    data_preparator = MedicalFeaturePreparator()
    prepared_features = data_preparator.prepare_features(raw_patient_data)
    predictor = DiseaseRiskPredictor()
    predicted_risk = predictor.predict_risk(prepared_features)
    evaluator = RiskPredictionEvaluator()
    actual_outcome = raw_patient_data['actual_disease_outcome']
    evaluation_result = evaluator.evaluate_prediction(predicted_risk, actual_outcome)
    print(f"--- System Finished for Patient {patient_id}. Final Evaluation: {evaluation_result} ---")

run_healthcare_prediction_system(patient_id="P001")
print("\n" + "="*80 + "\n")
run_healthcare_prediction_system(patient_id="P002")