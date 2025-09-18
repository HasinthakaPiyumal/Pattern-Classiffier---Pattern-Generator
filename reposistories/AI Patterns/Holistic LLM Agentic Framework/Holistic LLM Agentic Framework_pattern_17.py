import json

class MockLLM:
    def __init__(self, medical_knowledge):
        self.medical_knowledge = medical_knowledge

    def clarify_intent(self, query):
        if "symptoms" in query or "diagnosis" in query:
            return "DIAGNOSIS_REQUEST"
        elif "medication" in query or "prescription" in query:
            return "MEDICATION_QUERY"
        elif "referral" in query or "specialist" in query:
            return "REFERRAL_REQUEST"
        return "GENERAL_INQUIRY"

    def reason(self, intent, context):
        if intent == "DIAGNOSIS_REQUEST":
            symptoms = context.get('symptoms', 'unknown symptoms')
            if "fever" in symptoms and "cough" in symptoms:
                return "Considering common cold or flu. Suggesting rest and fluids."
            return f"Analyzing symptoms: {symptoms}. Need more specific information or tests."
        elif intent == "MEDICATION_QUERY":
            medication = context.get('medication_name', 'unknown medication')
            if medication in self.medical_knowledge.get('medications', {}):
                return f"Information on {medication}: {self.medical_knowledge['medications'][medication]}"
            return f"Could not find information for {medication}."
        elif intent == "REFERRAL_REQUEST":
            condition = context.get('condition', 'general health issue')
            return f"Considering referral for {condition}. Recommending a general practitioner for initial assessment."
        return "I am processing your request. Please provide more details."

    def generate_response(self, reasoning_output, tool_results=None):
        response = reasoning_output
        if tool_results:
            for tool_name, result in tool_results.items():
                response += f"\nTool Result ({tool_name}): {result}"
        return response + "\nConsult a medical professional for definitive advice."

class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []  # Patient history
        self.semantic_memory = {}
        self.procedural_memory = {}

    def add_to_working_memory(self, key, value):
        self.working_memory[key] = value

    def retrieve_from_working_memory(self, key):
        return self.working_memory.get(key)

    def add_episodic_memory(self, experience):
        self.episodic_memory.append(experience)

    def get_patient_history(self):
        return self.episodic_memory

    def update_semantic_memory(self, key, value):
        self.semantic_memory[key] = value

    def get_semantic_memory(self, key):
        return self.semantic_memory.get(key)

class MedicalKnowledgeBase:
    def __init__(self, data):
        self.data = data

    def retrieve(self, query, strategy="simple"):
        if "symptoms" in query:
            for condition, info in self.data.get('conditions', {}).items():
                if all(s in query for s in info['symptoms']):
                    return {"type": "condition", "name": condition, "info": info}
        if "medication" in query:
            med_name = query.split("medication ")[-1]
            if med_name in self.data.get('medications', {}):
                return {"type": "medication", "name": med_name, "info": self.data['medications'][med_name]}
        return None

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "symptom_checker": self._symptom_checker_tool,
            "medication_lookup": self._medication_lookup_tool,
            "referral_system": self._referral_system_tool,
        }

    def _symptom_checker_tool(self, symptoms):
        if "fever" in symptoms and "cough" in symptoms:
            return "Potential diagnosis: Common Cold or Flu. Recommended actions: Rest, hydration."
        if "headache" in symptoms and "nausea" in symptoms:
            return "Potential diagnosis: Migraine. Recommended actions: Pain relief, quiet environment."
        return "Symptoms are non-specific. Consult a doctor for detailed examination."

    def _medication_lookup_tool(self, medication_name, knowledge_base):
        info = knowledge_base.retrieve(f"medication {medication_name}")
        return info['info'] if info else f"No information found for {medication_name}."

    def _referral_system_tool(self, condition, specialist_type=None):
        if condition == "cardiac issues":
            return "Referral to Cardiologist recommended."
        if condition == "skin rash":
            return "Referral to Dermatologist recommended."
        return f"Referral to a General Practitioner for {condition} is a good first step."

    def execute_tool(self, tool_name, *args, **kwargs):
        if tool_name in self.tools:
            return self.tools[tool_name](*args, **kwargs)
        return f"Tool '{tool_name}' not found."

class HealthcareAgent:
    def __init__(self, medical_data):
        self.memory = MemorySystem()
        self.knowledge_base = MedicalKnowledgeBase(medical_data)
        self.llm = MockLLM(medical_data)
        self.tool_registry = ToolRegistry()
        self.memory.update_semantic_memory('medical_conditions', medical_data.get('conditions', {}))
        self.memory.update_semantic_memory('medications', medical_data.get('medications', {}))

    def process_query(self, user_query):
        print(f"\nUser: {user_query}")

        # 1. LLM as Central Intelligence & Orchestrator: Intent Understanding
        intent = self.llm.clarify_intent(user_query)
        print(f"Agent (LLM Intent): Detected intent as {intent}.")
        self.memory.add_to_working_memory('current_intent', intent)

        context = {'user_query': user_query}
        if intent == "DIAGNOSIS_REQUEST":
            symptoms = user_query.replace("I have symptoms like ", "").replace("What is my diagnosis for ", "").lower()
            context['symptoms'] = symptoms
            self.memory.add_to_working_memory('symptoms', symptoms)
        elif intent == "MEDICATION_QUERY":
            med_name = user_query.replace("Tell me about medication ", "").replace("What is ", "").replace("?", "").strip()
            context['medication_name'] = med_name
            self.memory.add_to_working_memory('medication_name', med_name)
        elif intent == "REFERRAL_REQUEST":
            condition = user_query.replace("I need a referral for ", "").replace("Who should I see for ", "").strip()
            context['condition'] = condition
            self.memory.add_to_working_memory('condition', condition)

        # 2. Dynamic Knowledge & Memory System: RAG and Memory Retrieval
        rag_result = None
        if intent == "DIAGNOSIS_REQUEST":
            rag_result = self.knowledge_base.retrieve(f"symptoms {context['symptoms']}")
            if rag_result: print(f"Agent (RAG): Retrieved knowledge for symptoms: {rag_result.get('name')}")
        elif intent == "MEDICATION_QUERY":
            rag_result = self.knowledge_base.retrieve(f"medication {context['medication_name']}")
            if rag_result: print(f"Agent (RAG): Retrieved knowledge for medication: {rag_result.get('name')}")

        # 3. Advanced Tool Integration & Interaction: Tool Orchestration
        tool_results = {}
        if intent == "DIAGNOSIS_REQUEST":
            tool_output = self.tool_registry.execute_tool("symptom_checker", symptoms=context['symptoms'])
            tool_results['symptom_checker'] = tool_output
            print(f"Agent (Tool Use): Executed symptom_checker. Result: {tool_output}")
        elif intent == "MEDICATION_QUERY":
            tool_output = self.tool_registry.execute_tool("medication_lookup", context['medication_name'], self.knowledge_base)
            tool_results['medication_lookup'] = tool_output
            print(f"Agent (Tool Use): Executed medication_lookup. Result: {tool_output}")
        elif intent == "REFERRAL_REQUEST":
            tool_output = self.tool_registry.execute_tool("referral_system", context['condition'])
            tool_results['referral_system'] = tool_output
            print(f"Agent (Tool Use): Executed referral_system. Result: {tool_output}")

        # 4. Adaptive Planning & Decision-Making (LLM's reasoning combined with tool/RAG results)
        reasoning_context = {
            'intent': intent,
            'context_data': context,
            'rag_data': rag_result,
            'tool_data': tool_results,
            'patient_history': self.memory.get_patient_history()
        }
        reasoning_output = self.llm.reason(intent, reasoning_context)
        print(f"Agent (LLM Reasoning): {reasoning_output}")

        # 5. Continuous Learning & Self-Improvement (simple: add to episodic memory)
        self.memory.add_episodic_memory({"query": user_query, "response": reasoning_output, "tool_results": tool_results})

        # 8. Output Generation & Integration
        final_response = self.llm.generate_response(reasoning_output, tool_results)
        print(f"Agent: {final_response}")
        return final_response


def simulate_healthcare_scenario():
    print("--- Healthcare Agent Simulation ---")
    medical_data = {
        "conditions": {
            "common cold": {"symptoms": ["fever", "cough", "runny nose"], "treatment": "Rest, fluids"},
            "flu": {"symptoms": ["fever", "cough", "body aches"], "treatment": "Antivirals, rest"},
            "migraine": {"symptoms": ["headache", "nausea", "light sensitivity"], "treatment": "Pain relief"}
        },
        "medications": {
            "Paracetamol": "Pain reliever and fever reducer.",
            "Ibuprofen": "Anti-inflammatory and pain reliever."
        }
    }
    agent = HealthcareAgent(medical_data)

    # Real-world usage: Patient describes symptoms
    agent.process_query("I have symptoms like fever and cough. What is my diagnosis?")
    # Real-world usage: Patient asks about medication
    agent.process_query("Tell me about medication Paracetamol.")
    # Real-world usage: Patient needs a referral
    agent.process_query("I need a referral for skin rash.")
    # Real-world usage: Vague query - LLM intent clarification
    agent.process_query("I don't feel well.")

simulate_healthcare_scenario()
