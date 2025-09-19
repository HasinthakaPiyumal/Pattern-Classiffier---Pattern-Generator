import random

class ProductRecommendationGenerator:
    def __init__(self, all_products):
        self.all_products = all_products

    def generate_recommendations(self, user_id, num_candidates=5):
        candidate_recommendations = []
        for _ in range(num_candidates):
            recommendation_list = random.sample(self.all_products, 3)
            candidate_recommendations.append(recommendation_list)
        return candidate_recommendations

class RecommendationRewardModel:
    def __init__(self, user_preferences):
        self.user_preferences = user_preferences

    def score_recommendation(self, recommendation_list):
        score = 0
        for product in recommendation_list:
            if product['category'] == self.user_preferences.get('category'):
                score += 0.6
            if product['brand'] == self.user_preferences.get('brand_affinity'):
                score += 0.4
            score += random.uniform(-0.1, 0.1)
        return score

all_available_products = [
    {'id': 'P1', 'name': 'Laptop X', 'category': 'electronics', 'brand': 'Sony'},
    {'id': 'P2', 'name': 'Smartphone Y', 'category': 'electronics', 'brand': 'Samsung'},
    {'id': 'P3', 'name': 'Headphones Z', 'category': 'audio', 'brand': 'Bose'},
    {'id': 'P4', 'name': 'Smart TV A', 'category': 'electronics', 'brand': 'Sony'},
    {'id': 'P5', 'name': 'Gaming Mouse B', 'category': 'accessories', 'brand': 'Logitech'},
    {'id': 'P6', 'name': 'Wireless Charger C', 'category': 'electronics', 'brand': 'Anker'},
    {'id': 'P7', 'name': 'Coffee Maker D', 'category': 'home_appliances', 'brand': 'Keurig'},
]

current_user_id = 'user_123'
user_preferences_for_scoring = {'category': 'electronics', 'brand_affinity': 'Sony'}

if __name__ == "__main__":
    recommendation_generator = ProductRecommendationGenerator(all_available_products)
    num_candidates_to_generate = 10
    candidate_recommendation_lists = recommendation_generator.generate_recommendations(current_user_id, num_candidates_to_generate)

    reward_model = RecommendationRewardModel(user_preferences_for_scoring)
    scored_candidates = []
    for rec_list in candidate_recommendation_lists:
        score = reward_model.score_recommendation(rec_list)
        scored_candidates.append({'recommendation': rec_list, 'score': score})

    best_recommendation = max(scored_candidates, key=lambda x: x['score'])
    final_output = {
        "recommended_products": [p['name'] for p in best_recommendation['recommendation']],
        "score": best_recommendation['score']
    }
