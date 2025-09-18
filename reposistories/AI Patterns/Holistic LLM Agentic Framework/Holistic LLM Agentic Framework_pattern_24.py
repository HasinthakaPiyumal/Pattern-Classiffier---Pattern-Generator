import datetime

class SimulatedLLM:
    def process_query(self, query, context=None):
        if "recommend products" in query.lower() or "suggest something" in query.lower():
            return f"RECOMMEND: Based on your preferences and recent activity, I suggest 'Smart Coffee Maker' or 'Noise-Cancelling Headphones'. Context: {context}"
        elif "add to cart" in query.lower():
            product = query.split('add ')[1].split(' to cart')[0].strip(". ")
            return f"ACTION:ADD_TO_CART(product='{product}', quantity=1)"
        elif "check stock" in query.lower():
            product = query.split('check stock for ')[1].strip(". ")
            return f"ACTION:CHECK_STOCK(product='{product}')"
        elif "checkout" in query.lower() or "place order" in query.lower():
            return "ACTION:PROCESS_ORDER()"
        elif "user preferences" in query.lower():
            return "QUERY:RETRIEVE_USER_PREFERENCES()"
        return f"I'm not sure how to assist with '{query}'."

class ProductCatalog:
    def __init__(self):
        self._products = {
            "Smart Coffee Maker": {"price": 120.00, "stock": 10, "category": "Kitchen", "features": "Wi-Fi, programmable"},
            "Noise-Cancelling Headphones": {"price": 250.00, "stock": 5, "category": "Electronics", "features": "Bluetooth, ANC"},
            "Ergonomic Office Chair": {"price": 300.00, "stock": 2, "category": "Office", "features": "Adjustable lumbar, mesh back"},
            "Yoga Mat": {"price": 30.00, "stock": 50, "category": "Fitness", "features": "Non-slip, eco-friendly"}
        }

    def get_product_info(self, product_name):
        return self._products.get(product_name, None)

    def update_stock(self, product_name, quantity_change):
        if product_name in self._products:
            self._products[product_name]["stock"] += quantity_change
            return True
        return False

class UserMemory:
    def __init__(self, user_id):
        self.user_id = user_id
        self.working_memory = {}
        self.episodic_memory = [] # Past interactions, purchases
        self.semantic_memory = {
            'U001': {
                'preferences': {'category': 'Electronics', 'price_range': 'mid-high'},
                'past_purchases': ['Smart Coffee Maker']
            }
        }
        self.shopping_cart = []

    def update_preferences(self, new_prefs):
        self.semantic_memory[self.user_id]['preferences'].update(new_prefs)
        self.add_episodic_event(f"Updated preferences: {new_prefs}")

    def add_to_cart(self, product, quantity):
        self.shopping_cart.append({'product': product, 'quantity': quantity})
        self.add_episodic_event(f"Added {quantity}x {product} to cart.")

    def clear_cart(self):
        self.shopping_cart = []

    def add_episodic_event(self, event):
        self.episodic_memory.append(f"{datetime.datetime.now()}: {event}")

    def get_user_data(self):
        return self.semantic_memory.get(self.user_id, {})

class ShoppingAssistantAgent:
    def __init__(self, user_id):
        self.llm = SimulatedLLM()
        self.product_catalog = ProductCatalog()
        self.memory = UserMemory(user_id)
        self.user_id = user_id

    def _add_to_cart(self, product, quantity):
        product_info = self.product_catalog.get_product_info(product)
        if product_info and product_info['stock'] >= quantity:
            self.memory.add_to_cart(product, quantity)
            self.product_catalog.update_stock(product, -quantity)
            print(f"TOOL_EXEC: Added {quantity}x {product} to cart. Current cart: {self.memory.shopping_cart}\n")
            return f"Added {quantity}x {product} to your cart. Total items: {len(self.memory.shopping_cart)}"
        return f"Sorry, {product} is out of stock or quantity requested is too high."

    def _check_stock(self, product):
        product_info = self.product_catalog.get_product_info(product)
        if product_info:
            print(f"TOOL_EXEC: Checking stock for {product}. Stock: {product_info['stock']}\n")
            return f"There are {product_info['stock']} units of {product} available."
        return f"Product {product} not found."

    def _process_order(self):
        if not self.memory.shopping_cart:
            return "Your cart is empty. Nothing to order."
        total_price = sum(self.product_catalog.get_product_info(item['product'])['price'] * item['quantity'] for item in self.memory.shopping_cart)
        order_details = self.memory.shopping_cart.copy()
        self.memory.add_episodic_event(f"Order placed for {order_details} at total price {total_price}.")
        self.memory.clear_cart()
        print(f"TOOL_EXEC: Processing order for {len(order_details)} items. Total: ${total_price:.2f}\n")
        return f"Order successfully placed for {len(order_details)} items. Total amount: ${total_price:.2f}."

    def _retrieve_user_preferences(self):
        user_data = self.memory.get_user_data()
        print(f"TOOL_EXEC: Retrieving user preferences for {self.user_id}. Data: {user_data}\n")
        return user_data.get('preferences', {})

    def run(self, user_query):
        print(f"USER: {user_query}")
        user_data = self.memory.get_user_data()
        context = f"User ID: {self.user_id}, Preferences: {user_data.get('preferences')}, Cart: {self.memory.shopping_cart}"
        self.memory.update_working_memory('current_context', context)

        llm_response = self.llm.process_query(user_query, context)
        print(f"LLM_ORCHESTRATOR: {llm_response}")

        if llm_response.startswith("ACTION:"):
            action_str = llm_response[len("ACTION:"):]
            try:
                action_name = action_str.split('(')[0]
                params_str = action_str.split('(')[1][:-1]
                params = dict(item.split('=', 1) for item in params_str.split(', ') if item)
                for k, v in params.items():
                    params[k] = v.strip("'")
                    if v.isdigit(): params[k] = int(v)

                if action_name == "ADD_TO_CART":
                    tool_output = self._add_to_cart(**params)
                elif action_name == "CHECK_STOCK":
                    tool_output = self._check_stock(**params)
                elif action_name == "PROCESS_ORDER":
                    tool_output = self._process_order()
                else:
                    tool_output = "Unknown action."
                print(f"AGENT_RESPONSE: {tool_output}")
                self.memory.add_episodic_event(f"Agent executed {action_name} with result: {tool_output}")
            except Exception as e:
                print(f"TOOL_ERROR: Failed to execute action {action_str}. Error: {e}")
                print("AGENT_RESPONSE: I encountered an error while trying to perform that action.")
        elif llm_response.startswith("RECOMMEND:"):
            recommendation = llm_response[len("RECOMMEND:"):].split('Context:')[0].strip()
            print(f"AGENT_RESPONSE: {recommendation}")
            self.memory.add_episodic_event(f"Agent recommended: {recommendation}")
            # Simulate continuous learning based on implicit feedback
            if "Smart Coffee Maker" in recommendation and 'Kitchen' not in user_data.get('preferences', {}).get('category', ''):
                self.memory.update_preferences({'category': 'Kitchen'}) # Learn new preference
                print("AGENT_THOUGHT: User showed interest in Kitchen. Updated preferences.\n")
        elif llm_response.startswith("QUERY:"):
            query_str = llm_response[len("QUERY:"):]
            if query_str.startswith("RETRIEVE_USER_PREFERENCES"):
                prefs = self._retrieve_user_preferences()
                print(f"AGENT_RESPONSE: Your current preferences are: {prefs}")
                self.memory.add_episodic_event(f"Retrieved user preferences: {prefs}")
        else:
            print(f"AGENT_RESPONSE: {llm_response}")
        print("\n" + "-" * 50 + "\n")

# Real-world usage simulation: Personalized E-commerce Shopping Assistant
shopping_agent = ShoppingAssistantAgent(user_id='U001')
shopping_agent.run("Can you recommend some products for me?")
shopping_agent.run("I'd like to add the Smart Coffee Maker to my cart.")
shopping_agent.run("Check stock for Ergonomic Office Chair.")
shopping_agent.run("I want to checkout now.")
shopping_agent.run("What are my current preferences?")