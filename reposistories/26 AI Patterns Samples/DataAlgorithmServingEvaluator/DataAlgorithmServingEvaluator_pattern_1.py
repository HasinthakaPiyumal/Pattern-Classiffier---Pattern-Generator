import random

class UserActivityDataSource:
    def fetch_user_interactions(self, user_id):
        print(f"DataSource: Fetching user {user_id}'s activity data...")
        products_viewed = [f"prod_{random.randint(100, 109)}" for _ in range(random.randint(3, 7))]
        products_purchased = [f"prod_{random.randint(100, 109)}" for _ in range(random.randint(0, 2))]
        
        data = {
            'user_id': user_id,
            'viewed_products': list(set(products_viewed)),
            'purchased_products': list(set(products_purchased)),
            'favorite_category': random.choice(['Electronics', 'Books', 'Clothing', 'HomeGoods']),
            'actual_purchased_next': random.choice([f"prod_{random.randint(100, 109)}", None])
        }
        if data['actual_purchased_next'] and data['actual_purchased_next'] in data['purchased_products']:
             data['actual_purchased_next'] = f"prod_{random.randint(110, 119)}"
        print(f"DataSource: Fetched data: {data}")
        return data

class RecommendationFeaturePreparator:
    def prepare_features(self, raw_data):
        print("DataPreparator: Preparing recommendation features...")
        all_products = [f"prod_{i}" for i in range(100, 120)]
        
        user_vector = {
            'user_id': raw_data['user_id'],
            'favorite_category_encoded': raw_data['favorite_category']
        }
        for prod_id in all_products:
            user_vector[f'viewed_{prod_id}'] = 1 if prod_id in raw_data['viewed_products'] else 0
            user_vector[f'purchased_{prod_id}'] = 1 if prod_id in raw_data['purchased_products'] else 0
        
        print(f"DataPreparator: Prepared features for user {raw_data['user_id']}")
        return user_vector

class ProductRecommender:
    def __init__(self):
        print("Algorithm (Serving): Initializing Product Recommender model...")
        self.product_category_map = {
            f"prod_{i}": random.choice(['Electronics', 'Books', 'Clothing', 'HomeGoods']) for i in range(100, 120)
        }

    def recommend_products(self, features, num_recommendations=3):
        print(f"Algorithm (Serving): Generating {num_recommendations} product recommendations...")
        
        user_id = features['user_id']
        favorite_cat = features['favorite_category_encoded']
        
        potential_recommendations = []
        for prod_id, category in self.product_category_map.items():
            if category == favorite_cat and features.get(f'purchased_{prod_id}', 0) == 0:
                potential_recommendations.append(prod_id)
        
        if len(potential_recommendations) < num_recommendations:
            all_products = [f"prod_{i}" for i in range(100, 120)]
            random_adds = [p for p in all_products if p not in potential_recommendations and features.get(f'purchased_{p}', 0) == 0]
            potential_recommendations.extend(random.sample(random_adds, min(num_recommendations - len(potential_recommendations), len(random_adds))))

        random.shuffle(potential_recommendations)
        recommendations = potential_recommendations[:num_recommendations]
        
        print(f"Algorithm (Serving): Recommended products for {user_id}: {recommendations}")
        return recommendations

class RecommendationEvaluator:
    def evaluate_recommendations(self, recommended_products, actual_purchased_product):
        print("Algorithm (Evaluator): Evaluating recommendations...")
        
        if actual_purchased_product is None:
            print("Evaluator: No actual purchase to evaluate against this time.")
            return "No actual purchase"

        if actual_purchased_product in recommended_products:
            evaluation_result = "Relevant (Hit)"
            print(f"Evaluator: Actual purchase '{actual_purchased_product}' was in recommendations: {evaluation_result}")
        else:
            evaluation_result = "Not Relevant (Miss)"
            print(f"Evaluator: Actual purchase '{actual_purchased_product}' was NOT in recommendations: {evaluation_result}")
        
        return evaluation_result

def run_ecommerce_recommendation_system(user_id):
    print("\n--- Running E-commerce Product Recommendation System ---")
    data_source = UserActivityDataSource()
    raw_user_data = data_source.fetch_user_interactions(user_id)
    data_preparator = RecommendationFeaturePreparator()
    prepared_features = data_preparator.prepare_features(raw_user_data)
    recommender = ProductRecommender()
    recommended_products = recommender.recommend_products(prepared_features, num_recommendations=3)
    evaluator = RecommendationEvaluator()
    actual_purchased = raw_user_data['actual_purchased_next']
    evaluation_result = evaluator.evaluate_recommendations(recommended_products, actual_purchased)
    print(f"--- System Finished for User {user_id}. Final Evaluation: {evaluation_result} ---")

run_ecommerce_recommendation_system(user_id="U001")
print("\n" + "="*80 + "\n")
run_ecommerce_recommendation_system(user_id="U002")