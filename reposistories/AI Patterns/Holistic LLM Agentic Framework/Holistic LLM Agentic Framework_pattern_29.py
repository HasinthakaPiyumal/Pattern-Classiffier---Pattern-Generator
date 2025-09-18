import json
import time

class SimulatedLLM:
    def __init__(self):
        self.knowledge_base = {
            "transaction_details": {
                "TRN12345": {"amount": 150.00, "merchant": "Online Retailer X", "date": "2023-10-26", "type": "debit"},
                "TRN67890": {"amount": 50.00, "merchant": "Coffee Shop Y", "date": "2023-10-25", "type": "debit"},
                "TRN11223": {"amount": 1200.00, "merchant": "Travel Agency Z", "date": "2023-10-27", "type": "debit"},
                "TRN44556": {"amount": 25.00, "merchant": "Local Bakery", "date": "2023-10-28", "type": "debit"}
            },
            "fraud_rules": {
                "high_value_foreign": "Transactions over $1000 from unusual locations or merchants require verification.",
                "multiple_small_online": "Multiple small online transactions in a short period can be suspicious.",
                "unrecognized_merchant": "Transactions from merchants not previously used by the customer are flagged for review."
            },
            "financial_advice": {
                "budgeting": "Consider tracking your expenses for a month to identify spending patterns.",
                "savings": "Automate a small transfer to a savings account each payday."
            }
        }

    def generate_response(self, prompt, context=None):
        if "transaction" in prompt.lower() and "details" in prompt.lower():
            trn_id = next((word for word in prompt.split() if word.startswith("TRN")), None)
            if trn_id and trn_id in self.knowledge_base["transaction_details"]:
                details = self.knowledge_base["transaction_details"][trn_id]
                return f"The transaction {trn_id} on {details['date']} for ${details['amount']:.2f} was a {details['type']} at {details['merchant']}."
            return "I couldn't find details for that transaction ID."
        
        if "suspicious" in prompt.lower() or "fraud" in prompt.lower():
            if context and context.get("transaction_details"):
                tx_details = context["transaction_details"]
                if tx_details['amount'] > 1000 and tx_details['merchant'] == "Travel Agency Z": # Simple rule simulation
                    return f"Transaction {tx_details['id']} with {tx_details['merchant']} for ${tx_details['amount']:.2f} is flagged as potentially suspicious due to its high value and merchant type. It matches the 'high_value_foreign' rule. Would you like to initiate a fraud investigation?"
                return "Based on available information, this transaction does not appear suspicious."
            return "Please provide transaction details to check for suspicious activity."
        
        if "dispute" in prompt.lower():
            return "To dispute a charge, I need the transaction ID and a brief reason. I can then guide you through the process."

        if "financial advice" in prompt.lower() or "budget" in prompt.lower():
            return self.knowledge_base["financial_advice"].get("budgeting", "I can offer advice on budgeting or savings. What are you interested in?")

        return "I'm a banking assistant. How can I help you with your banking needs today?"

class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = [] # Store past interactions
        self.semantic_memory = {
            "banking_terms": ["debit", "credit", "balance", "statement"],
            "security_protocols": ["2FA", "PIN", "password policy"]
        }
        self.procedural_memory = {
            "dispute_steps": ["Identify transaction", "Gather evidence", "Submit form"],
            "fraud_check_flow": ["Analyze transaction history", "Cross-reference fraud rules", "Notify customer"]
        }

    def store_working_memory(self, key, value):
        self.working_memory[key] = value

    def retrieve_working_memory(self, key):
        return self.working_memory.get(key)

    def add_episodic_memory(self, interaction):
        self.episodic_memory.append((time.time(), interaction))

    def get_semantic_info(self, query):
        for key, values in self.semantic_memory.items():
            if query.lower() in key.lower() or any(query.lower() in v.lower() for v in values):
                return f"Found semantic info for '{query}' under '{key}'."
        return None
    
    def get_procedural_info(self, skill_name):
        return self.procedural_memory.get(skill_name)

class ToolKit:
    def get_transaction_details(self, trn_id):
        # Simulate a database lookup
        time.sleep(0.1) # Simulate latency
        if trn_id in SimulatedLLM().knowledge_base["transaction_details"]:
            return {"success": True, "data": SimulatedLLM().knowledge_base["transaction_details"][trn_id], "id": trn_id}
        return {"success": False, "error": "Transaction not found"}

    def check_fraud_rules(self, transaction_data):
        # Simulate checking against fraud rules engine
        time.sleep(0.1)
        if transaction_data.get("amount", 0) > 1000 and transaction_data.get("merchant") == "Travel Agency Z":
            return {"success": True, "flagged": True, "reason": "High value foreign transaction"}
        return {"success": True, "flagged": False, "reason": "No specific fraud pattern detected"}

    def initiate_dispute(self, trn_id, reason):
        # Simulate initiating a dispute in the banking system
        time.sleep(0.2)
        if trn_id in SimulatedLLM().knowledge_base["transaction_details"]:
            return {"success": True, "message": f"Dispute initiated for {trn_id} with reason: {reason}. A case will be opened."}
        return {"success": False, "error": "Cannot initiate dispute for unknown transaction."}

class BankingAgent:
    def __init__(self):
        self.llm = SimulatedLLM()
        self.memory = MemorySystem()
        self.toolkit = ToolKit()
        self.current_plan = []

    def _orchestrate_tools(self, tool_name, *args, **kwargs):
        tool_func = getattr(self.toolkit, tool_name, None)
        if tool_func:
            try:
                result = tool_func(*args, **kwargs)
                if not result.get("success"): # Basic error handling
                    self.memory.add_episodic_memory(f"Tool {tool_name} failed: {result.get('error')}")
                return result
            except Exception as e:
                self.memory.add_episodic_memory(f"Error executing tool {tool_name}: {e}")
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Tool not found"}

    def _plan_and_execute(self, user_query):
        # Adaptive Planning & Decision-Making
        response = ""
        if "transaction" in user_query.lower() and ("details" in user_query.lower() or "info" in user_query.lower()):
            trn_id = next((word for word in user_query.split() if word.startswith("TRN")), None)
            if trn_id:
                self.current_plan = ["get_transaction_details", "report_transaction_status"]
                self.memory.store_working_memory("current_trn_id", trn_id)
            else:
                return "Please provide a transaction ID (e.g., TRN12345) for details."
        elif "suspicious" in user_query.lower() or "fraud" in user_query.lower():
            current_trn_id = self.memory.retrieve_working_memory("current_trn_id")
            if current_trn_id:
                self.current_plan = ["get_transaction_details", "check_fraud_rules", "report_fraud_status"]
            else:
                return "Please specify which transaction you'd like me to check for fraud, or provide a transaction ID."
        elif "dispute" in user_query.lower():
            current_trn_id = self.memory.retrieve_working_memory("current_trn_id")
            if current_trn_id:
                self.current_plan = ["initiate_dispute_process"]
            else:
                return "To initiate a dispute, please first specify the transaction ID."
        elif "financial advice" in user_query.lower() or "budget" in user_query.lower():
            self.current_plan = ["provide_financial_advice"]
        else:
            self.current_plan = ["direct_llm_response"]

        for step in self.current_plan:
            if step == "get_transaction_details":
                trn_id = self.memory.retrieve_working_memory("current_trn_id")
                if trn_id:
                    tool_output = self._orchestrate_tools("get_transaction_details", trn_id)
                    if tool_output["success"]:
                        self.memory.store_working_memory("last_transaction_data", tool_output["data"])
                        self.memory.store_working_memory("last_transaction_id", trn_id)
                        response += f"Found details for {trn_id}: {tool_output['data']}.\n"
                    else:
                        response += f"Error retrieving transaction details: {tool_output['error']}.\n"
                        return response # Stop if details not found

            elif step == "report_transaction_status":
                trn_id = self.memory.retrieve_working_memory("current_trn_id")
                tx_data = self.memory.retrieve_working_memory("last_transaction_data")
                if tx_data:
                    llm_context = {"transaction_details": {"id": trn_id, **tx_data}}
                    response = self.llm.generate_response(f"Report details for transaction {trn_id}", context=llm_context)
                else:
                    response = "No transaction details available to report."

            elif step == "check_fraud_rules":
                tx_data = self.memory.retrieve_working_memory("last_transaction_data")
                trn_id = self.memory.retrieve_working_memory("last_transaction_id")
                if tx_data:
                    tool_output = self._orchestrate_tools("check_fraud_rules", tx_data)
                    self.memory.store_working_memory("fraud_check_result", tool_output)
                    llm_context = {"transaction_details": {"id": trn_id, **tx_data}, "fraud_check": tool_output}
                    if tool_output["success"] and tool_output["flagged"]:
                        response = self.llm.generate_response(f"Is transaction {trn_id} suspicious?", context=llm_context)
                    else:
                        response = self.llm.generate_response(f"Is transaction {trn_id} suspicious?", context=llm_context)
                else:
                    response = "Cannot check for fraud without transaction data."

            elif step == "report_fraud_status":
                fraud_result = self.memory.retrieve_working_memory("fraud_check_result")
                if fraud_result and fraud_result.get("flagged"):
                    response += f"Fraud check identified potential issue: {fraud_result['reason']}.\n"
                else:
                    response += "Fraud check found no immediate red flags.\n"

            elif step == "initiate_dispute_process":
                trn_id = self.memory.retrieve_working_memory("current_trn_id")
                reason = self.llm.generate_response(f"What's the reason for disputing {trn_id}?", context={"intent": "clarify_dispute_reason"})
                # In a real system, LLM would parse reason from user_query or ask interactively.
                tool_output = self._orchestrate_tools("initiate_dispute", trn_id, "User indicated unauthorized transaction.") # Simplified reason
                if tool_output["success"]:
                    response = tool_output["message"]
                else:
                    response = tool_output["error"]

            elif step == "provide_financial_advice":
                response = self.llm.generate_response(user_query)

            elif step == "direct_llm_response":
                response = self.llm.generate_response(user_query)

        return response

    def process_query(self, user_query):
        self.memory.add_episodic_memory(f"User Query: {user_query}")
        print(f"\nUser: {user_query}")

        # Intent Understanding & Core Reasoning by LLM (simulated planning)
        response = self._plan_and_execute(user_query)

        self.memory.add_episodic_memory(f"Agent Response: {response}")
        return response

# Real-world Usage Simulation: Banking Customer Support
banking_agent = BankingAgent()

print(banking_agent.process_query("What are the details of transaction TRN12345?"))
print(banking_agent.process_query("Is TRN11223 suspicious?"))
print(banking_agent.process_query("I want to dispute TRN44556."))
print(banking_agent.process_query("Give me some financial advice on budgeting."))

# Simulation Pattern: Handling an unknown query
print(banking_agent.process_query("Tell me a joke."))
