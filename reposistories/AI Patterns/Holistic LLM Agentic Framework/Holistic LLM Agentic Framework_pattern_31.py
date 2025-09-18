import json
import time

class SimulatedLLM:
    def __init__(self):
        self.product_catalog = {
            "P101": {"name": "Wireless Earbuds", "category": "Electronics", "price": 99.99, "stock": 150, "features": ["Bluetooth 5.0", "Noise Cancellation"], "reviews": ["Great sound!", "Comfortable fit."]},
            "P102": {"name": "Smartwatch Pro", "category": "Electronics", "price": 199.99, "stock": 75, "features": ["Heart Rate Monitor", "GPS"], "reviews": ["Long battery life.", "Stylish design."]},
            "P201": {"name": "Organic Coffee Beans", "category": "Groceries", "price": 12.50, "stock": 300, "features": ["Fair Trade", "Medium Roast"], "reviews": ["Rich flavor.", "Freshly roasted."]},
            "P301": {"name": "Ergonomic Office Chair", "category": "Furniture", "price": 249.00, "stock": 30, "features": ["Adjustable Lumbar", "Mesh Back"], "reviews": ["Very comfortable for long hours."]}
        }
        self.user_preferences = {
            "user_A": {"category_interest": ["Electronics"], "price_range": "medium", "past_purchases": ["P101"]},
            "user_B": {"category_interest": ["Groceries", "Home Goods"], "price_range": "low", "past_purchases": ["P201"]}
        }
        self.order_history = {
            "ORD5001": {"user_id": "user_A", "items": [{"id": "P101", "qty": 1}], "status": "shipped", "tracking": "ABC123XYZ"},
            "ORD5002": {"user_id": "user_B", "items": [{"id": "P201", "qty": 2}], "status": "processing"}
        }

    def generate_response(self, prompt, context=None):
        if "product details" in prompt.lower() and context and "product_id" in context:
            product_id = context["product_id"]
            if product_id in self.product_catalog:
                details = self.product_catalog[product_id]
                return f"Details for {details['name']} ({product_id}): Category: {details['category']}, Price: ${details['price']:.2f}, Features: {', '.join(details['features'])}. Reviews: '{details['reviews'][0]}'. Stock: {details['stock']} available."
            return f"Product {product_id} not found."
        
        if "recommend" in prompt.lower() and context and "user_id" in context:
            user_id = context["user_id"]
            prefs = self.user_preferences.get(user_id, {})
            recommendations = []
            for pid, details in self.product_catalog.items():
                if details["category"] in prefs.get("category_interest", []) and pid not in prefs.get("past_purchases", []):
                    recommendations.append(details["name"])
            
            if recommendations:
                return f"Based on your preferences, {user_id}, you might like: {', '.join(recommendations[:2])}."
            return "I couldn't find personalized recommendations at the moment. Try browsing our categories."

        if "order status" in prompt.lower() and context and "order_id" in context:
            order_id = context["order_id"]
            if order_id in self.order_history:
                order = self.order_history[order_id]
                return f"Order {order_id} (for {order['user_id']}) is currently '{order['status']}'. Tracking: {order.get('tracking', 'N/A')}."
            return f"Order {order_id} not found."

        return "I'm an e-commerce assistant. How can I help you today? (e.g., product details, recommendations, order status)"

class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = [] # Store past conversations/sessions
        self.semantic_memory = {
            "product_categories": ["Electronics", "Groceries", "Furniture", "Apparel"],
            "common_queries": ["shipping", "returns", "payment"]
        }
        self.procedural_memory = {
            "recommendation_flow": ["Identify user", "Fetch preferences", "Filter catalog", "Present products"],
            "order_inquiry_flow": ["Get order ID", "Look up status", "Provide tracking"]
        }

    def store_working_memory(self, key, value):
        self.working_memory[key] = value

    def retrieve_working_memory(self, key):
        return self.working_memory.get(key)

    def add_episodic_memory(self, interaction):
        self.episodic_memory.append((time.time(), interaction))

    def get_semantic_info(self, query):
        for category in self.semantic_memory["product_categories"]:
            if query.lower() in category.lower():
                return f"'{category}' is a valid product category."
        return None
    
    def get_procedural_info(self, skill_name):
        return self.procedural_memory.get(skill_name)

class ToolKit:
    def get_product_details(self, product_id):
        # Simulate a product database lookup
        time.sleep(0.1)
        if product_id in SimulatedLLM().product_catalog:
            return {"success": True, "data": SimulatedLLM().product_catalog[product_id], "id": product_id}
        return {"success": False, "error": "Product not found"}

    def get_user_preferences(self, user_id):
        # Simulate fetching user profile from a database
        time.sleep(0.05)
        if user_id in SimulatedLLM().user_preferences:
            return {"success": True, "data": SimulatedLLM().user_preferences[user_id]}
        return {"success": False, "error": "User preferences not found"}

    def check_order_status(self, order_id):
        # Simulate an order management system API call
        time.sleep(0.15)
        if order_id in SimulatedLLM().order_history:
            return {"success": True, "data": SimulatedLLM().order_history[order_id]}
        return {"success": False, "error": "Order not found"}

    def recommend_similar_products(self, product_id, user_id="guest"):
        # Simulate a recommendation engine based on product features/user history
        time.sleep(0.2)
        if product_id == "P101": # Wireless Earbuds
            return {"success": True, "recommendations": [{"id": "P102", "name": "Smartwatch Pro"}], "reason": "Customers who bought earbuds also liked smartwatches."}
        return {"success": True, "recommendations": [], "reason": "No specific similar products found."}

class ECommerceAgent:
    def __init__(self):
        self.llm = SimulatedLLM()
        self.memory = MemorySystem()
        self.toolkit = ToolKit()
        self.current_plan = []
        self.current_user_id = "guest" # Default user, can be set dynamically

    def _orchestrate_tools(self, tool_name, *args, **kwargs):
        tool_func = getattr(self.toolkit, tool_name, None)
        if tool_func:
            try:
                result = tool_func(*args, **kwargs)
                if not result.get("success"): 
                    self.memory.add_episodic_memory(f"Tool {tool_name} failed: {result.get('error')}")
                return result
            except Exception as e:
                self.memory.add_episodic_memory(f"Error executing tool {tool_name}: {e}")
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Tool not found"}

    def _parse_product_id(self, query):
        product_id = next((word for word in query.split() if word.startswith("P")), None)
        return product_id

    def _parse_order_id(self, query):
        order_id = next((word for word in query.split() if word.startswith("ORD")), None)
        return order_id

    def _plan_and_execute(self, user_query):
        response = ""
        product_id = self._parse_product_id(user_query)
        order_id = self._parse_order_id(user_query)

        if product_id and ("details" in user_query.lower() or "info" in user_query.lower()):
            self.current_plan = ["get_product_details"]
            self.memory.store_working_memory("current_product_id", product_id)
        elif "recommend" in user_query.lower():
            self.current_plan = ["get_user_preferences", "generate_recommendations"]
            self.memory.store_working_memory("current_user_id", self.current_user_id)
        elif order_id and "status" in user_query.lower():
            self.current_plan = ["check_order_status"]
            self.memory.store_working_memory("current_order_id", order_id)
        else:
            self.current_plan = ["direct_llm_response"]

        for step in self.current_plan:
            if step == "get_product_details":
                pid = self.memory.retrieve_working_memory("current_product_id")
                tool_output = self._orchestrate_tools("get_product_details", pid)
                if tool_output["success"]:
                    self.memory.store_working_memory("last_product_data", tool_output["data"])
                    llm_context = {"product_id": pid, "product_data": tool_output["data"]}
                    response = self.llm.generate_response(f"Details for {pid}", context=llm_context)
                else:
                    response = tool_output["error"]

            elif step == "get_user_preferences":
                uid = self.memory.retrieve_working_memory("current_user_id")
                tool_output = self._orchestrate_tools("get_user_preferences", uid)
                if tool_output["success"]:
                    self.memory.store_working_memory("user_preferences_data", tool_output["data"])
                else:
                    self.memory.store_working_memory("user_preferences_data", {})

            elif step == "generate_recommendations":
                uid = self.memory.retrieve_working_memory("current_user_id")
                llm_context = {"user_id": uid, "user_preferences": self.memory.retrieve_working_memory("user_preferences_data")}
                response = self.llm.generate_response(f"Recommend products for {uid}", context=llm_context)
                
                # Example of multi-strategy planning / further recommendation
                if "Wireless Earbuds" in response and self.memory.retrieve_working_memory("last_product_data") and self.memory.retrieve_working_memory("last_product_data")["id"] == "P101":
                    similar_recs = self._orchestrate_tools("recommend_similar_products", "P101", uid)
                    if similar_recs["success"] and similar_recs["recommendations"]:
                        response += f" Also, you might like {similar_recs['recommendations'][0]['name']} based on your interest in {self.memory.retrieve_working_memory('last_product_data')['name']}."

            elif step == "check_order_status":
                oid = self.memory.retrieve_working_memory("current_order_id")
                tool_output = self._orchestrate_tools("check_order_status", oid)
                if tool_output["success"]:
                    llm_context = {"order_id": oid, "order_data": tool_output["data"]}
                    response = self.llm.generate_response(f"Status of order {oid}", context=llm_context)
                else:
                    response = tool_output["error"]

            elif step == "direct_llm_response":
                response = self.llm.generate_response(user_query)

        return response

    def process_query(self, user_query, user_id="guest"):
        self.current_user_id = user_id # Set current user for personalized interaction
        self.memory.add_episodic_memory(f"User '{user_id}' Query: {user_query}")
        print(f"\nUser ({user_id}): {user_query}")

        response = self._plan_and_execute(user_query)

        self.memory.add_episodic_memory(f"Agent Response to '{user_id}': {response}")
        return response

# Real-world Usage Simulation: E-commerce Product Recommender & Support
ecommerce_agent = ECommerceAgent()

print(ecommerce_agent.process_query("Tell me about product P101.", user_id="user_A"))
print(ecommerce_agent.process_query("What can you recommend for me?", user_id="user_A"))
print(ecommerce_agent.process_query("What is the status of my order ORD5001?", user_id="user_A"))

# Simulation Pattern: New user, asking about a product not explicitly in their preferences but related
print(ecommerce_agent.process_query("Tell me about product P201.", user_id="user_A"))
print(ecommerce_agent.process_query("I need help.", user_id="guest"))
