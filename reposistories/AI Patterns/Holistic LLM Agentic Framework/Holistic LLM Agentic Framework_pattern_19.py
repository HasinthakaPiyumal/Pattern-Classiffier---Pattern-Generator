import json

class MockLLM:
    def __init__(self):
        pass

    def clarify_intent(self, query):
        if "recommend" in query or "suggest" in query or "looking for" in query:
            return "PRODUCT_RECOMMENDATION"
        elif "order" in query and ("status" in query or "track" in query or "issue" in query):
            return "ORDER_SUPPORT"
        elif "return" in query or "refund" in query:
            return "RETURN_REFUND_ASSISTANCE"
        return "GENERAL_INQUIRY"

    def reason(self, intent, context):
        if intent == "PRODUCT_RECOMMENDATION":
            prefs = context.get('preferences', 'general items')
            if "tool_data" in context and "product_search" in context['tool_data']:
                return f"Based on your preferences for {prefs} and available products, I've identified some top matches."
            return f"Analyzing preferences for {prefs}. Need to search the catalog."
        elif intent == "ORDER_SUPPORT":
            order_id = context.get('order_id', 'N/A')
            if "tool_data" in context and "order_tracking" in context['tool_data']:
                return f"Checking status for Order ID {order_id}."
            return f"To track order {order_id}, I need to access the order system."
        return "I am processing your request."

    def generate_response(self, reasoning_output, tool_results=None, rag_info=None):
        response = reasoning_output
        if tool_results:
            for tool_name, result in tool_results.items():
                response += f"\nTool Result ({tool_name}): {result}"
        if rag_info:
            response += f"\nFurther Details: {rag_info}"
        return response + "\nIs there anything else I can help with?"

class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []  # User purchase history, past interactions
        self.semantic_memory = {
            "product_categories": {"electronics": "Laptops, Phones", "apparel": "Shirts, Jeans"},
            "customer_faqs": {"return_policy": "30 days, original packaging"}
        }
        self.procedural_memory = {"recommendation_logic": "Match keywords to product attributes"}

    def add_to_working_memory(self, key, value):
        self.working_memory[key] = value

    def retrieve_from_working_memory(self, key):
        return self.working_memory.get(key)

    def add_episodic_memory(self, experience):
        self.episodic_memory.append(experience)

    def get_user_purchase_history(self, user_id):
        return [e for e in self.episodic_memory if e.get('user_id') == user_id and 'purchase' in e]

    def update_user_preferences(self, user_id, new_pref):
        # Simulate updating user profile in semantic memory or a dedicated user store
        print(f"(Learning) Updated preferences for user {user_id} with: {new_pref}")

class ProductCatalog:
    def __init__(self, data):
        self.data = data

    def retrieve_products(self, query_keywords):
        results = []
        for product_id, product_info in self.data.items():
            if any(keyword.lower() in product_info['name'].lower() or 
                   keyword.lower() in product_info['category'].lower() or 
                   keyword.lower() in product_info['description'].lower() 
                   for keyword in query_keywords):
                results.append(product_info)
        return results

    def get_product_details(self, product_id):
        return self.data.get(product_id)

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "product_search": self._product_search_tool,
            "order_tracking": self._order_tracking_tool,
            "discount_calculator": self._discount_calculator_tool,
        }

    def _product_search_tool(self, keywords, catalog):
        results = catalog.retrieve_products(keywords)
        if results:
            return f"Found {len(results)} products: {[p['name'] for p in results[:3]]}..."
        return "No products found matching your criteria."

    def _order_tracking_tool(self, order_id):
        # Mock order tracking system
        if order_id == "ORD123":
            return "Order ORD123: Shipped, estimated delivery May 15th."
        return f"Order {order_id} not found or invalid."

    def _discount_calculator_tool(self, price, percentage):
        discounted_price = price * (1 - percentage / 100)
        return f"Price after {percentage}% discount: ${discounted_price:.2f}"

    def execute_tool(self, tool_name, *args, **kwargs):
        if tool_name in self.tools:
            return self.tools[tool_name](*args, **kwargs)
        return f"Tool '{tool_name}' not found."

class ECommerceAgent:
    def __init__(self, product_data):
        self.memory = MemorySystem()
        self.product_catalog = ProductCatalog(product_data)
        self.llm = MockLLM()
        self.tool_registry = ToolRegistry()

    def process_query(self, user_id, user_query):
        print(f"\nUser {user_id}: {user_query}")

        # 1. LLM as Central Intelligence & Orchestrator: Intent Understanding
        intent = self.llm.clarify_intent(user_query)
        print(f"Agent (LLM Intent): Detected intent as {intent}.")
        self.memory.add_to_working_memory('current_intent', intent)

        context = {'user_id': user_id, 'user_query': user_query}
        tool_to_use = None
        if intent == "PRODUCT_RECOMMENDATION":
            keywords = [word for word in user_query.lower().split() if word not in ["i", "am", "looking", "for", "a", "to", "recommend", "suggest"]]
            context['preferences'] = keywords
            tool_to_use = "product_search"
        elif intent == "ORDER_SUPPORT":
            order_id = "ORD123" if "123" in user_query else ""
            context['order_id'] = order_id
            tool_to_use = "order_tracking"

        # 2. Dynamic Knowledge & Memory System: RAG and Memory Retrieval
        rag_info = None
        if intent == "RETURN_REFUND_ASSISTANCE":
            rag_info = self.memory.semantic_memory.get('customer_faqs', {}).get('return_policy')
            if rag_info: print(f"Agent (RAG): Retrieved return policy from FAQs.")
        elif intent == "PRODUCT_RECOMMENDATION" and context.get('preferences'):
            # Simulate retrieving detailed product info for potential recommendations
            related_products = self.product_catalog.retrieve_products(context['preferences'])
            if related_products: rag_info = f"Product details: {related_products[0]['description']}"
            if rag_info: print(f"Agent (RAG): Retrieved product details for recommendation.")

        # 3. Advanced Tool Integration & Interaction: Tool Orchestration & Execution
        tool_results = {}
        if tool_to_use == "product_search":
            tool_output = self.tool_registry.execute_tool("product_search", context['preferences'], self.product_catalog)
            tool_results['product_search'] = tool_output
            print(f"Agent (Tool Use): Executed product_search. Result: {tool_output}")
        elif tool_to_use == "order_tracking":
            tool_output = self.tool_registry.execute_tool("order_tracking", context['order_id'])
            tool_results['order_tracking'] = tool_output
            print(f"Agent (Tool Use): Executed order_tracking. Result: {tool_output}")

        # 4. Adaptive Planning & Decision-Making (LLM's reasoning)
        reasoning_context = {
            'intent': intent,
            'context_data': context,
            'tool_data': tool_results,
            'rag_data': rag_info,
            'purchase_history': self.memory.get_user_purchase_history(user_id)
        }
        reasoning_output = self.llm.reason(intent, reasoning_context)
        print(f"Agent (LLM Reasoning): {reasoning_output}")

        # 5. Continuous Learning & Self-Improvement (simple: add to episodic memory, update preferences)
        self.memory.add_episodic_memory({"user_id": user_id, "query": user_query, "response": reasoning_output, "tool_results": tool_results})
        if intent == "PRODUCT_RECOMMENDATION" and context.get('preferences'):
            self.memory.update_user_preferences(user_id, context['preferences'])

        # 8. Output Generation & Integration
        final_response = self.llm.generate_response(reasoning_output, tool_results, rag_info)
        print(f"Agent: {final_response}")
        return final_response

def simulate_ecommerce_scenario():
    print("--- E-commerce Agent Simulation ---")
    product_data = {
        "P001": {"name": "Laptop X", "category": "electronics", "description": "Powerful laptop for work and gaming.", "price": 1200},
        "P002": {"name": "Smartphone Y", "category": "electronics", "description": "Latest smartphone with amazing camera.", "price": 800},
        "P003": {"name": "T-Shirt Z", "category": "apparel", "description": "Comfortable cotton t-shirt.", "price": 25}
    }
    agent = ECommerceAgent(product_data)

    # Real-world usage: Customer asks for product recommendation
    agent.process_query("user_C", "I am looking for a new laptop. Can you recommend something powerful?")
    # Real-world usage: Customer tracks an order
    agent.process_query("user_D", "What is the status of my order ORD123?")
    # Real-world usage: Customer asks about return policy
    agent.process_query("user_C", "What is your return policy?")

simulate_ecommerce_scenario()
