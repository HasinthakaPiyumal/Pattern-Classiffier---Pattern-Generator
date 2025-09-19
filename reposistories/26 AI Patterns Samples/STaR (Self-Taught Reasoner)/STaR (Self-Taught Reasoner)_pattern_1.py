import random

class SimulatedLLMEcommerce:
    def __init__(self):
        self.recommendation_knowledge = {
            "electronics,gaming": ("Gaming Laptop", "User shows interest in electronics and gaming. A high-performance gaming laptop is a suitable recommendation."),
            "books,fantasy": ("Epic Fantasy Series", "Past purchases indicate a strong preference for fantasy books. Recommend a popular epic fantasy series."),
        }
        self.success_rate = 0.5

    def generate_rationale_and_recommendation(self, user_profile):
        interests = user_profile.get("interests", [])
        past_categories = user_profile.get("past_categories", [])
        profile_key = ",".join(sorted(interests + past_categories))
        
        if profile_key in self.recommendation_knowledge and random.random() < self.success_rate:
            product, rationale = self.recommendation_knowledge[profile_key]
            return rationale, product
        else:
            if "electronics" in interests:
                if "gaming" in interests:
                    product = "Gaming Mouse" if random.random() < 0.7 else "High-res Monitor"
                    rationale = f"Based on electronics and gaming interest, suggest a peripheral."
                else:
                    product = "Wireless Headphones"
                    rationale = f"General electronics interest. Recommend a popular accessory."
            elif "books" in past_categories:
                if "sci-fi" in interests:
                    product = "Classic Sci-Fi Novel"
                    rationale = f"User enjoys books and sci-fi. Suggest a well-regarded classic."
                else:
                    product = "Mystery Thriller"
                    rationale = f"General book interest, diversifying recommendation."
            else:
                product = "Popular Item X"
                rationale = "No specific patterns, recommending a trending item."
            return rationale, product

    def fine_tune(self, user_profile, rationale, recommendation):
        interests = user_profile.get("interests", [])
        past_categories = user_profile.get("past_categories", [])
        profile_key = ",".join(sorted(interests + past_categories))
        if profile_key not in self.recommendation_knowledge:
            self.recommendation_knowledge[profile_key] = (recommendation, rationale)
            self.success_rate = min(1.0, self.success_rate + 0.07)

def get_ground_truth_successful_recommendation(user_profile):
    interests = user_profile.get("interests", [])
    past_categories = user_profile.get("past_categories", [])

    if "electronics" in interests and "gaming" in interests:
        return "Gaming Laptop"
    if "books" in past_categories and "fantasy" in interests:
        return "Epic Fantasy Series"
    if "clothing" in past_categories and "sports" in interests:
        return "Running Shoes"
    if "home decor" in past_categories:
        return "Smart Lighting Kit"
    return None

def simulate_ecommerce_star_pattern():
    llm = SimulatedLLMEcommerce()
    user_profiles = [
        {"id": 1, "interests": ["electronics", "gaming"], "past_categories": ["electronics"]},
        {"id": 2, "interests": ["fantasy"], "past_categories": ["books"]},
        {"id": 3, "interests": ["sports"], "past_categories": ["clothing"]},
        {"id": 4, "interests": ["cooking"], "past_categories": ["kitchenware"]},
        {"id": 5, "interests": ["travel"], "past_categories": ["books"]}
    ]
    
    for _ in range(4): 
        for user_data in user_profiles:
            ground_truth_rec = get_ground_truth_successful_recommendation(user_data)
            if ground_truth_rec is None:
                continue
            
            rationale, recommended_product = llm.generate_rationale_and_recommendation(user_data)
            
            if recommended_product == ground_truth_rec:
                llm.fine_tune(user_data, rationale, recommended_product)

simulate_ecommerce_star_pattern()