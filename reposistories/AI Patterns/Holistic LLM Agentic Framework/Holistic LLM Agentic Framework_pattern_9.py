import json
import time

class MockLLM:
    def __init__(self):
        self.knowledge_base = {
            "fraud_patterns": [
                "large_purchase_unusual_location",
                "multiple_small_transactions_rapid_succession",
                "online_purchase_high_value_first_time_user",
                "international_transaction_no_travel_alert"
            ],
            "transaction_rules": {
                "max_daily_spend": 5000,
                "max_single_transaction": 2000,
                "max_international_spend": 1000
            }
        }
        self.tool_descriptions = {
            "check_transaction_rules": "Checks a transaction against pre-defined banking rules.",
            "block_card": "Blocks a customer's credit/debit card due to suspicious activity.",
            "notify_user": "Sends a notification to the user via SMS or email.",
            "initiate_investigation": "Flags a transaction for manual review by a fraud analyst."
        }

    def infer(self, prompt, context=None, persona="fraud_analyst"):
        if "analyze transaction" in prompt.lower():
            transaction_info = context.get("transaction_details", {})
            amount = transaction_info.get("amount", 0)
            location = transaction_info.get("location", "")
            is_international = transaction_info.get("is_international", False)
            
            if amount > self.knowledge_base["transaction_rules"]["max_single_transaction"] or \
               (is_international and amount > self.knowledge_base["transaction_rules"]["max_international_spend"]):
                return {
                    "action": "tool_use", 
                    "tool": "check_transaction_rules", 
                    "params": {"transaction": transaction_info, "reason": "potential_fraud_high_value"},
                    "thought": "High value or international transaction detected, needs rule check."
                }
            elif "unusual" in location.lower() and amount > 500:
                return {
                    "action": "tool_use", 
                    "tool": "check_transaction_rules", 
                    "params": {"transaction": transaction_info, "reason": "unusual_location"},
                    "thought": "Unusual location for a significant amount, check rules and patterns."
                }
            else:
                return {"action": "generate", "response": "Transaction appears normal based on initial assessment.", "thought": "Transaction seems routine, no immediate red flags."}

        if "block card for" in prompt.lower():
            account_id = prompt.split("block card for", 1)[1].strip().replace("?", "")
            return {"action": "tool_use", "tool": "block_card", "params": {"account_id": account_id}, "thought": "User requested card block, executing tool."}

        if "notify user about" in prompt.lower():
            message = prompt.split("notify user about", 1)[1].strip().replace("?", "")
            return {"action": "tool_use", "tool": "notify_user", "params": {"message": message}, "thought": "Preparing to send user notification."}

        if "investigate transaction" in prompt.lower():
            txn_id = prompt.split("investigate transaction", 1)[1].strip().replace("?", "")
            return {"action": "tool_use", "tool": "initiate_investigation", "params": {"transaction_id": txn_id}, "thought": "Escalating transaction for manual investigation."}

        return {"action": "generate", "response": "How can I assist with financial security today?", "thought": "Initial greeting or fallback."}

class BankingFraudAgent:
    def __init__(self):
        self.llm = MockLLM()
        self.working_memory = {}
        self.episodic_memory = [] # Past transactions, fraud alerts
        self.semantic_memory = self.llm.knowledge_base.copy() # Fraud patterns, rules
        self.procedural_memory = {
            "check_transaction_rules": self._tool_check_transaction_rules,
            "block_card": self._tool_block_card,
            "notify_user": self._tool_notify_user,
            "initiate_investigation": self._tool_initiate_investigation,
        }
        self.tools = self.procedural_memory
        self.user_profiles = {}

    def _tool_check_transaction_rules(self, transaction, reason):
        time.sleep(0.2) # Simulate rule engine check
        amount = transaction.get("amount", 0)
        location = transaction.get("location", "")
        is_international = transaction.get("is_international", False)
        account_id = transaction.get("account_id", "N/A")

        rules = self.semantic_memory["transaction_rules"]
        fraud_patterns = self.semantic_memory["fraud_patterns"]

        flags = []
        if amount > rules["max_single_transaction"]:
            flags.append(f"Exceeds max single transaction limit ({rules['max_single_transaction']})")
        if is_international and amount > rules["max_international_spend"]:
            flags.append(f"Exceeds international spend limit ({rules['max_international_spend']})")
        if "unusual_location" in reason and amount > 500:
            flags.append("Unusual high-value transaction location")
        
        # Simulate RAG for fraud patterns
        retrieved_patterns = [p for p in fraud_patterns if p.startswith(reason.split('_')[0])]
        if retrieved_patterns: flags.append(f"Matches known fraud patterns: {', '.join(retrieved_patterns)}")

        if flags:
            self.working_memory['fraud_alert'] = True
            self.working_memory['flags'] = flags
            return f"Transaction {transaction.get('id')} flagged. Reason: {', '.join(flags)}."
        
        self.working_memory['fraud_alert'] = False
        return f"Transaction {transaction.get('id')} passed rule checks."

    def _tool_block_card(self, account_id):
        time.sleep(0.5) # Simulate card blocking system
        self.episodic_memory.append(f"Card blocked for account {account_id}")
        self.working_memory['card_blocked'] = True
        return f"Card for account {account_id} has been successfully blocked."

    def _tool_notify_user(self, message, account_id="current_user"):
        time.sleep(0.3) # Simulate sending notification
        self.episodic_memory.append(f"Notification sent to {account_id}: '{message}'")
        self.working_memory['last_notification'] = message
        return f"Notification sent to user for account {account_id}: '{message}'"

    def _tool_initiate_investigation(self, transaction_id):
        time.sleep(00.7) # Simulate creating a case
        case_id = f"CASE-{int(time.time())}"
        self.episodic_memory.append(f"Investigation initiated for transaction {transaction_id}, Case ID: {case_id}")
        self.working_memory['investigation_initiated'] = case_id
        return f"Investigation initiated for transaction {transaction_id}. Case ID: {case_id}."

    def _reflect_on_outcome(self, user_query, llm_response, tool_output=None):
        if self.working_memory.get('fraud_alert'):
            print(f"[AGENT REFLECTS]: Fraud alert detected. Considering updating fraud patterns.")
            # Simulate continuous learning: if a specific pattern leads to a block, reinforce it
            if self.working_memory.get('card_blocked'):
                new_pattern = f"confirmed_fraud_{self.working_memory['flags'][0].replace(' ', '_').lower()}"
                if new_pattern not in self.semantic_memory["fraud_patterns"]:
                    self.semantic_memory["fraud_patterns"].append(new_pattern)
                    print(f"[AGENT LEARNS]: Added new fraud pattern: '{new_pattern}'.")

    def _verify_transaction(self, transaction):
        # Simple verification: check if transaction details align with known patterns or past alerts
        txn_id = transaction.get('id')
        for entry in self.episodic_memory:
            if f"Card blocked for account {transaction.get('account_id')}" in entry and txn_id in entry:
                return False, "Transaction denied: Card previously blocked for this account."
        return True, "No immediate conflicts with past actions/memory."

    def process_transaction(self, transaction_details):
        print(f"\n[NEW TRANSACTION]: {json.dumps(transaction_details)}")
        self.working_memory = {"transaction_details": transaction_details}
        
        # 7. Verification, Grounding & Explainability (Grounded Actions)
        verified, reason = self._verify_transaction(transaction_details)
        if not verified:
            print(f"[GROUNDING ERROR]: {reason}")
            return f"[AGENT RESPONSE]: Transaction {transaction_details['id']} declined. {reason}"

        # 1. LLM as Central Intelligence & Orchestrator
        llm_decision = self.llm.infer("analyze transaction", context=self.working_memory)
        
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
                    
                    # 4. Adaptive Planning & Decision-Making (Hierarchical & Iterative Planning)
                    if self.working_memory.get('fraud_alert'):
                        print("[AGENT PLANNING]: Fraud detected, initiating multi-step response.")
                        # Step 1: Notify user
                        notify_decision = self.llm.infer(f"notify user about suspicious transaction {transaction_details['id']} on account {transaction_details['account_id']}")
                        if notify_decision.get("action") == "tool_use":
                            self.tools[notify_decision["tool"]](**notify_decision["params"])
                            response += "\nUser notified of suspicious activity."
                        
                        # Step 2: Block card if critical fraud
                        if "high_value" in params.get("reason", "") or "unusual_location" in params.get("reason", ""):
                             block_card_decision = self.llm.infer(f"block card for {transaction_details['account_id']}")
                             if block_card_decision.get("action") == "tool_use":
                                 self.tools[block_card_decision["tool"]](**block_card_decision["params"])
                                 response += "\nCard has been blocked."
                             
                        # Step 3: Initiate investigation
                        investigate_decision = self.llm.infer(f"investigate transaction {transaction_details['id']}")
                        if investigate_decision.get("action") == "tool_use":
                            self.tools[investigate_decision["tool"]](**investigate_decision["params"])
                            response += "\nInvestigation initiated."


                except Exception as e:
                    response = f"Error executing tool {tool_name}: {e}"
                    print(f"[ERROR]: {response}")
            else:
                response = f"LLM suggested unknown tool: {tool_name}"
        elif llm_decision.get("action") == "generate":
            response = llm_decision["response"]
        else:
            response = "I'm not sure how to process this transaction."
        
        # 5. Continuous Learning & Self-Improvement (Automated Feedback & Reflection)
        self._reflect_on_outcome(f"transaction {transaction_details['id']}", llm_decision, tool_output)

        # 8. Output Generation & Integration
        final_output = f"[AGENT RESPONSE]: {response}"
        print(final_output)
        return final_output

# Real-world Usage: Automated Fraud Analyst / Transaction Monitoring System
# Simulation Pattern: Agent receives transaction details and decides whether to approve, flag, or block, possibly triggering multi-step actions.
banking_agent = BankingFraudAgent()

banking_agent.process_transaction({"id": "TXN001", "account_id": "ACC123", "amount": 150.00, "location": "New York", "is_international": False})
banking_agent.process_transaction({"id": "TXN002", "account_id": "ACC123", "amount": 2500.00, "location": "London", "is_international": True}) # Exceeds international limit
banking_agent.process_transaction({"id": "TXN003", "account_id": "ACC456", "amount": 3000.00, "location": "Paris", "is_international": False}) # Exceeds single transaction limit
banking_agent.process_transaction({"id": "TXN004", "account_id": "ACC789", "amount": 700.00, "location": "Bogota", "is_international": True}) # Unusual location, international
