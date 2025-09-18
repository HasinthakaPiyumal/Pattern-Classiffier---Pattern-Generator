import json
import time

class MockLLM:
    def __init__(self):
        self.product_catalog = {
            "laptop_pro": {"name": "Laptop Pro X1", "price": 1500, "category": "electronics", "stock": 10, "description": "High-performance laptop for professionals.", "reviews": ["Fast", "Great screen"]},
            "smart_watch_lite": {"name": "Smart Watch Lite", "price": 200, "category": "wearables", "stock": 50, "description": "Lightweight smartwatch with fitness tracking.", "reviews": ["Comfortable", "Good battery"]},
            "wireless_earbuds": {"name": "Wireless Earbuds Z", "price": 120, "category": "audio", "stock": 25, "description": "Premium sound quality, noise-cancelling.", "reviews": ["Amazing sound", "Snug fit"]},
            "ergonomic_chair": {"name": "Ergonomic Office Chair", "price": 400, "category": "furniture", "stock": 5, "description": "Comfortable and supportive for long work hours.", "reviews": ["Worth the price", "Easy assembly"]}
        }
        self.tool_descriptions = {
            "search_product_catalog": "Searches the product catalog for items matching keywords or criteria.",
            "check_order_status": "Retrieves the current status of a customer's order by ID.",
            "process_return": "Initiates a return for a product with a given order and item ID.",
            "generate_personalized_ad": "Generates a personalized product advertisement based on user preferences."
        }

    def infer(self, prompt, context=None, persona="shopping_assistant"):
        if "recommend a product" in prompt.lower() or "looking for" in prompt.lower():
            keywords = []
            if "laptop" in prompt.lower(): keywords.append("laptop")
            if "watch" in prompt.lower(): keywords.append("smart watch")
            if "earbuds" in prompt.lower() or "headphones" in prompt.lower(): keywords.append("earbuds")
            if "chair" in prompt.lower(): keywords.append("chair")
            if "budget" in prompt.lower():
                try:
                    budget = int(prompt.split("budget of", 1)[1].split(" ")[0].replace("$", ""))
                    keywords.append(f"max_price:{budget}")
                except:
                    pass
            
            if keywords:
                return {"action": "tool_use", "tool": "search_product_catalog", "params": {"keywords": keywords}, "thought": "User is asking for product recommendations, using search tool."}
            else:
                return {"action": "generate", "response": "I can recommend products if you tell me what you're looking for!", "thought": "Insufficient keywords for product search."}

        if "order status for" in prompt.lower():
            order_id = prompt.split("order status for", 1)[1].strip().replace("?", "")
            return {"action": "tool_use", "tool": "check_order_status", "params": {"order_id": order_id}, "thought": "User wants to check order status, using order tool."}
        
        if "return item from order" in prompt.lower():
            parts = prompt.split("return item from order", 1)[1].strip().split("item")
            order_id = parts[0].strip()
            item_id = parts[1].strip()
            return {"action": "tool_use", "tool": "process_return", "params": {"order_id": order_id, "item_id": item_id}, "thought": "User wants to return an item, using return tool."}

        if "show me personalized ads" in prompt.lower():
            return {"action": "tool_use", "tool": "generate_personalized_ad", "params": {"user_preferences": context.get("user_preferences", [])}, "thought": "User wants personalized ads, generating based on preferences."}

        return {"action": "generate", "response": "Welcome to our store! How can I help you with your shopping today?", "thought": "Initial greeting or fallback."}

class ECommerceAgent:
    def __init__(self):
        self.llm = MockLLM()
        self.working_memory = {}
        self.episodic_memory = [] # User's past interactions, purchases
        self.semantic_memory = self.llm.product_catalog.copy() # Product catalog, reviews
        self.procedural_memory = {
            "search_product_catalog": self._tool_search_product_catalog,
            "check_order_status": self._tool_check_order_status,
            "process_return": self._tool_process_return,
            "generate_personalized_ad": self._tool_generate_personalized_ad,
        }
        self.tools = self.procedural_memory
        self.user_profile = {"preferences": [], "purchase_history": []}
        self.order_database = {
            "ORD123": {"items": [{"id": "P001", "name": "Laptop Pro X1"}], "status": "shipped", "user": "user_a"},
            "ORD456": {"items": [{"id": "P002", "name": "Smart Watch Lite"}], "status": "delivered", "user": "user_b"}
        }

    def _tool_search_product_catalog(self, keywords):
        time.sleep(0.3) # Simulate database query
        results = []
        max_price = float('inf')
        for kw in keywords:
            if kw.startswith("max_price:"):
                max_price = int(kw.split(":")[1])
                keywords.remove(kw)
                break

        for product_id, details in self.semantic_memory.items():
            match_score = 0
            for keyword in keywords:
                if keyword.lower() in details['name'].lower() or \
                   keyword.lower() in details['description'].lower() or \
                   keyword.lower() in details['category'].lower():
                    match_score += 1
            if match_score > 0 and details['price'] <= max_price:
                results.append(details)
        
        self.working_memory['last_search_results'] = results
        if results:
            return f"Found {len(results)} products: {', '.join([p['name'] for p in results])}."
        return "No products found matching your criteria."

    def _tool_check_order_status(self, order_id):
        time.sleep(0.2) # Simulate order system lookup
        order = self.order_database.get(order_id)
        if order:
            self.working_memory['last_order_status'] = order['status']
            return f"Order {order_id} status: {order['status']}. Items: {', '.join([item['name'] for item in order['items']])}."
        return f"Order {order_id} not found."

    def _tool_process_return(self, order_id, item_id):
        time.sleep(0.5) # Simulate return system
        order = self.order_database.get(order_id)
        if order:
            for item in order['items']:
                if item['id'] == item_id:
                    # In a real system, this would update order status, issue refund etc.
                    self.episodic_memory.append(f"Return initiated for item {item_id} from order {order_id}")
                    self.working_memory['last_return'] = {'order_id': order_id, 'item_id': item_id}
                    return f"Return for item {item['name']} from order {order_id} initiated successfully."
            return f"Item {item_id} not found in order {order_id}."
        return f"Order {order_id} not found."

    def _tool_generate_personalized_ad(self, user_preferences):
        time.sleep(0.6) # Simulate ad generation engine
        if "electronics" in user_preferences or not user_preferences:
            ad_product = self.semantic_memory.get("laptop_pro")
        elif "wearables" in user_preferences:
            ad_product = self.semantic_memory.get("smart_watch_lite")
        else:
            ad_product = self.semantic_memory.get("wireless_earbuds") # Default
        
        if ad_product:
            ad = f"Special offer for you! Check out our {ad_product['name']} for just ${ad_product['price']}! {ad_product['description']}"
            self.working_memory['last_ad'] = ad
            return ad
        return "Could not generate a personalized ad at this moment."

    def _reflect_on_outcome(self, user_query, llm_response, tool_output=None):
        # Simulate learning: update user preferences based on searches or purchases
        if "search_product_catalog" in llm_response.get("tool", "") and self.working_memory.get('last_search_results'):
            for product in self.working_memory['last_search_results']:
                if product['category'] not in self.user_profile['preferences']:
                    self.user_profile['preferences'].append(product['category'])
                    print(f"[AGENT LEARNS]: Added '{product['category']}' to user preferences.")
        
        if "order status" in user_query.lower() and tool_output and "shipped" in tool_output:
            self.episodic_memory.append(f"User checked order status, order was shipped.")

    def _verify_availability(self, product_name):
        # Simple verification against semantic memory (product catalog)
        for prod_id, details in self.semantic_memory.items():
            if details['name'].lower() == product_name.lower():
                if details['stock'] > 0:
                    return True, f"'{product_name}' is in stock ({details['stock']} units)."
                else:
                    return False, f"'{product_name}' is out of stock."
        return False, f"'{product_name}' not found in catalog."

    def process_request(self, user_query):
        print(f"\n[USER]: {user_query}")
        self.working_memory = {"user_query": user_query, "user_preferences": self.user_profile['preferences']}
        
        # 1. LLM as Central Intelligence & Orchestrator
        llm_decision = self.llm.infer(user_query, context=self.working_memory)
        
        tool_output = None
        response = ""
        thought = llm_decision.get("thought", "No specific thought.")
        print(f"[LLM Thought]: {thought}")

        if llm_decision.get("action") == "tool_use":
            tool_name = llm_decision["tool"]
            params = llm_decision["params"]
            print(f"[AGENT ACTION]: Using tool '{tool_name}' with params: {params}")
            if tool_name in self.tools:
                try:
                    tool_output = self.tools[tool_name](**params)
                    response = tool_output

                    # 4. Adaptive Planning & Decision-Making (Multi-Strategy Planning, Grounded Planning)
                    if tool_name == "search_product_catalog" and self.working_memory.get('last_search_results'):
                        print("[AGENT PLANNING]: Search results obtained, verifying stock and suggesting best match.")
                        best_product = self.working_memory['last_search_results'][0] if self.working_memory['last_search_results'] else None
                        if best_product:
                            verified, stock_info = self._verify_availability(best_product['name'])
                            if verified:
                                response += f" The best match is {best_product['name']} for ${best_product['price']}. {stock_info}"
                                # Also generate a personalized ad based on this new interest
                                ad_decision = self.llm.infer("show me personalized ads", context={"user_preferences": self.user_profile['preferences'] + [best_product['category']]})
                                if ad_decision.get("action") == "tool_use":
                                    ad_output = self.tools[ad_decision["tool"]](**ad_decision["params"])
                                    response += f"\nConsider this: {ad_output}"
                            else:
                                response += f" However, {stock_info}"

                except Exception as e:
                    response = f"Error executing tool {tool_name}: {e}"
                    print(f"[ERROR]: {response}")
            else:
                response = f"LLM suggested unknown tool: {tool_name}"
        elif llm_decision.get("action") == "generate":
            response = llm_decision["response"]
        else:
            response = "I'm not sure how to respond to that."
        
        # 5. Continuous Learning & Self-Improvement (Automated Feedback & Reflection)
        self._reflect_on_outcome(user_query, llm_decision, tool_output)

        # 8. Output Generation & Integration
        final_output = f"[AGENT RESPONSE]: {response}"
        print(final_output)
        return final_output

# Real-world Usage: Smart Shopping Assistant / E-commerce Chatbot
# Simulation Pattern: User queries product recommendations, checks order status, or requests returns.
ecommerce_agent = ECommerceAgent()

ecommerce_agent.process_request("I'm looking for a new laptop.")
ecommerce_agent.process_request("What's the status for order ORD123?")
ecommerce_agent.process_request("Can you recommend a smart watch on a budget of $250?")
ecommerce_agent.process_request("I want to return item P001 from order ORD123.")
ecommerce_agent.process_request("Show me personalized ads.")
