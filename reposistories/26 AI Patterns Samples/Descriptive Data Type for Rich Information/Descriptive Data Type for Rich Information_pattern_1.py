
from typing import List, Dict

class RecommendationScore:
    def __init__(self, score: float, user_id: str, product_id: str,
                 model_name: str, score_type: str, explanation_features: Dict[str, float],
                 relevance_threshold: float = 0.5):
        if not (0.0 <= score <= 1.0):
            raise ValueError("Score must be between 0 and 1.")
        self.score = score
        self.user_id = user_id
        self.product_id = product_id
        self.model_name = model_name
        self.score_type = score_type
        self.explanation_features = explanation_features
        self.relevance_threshold = relevance_threshold

    def __repr__(self):
        return (f"RecommendationScore(user='{self.user_id}', product='{self.product_id}', "
                f"score={self.score:.4f}, type='{self.score_type}', model='{self.model_name}', "
                f"explanation={self.explanation_features})")

    def is_relevant(self) -> bool:
        return self.score >= self.relevance_threshold

def simulate_recommendation_engine(user_id: str, available_products: List[str]) -> List[RecommendationScore]:
    recommendations = []
    
    user_preferences = {
        "U001": {"P101": 0.9, "P102": 0.3, "P103": 0.8, "P104": 0.6},
        "U002": {"P101": 0.2, "P102": 0.95, "P103": 0.4, "P104": 0.85},
        "U003": {"P101": 0.7, "P102": 0.75, "P103": 0.9, "P104": 0.2},
    }

    for product_id in available_products:
        score_val = user_preferences.get(user_id, {}).get(product_id, 0.5)
        
        features = {}
        if product_id == "P101":
            features["user_history_category_A"] = 0.7 * score_val
            features["similar_users_purchased"] = 0.3 * score_val
        elif product_id == "P102":
            features["user_view_duration"] = 0.8 * score_val
            features["seasonal_trend"] = 0.2 * score_val
        else:
            features["default_affinity"] = 0.5 * score_val
            features["new_product_boost"] = 0.5 * score_val

        recommendations.append(
            RecommendationScore(
                score=score_val,
                user_id=user_id,
                product_id=product_id,
                model_name="ProductRecNet_v4.1",
                score_type="purchase_probability",
                explanation_features=features
            )
        )
    return recommendations

if __name__ == "__main__":
    print("--- E-commerce System: Product Recommendation ---")

    all_products = ["P101", "P102", "P103", "P104"]
    
    user1_recs = simulate_recommendation_engine("U001", all_products)
    print(f"\nRecommendations for User U001:")
    for rec in user1_recs:
        print(f"  {rec}")
        if rec.is_relevant():
            print(f"    -> Highly relevant! Explanation: {rec.explanation_features}")
        else:
            print(f"    -> Less relevant. Explanation: {rec.explanation_features}")

    user2_recs = simulate_recommendation_engine("U002", all_products)
    print(f"\nRecommendations for User U002:")
    for rec in user2_recs:
        print(f"  {rec}")
        if rec.is_relevant(relevance_threshold=0.7):
            print(f"    -> Very relevant for U002! Explanation: {rec.explanation_features}")
        else:
            print(f"    -> Not highly relevant for U002. Explanation: {rec.explanation_features}")

    try:
        invalid_rec = RecommendationScore(1.5, "U004", "P105", "BadModel", "bad_score", {})
    except ValueError as e:
        print(f"\nAttempted to create invalid recommendation: {e}")
