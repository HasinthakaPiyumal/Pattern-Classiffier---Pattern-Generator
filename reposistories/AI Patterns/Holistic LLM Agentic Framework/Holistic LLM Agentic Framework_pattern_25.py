import datetime

class SimulatedLLM:
    def process_query(self, query, context=None):
        if "investment advice" in query.lower():
            return f"REASONING: Analyzing risk profile, market trends, and client goals. Considering diversified portfolio with focus on long-term growth. Context: {context}"
        elif "calculate ROI" in query.lower():
            return "ACTION:CALCULATE_ROI(investment_amount=10000, expected_return=0.07, years=5)"
        elif "propose investment" in query.lower():
            return "ACTION:PROPOSE_INVESTMENT(client_id='C201', type='stocks', amount=5000)"
        elif "check compliance" in query.lower():
            return "ACTION:CHECK_COMPLIANCE(investment_type='stocks', client_risk_level='medium')"
        elif "financial goals" in query.lower():
            return "QUERY:RETRIEVE_CLIENT_GOALS(client_id='C201')"
        return f"I cannot process that request: '{query}'."

class KnowledgeGraph:
    def __init__(self):
        self._graph = {
            "stocks": {"risk": "high", "return_potential": "high", "liquidity": "medium"},
            "bonds": {"risk": "low", "return_potential": "low", "liquidity": "high"},
            "mutual_funds": {"risk": "medium", "return_potential": "medium", "liquidity": "medium"},
            "client_risk_levels": {"low": ["bonds", "mutual_funds"], "medium": ["mutual_funds", "stocks"], "high": ["stocks"]},
            "regulation_A": "All investments must align with client's declared risk profile."
        }

    def query_node(self, node_id):
        return self._graph.get(node_id, "Node not found.")

    def query_path(self, start_node, end_node):
        # Simplified path query
        if start_node in self._graph and end_node in self._graph:
            return f"Path from {start_node} to {end_node} exists. e.g., {start_node} -> characteristics -> {end_node}"
        return "No direct path found."

class RegulationsDatabase:
    def __init__(self):
        self._regulations = {
            "investment_suitability": "All investment recommendations must be suitable for the client's financial situation and risk tolerance.",
            "disclosure_requirements": "Clients must be fully informed of all fees and risks."
        }

    def get_regulation(self, rule_id):
        return self._regulations.get(rule_id, "Regulation not found.")

class ClientPortfolioMemory:
    def __init__(self, client_id):
        self.client_id = client_id
        self.working_memory = {}
        self.episodic_memory = [] # Past advice, transactions
        self.semantic_memory = {
            'C201': {
                'name': 'Jane Smith',
                'risk_level': 'medium',
                'goals': ['retirement', 'house_downpayment'],
                'current_investments': {'stocks': 15000, 'bonds': 10000}
            }
        }

    def update_portfolio(self, investment_type, amount):
        current = self.semantic_memory[self.client_id]['current_investments'].get(investment_type, 0)
        self.semantic_memory[self.client_id]['current_investments'][investment_type] = current + amount
        self.add_episodic_event(f"Updated portfolio: added {amount} to {investment_type}.")

    def add_episodic_event(self, event):
        self.episodic_memory.append(f"{datetime.datetime.now()}: {event}")

    def get_client_data(self):
        return self.semantic_memory.get(self.client_id, {})

class ComplianceAgent:
    def __init__(self, kg, regulations_db):
        self.kg = kg
        self.regulations_db = regulations_db

    def check_suitability(self, investment_type, client_risk_level):
        allowed_investments = self.kg.query_node("client_risk_levels").get(client_risk_level, [])
        is_suitable = investment_type in allowed_investments
        regulation_text = self.regulations_db.get_regulation("investment_suitability")
        print(f"COMPLIANCE_AGENT: Checking suitability for {investment_type} (risk: {client_risk_level}). Suitable: {is_suitable}. Regulation: '{regulation_text}'\n")
        return is_suitable, regulation_text

class FinancialAdvisorAgent:
    def __init__(self, client_id):
        self.llm = SimulatedLLM()
        self.kg = KnowledgeGraph()
        self.regulations_db = RegulationsDatabase()
        self.memory = ClientPortfolioMemory(client_id)
        self.client_id = client_id
        self.compliance_agent = ComplianceAgent(self.kg, self.regulations_db)

    def _calculate_roi(self, investment_amount, expected_return, years):
        roi = investment_amount * ((1 + expected_return) ** years - 1)
        print(f"TOOL_EXEC: Calculated ROI for ${investment_amount} over {years} years at {expected_return*100}% return: ${roi:.2f}\n")
        return f"The estimated ROI is ${roi:.2f}."

    def _propose_investment(self, client_id, type, amount):
        client_data = self.memory.get_client_data()
        is_suitable, _ = self.compliance_agent.check_suitability(type, client_data['risk_level'])
        if not is_suitable:
            return f"Investment of type '{type}' is not suitable for client {client_id} with a '{client_data['risk_level']}' risk level. Compliance check failed."

        self.memory.update_portfolio(type, amount)
        print(f"TOOL_EXEC: Proposed investment of ${amount} in {type} for client {client_id}.\n")
        return f"Investment of ${amount} in {type} proposed and recorded for client {client_id}."

    def _check_compliance(self, investment_type, client_risk_level):
        is_suitable, regulation = self.compliance_agent.check_suitability(investment_type, client_risk_level)
        return f"Compliance check for {investment_type} with {client_risk_level} risk: {'Passed' if is_suitable else 'Failed'}. Regulation: {regulation}"

    def _retrieve_client_goals(self, client_id):
        client_data = self.memory.get_client_data()
        print(f"TOOL_EXEC: Retrieving client goals for {client_id}. Goals: {client_data.get('goals')}\n")
        return client_data.get('goals', [])

    def _verify_advice_against_regulations(self, advice, client_data):
        # Simulate verification of advice against rules and client profile
        if "diversified portfolio" in advice.lower() and client_data['risk_level'] == 'medium':
            return True, "Advice aligns with medium risk diversified strategy."
        return False, "Advice needs further regulatory review."

    def run(self, user_query):
        print(f"USER: {user_query}")
        client_data = self.memory.get_client_data()
        context = f"Client ID: {self.client_id}, Profile: {client_data}, KG Info: {self.kg.query_node('stocks')}"
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
                    if v.replace('.', '', 1).isdigit(): 
                        params[k] = float(v) if '.' in v else int(v)

                if action_name == "CALCULATE_ROI":
                    tool_output = self._calculate_roi(**params)
                elif action_name == "PROPOSE_INVESTMENT":
                    tool_output = self._propose_investment(**params)
                elif action_name == "CHECK_COMPLIANCE":
                    tool_output = self._check_compliance(**params)
                else:
                    tool_output = "Unknown action."
                print(f"AGENT_RESPONSE: {tool_output}")
                self.memory.add_episodic_event(f"Agent executed {action_name} with result: {tool_output}")
            except Exception as e:
                print(f"TOOL_ERROR: Failed to execute action {action_str}. Error: {e}")
                print("AGENT_RESPONSE: I encountered an error while trying to perform that action.")
        elif llm_response.startswith("REASONING:"):
            reasoning = llm_response[len("REASONING:"):].split('Context:')[0].strip()
            is_verified, verification_msg = self._verify_advice_against_regulations(reasoning, client_data)
            print(f"AGENT_THOUGHT: {reasoning} -- Verification: {verification_msg}\n")
            print(f"AGENT_RESPONSE: {reasoning} {verification_msg}")
            self.memory.add_episodic_event(f"Agent reasoned: {reasoning} and verified: {verification_msg}")
        elif llm_response.startswith("QUERY:"):
            query_str = llm_response[len("QUERY:"):]
            if query_str.startswith("RETRIEVE_CLIENT_GOALS"):
                client_id = query_str.split("(")[1].split("=")[1].strip("')")
                goals = self._retrieve_client_goals(client_id)
                print(f"AGENT_RESPONSE: Client {client_id}'s financial goals are: {', '.join(goals)}")
                self.memory.add_episodic_event(f"Retrieved goals for {client_id}: {goals}")
        else:
            print(f"AGENT_RESPONSE: {llm_response}")
        print("\n" + "-" * 50 + "\n")

# Real-world usage simulation: Financial Advisor Agent with compliance checks
financial_agent = FinancialAdvisorAgent(client_id='C201')
financial_agent.run("I need some investment advice for my retirement plan.")
financial_agent.run("Calculate the ROI for an investment of $10,000 with a 7% annual return over 5 years.")
financial_agent.run("I want to invest $5,000 in stocks. Can you propose this investment?")
financial_agent.run("What are my current financial goals?")