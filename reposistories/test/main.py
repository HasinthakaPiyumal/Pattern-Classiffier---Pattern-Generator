class AgentMemory:
    def __init__(self):
        self.working_memory = {"current_task": None, "intermediate_steps": []}
        self.episodic_memory = []

    def add_step(self, thought: str, action: str, action_input: dict, observation: str):
        step = {
            "thought": thought,
            "action": action,
            "action_input": action_input,
            "observation": observation
        }
        self.working_memory["intermediate_steps"].append(step)
        self.episodic_memory.append(step)
        print(f"🧠 Memory Updated: Added step for action '{action}'.")

    def get_context(self) -> str:
        return json.dumps(self.working_memory, indent=2)

    def clear_working_memory(self):
        self.working_memory = {"current_task": None, "intermediate_steps": []}


class ToolRegistry:
    def __init__(self):
        self.tools = {
            "get_current_time": self.get_current_time,
            "calculator": self.calculator,
        }
        print(f"🔧 Tools Registered: {list(self.tools.keys())}")

    def get_tool_names(self) -> list[str]:
        return list(self.tools.keys())

    def use_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name in self.tools:
            try:
                result = self.tools[tool_name](**tool_input)
                return f"Tool '{tool_name}' returned: {result}"
            except Exception as e:
                return f"Error using tool '{tool_name}': {e}"
        else:
            return f"Error: Tool '{tool_name}' not found."

    def get_current_time(self, timezone: str) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calculator(self, expression: str) -> str:
        return str(eval(expression, {"__builtins__": {}}, {}))


class HolisticAgent:
    def __init__(self, llm_client, memory, tool_registry):
        self.llm = llm_client
        self.memory = memory
        self.tools = tool_registry
        self.max_steps = 5

    def run(self, user_query: str):
        self.memory.clear_working_memory()
        self.memory.working_memory["current_task"] = user_query

        for i in range(self.max_steps):
            print(f"\n--- STEP {i+1} ---")
            prompt = self._build_prompt(user_query)

            response_str = self.llm.query(prompt)
            try:
                response_json = json.loads(response_str)
            except json.JSONDecodeError:
                print("Error: LLM returned invalid JSON. Stopping.")
                break

            thought = response_json.get("thought", "")
            action = response_json.get("action", "Final Answer")
            action_input = response_json.get("action_input", "")

            if action == "Final Answer":
                print(f"\n✅ Final Answer: {action_input}")
                break
            
            print(f"🤖 Action: Using tool '{action}' with input '{action_input}'")
            observation = self.tools.use_tool(action, action_input)
            print(f"👀 Observation: {observation}")
            
            self.memory.add_step(thought, action, action_input, observation)
        else:
            print("\n⚠️ Agent stopped: Reached maximum steps.")
            
    def _build_prompt(self, query: str) -> str:
        return f"""
        You are an intelligent agent. Your goal is to solve the user's request by reasoning and using the available tools.
        Follow the Thought-Action-Observation loop (ReAct pattern).

        Available Tools: {self.tools.get_tool_names()}

        User Query: {query}
        
        Previous Steps (Memory):
        {self.memory.get_context()}

        Your response MUST be a JSON object with 'thought', 'action', and 'action_input'.
        'action' should be one of the available tools or 'Final Answer'.
        """


if __name__ == "__main__":
    llm_client = MockLLMClient()
    agent_memory = AgentMemory()
    tool_registry = ToolRegistry()
    
    agent = HolisticAgent(
        llm_client=llm_client,
        memory=agent_memory,
        tool_registry=tool_registry
    )

    agent.run("What is the of Sri Lanka, what is the current time in Colombo, hi and what is 25 * 8?")
