import random

class ProductRecommender:
    def __init__(self, categories):
        self.categories = categories
        self.user_preferences = {}

    def get_recommendations(self, user_id, num_recs=3):
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {cat: 0.5 for cat in self.categories}

        sorted_prefs = sorted(self.user_preferences[user_id].items(), key=lambda item: item[1], reverse=True)
        
        recommendations = []
        for i in range(num_recs):
            chosen_category = random.choices([item[0] for item in sorted_prefs], 
                                             weights=[item[1] for item in sorted_prefs], k=1)[0]
            recommendations.append(f"Product from {chosen_category} category")
        return recommendations

    def process_feedback(self, user_id, recommended_products, feedback):
        if user_id not in self.user_preferences:
            return

        for category in feedback.get('liked_categories', []):
            self.user_preferences[user_id][category] = min(1.0, self.user_preferences[user_id].get(category, 0.5) + 0.1)
        for category in feedback.get('disliked_categories', []):
            self.user_preferences[user_id][category] = max(0.0, self.user_preferences[user_id].get(category, 0.5) - 0.1)
        
        print(f"User {user_id} preferences updated: {self.user_preferences[user_id]}")

def simulate_user_interaction(user_id, recommendations):
    print(f"\n--- User {user_id} sees recommendations ---")
    for i, rec in enumerate(recommendations):
        print(f"{i+1}. {rec}")
    
    liked_categories = []
    disliked_categories = []
    
    possible_categories = list(set([rec.split(' from ')[1].split(' category')[0] for rec in recommendations]))
    if random.random() < 0.7:
        liked_category = random.choice(possible_categories)
        liked_categories.append(liked_category)
        print(f"User {user_id} liked a product from {liked_category}.")
    elif random.random() < 0.3:
        disliked_category = random.choice(possible_categories)
        disliked_categories.append(disliked_category)
        print(f"User {user_id} disliked a product from {disliked_category}.")

    return {'liked_categories': liked_categories, 'disliked_categories': disliked_categories}

all_product_categories = ["Electronics", "Books", "Apparel", "Home Goods", "Bags", "Sports"]
recommender = ProductRecommender(all_product_categories)

user_id = "user_A"
print("--- Starting E-commerce Recommendation Loop ---")

for i in range(5):
    print(f"\n--- Cycle {i+1} ---")
    current_recommendations = recommender.get_recommendations(user_id)
    print(f"Recommending to {user_id}: {current_recommendations}")
    
    feedback = simulate_user_interaction(user_id, current_recommendations)
    recommender.process_feedback(user_id, current_recommendations, feedback)
    
    print(f"Current preferences for {user_id}: {recommender.user_preferences.get(user_id)}")

print("\n--- E-commerce Recommendation Loop Finished ---")