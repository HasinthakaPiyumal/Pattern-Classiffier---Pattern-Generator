import random
import time

class LLMCore:
    def __init__(self, name="ShopAdvisorLLM"):
        self.name = name

    def reason(self, prompt, context, memory, tools_available):
        if "recommend" in prompt.lower() or "suggest" in prompt.lower():
            if "shoes" in prompt.lower():
                intent = "product_recommendation_shoes"
            elif "electronics" in prompt.lower():
                intent = "product_recommendation_electronics"
            else:
                intent = "product_recommendation_general"
            
            plan = f"PLAN: Retrieve user preferences, then search product catalog for '{prompt}' using SearchTool, then personalize recommendations, then generate response."
            return {"intent": intent, "plan": plan}
        elif "compare" in prompt.lower():
            intent = "product_comparison"
            plan = f"PLAN: Use SearchTool to find products, then compare features, then generate response."
            return {"intent": intent, "plan": plan}
        else:
            return {"intent": "general_query", "plan": "PLAN: Direct generation based on context."}

    def generate_response(self, plan_output, tool_output, memory_info, contextual_info):
        response = f"Hello! Based on your request and my analysis:\n"
        if "recommend" in plan_output.get("plan", ""):
            if tool_output and "recommendations" in tool_output:
                response += f"Here are some personalized recommendations for you:\n"
                for rec in tool_output["recommendations"]:
                    response += f"- {rec['name']} (${rec['price']}) - {rec['description']}\n"
            else:
                response += f"I couldn't find specific recommendations at this moment. {contextual_info}\n"
        elif "compare" in plan_output.get("plan", ""):
            response += f"Here's a comparison based on the available data: {tool_output}\n"
        else:
            response += f"I'm here to help with shopping advice. {contextual_info}\n"

        if memory_info:
            response += f"\n(Considering your past interactions: {memory_info})"
        return response

class ProductCatalog:
    def __init__(self):
        self.products = [
            {"id": "P001", "category": "electronics", "name": "Smartwatch X", "price": 299.99, "features": ["GPS", "Heart Rate", "Waterproof"], "description": "Advanced smartwatch with health tracking."},
            {"id": "P002", "category": "shoes", "name": "Running Shoes Alpha", "price": 120.00, "features": ["Lightweight", "Cushioned", "Breathable"], "description": "Comfortable running shoes for daily use."},
            {"id": "P003", "category": "electronics", "name": "Noise-Cancelling Headphones", "price": 199.99, "features": ["ANC", "Bluetooth 5.0", "Long Battery"], "description": "Immersive audio experience."},
            {"id": "P004", "category": "shoes", "name": "Hiking Boots Pro", "price": 180.00, "features": ["Waterproof", "Ankle Support", "Durable"], "description": "Rugged boots for outdoor adventures."},
            {"id": "P005", "category": "books", "name": "The AI Revolution", "price": 25.00, "features": ["Bestseller", "Non-fiction"], "description": "Explore the future of artificial intelligence."},
            {"id": "P006", "category": "electronics", "name": "Portable Charger", "price": 45.00, "features": ["10000mAh", "Fast Charge"], "description": "Keep your devices powered on the go."},
        ]

    def search_products(self, query, category=None):
        results = []
        query_lower = query.lower()
        for p in self.products:
            if category and p["category"] != category:
                continue
            if query_lower in p["name"].lower() or query_lower in p["description"].lower() or query_lower in p["category"].lower():
                results.append(p)
        return results

    def get_product_details(self, product_id):
        for p in self.products:
            if p["id"] == product_id:
                return p
        return None

class UserBehaviorMemory:
    def __init__(self, user_id):
        self.user_id = user_id
        self.browsing_history = []
        self.purchase_history = []
        self.preferences = {"category_affinity": {}, "price_range": None, "brands": []}

    def add_browsing_event(self, product_id):
        self.browsing_history.append({"product_id": product_id, "timestamp": time.time()})
        self._update_preferences(product_id)

    def add_purchase_event(self, product_id, price):
        self.purchase_history.append({"product_id": product_id, "price": price, "timestamp": time.time()})
        self._update_preferences(product_id)

    def _update_preferences(self, product_id):
        product = ProductCatalog().get_product_details(product_id)
        if product:
            category = product["category"]
            self.preferences["category_affinity"][category] = self.preferences["category_affinity"].get(category, 0) + 1

    def get_user_context(self):
        most_liked_category = max(self.preferences["category_affinity"], key=self.preferences["category_affinity"].get) if self.preferences["category_affinity"] else "general"
        return f"User {self.user_id} has browsed {len(self.browsing_history)} items, purchased {len(self.purchase_history)}. Appears to like {most_liked_category} products."

class SearchTool:
    def __init__(self, catalog):
        self.catalog = catalog

    def search(self, query, category=None):
        print(f"  [Tool] Searching catalog for '{query}' in category '{category or 'any'}'...")
        time.sleep(0.1)
        return self.catalog.search_products(query, category)

class PersonalizationTool:
    def __init__(self, user_memory):
        self.user_memory = user_memory

    def personalize(self, products):
        print(f"  [Tool] Personalizing {len(products)} products for user {self.user_memory.user_id}...")
        time.sleep(0.1)
        user_category_affinity = self.user_memory.preferences["category_affinity"]
        if not user_category_affinity:
            return products

        sorted_products = sorted(products, key=lambda p: user_category_affinity.get(p["category"], 0), reverse=True)
        return sorted_products

class ECommerceAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.llm_core = LLMCore()
        self.product_catalog = ProductCatalog()
        self.user_memory = UserBehaviorMemory(user_id)
        self.search_tool = SearchTool(self.product_catalog)
        self.personalization_tool = PersonalizationTool(self.user_memory)
        self.available_tools = {
            "search_products": self.search_tool.search,
            "personalize_recommendations": self.personalization_tool.personalize
        }
        print(f"ECommerceAgent initialized for User ID: {user_id}")

    def process_request(self, query):
        print(f"\n[Agent] Processing request: '{query}'")
        self.user_memory.update_working_memory("last_query", query)
        user_context = self.user_memory.get_user_context()
        llm_decision = self.llm_core.reason(query, user_context, self.user_memory, self.available_tools)
        print(f"[Agent] LLM Decision: Intent='{llm_decision['intent']}', Plan='{llm_decision['plan']}'")

        tool_output = {}
        contextual_info = "No specific product information yet."

        if llm_decision["intent"].startswith("product_recommendation"):
            category = llm_decision["intent"].replace("product_recommendation_", "") if "product_recommendation_" in llm_decision["intent"] else None
            
            search_query = query.replace("recommend", "").replace("suggest", "").strip()
            if "shoes" in query.lower(): category = "shoes"
            if "electronics" in query.lower(): category = "electronics"
            
            found_products = self.available_tools["search_products"](search_query, category)
            contextual_info = f"Found {len(found_products)} products matching '{search_query}'."

            personalized_products = self.available_tools["personalize_recommendations"](found_products)
            tool_output["recommendations"] = personalized_products[:3]

        elif llm_decision["intent"] == "product_comparison":
            search_query = query.replace("compare", "").strip()
            products_to_compare = self.available_tools["search_products"](search_query)
            if len(products_to_compare) > 1:
                tool_output["comparison"] = [f"{p['name']} (${p['price']}) with features {p['features']}" for p in products_to_compare]
                contextual_info = f"Compared {len(products_to_compare)} products."
            else:
                contextual_info = "Need at least two products to compare."

        if tool_output.get("recommendations"):
            selected_rec_id = tool_output["recommendations"][0]["id"]
            self.user_memory.add_browsing_event(selected_rec_id)
            print(f"  [Agent] (Simulating user interaction: browsed {selected_rec_id})")

        response = self.llm_core.generate_response(llm_decision, tool_output, self.user_memory.get_user_context(), contextual_info)
        return response

print("--- E-commerce Agent: Personalized Product Recommender ---")
user_agent = ECommerceAgent(user_id="U789")

print(user_agent.process_request("Can you recommend some running shoes for me?"))
time.sleep(0.5)

print(user_agent.process_request("What about some good hiking boots?"))
time.sleep(0.5)

user_agent.user_memory.add_purchase_event("P002", 120.00)
print("\n[Agent] (Simulating user purchase of Running Shoes Alpha)")
time.sleep(0.5)

print(user_agent.process_request("I'm looking for a new smartwatch."))
time.sleep(0.5)

print(user_agent.process_request("Tell me about your services."))