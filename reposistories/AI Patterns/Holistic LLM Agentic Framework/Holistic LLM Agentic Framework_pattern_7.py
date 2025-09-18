import json
import time
import random

class MockLLM:
    def __init__(self, name="FinAdvisorGPT"):
        self.name = name

    def generate(self, prompt, context="", tools_available=None):
        print(f"[{self.name} - Generating]: {prompt[:100]}...")
        if "investment advice" in prompt.lower():
            if "low risk" in prompt.lower() and "long term" in prompt.lower():
                return "For low-risk, long-term investment, consider diversified index funds or government bonds. Context: 'low risk', 'long term'."
            elif "high growth" in prompt.lower() and "tech stocks" in prompt.lower():
                return "For high growth, consider tech sector ETFs or individual blue-chip tech stocks. Note higher risk. Context: 'high growth', 'tech stocks'."
            return "General investment advice: diversify, understand risk tolerance."
        elif "tool_use_plan" in prompt.lower():
            return self._plan_tool_use(prompt, tools_available)
        elif "clarify" in prompt.lower():
            return "Could you specify your financial goals, risk tolerance (low, medium, high), and investment horizon (short, medium, long term)?"
        elif "explain" in prompt.lower():
            return "An index fund tracks a market index, offering diversification and typically lower fees."
        return "Understood. How can I assist with your financial planning today?"

    def _plan_tool_use(self, prompt, tools_available):
        if "get stock price" in prompt.lower() and "apple" in prompt.lower():
            return {"action": "call_tool", "tool_name": "StockMarketAPI", "parameters": {"ticker": "AAPL"}}
        if "assess risk" in prompt.lower() and "portfolio" in prompt.lower():
            return {"action": "call_tool", "tool_name": "RiskAssessor", "parameters": {"user_id": "U001"}}
        if "optimize portfolio" in prompt.lower() and "goal" in prompt.lower():
            goal = prompt.split("goal:")[1].split(" ")[0].strip()
            return {"action": "call_tool", "tool_name": "PortfolioOptimizer", "parameters": {"user_id": "U001", "goal": goal}}
        return {"action": "respond", "response": "No specific tool action planned based on this request."}

    def verify_compliance(self, advice, user_profile, regulatory_rules):
        if "high risk" in advice.lower() and user_profile.get("risk_tolerance") == "low":
            return False, "Advice contradicts user's low risk tolerance."
        if "unregistered investment" in advice.lower() and "SEC regulations" in regulatory_rules:
            return False, "Advice violates SEC regulations."
        return True, "Advice seems compliant and aligned with profile."

class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []
        self.semantic_memory = {
            "market_data": {
                "AAPL": {"price": 175.25, "sector": "Technology", "P/E": 28.5},
                "SPY": {"price": 430.10, "sector": "ETF", "type": "Index Fund"},
            },
            "user_profiles": {
                "U001": {"name": "Charlie Brown", "risk_tolerance": "medium", "investment_horizon": "long term", "goals": ["retirement", "house_downpayment"], "current_portfolio": {"AAPL": 10, "SPY": 20}},
                "U002": {"name": "Lucy Van Pelt", "risk_tolerance": "low", "investment_horizon": "short term", "goals": ["emergency_fund"], "current_portfolio": {}},
            },
            "investment_strategies": {
                "low_risk_long_term": "Diversified index funds, government bonds.",
                "high_growth_medium_risk": "Tech ETFs, growth stocks.",
            },
            "regulatory_rules": ["SEC regulations for registered investments", "KYC compliance", "anti-money laundering"]
        }
        self.procedural_memory = {
            "investment_advisory_flow": "1. Understand goals & risk. 2. Retrieve market data & strategies. 3. Generate advice. 4. Verify compliance.",
            "portfolio_optimization_flow": "1. Assess current portfolio. 2. Define goals. 3. Use PortfolioOptimizer tool. 4. Present optimized plan."
        }

    def retrieve(self, query_type, key=None, context=""):
        if query_type == "semantic":
            if key and key.startswith("user:"):
                return self.semantic_memory["user_profiles"].get(key.split(":")[1])
            if key and key.startswith("market:"):
                return self.semantic_memory["market_data"].get(key.split(":")[1])
            if key == "regulatory_rules":
                return self.semantic_memory["regulatory_rules"]
            if "low risk" in context.lower() and "long term" in context.lower():
                return self.semantic_memory["investment_strategies"]["low_risk_long_term"]
            if "high growth" in context.lower():
                return self.semantic_memory["investment_strategies"]["high_growth_medium_risk"]
            return "No specific semantic knowledge found."
        elif query_type == "episodic":
            return [e for e in self.episodic_memory if key in str(e)] if key else self.episodic_memory
        elif query_type == "procedural":
            return self.procedural_memory.get(key, "No specific procedure found.")
        elif query_type == "working":
            return self.working_memory.get(key)
        return "Invalid memory query type."

    def store(self, memory_type, key, value):
        if memory_type == "working":
            self.working_memory[key] = value
        elif memory_type == "episodic":
            self.episodic_memory.append({key: value, "timestamp": time.time()})
        elif memory_type == "semantic":
            if key.startswith("user_profile_update:"):
                user_id = key.split(":")[1]
                self.semantic_memory["user_profiles"].setdefault(user_id, {}).update(value)
            else:
                self.semantic_memory[key] = value
        print(f"Stored in {memory_type} memory: {key} = {value}")

class StockMarketAPI:
    def get_price(self, ticker):
        print(f"--- TOOL: StockMarketAPI - Getting price for {ticker} ---")
        time.sleep(0.5)
        mock_prices = {"AAPL": 175.25, "GOOG": 135.80, "MSFT": 330.15, "SPY": 430.10}
        return {"status": "success", "ticker": ticker, "price": mock_prices.get(ticker, "N/A")}

class RiskAssessor:
    def assess_portfolio_risk(self, user_id):
        print(f"--- TOOL: RiskAssessor - Assessing portfolio risk for {user_id} ---")
        time.sleep(1)
        user_profile = MemorySystem().retrieve("semantic", f"user:{user_id}")
        portfolio = user_profile.get("current_portfolio", {})
        if "AAPL" in portfolio and "SPY" in portfolio:
            return {"status": "success", "user_id": user_id, "risk_level": "medium", "diversification_score": 0.75}
        elif "AAPL" in portfolio and len(portfolio) == 1:
            return {"status": "success", "user_id": user_id, "risk_level": "high", "diversification_score": 0.2}
        return {"status": "success", "user_id": user_id, "risk_level": "low", "diversification_score": 0.9}

class PortfolioOptimizer:
    def optimize(self, user_id, goal):
        print(f"--- TOOL: PortfolioOptimizer - Optimizing portfolio for {user_id} towards goal: {goal} ---")
        time.sleep(1.5)
        user_profile = MemorySystem().retrieve("semantic", f"user:{user_id}")
        if goal == "retirement" and user_profile.get("risk_tolerance") == "medium":
            return {"status": "success", "user_id": user_id, "optimized_plan": "Increase SPY holdings, add some bonds, maintain AAPL.", "projected_return": "8% annually"}
        return {"status": "success", "user_id": user_id, "optimized_plan": "Adjust portfolio based on generic diversification principles.", "projected_return": "5% annually"}

class FinancialAdvisorAgent:
    def __init__(self):
        self.llm = MockLLM()
        self.memory = MemorySystem()
        self.tools = {
            "StockMarketAPI": StockMarketAPI(),
            "RiskAssessor": RiskAssessor(),
            "PortfolioOptimizer": PortfolioOptimizer()
        }
        self.user_id = "U001"

    def _execute_tool_action(self, action):
        tool_name = action["tool_name"]
        parameters = action["parameters"]
        tool_instance = self.tools.get(tool_name)
        if not tool_instance:
            return {"status": "error", "message": f"Tool '{tool_name}' not found."}

        method_name = None
        if tool_name == "StockMarketAPI":
            method_name = "get_price"
        elif tool_name == "RiskAssessor":
            method_name = "assess_portfolio_risk"
        elif tool_name == "PortfolioOptimizer":
            method_name = "optimize"

        if method_name and hasattr(tool_instance, method_name):
            try:
                result = getattr(tool_instance, method_name)(**parameters)
                return {"status": "success", "tool_result": result}
            except Exception as e:
                return {"status": "error", "message": f"Tool execution failed: {e}"}
        return {"status": "error", "message": f"Tool '{tool_name}' has no '{method_name}' method."}

    def process_request(self, user_query):
        self.memory.store("working", "current_user_query", user_query)
        self.memory.store("working", "current_user_id", self.user_id)

        print(f"\n[Agent]: Processing request: '{user_query}' for user {self.user_id}")

        llm_response = self.llm.generate(f"Clarify intent for: {user_query}")
        if "specify your financial goals" in llm_response.lower():
            print(f"[Agent]: {llm_response}")
            user_query += " My goal is retirement, I have a medium risk tolerance and long-term horizon."
            self.memory.store("working", "current_user_query", user_query)
            print("[Agent]: (Simulated user clarification provided.)")
            self.memory.store("semantic", f"user_profile_update:{self.user_id}", {"risk_tolerance": "medium", "investment_horizon": "long term", "goals": ["retirement"]})

        user_profile = self.memory.retrieve("semantic", f"user:{self.user_id}")
        regulatory_rules = self.memory.retrieve("semantic", "regulatory_rules")
        context = f"User profile: {user_profile}. Regulatory rules: {regulatory_rules}. Current query: {user_query}. "
        relevant_strategy = self.memory.retrieve("semantic", key="investment_strategy", context=context)
        print(f"[Agent]: Retrieved relevant knowledge (RAG): {relevant_strategy}")
        self.memory.store("working", "retrieved_strategy", relevant_strategy)

        llm_plan_prompt = f"Given user profile, query, and retrieved strategy, generate investment advice. Suggest tool use if appropriate (e.g., portfolio optimization). Context: {context}"
        reasoning_output = self.llm.generate(llm_plan_prompt, context=context, tools_available=list(self.tools.keys()))
        self.memory.store("working", "llm_reasoning_output", reasoning_output)
        print(f"[Agent]: LLM's initial reasoning: {reasoning_output}")

        tool_planning_prompt = f"Based on the reasoning: '{reasoning_output}', determine if any tools should be called. If so, provide a JSON action. Context: {context} Available tools: {list(self.tools.keys())}. Prepend with 'tool_use_plan:'"
        tool_action_suggestion = self.llm.generate(tool_planning_prompt, tools_available=list(self.tools.keys()))

        final_advice = reasoning_output
        if isinstance(tool_action_suggestion, dict) and tool_action_suggestion.get("action") == "call_tool":
            print(f"[Agent]: LLM suggests tool use: {tool_action_suggestion}")
            tool_result = self._execute_tool_action(tool_action_suggestion)
            self.memory.store("episodic", "tool_execution_log", {"action": tool_action_suggestion, "result": tool_result})
            print(f"[Agent]: Tool execution result: {tool_result}")
            context += f" Tool result: {tool_result}. "
            final_advice = self.llm.generate(f"Integrate tool result into final financial advice: {reasoning_output}. Tool result: {tool_result}", context=context)

        user_profile_for_verification = self.memory.retrieve("semantic", f"user:{self.user_id}")
        is_compliant, compliance_msg = self.llm.verify_compliance(final_advice, user_profile_for_verification, regulatory_rules)
        print(f"[Agent]: Compliance and alignment check: {is_compliant} - {compliance_msg}")
        if not is_compliant:
            print("[Agent]: Self-correction: Refining advice due to compliance/alignment issue.")
            final_advice = self.llm.generate(f"Refine the following advice to ensure compliance and alignment with user profile: {final_advice}. Context: {context}. Compliance issues: {compliance_msg}", context=context)
        
        print(f"\n[Agent]: Final Financial Advice for {user_profile.get('name', 'user')}:")
        print(final_advice)
        self.memory.store("episodic", "final_advice", final_advice)
        return final_advice

def simulate_financial_advisor_usage():
    print("--- Simulating Financial Advisor Agent in Banking/Finance ---")
    agent = FinancialAdvisorAgent()

    agent.process_request("I need investment advice.")

    agent.process_request("What's the current price of Apple stock?")

    agent.process_request("Can you help me optimize my portfolio for retirement?")

    agent.user_id = "U002"
    print(f"\n--- Switching to user U002 (Lucy Van Pelt - low risk) ---")
    agent.process_request("I want to invest in high-growth tech stocks for quick returns.")

simulate_financial_advisor_usage()