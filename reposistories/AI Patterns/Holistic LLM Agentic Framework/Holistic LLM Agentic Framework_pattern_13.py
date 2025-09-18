import random
import time

class LLMCore:
    def __init__(self, name="BankAdvisorLLM"):
        self.name = name
        self.thoughts = []

    def reason(self, prompt, context, memory_snapshot, tools_available):
        self.thoughts.append(f"[{self.name}] Analyzing query: '{prompt[:50]}'")
        prompt_lower = prompt.lower()

        if "fraud" in prompt_lower or "unauthorized" in prompt_lower or "suspicious" in prompt_lower:
            intent = "fraud_detection"
            plan = "PLAN: First, use FraudDetectionTool to analyze transactions. Second, access TransactionHistory. Third, consult FinancialRegulationsDB. Finally, generate advice."
        elif "invest" in prompt_lower or "investment" in prompt_lower or "portfolio" in prompt_lower:
            intent = "investment_advice"
            plan = "PLAN: First, retrieve user's portfolio from TransactionHistory. Second, use InvestmentAnalysisTool. Third, generate personalized investment recommendations."
        elif "balance" in prompt_lower or "transactions" in prompt_lower:
            intent = "account_inquiry"
            plan = "PLAN: Use AccountAccessTool to get current balance/transactions. Generate direct response."
        else:
            intent = "general_financial_inquiry"
            plan = "PLAN: Access general financial knowledge. Generate informative response."
        
        self.thoughts.append(f"[{self.name}] Intent: {intent}, Plan: {plan}")
        return {"intent": intent, "plan": plan}

    def generate_response(self, plan_output, tool_results, memory_info, verification_status):
        response = f"Hello! I'm your Financial Advisor. Here's what I've found:\n"
        
        if "fraud_detection" in plan_output["intent"]:
            response += f"Fraud Check Result: {tool_results.get('fraud_status', 'N/A')}\n"
            if tool_results.get('fraud_details'):
                response += f"Details: {tool_results['fraud_details']}\n"
            response += f"Recommendation: {tool_results.get('fraud_recommendation', 'Please review your recent activity.')}\n"
        elif "investment_advice" in plan_output["intent"]:
            response += f"Investment Analysis:\n"
            if tool_results.get('portfolio_summary'):
                response += f"  Your portfolio summary: {tool_results['portfolio_summary']}\n"
            if tool_results.get('investment_recommendations'):
                response += f"  Recommendations: {tool_results['investment_recommendations']}\n"
        elif "account_inquiry" in plan_output["intent"]:
            response += f"Account Information:\n"
            if tool_results.get('balance'):
                response += f"  Current Balance: ${tool_results['balance']:.2f}\n"
            if tool_results.get('transactions'):
                response += f"  Recent Transactions: {', '.join(tool_results['transactions'])}\n"
        else:
            response += f"General Information: {tool_results.get('general_info', 'I can help with fraud, investments, or account inquiries.')}\n"

        if verification_status:
            response += f"\n(Verification: {verification_status})"
        if memory_info:
            response += f"\n(Context from your past interactions: {memory_info})"
        
        self.thoughts = []
        return response

class TransactionHistory:
    def __init__(self, user_id):
        self.user_id = user_id
        self.transactions = [
            {"id": "T001", "amount": 50.00, "type": "debit", "merchant": "Coffee Shop", "timestamp": "2023-10-26 09:30"},
            {"id": "T002", "amount": 1200.00, "type": "credit", "merchant": "Salary Deposit", "timestamp": "2023-10-25 15:00"},
            {"id": "T003", "amount": 75.00, "type": "debit", "merchant": "Grocery Store", "timestamp": "2023-10-24 18:45"},
            {"id": "T004", "amount": 5000.00, "type": "debit", "merchant": "Intl. Online Store", "timestamp": "2023-10-26 11:00", "suspicious": True},
            {"id": "T005", "amount": 25.00, "type": "debit", "merchant": "Streaming Service", "timestamp": "2023-10-26 10:15"},
        ]
        self.account_balance = 15000.00
        self.portfolio = {"stocks": {"AAPL": 10, "GOOG": 5}, "bonds": 2000}

    def get_recent_transactions(self, count=5):
        return [t for t in self.transactions if not t.get("is_hidden")][:count]

    def get_balance(self):
        return self.account_balance

    def get_portfolio_summary(self):
        return f"Stocks: {self.portfolio['stocks']}, Bonds: ${self.portfolio['bonds']}"

    def add_transaction(self, transaction_data):
        self.transactions.insert(0, transaction_data)
        if transaction_data["type"] == "debit":
            self.account_balance -= transaction_data["amount"]
        else:
            self.account_balance += transaction_data["amount"]

class FinancialRegulationsDB:
    def __init__(self):
        self.rules = {
            "fraud_threshold_large_intl": "Transactions over $1000 from international online stores are high risk.",
            "investment_diversification": "Recommend diversification across asset classes (stocks, bonds, real estate).",
            "KYC_requirements": "Know Your Customer (KYC) checks are mandatory for new accounts and large transactions."
        }

    def retrieve_regulation(self, query):
        query_lower = query.lower()
        if "fraud" in query_lower and "international" in query_lower:
            return self.rules["fraud_threshold_large_intl"]
        elif "investment" in query_lower and "diversification" in query_lower:
            return self.rules["investment_diversification"]
        return "No specific regulation found for this query."

class FraudDetectionTool:
    def __init__(self, transaction_history):
        self.transaction_history = transaction_history
        self.known_fraud_patterns = [
            {"merchant_contains": "Intl. Online Store", "min_amount": 1000, "threshold": 0.8},
            {"amount_spike_factor": 5, "time_window_minutes": 60, "threshold": 0.9}
        ]

    def detect_fraud(self, user_id):
        print(f"  [Tool] Running fraud detection for user {user_id}...")
        time.sleep(0.1)
        recent_txns = self.transaction_history.get_recent_transactions(10)
        suspicious_txns = []

        for txn in recent_txns:
            if txn.get("suspicious"):
                suspicious_txns.append(txn)
                continue

            for pattern in self.known_fraud_patterns:
                is_suspicious = False
                if "merchant_contains" in pattern and pattern["merchant_contains"] in txn.get("merchant", "") and txn["amount"] >= pattern["min_amount"]:
                    is_suspicious = True

                if is_suspicious:
                    suspicious_txns.append(txn)
                    break
        
        if suspicious_txns:
            return {"status": "ALERT", "details": f"Found {len(suspicious_txns)} potentially fraudulent transactions: " + ", ".join([f"ID:{t['id']} ({t['amount']})" for t in suspicious_txns])}
        return {"status": "CLEAN", "details": "No immediate fraud detected."}

class InvestmentAnalysisTool:
    def __init__(self, transaction_history):
        self.transaction_history = transaction_history

    def analyze_portfolio(self, user_id):
        print(f"  [Tool] Analyzing investment portfolio for user {user_id}...")
        time.sleep(0.1)
        portfolio = self.transaction_history.get_portfolio_summary()
        recommendations = "Consider diversifying into real estate or fixed-income assets to balance risk. Monitor tech stock performance."
        return {"portfolio_summary": portfolio, "investment_recommendations": recommendations}

class AccountAccessTool:
    def __init__(self, transaction_history):
        self.transaction_history = transaction_history

    def get_account_data(self, user_id):
        print(f"  [Tool] Accessing account data for user {user_id}...")
        time.sleep(0.1)
        balance = self.transaction_history.get_balance()
        transactions = [f"{t['merchant']} - ${t['amount']}" for t in self.transaction_history.get_recent_transactions(3)]
        return {"balance": balance, "transactions": transactions}

class FinancialAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.llm_core = LLMCore()
        self.transaction_history = TransactionHistory(user_id)
        self.regulations_db = FinancialRegulationsDB()
        self.fraud_tool = FraudDetectionTool(self.transaction_history)
        self.investment_tool = InvestmentAnalysisTool(self.transaction_history)
        self.account_tool = AccountAccessTool(self.transaction_history)
        self.available_tools = {
            "fraud_detection": self.fraud_tool.detect_fraud,
            "investment_analysis": self.investment_tool.analyze_portfolio,
            "account_access": self.account_tool.get_account_data
        }
        self.long_term_memory = {}
        print(f"FinancialAgent initialized for User ID: {user_id}")

    def process_request(self, query):
        print(f"\n[Agent] Processing request: '{query}'")
        
        memory_snapshot = self.transaction_history.get_recent_transactions(1)
        llm_decision = self.llm_core.reason(query, self.user_id, memory_snapshot, self.available_tools)
        
        tool_results = {}
        verification_status = "Not explicitly verified."

        if "fraud_detection" in llm_decision["plan"]:
            fraud_result = self.available_tools["fraud_detection"](self.user_id)
            tool_results["fraud_status"] = fraud_result["status"]
            tool_results["fraud_details"] = fraud_result["details"]
            
            regulation_info = self.regulations_db.retrieve_regulation(query)
            tool_results["fraud_recommendation"] = f"Action: Investigate these transactions. {regulation_info}"

            if fraud_result["status"] == "ALERT":
                verification_status = "Fraud alert verified against internal patterns and regulations."
                self.llm_core.thoughts.append("VERIFIED: Fraud alert is consistent with known patterns and regulations.")

        elif "investment_advice" in llm_decision["plan"]:
            investment_result = self.available_tools["investment_analysis"](self.user_id)
            tool_results.update(investment_result)
            regulation_info = self.regulations_db.retrieve_regulation("investment diversification")
            tool_results["investment_recommendations"] += f" (Note: {regulation_info})"
            verification_status = "Investment advice grounded in user portfolio and general market principles."
            self.llm_core.thoughts.append("VERIFIED: Investment advice is grounded in user data and diversification principles.")

        elif "account_inquiry" in llm_decision["plan"]:
            account_data = self.available_tools["account_access"](self.user_id)
            tool_results.update(account_data)
            verification_status = "Account data retrieved directly from system."
            self.llm_core.thoughts.append("VERIFIED: Account data is accurate as per system records.")

        else:
            tool_results["general_info"] = "I am designed to assist with fraud, investment, and account-related queries."
            verification_status = "General information provided."

        self.long_term_memory[time.time()] = {"query": query, "intent": llm_decision["intent"], "outcome": tool_results.get("fraud_status", "N/A")}

        response = self.llm_core.generate_response(llm_decision, tool_results, self.transaction_history.get_recent_transactions(1), verification_status)
        
        response += "\n\n--- Agent's Internal Thoughts ---\n" + "\n".join(self.llm_core.thoughts)
        return response

print("--- Banking Agent: Fraud Detection & Financial Advisor ---")
bank_agent = FinancialAgent(user_id="U456")

print(bank_agent.process_request("I see a suspicious large international transaction. Can you check for fraud?"))
time.sleep(0.5)

print(bank_agent.process_request("I'd like some advice on my investment portfolio."))
time.sleep(0.5)

print(bank_agent.process_request("What's my current account balance and recent transactions?"))
time.sleep(0.5)

print(bank_agent.process_request("What are your operating hours?"))