import json
import time

class MockLLM:
    def __init__(self, name="MedGPT"):
        self.name = name

    def generate(self, prompt, context="", tools_available=None):
        print(f"[{self.name} - Generating]: {prompt[:100]}...")
        if "diagnose" in prompt.lower():
            if "fever" in prompt.lower() and "cough" in prompt.lower():
                return "Based on symptoms: common cold. Consider tests for flu if symptoms worsen."
            elif "chest pain" in prompt.lower() and "shortness of breath" in prompt.lower():
                return "Potential cardiac issue. Recommend immediate ECG and blood tests."
            else:
                return "Further information needed for diagnosis. Suggest detailed symptom logging."
        elif "tool_use_plan" in prompt.lower():
            return self._plan_tool_use(prompt, tools_available)
        elif "clarify" in prompt.lower():
            return "Could you provide more details on the duration and severity of the symptoms?"
        elif "recommend treatment" in prompt.lower():
            return "For common cold: rest, fluids, OTC pain relievers. For cardiac: consult specialist, prescribed medications."
        return "Understood. How can I assist further?"

    def _plan_tool_use(self, prompt, tools_available):
        if "order lab" in prompt.lower() and "blood test" in prompt.lower():
            return {"action": "call_tool", "tool_name": "LabOrderSystem", "parameters": {"test_type": "blood_panel", "patient_id": "P123"}}
        if "check drug interaction" in prompt.lower() and "aspirin" in prompt.lower() and "warfarin" in prompt.lower():
            return {"action": "call_tool", "tool_name": "DrugInteractionChecker", "parameters": {"drugs": ["aspirin", "warfarin"]}}
        if "schedule appointment" in prompt.lower() and "cardiology" in prompt.lower():
            return {"action": "call_tool", "tool_name": "AppointmentScheduler", "parameters": {"specialty": "cardiology", "patient_id": "P123"}}
        return {"action": "respond", "response": "No specific tool action planned based on this request."}

    def verify_reasoning(self, statement, context):
        if "common cold" in statement and "fever" in context:
            return True, "Verified against common symptom-disease associations."
        if "cardiac issue" in statement and "chest pain" in context:
            return True, "Strong correlation with reported symptoms."
        return False, "Insufficient information for robust verification."

class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []
        self.semantic_memory = {
            "common_cold_symptoms": ["fever", "cough", "sore throat", "runny nose"],
            "cardiac_symptoms": ["chest pain", "shortness of breath", "palpitations"],
            "drug_interactions": {"aspirin": {"warfarin": "high bleeding risk"}},
            "patient_data": {"P123": {"name": "Alice Smith", "age": 45, "conditions": ["hypertension"], "medications": ["amlodipine"]}}
        }
        self.procedural_memory = {
            "diagnosis_flow": "1. Collect symptoms. 2. Query semantic memory. 3. Propose differential diagnosis. 4. Recommend tests. 5. Propose treatment.",
            "cardiac_emergency_protocol": "1. ECG. 2. Troponin test. 3. Consult cardiologist."
        }

    def retrieve(self, query_type, key=None, context=""):
        if query_type == "semantic":
            if "common cold" in key or "symptoms" in context:
                return self.semantic_memory.get("common_cold_symptoms", [])
            if "cardiac" in key or "chest pain" in context:
                return self.semantic_memory.get("cardiac_symptoms", [])
            if "drug interaction" in key:
                return self.semantic_memory.get("drug_interactions", {})
            if "patient_data" in key and key.split(":")[1] in self.semantic_memory["patient_data"]:
                return self.semantic_memory["patient_data"][key.split(":")[1]]
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
            self.semantic_memory[key] = value
        print(f"Stored in {memory_type} memory: {key} = {value}")

class LabOrderSystem:
    def order_test(self, test_type, patient_id):
        print(f"--- TOOL: LabOrderSystem - Ordering {test_type} for {patient_id} ---")
        time.sleep(1)
        if test_type == "blood_panel":
            return {"status": "success", "order_id": "LAB001", "results_expected": "24 hours"}
        return {"status": "failed", "message": "Unknown test type."}

class DrugInteractionChecker:
    def check_interactions(self, drugs):
        print(f"--- TOOL: DrugInteractionChecker - Checking interactions for {drugs} ---")
        time.sleep(0.5)
        if "aspirin" in drugs and "warfarin" in drugs:
            return {"status": "warning", "interaction": "High bleeding risk", "severity": "severe"}
        return {"status": "no_significant_interaction"}

class AppointmentScheduler:
    def schedule(self, specialty, patient_id):
        print(f"--- TOOL: AppointmentScheduler - Scheduling {specialty} for {patient_id} ---")
        time.sleep(1.5)
        return {"status": "success", "appointment_id": "APP001", "date": "2023-10-26", "time": "10:00 AM"}

class MedicalAgent:
    def __init__(self):
        self.llm = MockLLM()
        self.memory = MemorySystem()
        self.tools = {
            "LabOrderSystem": LabOrderSystem(),
            "DrugInteractionChecker": DrugInteractionChecker(),
            "AppointmentScheduler": AppointmentScheduler()
        }
        self.human_in_the_loop_approval = True

    def _execute_tool_action(self, action):
        tool_name = action["tool_name"]
        parameters = action["parameters"]
        tool_instance = self.tools.get(tool_name)
        if not tool_instance:
            return {"status": "error", "message": f"Tool '{tool_name}' not found."}

        method_name = None
        if tool_name == "LabOrderSystem":
            method_name = "order_test"
        elif tool_name == "DrugInteractionChecker":
            method_name = "check_interactions"
        elif tool_name == "AppointmentScheduler":
            method_name = "schedule"

        if method_name and hasattr(tool_instance, method_name):
            try:
                result = getattr(tool_instance, method_name)(**parameters)
                return {"status": "success", "tool_result": result}
            except Exception as e:
                return {"status": "error", "message": f"Tool execution failed: {e}"}
        return {"status": "error", "message": f"Tool '{tool_name}' has no '{method_name}' method."}

    def process_request(self, user_query, patient_id="P123"):
        self.memory.store("working", "current_user_query", user_query)
        self.memory.store("working", "current_patient_id", patient_id)

        print(f"\n[Agent]: Processing request: '{user_query}' for patient {patient_id}")

        llm_response = self.llm.generate(f"Clarify intent for: {user_query}")
        if "more details" in llm_response.lower():
            print(f"[Agent]: {llm_response}")
            user_query += " Patient reports fever for 3 days, persistent cough, and mild sore throat."
            self.memory.store("working", "current_user_query", user_query)
            print("[Agent]: (Simulated user clarification provided.)")

        patient_data = self.memory.retrieve("semantic", f"patient_data:{patient_id}")
        context = f"Patient history: {patient_data}. Current symptoms: {user_query}. "
        llm_plan_prompt = f"Given patient data and symptoms, generate a diagnosis, suggest necessary tests, and outline a treatment plan. Also, consider if any tools are needed. Context: {context}"
        
        reasoning_output = self.llm.generate(llm_plan_prompt, context=context, tools_available=list(self.tools.keys()))
        self.memory.store("working", "llm_reasoning_output", reasoning_output)
        print(f"[Agent]: LLM's initial reasoning: {reasoning_output}")

        relevant_symptoms = self.memory.retrieve("semantic", "common_cold")
        print(f"[Agent]: Retrieved relevant knowledge (RAG): {relevant_symptoms}")
        self.memory.store("working", "retrieved_knowledge", relevant_symptoms)

        tool_planning_prompt = f"Based on the diagnosis and treatment plan: '{reasoning_output}', determine if any tools should be called. If so, provide a JSON action. Context: {context} Available tools: {list(self.tools.keys())}. Prepend with 'tool_use_plan:'"
        tool_action_suggestion = self.llm.generate(tool_planning_prompt, tools_available=list(self.tools.keys()))

        if isinstance(tool_action_suggestion, dict) and tool_action_suggestion.get("action") == "call_tool":
            print(f"[Agent]: LLM suggests tool use: {tool_action_suggestion}")
            if self.human_in_the_loop_approval:
                print("[Agent]: Human approval required for critical action (simulated 'Approved').")
            
            tool_result = self._execute_tool_action(tool_action_suggestion)
            self.memory.store("episodic", "tool_execution_log", {"action": tool_action_suggestion, "result": tool_result})
            print(f"[Agent]: Tool execution result: {tool_result}")
            context += f" Tool result: {tool_result}. "
            final_llm_response = self.llm.generate(f"Integrate tool result into final recommendation: {reasoning_output}. Tool result: {tool_result}", context=context)
        else:
            final_llm_response = reasoning_output

        is_verified, verification_msg = self.llm.verify_reasoning(final_llm_response, context)
        print(f"[Agent]: Verification check: {is_verified} - {verification_msg}")
        if not is_verified:
            print("[Agent]: Self-correction needed. Re-evaluating...")
            final_llm_response = self.llm.generate(f"Refine the following given verification failure: {final_llm_response}. Context: {context}. Focus on factual accuracy.", context=context)

        print(f"\n[Agent]: Final Recommendation for Patient {patient_id}:")
        print(final_llm_response)
        self.memory.store("episodic", "final_recommendation", final_llm_response)

        return final_llm_response

def simulate_medical_agent_usage():
    print("--- Simulating Medical Agent in Healthcare ---")
    agent = MedicalAgent()

    agent.process_request("I have a fever and cough, what could it be?")

    agent.process_request("I'm experiencing chest pain and shortness of breath. What should I do?")

    agent.process_request("Can I take aspirin with warfarin?")

    agent.process_request("I need to see a cardiologist for my heart condition.")

simulate_medical_agent_usage()