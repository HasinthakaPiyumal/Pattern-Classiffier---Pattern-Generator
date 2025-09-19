import random
import time

class ProductFeatureExtractor:
    def __init__(self):
        self.category_mapping = {}
        self.max_interactions = 0

    def fit(self, raw_data):
        all_categories = set()
        all_interaction_counts = []
        for item in raw_data:
            all_categories.add(item['category'])
            all_interaction_counts.append(item['views'] + item['purchases'])
        
        for i, cat in enumerate(sorted(list(all_categories))):
            self.category_mapping[cat] = i
        if all_interaction_counts:
            self.max_interactions = max(all_interaction_counts)
        else:
            self.max_interactions = 1 # Avoid division by zero

    def transform(self, raw_item):
        category_encoded = [0] * len(self.category_mapping)
        if raw_item['category'] in self.category_mapping:
            category_encoded[self.category_mapping[raw_item['category']]] = 1
        
        total_interactions = raw_item['views'] + raw_item['purchases']
        normalized_interactions = total_interactions / self.max_interactions
        
        return {
            'product_id': raw_item['product_id'],
            'category_features': category_encoded,
            'normalized_interactions': normalized_interactions,
            'price_level': 1 if raw_item['price'] > 50 else 0
        }

class RecommendationResult:
    def __init__(self, user_id, recommended_products, confidence_score):
        self.user_id = user_id
        self.recommended_products = recommended_products
        self.confidence_score = confidence_score

    def __str__(self):
        return f"User {self.user_id}: Recommended {self.recommended_products} with confidence {self.confidence_score:.2f}"

# --- Simulation of Training Pipeline ---
print("--- Training Pipeline Simulation ---")

# Raw training data (simulated user interactions with products)
train_raw_data = [
    {'product_id': 'P101', 'category': 'Electronics', 'views': 10, 'purchases': 2, 'price': 120},
    {'product_id': 'P102', 'category': 'Books', 'views': 5, 'purchases': 1, 'price': 15},
    {'product_id': 'P103', 'category': 'Electronics', 'views': 15, 'purchases': 3, 'price': 80},
    {'product_id': 'P104', 'category': 'HomeGoods', 'views': 8, 'purchases': 0, 'price': 30},
    {'product_id': 'P105', 'category': 'Books', 'views': 20, 'purchases': 5, 'price': 25},
]

# Initialize and fit the shared feature extractor on training data
feature_extractor = ProductFeatureExtractor()
feature_extractor.fit(train_raw_data)

# Process training data using the shared logic
train_processed_features = [feature_extractor.transform(item) for item in train_raw_data]

print("Processed features for training data:")
for feature in train_processed_features:
    print(feature)

# Simulate model training with processed features (simplified)
class MockModel:
    def predict(self, features):
        # A very simple mock prediction: recommend high-interaction products
        # and products from the 'Electronics' category based on feature values
        recommended = []
        if features['normalized_interactions'] > 0.6 and features['price_level'] == 1:
            recommended.append(f"High-Value Product {features['product_id']}")
        elif features['category_features'][feature_extractor.category_mapping.get('Electronics', -1)] == 1:
            recommended.append(f"Electronic Gadget {features['product_id']}")
        else:
            recommended.append(f"General Item {features['product_id']}")
        return recommended, random.uniform(0.7, 0.95)

mock_model = MockModel()

print("\n--- Serving Pipeline Simulation ---")

# Raw data for a live user query
live_user_id = "U001"
live_user_query_data = [
    {'product_id': 'P201', 'category': 'Electronics', 'views': 7, 'purchases': 1, 'price': 95},
    {'product_id': 'P202', 'category': 'Books', 'views': 3, 'purchases': 0, 'price': 10},
    {'product_id': 'P203', 'category': 'HomeGoods', 'views': 12, 'purchases': 2, 'price': 45},
]

# Process live data using the *same* shared feature extractor instance
live_processed_features = [feature_extractor.transform(item) for item in live_user_query_data]

print("Processed features for live user query:")
for feature in live_processed_features:
    print(feature)

# Simulate model inference and present results
all_recommendations = []
for features in live_processed_features:
    recommended_items, confidence = mock_model.predict(features)
    all_recommendations.extend(recommended_items)

final_recommendation = RecommendationResult(live_user_id, all_recommendations, sum(c for _, c in [mock_model.predict(f) for f in live_processed_features]) / len(live_processed_features))
print(f"\n{final_recommendation}")

# Another live query example
live_user_id_2 = "U002"
live_user_query_data_2 = [
    {'product_id': 'P204', 'category': 'Electronics', 'views': 25, 'purchases': 8, 'price': 250},
    {'product_id': 'P205', 'category': 'Books', 'views': 1, 'purchases': 0, 'price': 8},
]

live_processed_features_2 = [feature_extractor.transform(item) for item in live_user_query_data_2]

all_recommendations_2 = []
for features in live_processed_features_2:
    recommended_items, confidence = mock_model.predict(features)
    all_recommendations_2.extend(recommended_items)

final_recommendation_2 = RecommendationResult(live_user_id_2, all_recommendations_2, sum(c for _, c in [mock_model.predict(f) for f in live_processed_features_2]) / len(live_processed_features_2))
print(f"\n{final_recommendation_2}")