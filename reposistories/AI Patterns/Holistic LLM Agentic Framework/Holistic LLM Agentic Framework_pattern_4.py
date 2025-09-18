import random

class SimulatedLLM:
    def __init__(self, name="FinAdvisorLLM"):
        self.name = name
        self.reasoning_trace = []

    def _simulate_reasoning(self, prompt, context):
        self.reasoning_trace.append(f"LLM: Analyzing prompt '{prompt}' with context: {context}")
        if "investment_advice" in context.get("intent", ""):
            return "risk assessment and portfolio diversification"
        elif "budget_planning" in context.get("intent", ""):
            return "income-expense analysis"
        elif "fraud_check" in context.get("intent", ""):
            return "transaction anomaly detection"
        return "general financial guidance"

    def understand_intent_and_orchestrate(self, user_query, current_state):
        self.reasoning_trace = []
        self.reasoning_trace.append(f"LLM: Understanding intent for query: '{user_query}'")
        query_lower = user_query.lower()
        if "invest" in query_lower or "portfolio" in query_lower or "stocks" in query_lower:
            intent = "investment_advice"
            self.reasoning_trace.append("LLM: Intent identified: Investment Advice.")
        elif "budget" in query_lower or "spending" in query_lower or "save money" in query_lower:
            intent = "budget_planning"
            self.reasoning_trace.append("LLM: Intent identified: Budget Planning.")
        elif "suspicious transaction" in query_lower or "fraud" in query_lower:
            intent = "fraud_check"
            self.reasoning_trace.append("LLM: Intent identified: Fraud Check.")
        else:
            intent = "general_financial_inquiry"
            self.reasoning_trace.append("LLM: Intent identified: General Financial Inquiry.")

        context = {"user_query": user_query, "current_state": current_state, "intent": intent}
        reasoning_output = self._simulate_reasoning(user_query, context)
        self.reasoning_trace.append(f"LLM: Core reasoning output: {reasoning_output}")
        return {"intent": intent, "reasoning_output": reasoning_output, "trace": self.reasoning_trace}

    def generate_response(self, context):
        response_template = f"Based on your request ({context.get('intent', 'unknown intent')}): "
        if context["intent"] == "investment_advice":
            advice = context.get("investment_advice", "Consider diverse low-cost index funds.")
            return response_template + f"Here's some investment advice: {advice} Always consult a human advisor for final decisions."
        elif context["intent"] == "budget_planning":
            plan = context.get("budget_plan", "Track your income and expenses for a month to identify saving opportunities.")
            return response_template + f"Here's a budget planning tip: {plan}"
        elif context["intent"] == "fraud_check":
            fraud_status = context.get("fraud_status", "No suspicious activity detected.")
            return response_template + f"Fraud check result: {fraud_status}"
        else:
            return response_template + "How can I assist with your financial needs today?"

class FinancialKnowledgeBase:
    def __init__(self, regulations_data, market_data_feed):
        self.regulations = regulations_data
        self.market_data_feed = market_data_feed

    def retrieve_regulation(self, topic):
        for key, value in self.regulations.items():
            if topic.lower() in key.lower() or topic.lower() in value.lower():
                return f"Regulation on {key}: {value}"
        return "No specific regulation found for this topic."

    def get_market_data(self, asset):
        return self.market_data_feed.get(asset.lower(), "Data not available.")

class ClientPortfolio:
    def __init__(self, client_id):
        self.client_id = client_id
        self.accounts = {
            "checking": 5000,
            "savings": 15000,
            "investments": {"stocks": 10000, "bonds": 5000}
        }
        self.income = 6000
        self.expenses = 3500
        self.risk_profile = "moderate"
        self.transaction_history = []
        self.working_memory = {}

    def get_balance(self, account_type):
        return self.accounts.get(account_type, 0)

    def record_transaction(self, transaction):
        self.transaction_history.append(transaction)
        self.working_memory["last_transaction"] = transaction

    def get_portfolio_summary(self):
        return self.accounts["investments"]

    def get_financial_summary(self):
        return {"income": self.income, "expenses": self.expenses, "risk_profile": self.risk_profile}

class InvestmentAnalysisTool:
    def execute(self, portfolio, market_data):
        print(f"Executing Investment Analysis Tool for client {portfolio.client_id}...")
        summary = portfolio.get_portfolio_summary()
        advice = []
        if summary.get("stocks", 0) < 10000 and portfolio.risk_profile == "moderate":
            advice.append("Consider increasing stock exposure, especially in diversified ETFs.")
        if market_data.get("tech_stocks", 0) > 0.05:
            advice.append("Tech stocks are performing well, but diversify to mitigate risk.")
        return " ".join(advice) if advice else "Your current portfolio seems balanced given your risk profile."

class BudgetPlannerTool:
    def execute(self, client_portfolio):
        print(f"Executing Budget Planner Tool for client {client_portfolio.client_id}...")
        income = client_portfolio.income
        expenses = client_portfolio.expenses
        disposable = income - expenses
        if disposable > 0:
            return f"You have ${disposable} disposable income. Consider allocating 20% to savings, 30% to investments."
        else:
            return "Your expenses exceed your income. Review your spending categories to find areas for reduction."

class FraudMonitorAgent:
    def __init__(self, client_portfolio):
        self.client_portfolio = client_portfolio
        self.rules = {
            "large_transaction_threshold": 2000,
            "international_transaction_alert": True,
            "unusual_location_change": True
        }

    def check_transaction_for_fraud(self, transaction):
        print(f"Fraud Monitor Agent: Checking transaction {transaction['id']} for anomalies...")
        is_fraudulent = False
        reason = []

        if transaction["amount"] > self.rules["large_transaction_threshold"]:
            is_fraudulent = True
            reason.append(f"Transaction amount (${transaction['amount']}) exceeds large transaction threshold.")
        if transaction.get("location") == "international" and self.rules["international_transaction_alert"]:
            is_fraudulent = True
            reason.append("International transaction detected, requires verification.")
        past_transactions = [t for t in self.client_portfolio.transaction_history if t["id"] != transaction["id"]]
        if not past_transactions and transaction["amount"] > 1000:
             is_fraudulent = True
             reason.append("First large transaction on a new account, suspicious.")

        if is_fraudulent:
            return {"is_fraud": True, "reason": ", ".join(reason)}
        return {"is_fraud": False, "reason": "No immediate red flags."}

class FinancialAdvisorAgent:
    def __init__(self, client_id="C001"):
        self.llm = SimulatedLLM()
        self.client_portfolio = ClientPortfolio(client_id)
        self.financial_kb = FinancialKnowledgeBase(
            regulations_data={
                "KYC": "Know Your Customer (KYC) regulations require financial institutions to verify the identity of their clients.",
                "AML": "Anti-Money Laundering (AML) laws combat illegal financial activities."
            },
            market_data_feed={
                "tech_stocks": 0.07,
                "bonds": 0.01,
                "gold": -0.005
            }
        )
        self.investment_tool = InvestmentAnalysisTool()
        self.budget_tool = BudgetPlannerTool()
        self.fraud_monitor_agent = FraudMonitorAgent(self.client_portfolio)
        self.current_state = {}

    def process_query(self, user_query):
        self.client_portfolio.working_memory["last_query"] = user_query

        llm_analysis = self.llm.understand_intent_and_orchestrate(user_query, self.current_state)
        intent = llm_analysis["intent"]
        reasoning_output = llm_analysis["reasoning_output"]
        print("\n--- LLM Orchestration & Reasoning Trace ---")
        for step in llm_analysis["trace"]:
            print(step)
        print("------------------------------------------")

        response_context = {"intent": intent, "reasoning_output": reasoning_output}

        print(f"Memory: Client financial summary: {self.client_portfolio.get_financial_summary()}")
        regulation_info = self.financial_kb.retrieve_regulation(user_query)
        self.client_portfolio.working_memory["retrieved_regulation"] = regulation_info
        response_context["retrieved_regulation"] = regulation_info
        print(f"Memory: Retrieved regulation: {regulation_info}")

        if intent == "investment_advice":
            market_data = {
                "tech_stocks": self.financial_kb.get_market_data("tech_stocks"),
                "bonds": self.financial_kb.get_market_data("bonds")
            }
            investment_advice = self.investment_tool.execute(self.client_portfolio, market_data)
            response_context["investment_advice"] = investment_advice
            print(f"Tool: Investment advice generated.")
            if self.client_portfolio.risk_profile == "conservative" and "increase stock exposure" in investment_advice:
                response_context["investment_advice"] += " (However, given your conservative profile, proceed cautiously and consider lower-risk alternatives.)"
                print("Agent: Adjusted advice for conservative risk profile.")

        elif intent == "budget_planning":
            budget_plan = self.budget_tool.execute(self.client_portfolio)
            response_context["budget_plan"] = budget_plan
            print(f"Tool: Budget plan generated.")

        elif intent == "fraud_check":
            new_transaction = {"id": f"TRN{random.randint(10000, 99999)}", "amount": 2500, "merchant": "Online Store", "location": "international"}
            self.client_portfolio.record_transaction(new_transaction)
            fraud_result = self.fraud_monitor_agent.check_transaction_for_fraud(new_transaction)
            response_context["fraud_status"] = f"Transaction {new_transaction['id']}: {'FRAUDULENT' if fraud_result['is_fraud'] else 'CLEARED'}. Reason: {fraud_result['reason']}"
            print(f"Multi-Agent: Fraud check completed by Fraud Monitor Agent.")
            response_context["explanation"] = f"Fraud check performed using pre-defined rules and analysis of transaction history. {fraud_result['reason']}"

        final_response = self.llm.generate_response(response_context)
        return final_response, self.client_portfolio.working_memory

if __name__ == "__main__":
    advisor_agent = FinancialAdvisorAgent()
    print("Financial Advisor Agent Activated. Type 'exit' to quit.")

    queries = [
        "I want to invest some money, what should I do?",
        "How can I manage my budget better?",
        "Is there any suspicious activity on my account? I made a large international purchase.",
        "What are the regulations for investing?"
    ]

    for query in queries:
        print(f"\n--- User Query: {query} ---")
        response, state = advisor_agent.process_query(query)
        print(f"\nAgent Response: {response}")
        print(f"Current Agent State (Working Memory): {state}")
