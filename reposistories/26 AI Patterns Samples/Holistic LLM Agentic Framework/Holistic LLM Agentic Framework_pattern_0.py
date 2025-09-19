import random
import time

class LLM:
    def process_query(self, prompt, context=None):
        if "clarify" in prompt.lower():
            return "Please provide more details about your symptoms or medical history."
        if "diagnose" in prompt.lower():
            return "Based on the information, it seems like you might have a common cold or flu. For a precise diagnosis, consult a doctor."
        if "recommend" in prompt.lower() and "diet" in prompt.lower():
            return "For a healthy diet, focus on whole foods, lean proteins, and plenty of fruits and vegetables."
        if "explain" in prompt.lower():
            return "A fever is an elevated body temperature, often a sign that your body is fighting an infection."
        if "plan" in prompt.lower() and "treatment" in prompt.lower():
            return "Let's consider available treatments and your preferences."
        if "summarize" in prompt.lower():
            return "Summary generated based on provided text."
        return "I understand you're asking about healthcare. How can I assist further?"

class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []
        self.semantic_memory = {
            "fever": "An elevated body temperature, often due to infection.",
            "headache": "Pain in the head.",
            "common cold": "A viral infectious disease of the upper respiratory tract.",
            "flu": "Influenza, a contagious respiratory illness caused by influenza viruses.",
            "paracetamol": "A common pain reliever and fever reducer.",
            "ibuprofen": "A nonsteroidal anti-inflammatory drug (NSAID) used for pain and inflammation.",
            "allergy": "An immune system reaction to a substance that is normally harmless."
        }
        self.procedural_memory = {
            "check_symptoms": self._check_symptoms_procedure,
            "schedule_appointment": self._schedule_appointment_procedure
        }

    def _check_symptoms_procedure(self, symptoms):
        potential_conditions = []
        for symptom in symptoms:
            if symptom.lower() in self.semantic_memory:
                potential_conditions.append(f"Possible link to: {self.semantic_memory[symptom.lower()]}")
        return potential_conditions if potential_conditions else ["No direct match in semantic memory for these symptoms."]

    def _schedule_appointment_procedure(self, patient_id, preferred_time):
        return f"Appointment for patient {patient_id} scheduled for {preferred_time}."

    def retrieve_info(self, query):
        query_lower = query.lower()
        if query_lower in self.semantic_memory:
            return self.semantic_memory[query_lower]
        for key, value in self.semantic_memory.items():
            if query_lower in key or query_lower in value.lower():
                return value
        return None

    def update_working_memory(self, key, value):
        self.working_memory[key] = value

    def add_episodic_memory(self, event):
        self.episodic_memory.append(event)

class ToolManager:
    def __init__(self):
        self.tools = {
            "symptom_checker": self.symptom_checker_tool,
            "appointment_scheduler": self.appointment_scheduler_tool,
            "medication_info": self.medication_info_tool
        }

    def symptom_checker_tool(self, symptoms):
        simulated_diagnosis = f"Simulating symptom check for {', '.join(symptoms)}. Potential conditions: Common cold, seasonal allergies."
        return simulated_diagnosis

    def appointment_scheduler_tool(self, patient_id, date, time):
        return f"Appointment confirmed for Patient {patient_id} on {date} at {time}."

    def medication_info_tool(self, medication_name):
        info = {
            "paracetamol": "Used for pain relief and fever reduction.",
            "ibuprofen": "Reduces pain, inflammation, and fever."
        }
        return info.get(medication_name.lower(), "Medication information not found.")

    def execute_tool(self, tool_name, *args, **kwargs):
        tool = self.tools.get(tool_name)
        if tool:
            try:
                return tool(*args, **kwargs)
            except Exception as e:
                return f"Error executing tool {tool_name}: {e}"
        return f"Tool '{tool_name}' not found."

class HealthAgent:
    def __init__(self):
        self.llm = LLM()
        self.memory = MemorySystem()
        self.tool_manager = ToolManager()
        self.patient_id_counter = 1000

    def _generate_patient_id(self):
        self.patient_id_counter += 1
        return f"PAT{self.patient_id_counter}"

    def _plan_action(self, intent, context):
        if "symptom check" in intent.lower():
            symptoms = context.get("symptoms", [])
            if not symptoms:
                return {"action": "clarify", "message": "Please list your symptoms."}
            return {"action": "tool_use", "tool": "symptom_checker", "params": {"symptoms": symptoms}}
        elif "schedule appointment" in intent.lower():
            patient_id = context.get("patient_id", self._generate_patient_id())
            date = context.get("date", "tomorrow")
            time = context.get("time", "10:00 AM")
            self.memory.update_working_memory("current_patient_id", patient_id)
            return {"action": "tool_use", "tool": "appointment_scheduler", "params": {"patient_id": patient_id, "date": date, "time": time}}
        elif "medication info" in intent.lower():
            med_name = context.get("medication", "")
            if not med_name:
                return {"action": "clarify", "message": "Which medication are you asking about?"}
            return {"action": "tool_use", "tool": "medication_info", "params": {"medication_name": med_name}}
        elif "explain" in intent.lower() or "what is" in intent.lower():
            topic = context.get("topic", "")
            if not topic:
                return {"action": "clarify", "message": "What topic do you want me to explain?"}
            retrieved_info = self.memory.retrieve_info(topic)
            if retrieved_info:
                return {"action": "llm_direct_gen", "response": f"From our knowledge base: {retrieved_info}"}
            else:
                return {"action": "llm_direct_gen", "response": self.llm.process_query(f"explain {topic}")}
        else:
            return {"action": "llm_direct_gen", "response": self.llm.process_query(intent, context)}

    def process_request(self, user_query):
        print(f"\nUser: {user_query}")

        # 1. LLM as Central Intelligence & Orchestrator (Intent Understanding & Core Reasoning)
        intent_clarification_prompt = f"Clarify the user's intent: {user_query}"
        llm_response = self.llm.process_query(intent_clarification_prompt, context=self.memory.working_memory)
        # Simplified intent extraction for demonstration
        intent = user_query.lower()
        context = {"query": user_query}

        if "symptoms" in intent or "sick" in intent:
            context["symptoms"] = [s for s in ['fever', 'headache', 'cough'] if s in intent]
            intent = "symptom check"
        elif "appointment" in intent or "see a doctor" in intent:
            intent = "schedule appointment"
        elif "medication" in intent or "drug" in intent:
            context["medication"] = "paracetamol" if "paracetamol" in intent else "ibuprofen" if "ibuprofen" in intent else ""
            intent = "medication info"
        elif "what is" in intent or "explain" in intent:
            parts = intent.split("what is ")
            if len(parts) > 1: context["topic"] = parts[1].strip("?")
            else: context["topic"] = intent.split("explain ")[1].strip("?") if "explain " in intent else ""
            intent = "explain"

        self.memory.update_working_memory("last_intent", intent)
        self.memory.update_working_memory("last_context", context)

        # 4. Adaptive Planning & Decision-Making
        plan = self._plan_action(intent, context)
        print(f"Agent Plan: {plan['action']} (intent: {intent})")

        final_response = ""
        if plan["action"] == "clarify":
            final_response = plan["message"]
        elif plan["action"] == "tool_use":
            tool_output = self.tool_manager.execute_tool(plan["tool"], **plan["params"])
            print(f"Tool Output ({plan['tool']}): {tool_output}")
            # 8. Output Generation & Integration
            llm_integration_prompt = f"Integrate tool output '{tool_output}' with user query '{user_query}' and generate a user-friendly response."
            final_response = self.llm.process_query(llm_integration_prompt)
            final_response = f"I have processed your request using the {plan['tool']} tool. {tool_output} For further details, please consult a medical professional."
            # 5. Continuous Learning & Self-Improvement (simple: remember interaction)
            self.memory.add_episodic_memory(f"User asked about {intent}, used {plan['tool']}, got {tool_output}")
        elif plan["action"] == "llm_direct_gen":
            final_response = plan["response"]
            self.memory.add_episodic_memory(f"User asked about {intent}, got LLM direct generation: {final_response}")

        # 2. Dynamic Knowledge & Memory System (RAG for verification)
        if "symptom check" in intent and "cold" in final_response.lower():
            rag_info = self.memory.retrieve_info("common cold")
            if rag_info:
                final_response += f" (RAG info: {rag_info})"

        # 7. Verification, Grounding & Explainability (simple self-correction)
        if "error" in final_response.lower():
            print("Agent detected an error, attempting self-correction...")
            final_response = self.llm.process_query(f"Refine response given error: {final_response}")

        print(f"Agent: {final_response}")
        return final_response

# Real-world usage simulation: Healthcare Assistant
if __name__ == "__main__":
    agent = HealthAgent()
    print("Holistic LLM Healthcare Agent Activated. How can I help you today?")

    agent.process_request("I have a fever and a headache, what should I do?")
    agent.process_request("What is paracetamol used for?")
    agent.process_request("Can you schedule an appointment for me tomorrow at 3 PM?")
    agent.process_request("Explain flu symptoms.")
    agent.process_request("My symptoms are cough and sneezing.")
    agent.process_request("I need to know about allergy.")
    agent.process_request("Diagnose my condition please.")
