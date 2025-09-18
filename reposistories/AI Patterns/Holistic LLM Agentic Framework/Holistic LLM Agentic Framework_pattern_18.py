import json

class MockLLM:
    def __init__(self):
        pass

    def clarify_intent(self, query):
        if "transaction" in query and ("suspicious" in query or "fraud" in query):
            return "FRAUD_INVESTIGATION"
        elif "investment" in query or "savings" in query or "loan" in query:
            return "FINANCIAL_ADVICE"
        elif "account balance" in query or "statement" in query:
            return "ACCOUNT_INQUIRY"
        return "GENERAL_BANKING"

    def reason(self, intent, context):
        if intent == "FRAUD_INVESTIGATION":
            transaction_id = context.get('transaction_id', 'N/A')
            amount = context.get('amount', 'N/A')
            location = context.get('location', 'N/A')
            if 'unusual_pattern_detected' in context.get('tool_data', {}) and context['tool_data']['transaction_analyzer'] == 'Unusual pattern detected':
                return f"Transaction {transaction_id} of {amount} at {location} flagged. Recommend temporary lock and customer contact."
            return f"Investigating transaction {transaction_id}."
        elif intent == "FINANCIAL_ADVICE":
            goal = context.get('financial_goal', 'general advice')
            if goal == "investment":
                return "Considering investment options based on risk profile and current market trends. Suggesting a diversified portfolio."
            return f"Providing advice for financial goal: {goal}."
        return "I'm processing your request. Please wait."

    def generate_response(self, reasoning_output, tool_results=None, rag_info=None):
        response = reasoning_output
        if tool_results:
            for tool_name, result in tool_results.items():
                response += f"\nTool Result ({tool_name}): {result}"
        if rag_info:
            response += f"\nAdditional Info: {rag_info}"
        return response + "\nFor further assistance, please contact customer support."

class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []  # User transaction history, past interactions
        self.semantic_memory = {
            "fraud_patterns": {"large_international_transactions": "High risk", "multiple_small_purchases_rapidly": "Medium risk"},
            "financial_products": {"savings_account": "Low risk, low return", "stock_market": "High risk, high return"}
        }
        self.procedural_memory = {"fraud_detection_rules": "Check velocity, location, amount anomalies"}

    def add_to_working_memory(self, key, value):
        self.working_memory[key] = value

    def retrieve_from_working_memory(self, key):
        return self.working_memory.get(key)

    def add_episodic_memory(self, experience):
        self.episodic_memory.append(experience)

    def get_transaction_history(self, user_id):
        return [e for e in self.episodic_memory if e.get('user_id') == user_id]

    def get_semantic_info(self, key):
        return self.semantic_memory.get(key)

    def update_fraud_patterns(self, new_pattern, risk_level):
        self.semantic_memory['fraud_patterns'][new_pattern] = risk_level

class FinancialKnowledgeBase:
    def __init__(self, data):
        self.data = data

    def retrieve(self, query, strategy="simple"):
        if "fraud regulation" in query:
            return self.data.get('regulations', {}).get('fraud_prevention', 'Standard fraud prevention guidelines apply.')
        if "investment product" in query:
            product_name = query.split("investment product ")[-1]
            return self.data.get('products', {}).get(product_name, 'Product not found.')
        return None

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "transaction_analyzer": self._transaction_analyzer_tool,
            "investment_calculator": self._investment_calculator_tool,
            "credit_score_api": self._credit_score_api_tool,
        }

    def _transaction_analyzer_tool(self, transaction_details, fraud_patterns):
        if transaction_details.get('amount', 0) > 10000 and transaction_details.get('location') == 'International':
            return "Unusual pattern detected"
        if transaction_details.get('velocity', 0) > 5 and transaction_details.get('amount') < 50:
            return "Multiple small transactions, potential fraud"
        return "No immediate red flags"

    def _investment_calculator_tool(self, principal, interest_rate, years):
        future_value = principal * (1 + interest_rate)**years
        return f"Projected future value: ${future_value:.2f}"

    def _credit_score_api_tool(self, user_id):
        # Mock API call
        return "Credit Score: 750 (Excellent)"

    def execute_tool(self, tool_name, *args, **kwargs):
        if tool_name in self.tools:
            return self.tools[tool_name](*args, **kwargs)
        return f"Tool '{tool_name}' not found."

class BankingAgent:
    def __init__(self, financial_data):
        self.memory = MemorySystem()
        self.knowledge_base = FinancialKnowledgeBase(financial_data)
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
        if intent == "FRAUD_INVESTIGATION":
            context['transaction_id'] = "TXN12345"
            context['amount'] = 12000
            context['location'] = "International"
            tool_to_use = "transaction_analyzer"
        elif intent == "FINANCIAL_ADVICE":
            if "investment" in user_query: context['financial_goal'] = "investment"
            tool_to_use = "investment_calculator"

        # 2. Dynamic Knowledge & Memory System: RAG and Memory Retrieval
        rag_info = None
        if intent == "FRAUD_INVESTIGATION":
            rag_info = self.knowledge_base.retrieve("fraud regulation")
            if rag_info: print(f"Agent (RAG): Retrieved fraud regulations.")
        elif intent == "FINANCIAL_ADVICE":
            rag_info = self.knowledge_base.retrieve(f"investment product {context.get('financial_goal', 'general')}")
            if rag_info and rag_info != 'Product not found.': print(f"Agent (RAG): Retrieved investment product info.")

        # 3. Advanced Tool Integration & Interaction: Tool Orchestration & Execution
        tool_results = {}
        if tool_to_use == "transaction_analyzer":
            fraud_patterns = self.memory.get_semantic_info('fraud_patterns')
            tool_output = self.tool_registry.execute_tool(
                "transaction_analyzer", 
                transaction_details={'amount': context['amount'], 'location': context['location'], 'velocity': 1},
                fraud_patterns=fraud_patterns
            )
            tool_results['transaction_analyzer'] = tool_output
            print(f"Agent (Tool Use): Executed transaction_analyzer. Result: {tool_output}")
        elif tool_to_use == "investment_calculator":
            tool_output = self.tool_registry.execute_tool("investment_calculator", principal=10000, interest_rate=0.05, years=5)
            tool_results['investment_calculator'] = tool_output
            print(f"Agent (Tool Use): Executed investment_calculator. Result: {tool_output}")

        # 4. Adaptive Planning & Decision-Making (LLM's reasoning)
        reasoning_context = {
            'intent': intent,
            'context_data': context,
            'tool_data': tool_results,
            'rag_data': rag_info,
            'transaction_history': self.memory.get_transaction_history(user_id)
        }
        reasoning_output = self.llm.reason(intent, reasoning_context)
        print(f"Agent (LLM Reasoning): {reasoning_output}")

        # 5. Continuous Learning & Self-Improvement (simple: add to episodic memory, update fraud patterns)
        self.memory.add_episodic_memory({"user_id": user_id, "query": user_query, "response": reasoning_output, "tool_results": tool_results})
        if intent == "FRAUD_INVESTIGATION" and tool_results.get('transaction_analyzer') == 'Unusual pattern detected':
            self.memory.update_fraud_patterns('large_international_anomaly', 'Very High risk')
            print("Agent (Learning): Updated fraud patterns based on new detection.")

        # 8. Output Generation & Integration
        final_response = self.llm.generate_response(reasoning_output, tool_results, rag_info)
        print(f"Agent: {final_response}")
        return final_response

def simulate_banking_scenario():
    print("--- Banking Agent Simulation ---")
    financial_data = {
        "regulations": {"fraud_prevention": "All transactions over $10k require secondary verification if international."},
        "products": {"stock_market": "High potential returns, higher risk.", "savings_account": "Low risk, guaranteed returns."}
    }
    agent = BankingAgent(financial_data)

    # Real-world usage: User reports suspicious activity
    agent.process_query("user_A", "I see a suspicious international transaction for $12,000. Is this fraud?")
    # Real-world usage: User asks for investment advice
    agent.process_query("user_B", "I want to invest $10,000 for 5 years. What are my options?")
    # Simulation of learning and adaptation
    agent.process_query("user_A", "What are the latest fraud prevention measures?") # This query will trigger RAG and reflect updated knowledge

simulate_banking_scenario()
