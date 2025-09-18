import json
import time
import random

class MockLLM:
    def __init__(self, name="ShopGPT"):
        self.name = name

    def generate(self, prompt, context="", tools_available=None):
        print(f"[{self.name} - Generating]: {prompt[:100]}...")
        if "recommend products" in prompt.lower():
            if "laptop" in prompt.lower() and "gaming" in prompt.lower():
                return "Gaming Laptop: High-performance, dedicated GPU. Brands: Alienware, ASUS ROG. Based on your preference for 'gaming'."
            elif "eco-friendly" in prompt.lower() and "clothing" in prompt.lower():
                return "Eco-friendly T-shirt: Organic cotton, sustainable production. Brands: Patagonia, Tentree. Based on your preference for 'eco-friendly'."
            return "Generic product recommendation. Please specify category or preferences."
        elif "tool_use_plan" in prompt.lower():
            return self._plan_tool_use(prompt, tools_available)
        elif "clarify" in prompt.lower():
            return "Could you specify the type of product, your budget, or any specific features you are looking for?"
        elif "compare prices" in prompt.lower():
            return "Comparing prices across various retailers..."
        return "Understood. How can I help with your shopping today?"

    def _plan_tool_use(self, prompt, tools_available):
        if "search product" in prompt.lower() and "laptop" in prompt.lower():
            return {"action": "call_tool", "tool_name": "ProductSearchAPI", "parameters": {"query": "gaming laptop", "limit": 3}}
        if "compare price" in prompt.lower() and "product_id" in prompt.lower():
            product_id = prompt.split("product_id:")[1].split(" ")[0].strip()
            return {"action": "call_tool", "tool_name": "PriceComparisonAPI", "parameters": {"product_id": product_id}}
        if "check reviews" in prompt.lower() and "product_id" in prompt.lower():
            product_id = prompt.split("product_id:")[1].split(" ")[0].strip()
            return {"action": "call_tool", "tool_name": "ReviewSentimentAnalyzer", "parameters": {"product_id": product_id}}
        return {"action": "respond", "response": "No specific tool action planned based on this request."}

    def verify_recommendation_relevance(self, recommendation, user_preferences, product_details):
        if "gaming laptop" in recommendation.lower() and "gaming" in user_preferences.get("interests", []):
            return True, "Recommendation aligns with user's gaming interest."
        if "eco-friendly" in recommendation.lower() and "sustainability" in user_preferences.get("values", []):
            return True, "Recommendation aligns with user's sustainability values."
        if "out of stock" in product_details.get("availability", "").lower() and "recommend" in recommendation.lower():
            return False, "Recommended an out-of-stock item."
        return False, "Recommendation relevance could not be fully verified against preferences."


class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []
        self.semantic_memory = {
            "product_catalog": {
                "P001": {"name": "Gaming Laptop X", "category": "Electronics", "price": 1500, "features": ["RTX 3070", "16GB RAM"], "availability": "In Stock"},
                "P002": {"name": "Eco-friendly T-shirt", "category": "Apparel", "price": 30, "features": ["Organic Cotton", "Fair Trade"], "availability": "In Stock"},
                "P003": {"name": "Noise-Cancelling Headphones", "category": "Electronics", "price": 250, "features": ["ANC", "Bluetooth 5.0"], "availability": "Out of Stock"},
            },
            "user_profiles": {
                "U101": {"name": "John Doe", "interests": ["gaming", "tech gadgets"], "values": ["performance"], "past_purchases": ["P001"]},
                "U102": {"name": "Jane Smith", "interests": ["fashion", "outdoors"], "values": ["sustainability", "comfort"], "past_purchases": ["P002"]},
            },
            "category_keywords": {"laptop": ["electronics", "computer"], "t-shirt": ["apparel", "clothing"]}
        }
        self.procedural_memory = {
            "recommendation_flow": "1. Understand intent. 2. Retrieve user profile. 3. Search product catalog. 4. Filter by preferences. 5. Generate recommendation.",
            "price_comparison_flow": "1. Identify product. 2. Call PriceComparisonAPI. 3. Present results."
        }

    def retrieve(self, query_type, key=None, context=""):
        if query_type == "semantic":
            if key == "product_catalog":
                return self.semantic_memory["product_catalog"]
            if key and key.startswith("product:"):
                return self.semantic_memory["product_catalog"].get(key.split(":")[1])
            if key and key.startswith("user:"):
                return self.semantic_memory["user_profiles"].get(key.split(":")[1])
            if "gaming laptop" in context.lower():
                return [p for p in self.semantic_memory["product_catalog"].values() if "gaming" in p.get("name", "").lower() and "laptop" in p.get("name", "").lower()]
            if "eco-friendly clothing" in context.lower():
                return [p for p in self.semantic_memory["product_catalog"].values() if "eco-friendly" in p.get("name", "").lower() or "organic" in p.get("features", [])]
            return "No specific semantic knowledge found."
        elif query_type == "episodic":
            return [e for e in self.episodic_memory if key in str(e)] if key else self.episodic_memory
        elif query_type == "procedural":
            return self.procedural_memory.get(key, "No specific procedure found.")
        elif query_type == "working":
            return self.working_memory.get(key)
        return "Invalid memory query type."

    def store(self, memory_type, key, value):
        if memory_type == "working":
            self.working_memory[key] = value
        elif memory_type == "episodic":
            self.episodic_memory.append({key: value, "timestamp": time.time()})
        elif memory_type == "semantic":
            if key.startswith("user_profile_update:"):
                user_id = key.split(":")[1]
                self.semantic_memory["user_profiles"].setdefault(user_id, {}).update(value)
            else:
                self.semantic_memory[key] = value
        print(f"Stored in {memory_type} memory: {key} = {value}")

class ProductSearchAPI:
    def search_products(self, query, limit=5):
        print(f"--- TOOL: ProductSearchAPI - Searching for '{query}' (limit: {limit}) ---")
        time.sleep(0.8)
        mock_results = [
            {"id": "P001", "name": "Gaming Laptop X", "price": 1500, "rating": 4.5},
            {"id": "P004", "name": "Ultra Gaming Rig Z", "price": 2200, "rating": 4.8},
            {"id": "P005", "name": "Budget Gaming Laptop", "price": 900, "rating": 4.0},
            {"id": "P002", "name": "Eco-friendly T-shirt", "price": 30, "rating": 4.2},
        ]
        results = [p for p in mock_results if query.lower() in p["name"].lower()][:limit]
        return {"status": "success", "products": results}

class PriceComparisonAPI:
    def compare_prices(self, product_id):
        print(f"--- TOOL: PriceComparisonAPI - Comparing prices for {product_id} ---")
        time.sleep(0.6)
        prices = {
            "P001": {"Retailer A": 1499, "Retailer B": 1550, "Retailer C": 1475},
            "P002": {"Retailer A": 29, "Retailer B": 32},
        }
        return {"status": "success", "product_id": product_id, "prices": prices.get(product_id, {"Retailer A": random.randint(50, 500)})}

class ReviewSentimentAnalyzer:
    def analyze_reviews(self, product_id):
        print(f"--- TOOL: ReviewSentimentAnalyzer - Analyzing reviews for {product_id} ---")
        time.sleep(1)
        sentiments = {
            "P001": {"overall_sentiment": "positive", "score": 0.85, "summary": "Users praise performance."},
            "P002": {"overall_sentiment": "very positive", "score": 0.92, "summary": "Comfortable and sustainable."},
        }
        return {"status": "success", "product_id": product_id, "sentiment": sentiments.get(product_id, {"overall_sentiment": "neutral", "score": 0.6})}

class ShoppingAssistantAgent:
    def __init__(self):
        self.llm = MockLLM()
        self.memory = MemorySystem()
        self.tools = {
            "ProductSearchAPI": ProductSearchAPI(),
            "PriceComparisonAPI": PriceComparisonAPI(),
            "ReviewSentimentAnalyzer": ReviewSentimentAnalyzer()
        }
        self.user_id = "U101"

    def _execute_tool_action(self, action):
        tool_name = action["tool_name"]
        parameters = action["parameters"]
        tool_instance = self.tools.get(tool_name)
        if not tool_instance:
            return {"status": "error", "message": f"Tool '{tool_name}' not found."}

        method_name = None
        if tool_name == "ProductSearchAPI":
            method_name = "search_products"
        elif tool_name == "PriceComparisonAPI":
            method_name = "compare_prices"
        elif tool_name == "ReviewSentimentAnalyzer":
            method_name = "analyze_reviews"

        if method_name and hasattr(tool_instance, method_name):
            try:
                result = getattr(tool_instance, method_name)(**parameters)
                return {"status": "success", "tool_result": result}
            except Exception as e:
                return {"status": "error", "message": f"Tool execution failed: {e}"}
        return {"status": "error", "message": f"Tool '{tool_name}' has no '{method_name}' method."}

    def process_request(self, user_query):
        self.memory.store("working", "current_user_query", user_query)
        self.memory.store("working", "current_user_id", self.user_id)

        print(f"\n[Agent]: Processing request: '{user_query}' for user {self.user_id}")

        llm_response = self.llm.generate(f"Clarify intent for: {user_query}")
        if "specify the type of product" in llm_response.lower():
            print(f"[Agent]: {llm_response}")
            user_query += " I'm looking for a new gaming laptop."
            self.memory.store("working", "current_user_query", user_query)
            print("[Agent]: (Simulated user clarification provided: 'gaming laptop')")

        user_profile = self.memory.retrieve("semantic", f"user:{self.user_id}")
        context = f"User profile: {user_profile}. Current query: {user_query}. "
        relevant_products = self.memory.retrieve("semantic", key="gaming laptop", context=context)
        print(f"[Agent]: Retrieved relevant knowledge (RAG): {relevant_products}")
        self.memory.store("working", "retrieved_products", relevant_products)

        llm_plan_prompt = f"Given user profile, query, and retrieved products, recommend suitable items and suggest further actions (e.g., compare prices, check reviews). Context: {context}"
        reasoning_output = self.llm.generate(llm_plan_prompt, context=context, tools_available=list(self.tools.keys()))
        self.memory.store("working", "llm_reasoning_output", reasoning_output)
        print(f"[Agent]: LLM's initial reasoning: {reasoning_output}")

        tool_planning_prompt = f"Based on the reasoning: '{reasoning_output}', determine if any tools should be called. If so, provide a JSON action. Context: {context} Available tools: {list(self.tools.keys())}. Prepend with 'tool_use_plan:'"
        tool_action_suggestion = self.llm.generate(tool_planning_prompt, tools_available=list(self.tools.keys()))

        final_recommendation = reasoning_output
        if isinstance(tool_action_suggestion, dict) and tool_action_suggestion.get("action") == "call_tool":
            print(f"[Agent]: LLM suggests tool use: {tool_action_suggestion}")
            tool_result = self._execute_tool_action(tool_action_suggestion)
            self.memory.store("episodic", "tool_execution_log", {"action": tool_action_suggestion, "result": tool_result})
            print(f"[Agent]: Tool execution result: {tool_result}")
            context += f" Tool result: {tool_result}. "
            final_recommendation = self.llm.generate(f"Integrate tool result into final recommendation: {reasoning_output}. Tool result: {tool_result}", context=context)
        
        if "gaming laptop" in user_query.lower() and "gaming" not in user_profile.get("interests", []):
            self.memory.store("semantic", f"user_profile_update:{self.user_id}", {"interests": user_profile.get("interests", []) + ["gaming"]})
            print(f"[Agent]: Updated user profile for {self.user_id} with new interest: 'gaming'.")

        user_preferences_for_verification = self.memory.retrieve("semantic", f"user:{self.user_id}")
        product_details_for_verification = self.memory.retrieve("semantic", f"product:P001")
        is_verified, verification_msg = self.llm.verify_recommendation_relevance(final_recommendation, user_preferences_for_verification, product_details_for_verification)
        print(f"[Agent]: Recommendation verification: {is_verified} - {verification_msg}")
        if not is_verified and "out of stock" in verification_msg:
            print("[Agent]: Self-correction: Recommending alternative due to stock issue.")
            final_recommendation = self.llm.generate(f"The previous recommendation was for an out-of-stock item. Suggest an alternative gaming laptop. Context: {context}", context=context)

        print(f"\n[Agent]: Final Recommendation for {user_profile.get('name', 'user')}:")
        print(final_recommendation)
        self.memory.store("episodic", "final_recommendation", final_recommendation)
        return final_recommendation

def simulate_shopping_assistant_usage():
    print("--- Simulating Personalized Shopping Assistant in E-commerce ---")
    agent = ShoppingAssistantAgent()

    agent.process_request("I need a new laptop.")

    agent.user_id = "U102"
    print(f"\n--- Switching to user U102 (Jane Smith) ---")
    agent.process_request("I'm looking for some new clothes, something sustainable.")

    agent.user_id = "U101"
    print(f"\n--- Switching to user U101 (John Doe) for a specific product ---")
    agent.process_request("Compare prices for Gaming Laptop X (P001).")

simulate_shopping_assistant_usage()