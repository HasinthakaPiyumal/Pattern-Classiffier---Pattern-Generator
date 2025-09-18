import random

class UserPreferences:
    def __init__(self, user_id, browsing_history, purchase_history, demographics):
        self.user_id = user_id
        self.browsing_history = browsing_history
        self.purchase_history = purchase_history
        self.demographics = demographics

    def __repr__(self):
        return f"User(ID: {self.user_id}, Browsed: {', '.join(self.browsing_history)}, Purchased: {', '.join(self.purchase_history)})"

class ProductRecommendation:
    def __init__(self, user_id, recommended_products):
        self.user_id = user_id
        self.recommended_products = recommended_products

    def __repr__(self):
        return f"Recommendation(User: {self.user_id}, Products: {', '.join(self.recommended_products)})"

class RecommendationEngine:
    def __init__(self, available_products):
        self.available_products = available_products

    def generate_recommendations(self, user_preferences, num_recs=3):
        possible_recs = set()
        
        for category in user_preferences.browsing_history:
            for prod_id, details in self.available_products.items():
                if details["category"] == category:
                    possible_recs.add(prod_id)
        
        if len(possible_recs) < num_recs:
            popular_items = [p for p in self.available_products if self.available_products[p]["category"] == "Electronics"]
            possible_recs.update(random.sample(popular_items, min(num_recs - len(possible_recs), len(popular_items))))

        final_recs = list(possible_recs - set(user_preferences.purchase_history))
        random.shuffle(final_recs)
        return ProductRecommendation(user_preferences.user_id, final_recs[:num_recs])

class FairnessAndComplianceChecker:
    def __init__(self, available_products):
        self.available_products = available_products
        self.banned_keywords = ["explosive", "illegal", "harmful chemical"]
        self.high_risk_categories = ["Weapons", "Pharmaceuticals (prescription)"]
        self.diversity_threshold = 2

    def evaluate_recommendation(self, user_preferences, recommendation):
        issues = []
        recommended_categories = set()

        for product_id in recommendation.recommended_products:
            product_details = self.available_products.get(product_id)
            if not product_details:
                issues.append(f"Recommended product '{product_id}' not found in catalog.")
                continue

            for keyword in self.banned_keywords:
                if keyword in product_id.lower() or keyword in product_details.get("description", "").lower():
                    issues.append(f"Product '{product_id}' contains banned keyword '{keyword}'.")

            if product_details["category"] in self.high_risk_categories:
                issues.append(f"Product '{product_id}' is from a high-risk category: '{product_details['category']}'. Requires special approval.")

            if product_details.get("min_age") and user_preferences.demographics.get("age_group"):
                user_age_lower_bound = int(user_preferences.demographics["age_group"].split('-')[0])
                if user_age_lower_bound < product_details["min_age"]:
                    issues.append(f"Product '{product_id}' (min age {product_details['min_age']}) is not suitable for user (age group {user_preferences.demographics['age_group']}).")
            
            recommended_categories.add(product_details["category"])

        if len(recommendation.recommended_products) > 1 and len(recommended_categories) < self.diversity_threshold:
            issues.append(f"Recommendations lack diversity. Only {len(recommended_categories)} unique categories found for {len(recommendation.recommended_products)} products.")

        if user_preferences.demographics.get("age_group") == "18-25":
            all_cheap = all(self.available_products.get(pid, {}).get("price", 0) < 50 for pid in recommendation.recommended_products)
            if all_cheap and len(recommendation.recommended_products) > 0:
                issues.append(f"Potential bias: User in age group '{user_preferences.demographics['age_group']}' only recommended cheap items. Consider more diverse price points.")


        if issues:
            return False, issues
        else:
            return True, ["Recommendations appear compliant and fair."]

if __name__ == "__main__":
    all_products = {
        "Laptop_X1": {"category": "Electronics", "risk_level": "low", "price": 1200, "description": "High performance laptop"},
        "Smartphone_Y2": {"category": "Electronics", "risk_level": "low", "price": 800, "description": "Latest model smartphone"},
        "Book_SciFi_Z3": {"category": "Books", "risk_level": "low", "price": 25, "description": "Award-winning science fiction novel"},
        "Toy_Robot_A4": {"category": "Toys", "risk_level": "low", "price": 50, "min_age": 8, "description": "Interactive educational robot"},
        "Investment_Fund_B5": {"category": "Financial Services", "risk_level": "medium", "price": 0, "description": "High-yield investment fund"},
        "Pain_Reliever_C6": {"category": "Pharmaceuticals (OTC)", "risk_level": "low", "price": 15, "min_age": 12, "description": "Over-the-counter pain reliever"},
        "Hunting_Knife_D7": {"category": "Weapons", "risk_level": "high", "price": 75, "min_age": 18, "description": "Sharp hunting knife"},
        "Chemical_Cleaner_E8": {"category": "Home Goods", "risk_level": "medium", "description": "Industrial strength cleaner, handle with care"},
        "Kids_Puzzle_F9": {"category": "Toys", "risk_level": "low", "price": 20, "min_age": 3, "description": "Educational puzzle for toddlers"},
        "Smart_Watch_G0": {"category": "Electronics", "risk_level": "low", "price": 300, "description": "Fitness tracking smartwatch"},
        "Illegal_Item_H1": {"category": "Illegal Goods", "risk_level": "very high", "description": "Contains illegal substance"}
    }

    engine = RecommendationEngine(all_products)
    checker = FairnessAndComplianceChecker(all_products)

    user_scenarios = [
        UserPreferences("U001", ["Electronics", "Books"], ["Laptop_X1"], {"age_group": "30-45", "gender": "male"}),
        UserPreferences("U002", ["Toys"], ["Kids_Puzzle_F9"], {"age_group": "5-10", "gender": "female"}),
        UserPreferences("U003", ["Home Goods"], [], {"age_group": "18-25", "gender": "male"}),
        UserPreferences("U004", ["Weapons"], [], {"age_group": "25-35", "gender": "male"}),
        UserPreferences("U005", ["Electronics"], [], {"age_group": "16-20", "gender": "female"})
    ]

    print("--- Simulating E-commerce Recommendations and Review ---")
    for i, user in enumerate(user_scenarios):
        print(f"\n--- Scenario {i+1} ---")
        print(f"User Preferences: {user}")
        
        generated_recs = engine.generate_recommendations(user, num_recs=3)
        print(f"Generated: {generated_recs}")
        
        is_safe, findings = checker.evaluate_recommendation(user, generated_recs)
        
        if is_safe:
            print("  Review Status: Approved")
        else:
            print("  Review Status: Flagged for compliance/fairness issues")
        for finding in findings:
            print(f"    - {finding}")