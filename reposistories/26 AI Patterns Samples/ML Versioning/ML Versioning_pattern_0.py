import hashlib
import json
import os
import platform
import sys
import datetime

class ModelVersion:
    def __init__(self, version_id, model_name, model_type, hyperparameters,
                 data_version_id, data_source, data_preprocessing_steps,
                 system_info, training_timestamp, model_path):
        self.version_id = version_id
        self.model_name = model_name
        self.model_type = model_type
        self.hyperparameters = hyperparameters
        self.data_version_id = data_version_id
        self.data_source = data_source
        self.data_preprocessing_steps = data_preprocessing_steps
        self.system_info = system_info
        self.training_timestamp = training_timestamp
        self.model_path = model_path

    def to_dict(self):
        return {
            "version_id": self.version_id,
            "model_name": self.model_name,
            "model_type": self.model_type,
            "hyperparameters": self.hyperparameters,
            "data_version_id": self.data_version_id,
            "data_source": self.data_source,
            "data_preprocessing_steps": self.data_preprocessing_steps,
            "system_info": self.system_info,
            "training_timestamp": self.training_timestamp,
            "model_path": self.model_path
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class ModelRegistry:
    def __init__(self, registry_file="model_registry_healthcare.json"):
        self.registry_file = registry_file
        self.versions = self._load_registry()

    def _load_registry(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                return {v_id: ModelVersion.from_dict(v_data) for v_id, v_data in data.items()}
        return {}

    def _save_registry(self):
        with open(self.registry_file, 'w') as f:
            json.dump({v_id: v.to_dict() for v_id, v in self.versions.items()}, f, indent=4)

    def register_model_version(self, model_version):
        if model_version.version_id in self.versions:
            print(f"Warning: Model version {model_version.version_id} already exists. Overwriting.")
        self.versions[model_version.version_id] = model_version
        self._save_registry()
        print(f"Model version {model_version.version_id} registered.")

    def get_model_version(self, version_id):
        return self.versions.get(version_id)

    def list_all_versions(self):
        return list(self.versions.values())

def get_system_info():
    return {
        "python_version": sys.version,
        "os": platform.system(),
        "processor": platform.processor(),
        "libraries": {
            "scikit-learn": "1.0.2",
            "pandas": "1.4.1",
            "numpy": "1.22.2"
        }
    }

def simulate_train_model(model_name, model_type, hyperparameters, data_id, data_preprocessing):
    model_file_name = f"{model_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pkl"
    with open(model_file_name, 'w') as f:
        f.write("DUMMY_MODEL_CONTENT")
    print(f"Simulated training for {model_name}. Model saved to {model_file_name}")
    return model_file_name

class DiseasePredictor:
    def __init__(self, model_registry, version_id):
        self.model_registry = model_registry
        self.model_version_info = self.model_registry.get_model_version(version_id)
        if not self.model_version_info:
            raise ValueError(f"Model version {version_id} not found in registry.")
        print(f"DiseasePredictor initialized with model version: {version_id} ({self.model_version_info.model_name})")
        self.model = f"Loaded_Model_from_{self.model_version_info.model_path}"

    def predict(self, patient_data):
        print(f"Using model '{self.model_version_info.model_name}' (v{self.model_version_info.version_id}) trained on data v{self.model_version_info.data_version_id} for prediction.")
        print(f"Patient data: {patient_data}")
        if "fever" in patient_data and patient_data["fever"] > 38.0 and "cough" in patient_data:
            return "Flu"
        elif "chest_pain" in patient_data and patient_data["chest_pain"] == "severe":
            return "Cardiac Risk"
        return "Healthy"

if __name__ == "__main__":
    registry = ModelRegistry()

    print("\n--- Training and Registering Model v1.0 ---")
    model_v1_hyperparams = {"n_estimators": 100, "max_depth": 10, "random_state": 42}
    data_v1_preprocessing = ["min-max scaling", "impute missing with mean"]
    data_v1_id = hashlib.sha256("patient_data_20230101".encode()).hexdigest()[:8]
    model_v1_path = simulate_train_model("DiseasePredictor_RF", "RandomForestClassifier",
                                         model_v1_hyperparams, data_v1_id, data_v1_preprocessing)

    model_v1 = ModelVersion(
        version_id="v1.0",
        model_name="DiseasePredictor_RF",
        model_type="RandomForestClassifier",
        hyperparameters=model_v1_hyperparams,
        data_version_id=data_v1_id,
        data_source="Electronic_Health_Records_2023Q1",
        data_preprocessing_steps=data_v1_preprocessing,
        system_info=get_system_info(),
        training_timestamp=datetime.datetime.now().isoformat(),
        model_path=model_v1_path
    )
    registry.register_model_version(model_v1)

    print("\n--- Training and Registering Model v1.1 ---")
    model_v2_hyperparams = {"n_estimators": 150, "max_depth": 12, "min_samples_leaf": 5, "random_state": 42}
    data_v2_preprocessing = ["standard scaling", "impute missing with median", "feature engineering: BMI"]
    data_v2_id = hashlib.sha256("patient_data_20230601".encode()).hexdigest()[:8]
    model_v2_path = simulate_train_model("DiseasePredictor_RF_Improved", "RandomForestClassifier",
                                         model_v2_hyperparams, data_v2_id, data_v2_preprocessing)

    model_v2 = ModelVersion(
        version_id="v1.1",
        model_name="DiseasePredictor_RF_Improved",
        model_type="RandomForestClassifier",
        hyperparameters=model_v2_hyperparams,
        data_version_id=data_v2_id,
        data_source="Electronic_Health_Records_2023Q2",
        data_preprocessing_steps=data_v2_preprocessing,
        system_info=get_system_info(),
        training_timestamp=datetime.datetime.now().isoformat(),
        model_path=model_v2_path
    )
    registry.register_model_version(model_v2)

    print("\n--- Using specific model versions for prediction ---")

    print("\n--- Doctor's Office A (using v1.0) ---")
    try:
        predictor_v1 = DiseasePredictor(registry, "v1.0")
        patient_a = {"age": 45, "fever": 38.5, "cough": "mild", "fatigue": True}
        print(f"Prediction for Patient A (v1.0): {predictor_v1.predict(patient_a)}")
        patient_b = {"age": 60, "chest_pain": "severe", "shortness_of_breath": True}
        print(f"Prediction for Patient B (v1.0): {predictor_v1.predict(patient_b)}")
    except ValueError as e:
        print(e)

    print("\n--- Hospital Department B (using v1.1) ---")
    try:
        predictor_v2 = DiseasePredictor(registry, "v1.1")
        patient_c = {"age": 30, "fever": 37.0, "cough": "none", "fatigue": False}
        print(f"Prediction for Patient C (v1.1): {predictor_v2.predict(patient_c)}")
        patient_d = {"age": 55, "fever": 39.2, "cough": "severe", "headache": True}
        print(f"Prediction for Patient D (v1.1): {predictor_v2.predict(patient_d)}")
    except ValueError as e:
        print(e)

    print("\n--- Auditing a past prediction made with v1.0 ---")
    audited_version_info = registry.get_model_version("v1.0")
    if audited_version_info:
        print(f"Auditing details for v1.0:")
        print(f"  Model Type: {audited_version_info.model_type}")
        print(f"  Hyperparameters: {audited_version_info.hyperparameters}")
        print(f"  Data Version ID: {audited_version_info.data_version_id}")
        print(f"  Data Source: {audited_version_info.data_source}")
        print(f"  Preprocessing: {audited_version_info.data_preprocessing_steps}")
        print(f"  Training System: {audited_version_info.system_info['python_version']}, OS: {audited_version_info.system_info['os']}")
        print(f"  Model Path: {audited_version_info.model_path}")
    else:
        print("Model v1.0 not found for auditing.")

    for version_info in registry.list_all_versions():
        if os.path.exists(version_info.model_path):
            os.remove(version_info.model_path)
    if os.path.exists(registry.registry_file):
        os.remove(registry.registry_file)
