import json

class BankingLLM:
    def __init__(self, knowledge_base, tools):
        self.knowledge_base = knowledge_base
        self.tools = tools
        self.working_memory = {}
        self.episodic_memory = []

    def _retrieve_knowledge(self, query):
        for topic, content in self.knowledge_base.items():
            if topic in query.lower() or any(k in query.lower() for k in content.get("keywords", [])):
                return content["description"]
        return "Information not found in knowledge base."

    def _parse_intent_and_extract_params(self, query):
        query_lower = query.lower()
        if "balance" in query_lower:
            return "get_balance", {}
        elif "transfer" in query_lower and "from" in query_lower and "to" in query_lower and "amount" in query_lower:
            try:
                amount_str = query_lower.split("amount ")[1].split(" ")[0].replace("$", "")
                amount = float(amount_str)
                from_account = "checking" if "checking" in query_lower.split("from ")[1] else "savings"
                to_account = "savings" if "savings" in query_lower.split("to ")[1] else "checking"
                return "transfer_funds", {"amount": amount, "from_account": from_account, "to_account": to_account}
            except (ValueError, IndexError):
                return "clarify_transfer", {}
        elif "policy" in query_lower or "overdraft" in query_lower or "loan" in query_lower:
            return "get_policy", {"query": query_lower}
        return "unknown", {}

    def _orchestrate_tools(self, intent, params):
        if intent == "get_balance":
            account = params.get("account", "checking")
            balance = self.tools.get_account_balance(account)
            return f"Your {account} balance is ${balance:.2f}."
        elif intent == "transfer_funds":
            amount = params["amount"]
            from_account = params["from_account"]
            to_account = params["to_account"]
            success, message = self.tools.transfer_funds(from_account, to_account, amount)
            return message
        elif intent == "get_policy":
            return self._retrieve_knowledge(params["query"])
        elif intent == "clarify_transfer":
            return "I need more details to process the transfer. Please specify the amount, 'from' account, and 'to' account."
        return "I'm not sure how to handle that request."

    def process_query(self, user_query):
        intent, params = self._parse_intent_and_extract_params(user_query)
        self.working_memory["last_intent"] = intent
        self.working_memory["last_params"] = params
        self.episodic_memory.append({"query": user_query, "intent": intent, "params": params})

        if intent == "get_policy":
            return self._orchestrate_tools(intent, params)

        response = self._orchestrate_tools(intent, params)

        if "error" in response.lower():
            self.working_memory["last_error"] = response
            response += "\nI will try to improve my understanding for similar requests in the future."

        return response

class BankingTools:
    def __init__(self, initial_balances):
        self.accounts = initial_balances

    def get_account_balance(self, account_name):
        return self.accounts.get(account_name, 0.0)

    def transfer_funds(self, from_account, to_account, amount):
        if from_account not in self.accounts or to_account not in self.accounts:
            return False, "Error: Invalid account(s) specified."
        if self.accounts[from_account] < amount:
            return False, "Error: Insufficient funds."
        if amount <= 0:
            return False, "Error: Transfer amount must be positive."

        self.accounts[from_account] -= amount
        self.accounts[to_account] += amount
        return True, f"Successfully transferred ${amount:.2f} from {from_account} to {to_account}. Your new {from_account} balance is ${self.accounts[from_account]:.2f}."

if __name__ == "__main__":
    initial_balances = {"checking": 1250.75, "savings": 5000.00}
    banking_tools = BankingTools(initial_balances)

    bank_knowledge_base = {
        "overdraft": {
            "description": "Our overdraft policy allows up to $100 coverage with a $35 fee per incident. You can opt-in via online banking.",
            "keywords": ["overdraft", "fee"]
        },
        "loan_application": {
            "description": "To apply for a loan, visit our website or speak to a representative. Requirements include a good credit score and proof of income.",
            "keywords": ["loan", "apply"]
        }
    }

    banking_agent = BankingLLM(bank_knowledge_base, banking_tools)

    print("--- Banking Assistant Simulation ---")

    user_query = "What's my checking account balance?"
    print(f"\nUser: {user_query}")
    response = banking_agent.process_query(user_query)
    print(f"Agent: {response}")

    user_query = "I want to transfer $200 from checking to savings."
    print(f"\nUser: {user_query}")
    response = banking_agent.process_query(user_query)
    print(f"Agent: {response}")
    print(f"Current checking: ${banking_tools.accounts['checking']:.2f}, savings: ${banking_tools.accounts['savings']:.2f}")

    user_query = "Can you tell me about your overdraft policy?"
    print(f"\nUser: {user_query}")
    response = banking_agent.process_query(user_query)
    print(f"Agent: {response}")

    user_query = "Please transfer $2000 from checking to savings."
    print(f"\nUser: {user_query}")
    response = banking_agent.process_query(user_query)
    print(f"Agent: {response}")
    print(f"Current checking: ${banking_tools.accounts['checking']:.2f}, savings: ${banking_tools.accounts['savings']:.2f}")

    user_query = "I want to transfer money."
    print(f"\nUser: {user_query}")
    response = banking_agent.process_query(user_query)
    print(f"Agent: {response}")

    print("\n--- Agent Memory Snapshot ---")
    print(f"Working Memory: {banking_agent.working_memory}")
    print(f"Episodic Memory (last 2): {banking_agent.episodic_memory[-2:]}")