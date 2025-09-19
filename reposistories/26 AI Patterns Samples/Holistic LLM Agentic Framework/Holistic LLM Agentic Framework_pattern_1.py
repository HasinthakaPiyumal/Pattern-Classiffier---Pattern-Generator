import random
import time

class LLM:
    def process_request(self, prompt, context=None):
        if "recommendation" in prompt.lower():
            return f"Based on your preferences and recent activity, I recommend looking into some new products. Specifically, I'm thinking of something related to {context.get('last_category', 'electronics')}."
        if "explain" in prompt.lower():
            return "This product is popular due to its high ratings and advanced features."
        if "summarize" in prompt.lower():
            return "Summary of product reviews: Mostly positive, highlighting ease of use and durability."
        if "intent" in prompt.lower() and "clarify" in prompt.lower():
            return "Please tell me what kind of products you are interested in or what problem you're trying to solve."
        return "I am an e-commerce assistant. How can I help you find what you're looking for?"

class MemorySystem:
    def __init__(self):
        self.user_session_memory = {}
        self.episodic_memory = [] # Past recommendations/interactions
        self.product_catalog = {
            "laptop_x": {"category": "electronics", "price": 1200, "rating": 4.5, "stock": 10, "features": "fast, light"},
            "smartphone_y": {"category": "electronics", "price": 800, "rating": 4.2, "stock": 25, "features": "camera, durable"},
            "coffee_maker_z": {"category": "home_appliances", "price": 150, "rating": 4.7, "stock": 50, "features": "automatic, sleek"},
            "book_a": {"category": "books", "price": 25, "rating": 4.8, "stock": 100, "features": "best-seller, fiction"},
            "tshirt_b": {"category": "apparel", "price": 30, "rating": 4.0, "stock": 200, "features": "cotton, unisex"}
        }
        self.customer_behavior_rules = {
            "electronics_affinity": lambda user_history: "electronics" if "laptop" in user_history or "smartphone" in user_history else None,
            "price_sensitive": lambda user_history: True if "budget" in user_history else False
        }

    def retrieve_product_data(self, product_id):
        return self.product_catalog.get(product_id)

    def find_products_by_category(self, category):
        return {pid: data for pid, data in self.product_catalog.items() if data.get("category") == category}

    def update_session(self, key, value):
        self.user_session_memory[key] = value

    def add_episodic_event(self, event):
        self.episodic_memory.append(event)

class ToolManager:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.tools = {
            "recommendation_engine": self._recommendation_engine_tool,
            "inventory_checker": self._inventory_checker_tool,
            "review_aggregator": self._review_aggregator_tool
        }

    def _recommendation_engine_tool(self, user_preferences, category=None, max_price=None):
        print(f"  [Tool: RecommendationEngine] User preferences: {user_preferences}, Category: {category or 'Any'}")
        candidates = []
        if category:
            candidates.extend(self.memory.find_products_by_category(category).keys())
        else:
            candidates.extend(self.memory.product_catalog.keys())

        # Simulate filtering based on preferences and price
        filtered_recs = []
        for pid in candidates:
            product = self.memory.retrieve_product_data(pid)
            if product:
                if max_price is None or product["price"] <= max_price:
                    if "high_rating" in user_preferences and product["rating"] < 4.5:
                        continue
                    if "budget" in user_preferences and product["price"] > 500:
                        continue
                    filtered_recs.append(pid)
        random.shuffle(filtered_recs)
        return filtered_recs[:3] # Return top 3 simulated recommendations

    def _inventory_checker_tool(self, product_id):
        product = self.memory.retrieve_product_data(product_id)
        if product:
            return f"Product {product_id} has {product['stock']} units in stock."
        return f"Product {product_id} not found."

    def _review_aggregator_tool(self, product_id):
        reviews = {
            "laptop_x": "Excellent performance, good value.",
            "smartphone_y": "Great camera, but battery life could be better.",
            "coffee_maker_z": "Makes perfect coffee every time, easy to clean."
        }
        return reviews.get(product_id, "No reviews available.")

    def execute_tool(self, tool_name, *args, **kwargs):
        tool = self.tools.get(tool_name)
        if tool:
            try:
                return tool(*args, **kwargs)
            except Exception as e:
                return f"Error executing tool {tool_name}: {e}"
        return f"Tool '{tool_name}' not found."

class RecommendationAgent:
    def __init__(self):
        self.memory = MemorySystem()
        self.llm = LLM()
        self.tool_manager = ToolManager(self.memory)

    def _plan_recommendation(self, user_query, current_session):
        intent = current_session.get("intent", "recommendation")
        user_prefs = current_session.get("preferences", [])
        category = current_session.get("category", None)
        max_price = current_session.get("max_price", None)

        if "check stock" in user_query.lower():
            product_id = current_session.get("product_to_check", "laptop_x")
            return {"action": "tool_use", "tool": "inventory_checker", "params": {"product_id": product_id}}
        elif "reviews for" in user_query.lower():
            product_id = current_session.get("product_to_check", "laptop_x")
            return {"action": "tool_use", "tool": "review_aggregator", "params": {"product_id": product_id}}
        elif "recommend" in intent or "looking for" in user_query.lower():
            # Apply procedural memory rules for initial category hint
            for rule_name, rule_func in self.memory.customer_behavior_rules.items():
                if rule_func(current_session.get("history", [])) and not category:
                    if rule_name == "electronics_affinity":
                        category = "electronics"
                        print("  [Procedural Memory] Detected electronics affinity.")

            return {"action": "tool_use", "tool": "recommendation_engine", "params": {"user_preferences": user_prefs, "category": category, "max_price": max_price}}
        else:
            return {"action": "llm_direct_gen", "response": self.llm.process_request(user_query, current_session)}

    def process_user_request(self, user_query):
        print(f"\nUser: {user_query}")
        current_session = self.memory.user_session_memory.copy()
        current_session["query"] = user_query

        # 1. LLM as Central Intelligence & Orchestrator (Intent Understanding)
        llm_intent_clarification = self.llm.process_request(f"Clarify user intent for: {user_query}", current_session)
        # Simplified intent extraction for simulation
        intent = "recommendation"
        if "stock" in user_query.lower():
            intent = "check stock"
            current_session["product_to_check"] = user_query.lower().replace("check stock for ", "").strip().replace(" ", "_")
        elif "reviews" in user_query.lower():
            intent = "reviews for"
            current_session["product_to_check"] = user_query.lower().replace("reviews for ", "").strip().replace(" ", "_")
        elif "laptop" in user_query.lower() or "smartphone" in user_query.lower():
            current_session["category"] = "electronics"
            current_session["preferences"] = current_session.get("preferences", []) + ["high_rating"]
        elif "budget" in user_query.lower():
            current_session["preferences"] = current_session.get("preferences", []) + ["budget"]
            current_session["max_price"] = 500
        self.memory.update_session("intent", intent)
        self.memory.update_session("last_query", user_query)
        self.memory.update_session("preferences", current_session.get("preferences", []))
        self.memory.update_session("category", current_session.get("category", None))
        self.memory.update_session("max_price", current_session.get("max_price", None))
        self.memory.update_session("history", self.memory.user_session_memory.get("history", []) + [user_query])

        # 4. Adaptive Planning & Decision-Making
        plan = self._plan_recommendation(user_query, self.memory.user_session_memory)
        print(f"Agent Plan: {plan['action']} (intent: {intent})")

        response_parts = []
        if plan["action"] == "tool_use":
            tool_output = self.tool_manager.execute_tool(plan["tool"], **plan["params"])
            print(f"  Tool Output ({plan['tool']}): {tool_output}")

            # 8. Output Generation & Integration
            if plan["tool"] == "recommendation_engine":
                product_details = []
                for pid in tool_output:
                    product = self.memory.retrieve_product_data(pid)
                    if product: product_details.append(f"{pid.replace('_', ' ').title()} (Price: ${product['price']}, Rating: {product['rating']})")
                response_parts.append(f"Here are some recommendations for you: {', '.join(product_details)}.")
                self.memory.add_episodic_event(f"Recommended: {tool_output}")
            else:
                response_parts.append(tool_output)

            # 7. Verification, Grounding & Explainability (simple check for empty recommendations)
            if plan["tool"] == "recommendation_engine" and not tool_output:
                print("  [Verification] No recommendations found. Attempting re-planning...")
                response_parts.append("I couldn't find specific recommendations matching your criteria. Let me broaden the search.")
                # Re-plan with broader criteria (simplified)
                re_plan = self._plan_recommendation(user_query, {**self.memory.user_session_memory, "category": None, "max_price": None})
                if re_plan["action"] == "tool_use":
                    re_tool_output = self.tool_manager.execute_tool(re_plan["tool"], **re_plan["params"])
                    product_details = []
                    for pid in re_tool_output:
                        product = self.memory.retrieve_product_data(pid)
                        if product: product_details.append(f"{pid.replace('_', ' ').title()} (Price: ${product['price']}, Rating: {product['rating']})")
                    response_parts.append(f"Broader recommendations: {', '.join(product_details)}.")

        elif plan["action"] == "llm_direct_gen":
            response_parts.append(plan["response"])

        # 2. Dynamic Knowledge & Memory System (RAG for product details)
        if "recommendation" in intent and response_parts:
            first_rec = next(iter(plan["params"]["user_preferences"]), None) # Just an example
            if first_rec and self.memory.retrieve_product_data(first_rec):
                 response_parts.append(f" (RAG info: Details for {first_rec} retrieved from catalog.)")
            # 2. Dynamic Knowledge & Memory System (RAG for product details)
            if "recommendation" in intent and response_parts:
                # Attempt to extract product IDs from the current response to enrich with RAG
                potential_product_ids = [pid for pid in self.memory.product_catalog.keys() if pid.replace('_', ' ').lower() in ' '.join(response_parts).lower()]
                for pid in potential_product_ids:
                    product_info = self.memory.retrieve_product_data(pid)
                    if product_info:
                        response_parts.append(f"  [RAG] More about {pid.replace('_', ' ').title()}: Price ${product_info['price']}, Rating {product_info['rating']}.")
                        break # Just add info for one product for simplicity

        final_response = " ".join(response_parts)
        print(f"Agent: {final_response}")
        return final_response

# Simulation usage: E-commerce Recommendation Agent
if __name__ == "__main__":
    agent = RecommendationAgent()
    print("Holistic LLM E-commerce Agent Activated. How can I help you find products?")

    agent.process_user_request("I'm looking for a new laptop, something with a high rating.")
    agent.process_user_request("What about a smartphone, but I'm on a budget?")
    agent.process_user_request("Check stock for laptop_x.")
    agent.process_user_request("Tell me reviews for coffee_maker_z.")
    agent.process_user_request("Just recommend something for my home.")
    agent.process_user_request("I want something cheap.")
