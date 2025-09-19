import hashlib
import json
import os
import platform
import sys
import datetime

class RecommendationModelVersion:
    def __init__(self, version_id, model_name, algorithm_type, algorithm_params,
                 data_snapshot_id, data_source_url, feature_engineering_steps,
                 environment_details, training_date, model_artifact_path):
        self.version_id = version_id
        self.model_name = model_name
        self.algorithm_type = algorithm_type
        self.algorithm_params = algorithm_params
        self.data_snapshot_id = data_snapshot_id
        self.data_source_url = data_source_url
        self.feature_engineering_steps = feature_engineering_steps
        self.environment_details = environment_details
        self.training_date = training_date
        self.model_artifact_path = model_artifact_path

    def to_dict(self):
        return {
            "version_id": self.version_id,
            "model_name": self.model_name,
            "algorithm_type": self.algorithm_type,
            "algorithm_params": self.algorithm_params,
            "data_snapshot_id": self.data_snapshot_id,
            "data_source_url": self.data_source_url,
            "feature_engineering_steps": self.feature_engineering_steps,
            "environment_details": self.environment_details,
            "training_date": self.training_date,
            "model_artifact_path": self.model_artifact_path
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class RecommendationRegistry:
    def __init__(self, registry_file="model_registry_ecommerce.json"):
        self.registry_file = registry_file
        self.versions = self._load_registry()

    def _load_registry(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                return {v_id: RecommendationModelVersion.from_dict(v_data) for v_id, v_data in data.items()}
        return {}

    def _save_registry(self):
        with open(self.registry_file, 'w') as f:
            json.dump({v_id: v.to_dict() for v_id, v in self.versions.items()}, f, indent=4)

    def register_model_version(self, model_version):
        if model_version.version_id in self.versions:
            print(f"Warning: Model version {model_version.version_id} already exists. Overwriting.")
        self.versions[model_version.version_id] = model_version
        self._save_registry()
        print(f"Recommendation model version {model_version.version_id} registered.")

    def get_model_version(self, version_id):
        return self.versions.get(version_id)

    def list_all_versions(self):
        return list(self.versions.values())

def get_environment_details():
    return {
        "python_version": sys.version,
        "os": platform.system(),
        "libraries": {
            "surprise": "0.1.0",
            "pandas": "1.4.1",
            "numpy": "1.22.2"
        },
        "hardware": "CPU"
    }

def simulate_train_recommender(model_name, algorithm_type, algorithm_params, data_snapshot_id, feature_engineering):
    model_file_name = f"{model_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bin"
    with open(model_file_name, 'w') as f:
        f.write("DUMMY_RECOMMENDER_MODEL_ARTIFACT")
    print(f"Simulated training for {model_name}. Model artifact saved to {model_file_name}")
    return model_file_name

class RecommendationEngine:
    def __init__(self, registry, version_id):
        self.registry = registry
        self.model_version_info = self.registry.get_model_version(version_id)
        if not self.model_version_info:
            raise ValueError(f"Recommendation model version {version_id} not found in registry.")
        print(f"RecommendationEngine initialized with model version: {version_id} ({self.model_version_info.model_name})")
        self.model = f"Loaded_Recommender_from_{self.model_version_info.model_artifact_path}"

    def get_recommendations(self, user_id, num_recommendations=5):
        print(f"Generating recommendations for user {user_id} using model '{self.model_version_info.model_name}' (v{self.model_version_info.version_id})")
        print(f"  Algorithm: {self.model_version_info.algorithm_type}, trained on data snapshot: {self.model_version_info.data_snapshot_id}")
        if user_id == "user_A":
            return ["ProductX", "ProductY", "ProductZ"][:num_recommendations]
        elif user_id == "user_B":
            return ["Item1", "Item2", "Item3", "Item4"][:num_recommendations]
        return ["GenericProduct1", "GenericProduct2"][:num_recommendations]

if __name__ == "__main__":
    registry = RecommendationRegistry()

    print("\n--- Training and Registering Recommendation Model v1.0 (Collaborative Filtering) ---")
    model_v1_params = {"k": 40, "sim_options": {"name": "pearson", "user_based": False}}
    data_v1_fe_steps = ["user-item matrix creation", "implicit feedback conversion"]
    data_v1_snapshot_id = hashlib.sha256("ecommerce_data_20230101".encode()).hexdigest()[:8]
    model_v1_artifact_path = simulate_train_recommender("ItemCF_RecSys", "Item-Based CF",
                                                        model_v1_params, data_v1_snapshot_id, data_v1_fe_steps)

    model_v1 = RecommendationModelVersion(
        version_id="v1.0",
        model_name="ItemCF_RecSys",
        algorithm_type="Item-Based Collaborative Filtering",
        algorithm_params=model_v1_params,
        data_snapshot_id=data_v1_snapshot_id,
        data_source_url="s3://ecommerce-data-lake/2023Q1_interactions.csv",
        feature_engineering_steps=data_v1_fe_steps,
        environment_details=get_environment_details(),
        training_date=datetime.datetime.now().isoformat(),
        model_artifact_path=model_v1_artifact_path
    )
    registry.register_model_version(model_v1)

    print("\n--- Training and Registering Recommendation Model v1.1 (SVD) ---")
    model_v2_params = {"n_factors": 50, "n_epochs": 20, "lr_all": 0.005}
    data_v2_fe_steps = ["user-item matrix creation", "explicit feedback (ratings)", "cold-start handling"]
    data_v2_snapshot_id = hashlib.sha256("ecommerce_data_20230701".encode()).hexdigest()[:8]
    model_v2_artifact_path = simulate_train_recommender("SVD_RecSys_Improved", "SVD",
                                                        model_v2_params, data_v2_snapshot_id, data_v2_fe_steps)

    env_details_v2 = get_environment_details()
    env_details_v2["hardware"] = "GPU (NVIDIA A100)"
    env_details_v2["libraries"]["tensorflow"] = "2.9.1"

    model_v2 = RecommendationModelVersion(
        version_id="v1.1",
        model_name="SVD_RecSys_Improved",
        algorithm_type="Singular Value Decomposition (SVD)",
        algorithm_params=model_v2_params,
        data_snapshot_id=data_v2_snapshot_id,
        data_source_url="s3://ecommerce-data-lake/2023Q3_interactions.csv",
        feature_engineering_steps=data_v2_fe_steps,
        environment_details=env_details_v2,
        training_date=datetime.datetime.now().isoformat(),
        model_artifact_path=model_v2_artifact_path
    )
    registry.register_model_version(model_v2)

    print("\n--- Simulating A/B testing with different model versions ---")

    print("\n--- Recommendations for User Segment A (using v1.0) ---")
    try:
        recommender_v1 = RecommendationEngine(registry, "v1.0")
        print(f"User A recommendations: {recommender_v1.get_recommendations('user_A')}")
        print(f"User C recommendations: {recommender_v1.get_recommendations('user_C')}")
    except ValueError as e:
        print(e)

    print("\n--- Recommendations for User Segment B (using v1.1) ---")
    try:
        recommender_v2 = RecommendationEngine(registry, "v1.1")
        print(f"User B recommendations: {recommender_v2.get_recommendations('user_B')}")
        print(f"User D recommendations: {recommender_v2.get_recommendations('user_D')}")
    except ValueError as e:
        print(e)

    print("\n--- Debugging recommendations from v1.0 ---")
    debugged_version_info = registry.get_model_version("v1.0")
    if debugged_version_info:
        print(f"Details for v1.0 used for debugging:")
        print(f"  Algorithm Type: {debugged_version_info.algorithm_type}")
        print(f"  Algorithm Parameters: {debugged_version_info.algorithm_params}")
        print(f"  Data Snapshot ID: {debugged_version_info.data_snapshot_id}")
        print(f"  Data Source URL: {debugged_version_info.data_source_url}")
        print(f"  Feature Engineering: {debugged_version_info.feature_engineering_steps}")
        print(f"  Training Environment: {debugged_version_info.environment_details['python_version']}, Hardware: {debugged_version_info.environment_details['hardware']}")
        print(f"  Model Artifact Path: {debugged_version_info.model_artifact_path}")
    else:
        print("Model v1.0 not found for debugging.")

    for version_info in registry.list_all_versions():
        if os.path.exists(version_info.model_artifact_path):
            os.remove(version_info.model_artifact_path)
    if os.path.exists(registry.registry_file):
        os.remove(registry.registry_file)
