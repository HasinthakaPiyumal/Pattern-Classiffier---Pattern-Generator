import random
import time

class HealthcareTrainingPlatform:
    def __init__(self, model_registry_path="model_registry/"):
        self.model_registry_path = model_registry_path
        self.current_model = None
        print("Healthcare Training Platform Initialized. Ready for experimentation.")

    def load_training_data(self):
        print("Training: Loading large historical patient dataset from data lake (simulated 100GB).")
        time.sleep(1) 
        return {"patient_features": [[random.random() for _ in range(50)] for _ in range(100000)], "readmission_labels": [random.randint(0, 1) for _ in range(100000)]}

    def preprocess_data_for_training(self, data):
        print("Training: Applying flexible and experimental feature engineering (e.g., trying new aggregations).")
        time.sleep(0.5) 
        processed_data = {"features": data["patient_features"], "labels": data["readmission_labels"]}
        return processed_data

    def train_model(self, processed_data):
        print("Training: Starting resource-intensive model training on GPU cluster (simulated 2 hours).")
        time.sleep(2) 
        model_performance = random.uniform(0.75, 0.95)
        self.current_model = f"ReadmissionModel_v{int(time.time())}"
        print(f"Training: Model '{self.current_model}' trained with accuracy: {model_performance:.2f}")
        return self.current_model

    def evaluate_model(self, model_name, test_data):
        print(f"Training: Evaluating model '{model_name}' on held-out validation set.")
        time.sleep(0.5)
        print("Training: Comprehensive evaluation completed.")

    def save_model(self, model_name):
        model_path = f"{self.model_registry_path}{model_name}.pkl"
        print(f"Training: Saving trained model '{model_name}' to model registry at '{model_path}'.")
        return model_path

class HealthcareProductionSystem:
    def __init__(self, model_registry_path="model_registry/"):
        self.model_registry_path = model_registry_path
        self.active_model = None
        print("Healthcare Production System Initialized. Optimized for stability and low-latency inference.")

    def load_production_model(self, model_name):
        model_path = f"{self.model_registry_path}{model_name}.pkl"
        print(f"Production: Loading stable production model '{model_name}' from '{model_path}'.")
        time.sleep(0.1) 
        self.active_model = model_name
        return True

    def receive_patient_admission(self, patient_data):
        print(f"Production: Receiving real-time patient admission data for ID: {patient_data['patient_id']}.")
        return patient_data

    def preprocess_data_for_inference(self, patient_data):
        print("Production: Applying fixed, optimized preprocessing for inference.")
        time.sleep(0.05) 
        inference_features = [random.random() for _ in range(50)] 
        return {"patient_id": patient_data['patient_id'], "features": inference_features}

    def predict_readmission(self, processed_data):
        if not self.active_model:
            raise ValueError("No active model loaded in production.")
        print(f"Production: Predicting readmission risk using model '{self.active_model}' (optimized for CPU inference).")
        time.sleep(0.01) 
        prediction_score = random.uniform(0.05, 0.95)
        print(f"Production: Patient ID {processed_data['patient_id']} readmission risk: {prediction_score:.2f}")
        return {"patient_id": processed_data['patient_id'], "risk_score": prediction_score}

    def log_prediction(self, prediction_result):
        print(f"Production: Logging prediction for patient {prediction_result['patient_id']} (risk: {prediction_result['risk_score']:.2f}) to audit system.")

if __name__ == "__main__":
    print("--- Healthcare System ML Pipeline Demonstration ---")

    print("\n--- Initiating Training Pipeline (Development/Experimentation) ---")
    training_platform = HealthcareTrainingPlatform()
    training_data = training_platform.load_training_data()
    processed_training_data = training_platform.preprocess_data_for_training(training_data)
    trained_model_name = training_platform.train_model(processed_training_data)
    training_platform.evaluate_model(trained_model_name, {"test_data": "simulated_test"})
    saved_model_path = training_platform.save_model(trained_model_name)
    print(f"Training: Model '{trained_model_name}' is now available for deployment.")

    print("\n--- Simulating another experimental training run ---")
    new_training_platform = HealthcareTrainingPlatform() 
    new_training_data = new_training_platform.load_training_data()
    new_processed_data = new_training_platform.preprocess_data_for_training(new_training_data)
    new_trained_model_name = new_training_platform.train_model(new_processed_data)
    new_training_platform.evaluate_model(new_trained_model_name, {"test_data": "simulated_test_new"})
    new_saved_model_path = new_training_platform.save_model(new_trained_model_name)
    print(f"Training: A new model '{new_trained_model_name}' was trained and saved. This flexibility is key for development.")


    print("\n--- Initiating Production Pipeline (Stable/Low-Latency Inference) ---")
    production_system = HealthcareProductionSystem()
    production_system.load_production_model(trained_model_name) 

    print("\n--- Simulating real-time patient admissions for prediction ---")
    for i in range(3):
        patient_admission_data = {"patient_id": f"P{1001+i}", "admission_details": "emergency"}
        received_data = production_system.receive_patient_admission(patient_admission_data)
        processed_inference_data = production_system.preprocess_data_for_inference(received_data)
        prediction = production_system.predict_readmission(processed_inference_data)
        production_system.log_prediction(prediction)
        time.sleep(0.2) 

    print("\n--- Attempting to deploy the *new* experimental model to production (for demonstration purposes, typically requires more checks) ---")
    production_system.load_production_model(new_trained_model_name)
    patient_admission_data = {"patient_id": "P2000", "admission_details": "routine"}
    received_data = production_system.receive_patient_admission(patient_admission_data)
    processed_inference_data = production_system.preprocess_data_for_inference(received_data)
    prediction = production_system.predict_readmission(processed_inference_data)
    production_system.log_prediction(prediction)

    print("\n--- Healthcare System ML Pipeline Demonstration Complete ---")
