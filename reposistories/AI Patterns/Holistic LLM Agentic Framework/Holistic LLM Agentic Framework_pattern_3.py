import random

class SimulatedLLM:
    def __init__(self, name="ShopAssistLLM"):
        self.name = name
        self.reasoning_trace = []

    def _simulate_reasoning(self, prompt, context):
        self.reasoning_trace.append(f"LLM: Analyzing prompt '{prompt}' with context: {context}")
        if "product_search" in context.get("intent", ""):
            return "product search strategy"
        elif "compare_products" in context.get("intent", ""):
            return "product comparison strategy"
        elif "add_to_cart" in context.get("intent", ""):
            return "cart management strategy"
        elif "order_status" in context.get("intent", ""):
            return "order tracking strategy"
        return "general shopping assistance"

    def understand_intent_and_orchestrate(self, user_query, current_state):
        self.reasoning_trace = []
        self.reasoning_trace.append(f"LLM: Understanding intent for query: '{user_query}'")
        query_lower = user_query.lower()
        product_query = None
        if "look for" in query_lower or "find me" in query_lower or "search for" in query_lower:
            intent = "product_search"
            product_query = query_lower.split("for ")[-1].strip() if "for " in query_lower else query_lower
            self.reasoning_trace.append(f"LLM: Intent identified: Product Search for '{product_query}'.")
        elif "compare" in query_lower:
            intent = "compare_products"
            self.reasoning_trace.append("LLM: Intent identified: Compare Products.")
        elif "add to cart" in query_lower or "buy" in query_lower:
            intent = "add_to_cart"
            self.reasoning_trace.append("LLM: Intent identified: Add to Cart.")
        elif "my order" in query_lower or "where is" in query_lower:
            intent = "order_status"
            self.reasoning_trace.append("LLM: Intent identified: Order Status.")
        else:
            intent = "general_inquiry"
            self.reasoning_trace.append("LLM: Intent identified: General Inquiry.")

        context = {"user_query": user_query, "current_state": current_state, "intent": intent}
        reasoning_output = self._simulate_reasoning(user_query, context)
        self.reasoning_trace.append(f"LLM: Core reasoning output: {reasoning_output}")
        return {"intent": intent, "reasoning_output": reasoning_output, "product_query": product_query, "trace": self.reasoning_trace}

    def generate_response(self, context):
        response_template = f"Based on your request ({context.get('intent', 'unknown intent')}): "
        if context["intent"] == "product_search":
            products = context.get("search_results", [])
            if products:
                return response_template + "Here are some products I found: " + ", ".join([p["name"] for p in products]) + ". Would you like to compare any?"
            else:
                return response_template + "I couldn't find any products matching your query. Please try again."
        elif context["intent"] == "compare_products":
            comparison = context.get("comparison_results", "No comparison data.")
            return response_template + f"Here's a comparison: {comparison}"
        elif context["intent"] == "add_to_cart":
            item = context.get("item_added", "an item")
            return response_template + f"{item} has been added to your cart. Your cart now has {context.get('cart_size', 0)} items."
        elif context["intent"] == "order_status":
            status = context.get("order_status_info", "Status unknown.")
            return response_template + f"Your order status is: {status}"
        else:
            return response_template + "How can I help you with your shopping today?"

class ProductCatalog:
    def __init__(self, products_data):
        self.products = products_data

    def search(self, query):
        results = []
        for product in self.products:
            if query.lower() in product["name"].lower() or query.lower() in product["description"].lower():
                results.append(product)
        return results

    def get_product_details(self, product_name):
        for product in self.products:
            if product["name"].lower() == product_name.lower():
                return product
        return None

class UserMemory:
    def __init__(self):
        self.current_cart = []
        self.purchase_history = []
        self.preferences = {"favorite_categories": [], "price_range": "medium"}
        self.working_memory = {}

    def add_to_cart(self, product):
        self.current_cart.append(product)
        self.working_memory["last_added_item"] = product["name"]
        return len(self.current_cart)

    def get_cart_size(self):
        return len(self.current_cart)

    def update_preferences(self, new_pref):
        self.preferences.update(new_pref)
        print(f"User preferences updated: {self.preferences}")

class SearchTool:
    def execute(self, product_query, product_catalog):
        print(f"Executing Search Tool for '{product_query}'...")
        return product_catalog.search(product_query)

class ComparisonTool:
    def execute(self, products_to_compare):
        print(f"Executing Comparison Tool for {len(products_to_compare)} products...")
        if len(products_to_compare) < 2:
            return "Need at least two products to compare."
        comparison_str = "Comparison:\n"
        for i, prod in enumerate(products_to_compare):
            comparison_str += f"  Product {i+1}: {prod['name']} (Price: ${prod['price']:.2f}, Rating: {prod['rating']} stars)\n"
        return comparison_str

class CartManagementTool:
    def execute(self, product, user_memory):
        print(f"Executing Cart Management Tool to add '{product['name']}'...")
        cart_size = user_memory.add_to_cart(product)
        return {"item_added": product["name"], "cart_size": cart_size}

class OrderTrackingTool:
    def execute(self, order_id):
        print(f"Executing Order Tracking Tool for order {order_id}...")
        if order_id == "ORD12345":
            return {"status": "Shipped", "estimated_delivery": "2024-07-20"}
        return {"status": "Order not found", "estimated_delivery": "N/A"}

class ECommerceAgent:
    def __init__(self):
        self.llm = SimulatedLLM()
        self.product_catalog = ProductCatalog([
            {"id": "P001", "name": "Laptop Pro X", "price": 1200.00, "rating": 4.5, "description": "High performance laptop."},
            {"id": "P002", "name": "Laptop Lite Y", "price": 800.00, "rating": 4.0, "description": "Lightweight and affordable laptop."},
            {"id": "P003", "name": "Gaming PC Z", "price": 1800.00, "rating": 4.8, "description": "Ultimate gaming experience."},
            {"id": "P004", "name": "Wireless Mouse", "price": 25.00, "rating": 4.2, "description": "Ergonomic wireless mouse."},
            {"id": "P005", "name": "Mechanical Keyboard", "price": 75.00, "rating": 4.7, "description": "Durable mechanical keyboard."}
        ])
        self.user_memory = UserMemory()
        self.search_tool = SearchTool()
        self.comparison_tool = ComparisonTool()
        self.cart_tool = CartManagementTool()
        self.order_tool = OrderTrackingTool()
        self.current_state = {}

    def process_query(self, user_query):
        self.user_memory.working_memory["last_query"] = user_query

        llm_analysis = self.llm.understand_intent_and_orchestrate(user_query, self.current_state)
        intent = llm_analysis["intent"]
        reasoning_output = llm_analysis["reasoning_output"]
        product_query = llm_analysis["product_query"]
        print("\n--- LLM Orchestration & Reasoning Trace ---")
        for step in llm_analysis["trace"]:
            print(step)
        print("------------------------------------------")

        response_context = {"intent": intent, "reasoning_output": reasoning_output}

        print(f"Memory: Current cart size: {self.user_memory.get_cart_size()}")
        print(f"Memory: User preferences: {self.user_memory.preferences}")

        if intent == "product_search":
            search_results = self.search_tool.execute(product_query, self.product_catalog)
            self.user_memory.working_memory["last_search_results"] = search_results
            response_context["search_results"] = search_results
            print(f"Tool: Search results: {[p['name'] for p in search_results]}")
            if "gaming" in product_query.lower():
                self.user_memory.update_preferences({"favorite_categories": ["gaming"]})

        elif intent == "compare_products":
            products_to_compare = []
            if "laptop pro x" in user_query.lower() and "laptop lite y" in user_query.lower():
                products_to_compare.append(self.product_catalog.get_product_details("Laptop Pro X"))
                products_to_compare.append(self.product_catalog.get_product_details("Laptop Lite Y"))
            elif self.user_memory.working_memory.get("last_search_results"):
                products_to_compare = self.user_memory.working_memory["last_search_results"][:2]

            comparison_results = self.comparison_tool.execute(products_to_compare)
            response_context["comparison_results"] = comparison_results
            print(f"Tool: Comparison results generated.")

        elif intent == "add_to_cart":
            item_name = user_query.replace("add ", "").replace(" to cart", "").replace("buy ", "").strip()
            product_to_add = self.product_catalog.get_product_details(item_name)
            if product_to_add:
                cart_info = self.cart_tool.execute(product_to_add, self.user_memory)
                response_context.update(cart_info)
                print(f"Tool: Added '{item_name}' to cart.")
            else:
                response_context["item_added"] = "Unknown item"
                response_context["cart_size"] = self.user_memory.get_cart_size()
                print(f"Tool: Could not find '{item_name}' to add to cart.")

        elif intent == "order_status":
            order_id = "ORD12345"
            status_info = self.order_tool.execute(order_id)
            response_context["order_status_info"] = f"Order {order_id}: {status_info['status']} (ETA: {status_info['estimated_delivery']})"
            print(f"Tool: Order status retrieved.")

        explanation = f"I've processed your request. Current cart items: {', '.join([p['name'] for p in self.user_memory.current_cart]) if self.user_memory.current_cart else 'None'}."
        response_context["explanation"] = explanation
        print(f"Explainability: {explanation}")

        final_response = self.llm.generate_response(response_context)
        return final_response, self.user_memory.working_memory

if __name__ == "__main__":
    agent = ECommerceAgent()
    print("E-commerce Agent Activated. Type 'exit' to quit.")

    queries = [
        "Search for laptops.",
        "Compare Laptop Pro X and Laptop Lite Y.",
        "Add Laptop Pro X to cart.",
        "What is the status of my order ORD12345?",
        "Find me a gaming PC."
    ]

    for query in queries:
        print(f"\n--- User Query: {query} ---")
        response, state = agent.process_query(query)
        print(f"\nAgent Response: {response}")
        print(f"Current Agent State (Working Memory): {state}")
