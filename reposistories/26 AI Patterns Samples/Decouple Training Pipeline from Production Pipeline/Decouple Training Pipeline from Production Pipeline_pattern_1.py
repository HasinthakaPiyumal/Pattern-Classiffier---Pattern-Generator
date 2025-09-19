import random
import time

class RecommendationTrainingService:
    def __init__(self, model_store_url="http://model-store.ecommerce.com/"):
        self.model_store_url = model_store_url
        self.trained_model_info = None
        print("Recommendation Training Service Initialized. Focused on large-scale batch processing and model iteration.")

    def load_historical_user_data(self):
        print("Training: Loading massive historical user behavior data from HDFS/Data Lake (simulated 1TB).")
        time.sleep(2) 
        user_interactions = {"user_ids": [f"U{i}" for i in range(1000000)],
                             "item_ids": [f"I{random.randint(1, 10000)}" for _ in range(1000000)],
                             "interaction_type": [random.choice(["view", "click", "purchase"]) for _ in range(1000000)]}
        return user_interactions

    def feature_engineering_for_training(self, data):
        print("Training: Applying complex, experimental feature engineering (e.g., embedding generation, sequence modeling).")
        time.sleep(1.5) 
        processed_features = {"user_item_matrix": "simulated_sparse_matrix", "user_embeddings": "simulated_embeddings"}
        return processed_features

    def train_recommendation_model(self, processed_data):
        print("Training: Initiating distributed model training (e.g., Deep Learning on Kubernetes cluster with GPUs).")
        time.sleep(3) 
        model_version = f"RecModel_DeepLearning_v{int(time.time())}"
        model_metrics = {"precision@10": random.uniform(0.15, 0.35), "recall@10": random.uniform(0.10, 0.30)}
        self.trained_model_info = {"name": model_version, "metrics": model_metrics}
        print(f"Training: Model '{model_version}' trained. Metrics: {model_metrics}")
        return model_version

    def validate_model(self, model_name):
        print(f"Training: Running offline validation and preparing for A/B testing for model '{model_name}'.")
        time.sleep(1)
        print("Training: Validation complete. Model ready for publishing.")

    def publish_model(self, model_name):
        model_artifact_id = f"artifact_{model_name}"
        print(f"Training: Publishing model '{model_name}' artifacts to model store at '{self.model_store_url}{model_artifact_id}'.")
        return model_artifact_id

class RecommendationServingAPI:
    def __init__(self, model_store_url="http://model-store.ecommerce.com/"):
        self.model_store_url = model_store_url
        self.active_model_artifact = None
        print("Recommendation Serving API Initialized. Optimized for low-latency, high-throughput inference.")

    def load_active_model(self, model_artifact_id):
        print(f"Production: Loading active recommendation model '{model_artifact_id}' from '{self.model_store_url}{model_artifact_id}'.")
        time.sleep(0.1) 
        self.active_model_artifact = model_artifact_id
        return True

    def get_user_session_data(self, user_id):
        print(f"Production: Retrieving real-time session data for user '{user_id}' from cache/stream.")
        time.sleep(0.05) 
        session_data = {"user_id": user_id, "recently_viewed_items": [f"I{random.randint(1, 500)}" for _ in range(3)]}
        return session_data

    def prepare_data_for_inference(self, session_data):
        print("Production: Applying minimal, optimized preprocessing for real-time inference.")
        time.sleep(0.02) 
        inference_input = {"user_id": session_data['user_id'], "item_context": session_data['recently_viewed_items']}
        return inference_input

    def generate_recommendations(self, inference_input):
        if not self.active_model_artifact:
            raise ValueError("No active model loaded for recommendations.")
        print(f"Production: Generating recommendations using model '{self.active_model_artifact}' (low-latency API on edge servers).")
        time.sleep(0.03) 
        recommended_items = [f"I{random.randint(10001, 20000)}" for _ in range(5)]
        print(f"Production: User '{inference_input['user_id']}' recommended items: {', '.join(recommended_items)}")
        return {"user_id": inference_input['user_id'], "recommendations": recommended_items}

    def log_recommendation_event(self, recommendation_result):
        print(f"Production: Logging recommendation event for user {recommendation_result['user_id']} to analytics pipeline.")

if __name__ == "__main__":
    print("--- E-commerce Recommendation System ML Pipeline Demonstration ---")

    print("\n--- Initiating Training Service (Development/Experimentation) ---")
    training_service = RecommendationTrainingService()
    historical_data = training_service.load_historical_user_data()
    processed_training_features = training_service.feature_engineering_for_training(historical_data)
    trained_model_name = training_service.train_recommendation_model(processed_training_features)
    training_service.validate_model(trained_model_name)
    published_artifact_id = training_service.publish_model(trained_model_name)
    print(f"Training: Model '{trained_model_name}' (artifact ID: '{published_artifact_id}') is now ready for deployment consideration.")

    print("\n--- Simulating a new experimental training run for a different model type ---")
    new_training_service = RecommendationTrainingService() 
    new_historical_data = new_training_service.load_historical_user_data()
    new_processed_features = new_training_service.feature_engineering_for_training(new_historical_data)
    new_trained_model_name = new_training_service.train_recommendation_model(new_processed_features)
    new_training_service.validate_model(new_trained_model_name)
    new_published_artifact_id = new_training_service.publish_model(new_trained_model_name)
    print(f"Training: A new experimental model '{new_trained_model_name}' (artifact ID: '{new_published_artifact_id}') was trained.")


    print("\n--- Initiating Recommendation Serving API (Stable/Low-Latency Inference) ---")
    serving_api = RecommendationServingAPI()
    serving_api.load_active_model(published_artifact_id) 

    print("\n--- Simulating real-time user requests for recommendations ---")
    for i in range(3):
        user_id = f"Customer{2001+i}"
        session_data = serving_api.get_user_session_data(user_id)
        inference_input = serving_api.prepare_data_for_inference(session_data)
        recommendations = serving_api.generate_recommendations(inference_input)
        serving_api.log_recommendation_event(recommendations)
        time.sleep(0.3) 

    print("\n--- Simulating an update to a newer model in production (e.g., blue/green deployment) ---")
    serving_api.load_active_model(new_published_artifact_id)
    user_id = "Customer3000"
    session_data = serving_api.get_user_session_data(user_id)
    inference_input = serving_api.prepare_data_for_inference(session_data)
    recommendations = serving_api.generate_recommendations(inference_input)
    serving_api.log_recommendation_event(recommendations)

    print("\n--- E-commerce Recommendation System ML Pipeline Demonstration Complete ---")
