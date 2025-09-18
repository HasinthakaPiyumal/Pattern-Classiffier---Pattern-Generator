import json

class EcommerceLLM:
    def __init__(self, product_catalog, tools):
        self.product_catalog = product_catalog
        self.tools = tools
        self.user_preferences = {"budget": None, "category_interest": [], "brand_affinity": []}
        self.purchase_history = []
        self.working_memory = {}
        self.episodic_memory = []

    def _retrieve_products(self, query, filters=None):
        matching_products = []
        query_lower = query.lower()
        for prod_id, details in self.product_catalog.items():
            if query_lower in details["name"].lower() or \
               query_lower in details["description"].lower() or \
               any(q_word in details["category"].lower() for q_word in query_lower.split()):
                if filters:
                    match = True
                    for key, value in filters.items():
                        if key == "max_price" and details["price"] > value:
                            match = False
                            break
                        if key == "min_rating" and details["rating"] < value:
                            match = False
                            break
                        if key == "category" and details["category"].lower() != value.lower():
                            match = False
                            break
                    if match:
                        matching_products.append(details)
                else:
                    matching_products.append(details)
        return matching_products

    def _generate_recommendation(self, products, user_context):
        if not products:
            return "I couldn't find any products matching your criteria."

        ranked_products = sorted(products, key=lambda p: (
            (user_context.get("category_interest") and p["category"] in user_context["category_interest"]) * 10
            + (user_context.get("brand_affinity") and p["brand"] in user_context["brand_affinity"]) * 5
            + p["rating"]
        ), reverse=True)

        recommendation_text = "Here are some recommendations for you:\n"
        for i, prod in enumerate(ranked_products[:3]):
            recommendation_text += (
                f"{i+1}. {prod['name']} ({prod['category']}) by {prod['brand']} - ${prod['price']:.2f}\n"
                f"   Description: {prod['description']}\n"
                f"   Rating: {prod['rating']}/5.0\n"
            )
        return recommendation_text

    def _parse_intent_and_extract_params(self, query):
        query_lower = query.lower()
        filters = {}
        if "max price" in query_lower:
            try:
                price = float(query_lower.split("max price ")[1].split(" ")[0].replace("$", ""))
                filters["max_price"] = price
            except (ValueError, IndexError): pass
        if "category" in query_lower:
            for cat in ["laptop", "smartphone", "headphone"]:
                if cat in query_lower:
                    filters["category"] = cat
                    break
        if "gaming" in query_lower or "work" in query_lower:
            filters["usage"] = "gaming" if "gaming" in query_lower else "work"
            
        if "recommend" in query_lower or "suggest" in query_lower:
            return "recommend_products", {"query": query_lower.replace("recommend", "").replace("suggest", "").strip(), "filters": filters}
        elif "details for" in query_lower or "about" in query_lower:
            return "get_product_details", {"product_name": query_lower.replace("details for", "").replace("about", "").strip()}
        elif "similar to this" in query_lower:
            return "multimodal_recommendation", {"image_description": query_lower.replace("similar to this", "").strip()}
        elif "feedback" in query_lower:
            return "process_feedback", {"feedback_text": query_lower}
        return "search_products", {"query": query_lower, "filters": filters}

    def _orchestrate_actions(self, intent, params):
        if intent == "recommend_products" or intent == "search_products":
            products = self._retrieve_products(params["query"], params["filters"])
            return self._generate_recommendation(products, self.user_preferences)
        elif intent == "get_product_details":
            details = self.tools.get_product_details(params["product_name"])
            return details if details else f"Could not find details for {params['product_name']}."
        elif intent == "multimodal_recommendation":
            simulated_query = f"products related to {params['image_description']}"
            products = self._retrieve_products(simulated_query)
            return self._generate_recommendation(products, self.user_preferences)
        elif intent == "process_feedback":
            return self._reflect_on_recommendation(params["feedback_text"])
        return "I'm sorry, I cannot fulfill that request at the moment."

    def _reflect_on_recommendation(self, feedback_text):
        feedback_lower = feedback_text.lower()
        if "liked" in feedback_lower or "good" in feedback_lower:
            if "category" in self.working_memory:
                category = self.working_memory["category"]
                if category not in self.user_preferences["category_interest"]:
                    self.user_preferences["category_interest"].append(category)
                    return f"Thanks for the feedback! I've noted your interest in {category} for future recommendations."
            return "Glad you liked it! I'll keep your preferences in mind."
        elif "didn't like" in feedback_lower or "expensive" in feedback_lower:
            if "expensive" in feedback_lower and self.working_memory.get("last_recommendation_price"):
                self.user_preferences["budget"] = self.working_memory["last_recommendation_price"] * 0.8
                return "Understood. I'll aim for more budget-friendly options next time."
            return "Apologies. I'll try to refine my recommendations based on your input."
        return "Thank you for your feedback."

    def process_query(self, user_query):
        intent, params = self._parse_intent_and_extract_params(user_query)
        self.working_memory["last_intent"] = intent
        self.working_memory["last_params"] = params

        if intent == "recommend_products" and "category" in params["filters"]:
            self.working_memory["category"] = params["filters"]["category"]

        self.episodic_memory.append({"query": user_query, "intent": intent, "params": params})

        response = self._orchestrate_actions(intent, params)

        if "recommendation" in intent and "price" in response:
            try:
                price_str = response.split(" - $")[1].split("\n")[0]
                self.working_memory["last_recommendation_price"] = float(price_str)
            except (ValueError, IndexError):
                self.working_memory["last_recommendation_price"] = None

        return response

class EcommerceTools:
    def __init__(self, product_catalog):
        self.product_catalog = product_catalog

    def get_product_details(self, product_name):
        product_name_lower = product_name.lower()
        for prod_id, details in self.product_catalog.items():
            if product_name_lower in details["name"].lower():
                return (f"Details for {details['name']} ({details['category']}):\n"
                        f"  Brand: {details['brand']}\n"
                        f"  Price: ${details['price']:.2f}\n"
                        f"  Rating: {details['rating']}/5.0\n"
                        f"  Description: {details['description']}")
        return None

if __name__ == "__main__":
    product_catalog = {
        "P001": {"name": "Gaming Laptop Pro", "category": "Laptop", "brand": "TechPro", "price": 1800.00, "rating": 4.8, "description": "High-performance gaming laptop with RTX 3080."},
        "P002": {"name": "Ultra Slim Laptop", "category": "Laptop", "brand": "SlimTech", "price": 1200.00, "rating": 4.5, "description": "Lightweight laptop for work and travel."},
        "P003": {"name": "Ergonomic Headphones", "category": "Headphone", "brand": "AudioMax", "price": 150.00, "rating": 4.2, "description": "Comfortable over-ear headphones with noise cancellation."},
        "P004": {"name": "Wireless Earbuds", "category": "Headphone", "brand": "SoundFlow", "price": 80.00, "rating": 4.0, "description": "Compact earbuds for on-the-go audio."},
        "P005": {"name": "Flagship Smartphone X", "category": "Smartphone", "brand": "GlobalMobile", "price": 999.00, "rating": 4.7, "description": "Latest smartphone with advanced camera and long battery life."}
    }

    ecommerce_tools = EcommerceTools(product_catalog)

    ecommerce_agent = EcommerceLLM(product_catalog, ecommerce_tools)

    print("--- E-commerce Recommender Simulation ---")

    user_query = "Recommend a laptop for gaming."
    print(f"\nUser: {user_query}")
    response = ecommerce_agent.process_query(user_query)
    print(f"Agent: {response}")
    print(f"User Preferences (after): {ecommerce_agent.user_preferences}")

    user_query = "Can you recommend a laptop with a max price of $1500?"
    print(f"\nUser: {user_query}")
    response = ecommerce_agent.process_query(user_query)
    print(f"Agent: {response}")

    user_query = "Show me headphones similar to this description: sleek, over-ear, noise cancelling."
    print(f"\nUser: {user_query}")
    response = ecommerce_agent.process_query(user_query)
    print(f"Agent: {response}")

    user_query = "I liked the Gaming Laptop Pro recommendation."
    print(f"\nUser: {user_query}")
    response = ecommerce_agent.process_query(user_query)
    print(f"Agent: {response}")
    print(f"User Preferences (after feedback): {ecommerce_agent.user_preferences}")

    user_query = "The Gaming Laptop Pro was too expensive."
    print(f"\nUser: {user_query}")
    response = ecommerce_agent.process_query(user_query)
    print(f"Agent: {response}")
    print(f"User Preferences (after negative feedback): {ecommerce_agent.user_preferences}")

    print("\n--- Agent Memory Snapshot ---")
    print(f"Working Memory: {ecommerce_agent.working_memory}")
    print(f"Episodic Memory (last 2): {ecommerce_agent.episodic_memory[-2:]}")