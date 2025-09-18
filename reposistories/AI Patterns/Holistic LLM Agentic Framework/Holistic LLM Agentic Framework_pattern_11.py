import time

class LLMCore:
    def __init__(self, name="MediAgentLLM"):
        self.name = name
        self.reasoning_steps = []

    def reason(self, prompt, context, memory, tools_available):
        self.reasoning_steps.append(f"[{self.name}] Reasoning on: {prompt[:50]}...")
        if "symptoms" in prompt.lower() or "diagnosis" in prompt.lower():
            intent = "medical_diagnosis"
            self.reasoning_steps.append(f"[{self.name}] Intent identified: {intent}")
            if "lookup_symptoms" in tools_available:
                self.reasoning_steps.append(f"[{self.name}] Planning to use 'lookup_symptoms' tool.")
                return f"PLAN: Use lookup_symptoms with '{prompt}' then synthesize."
            return "PLAN: Synthesize information from context and memory."
        elif "medication" in prompt.lower() or "drug" in prompt.lower():
            intent = "medication_info"
            self.reasoning_steps.append(f"[{self.name}] Intent identified: {intent}")
            if "check_drug_interactions" in tools_available:
                self.reasoning_steps.append(f"[{self.name}] Planning to use 'check_drug_interactions' tool.")
                return f"PLAN: Use check_drug_interactions with '{prompt}' then synthesize."
            return "PLAN: Provide general medication info."
        else:
            return "PLAN: Direct generation or general information retrieval."

    def generate_response(self, plan, tool_output, memory_info, contextual_info):
        self.reasoning_steps.append(f"[{self.name}] Generating response based on plan: {plan[:50]}...")
        response = f"Based on your query and current information:\n"
        if "lookup_symptoms" in plan and tool_output:
            response += f"Symptoms analysis: {tool_output}\n"
        if "check_drug_interactions" in plan and tool_output:
            response += f"Medication check: {tool_output}\n"
        if memory_info:
            response += f"Previous context considered: {memory_info}\n"
        response += f"My current assessment is: {contextual_info}"
        self.reasoning_steps.append(f"[{self.name}] Generated response.")
        return response

class KnowledgeBase:
    def __init__(self):
        self.medical_conditions = {
            "fever, cough, fatigue": "Common Cold or Flu. Consider rest and hydration.",
            "chest pain, shortness of breath": "Potential cardiac issue. Seek immediate medical attention.",
            "headache, stiff neck, fever": "Possible Meningitis. Urgent medical consultation required.",
            "abdominal pain, nausea, jaundice": "Liver or Gallbladder issue. Consult a specialist.",
            "rash, itching, swelling": "Allergic reaction or skin condition."
        }
        self.medication_interactions = {
            "ibuprofen, warfarin": "High risk of bleeding. Avoid combination.",
            "antacids, antibiotics": "May reduce antibiotic effectiveness. Take separately."
        }
        self.patient_records = {}

    def retrieve_info(self, query, patient_id=None):
        query_lower = query.lower()
        if "symptoms" in query_lower or "condition" in query_lower:
            for symptoms_key, info in self.medical_conditions.items():
                if all(s.strip() in query_lower for s in symptoms_key.split(',')):
                    return f"Potential condition: {info}"
            return "Could not find a direct match for symptoms in knowledge base."
        elif "drug interaction" in query_lower or "medication" in query_lower:
            for drugs, interaction in self.medication_interactions.items():
                if all(d.strip() in query_lower for d in drugs.split(',')):
                    return f"Drug interaction alert: {interaction}"
            return "No specific drug interaction found in knowledge base."
        return "No relevant information found."

    def get_patient_history(self, patient_id):
        return self.patient_records.get(patient_id, "No past medical history available.")

    def update_patient_history(self, patient_id, new_entry):
        if patient_id not in self.patient_records:
            self.patient_records[patient_id] = []
        self.patient_records[patient_id].append(new_entry)

class PatientMemory:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.working_memory = {}
        self.episodic_memory = []
        self.semantic_memory_ref = KnowledgeBase()
        self.procedural_memory = {}

    def update_working_memory(self, key, value):
        self.working_memory[key] = value

    def get_working_memory(self, key):
        return self.working_memory.get(key)

    def add_episodic_event(self, event_description):
        self.episodic_memory.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event_description}")
        self.semantic_memory_ref.update_patient_history(self.patient_id, event_description)

    def get_full_context(self):
        context = f"Patient ID: {self.patient_id}\n"
        context += f"Current session thoughts: {self.working_memory}\n"
        context += f"Past medical history: {self.semantic_memory_ref.get_patient_history(self.patient_id)}\n"
        return context

class DiagnosticTools:
    def lookup_symptoms(self, symptoms_query):
        print(f"  [Tool] Looking up symptoms: '{symptoms_query}'...")
        time.sleep(0.1)
        if "fever" in symptoms_query and "cough" in symptoms_query:
            return "Common symptoms for respiratory infections like flu or cold."
        if "chest pain" in symptoms_query:
            return "Chest pain requires immediate medical evaluation. Could be cardiac or respiratory."
        return "Symptoms found: General malaise. More specific details needed."

    def check_drug_interactions(self, drug1, drug2):
        print(f"  [Tool] Checking drug interactions for '{drug1}' and '{drug2}'...")
        time.sleep(0.1)
        if "ibuprofen" in drug1.lower() and "warfarin" in drug2.lower():
            return "WARNING: High risk of increased bleeding. Consult a doctor immediately."
        return f"No severe interactions found between {drug1} and {drug2} in this check."

class MedicalAgent:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.llm_core = LLMCore()
        self.knowledge_base = KnowledgeBase()
        self.patient_memory = PatientMemory(patient_id)
        self.diagnostic_tools = DiagnosticTools()
        self.available_tools = {
            "lookup_symptoms": self.diagnostic_tools.lookup_symptoms,
            "check_drug_interactions": self.diagnostic_tools.check_drug_interactions
        }
        print(f"MedicalAgent initialized for Patient ID: {patient_id}")

    def process_query(self, query):
        print(f"\n[Agent] Processing query: '{query}'")
        self.patient_memory.update_working_memory("last_query", query)
        full_context = self.patient_memory.get_full_context()
        llm_plan = self.llm_core.reason(query, full_context, self.patient_memory, self.available_tools)
        print(f"[Agent] LLM Plan: {llm_plan}")

        tool_output = None
        final_assessment = "Gathering information..."

        if "lookup_symptoms" in llm_plan:
            tool_output = self.available_tools["lookup_symptoms"](query)
            final_assessment = self.knowledge_base.retrieve_info(query)
        elif "check_drug_interactions" in llm_plan:
            drugs = [word for word in query.lower().split() if word in ["ibuprofen", "warfarin", "antacids", "antibiotics"]]
            if len(drugs) >= 2:
                tool_output = self.available_tools["check_drug_interactions"](drugs[0], drugs[1])
                final_assessment = self.knowledge_base.retrieve_info(f"drug interaction {drugs[0]}, {drugs[1]}")
            else:
                tool_output = "Insufficient drug names for interaction check."

        rag_info = self.knowledge_base.retrieve_info(query, self.patient_id)
        if rag_info:
            final_assessment = rag_info if not tool_output else f"{rag_info}. Tool output: {tool_output}"
        elif tool_output:
            final_assessment = tool_output

        self.patient_memory.add_episodic_event(f"Query: '{query}', Interim Assessment: '{final_assessment}'")

        explanation = f"Reasoning path:\n" + "\n".join(self.llm_core.reasoning_steps)
        self.llm_core.reasoning_steps = []

        response = self.llm_core.generate_response(llm_plan, tool_output, self.patient_memory.get_full_context(), final_assessment)
        return response + "\n\n" + explanation

print("--- Healthcare Agent: Medical Diagnostic Assistant ---")
patient_agent = MedicalAgent(patient_id="P1001")

print(patient_agent.process_query("I have a fever, cough, and feel very tired. What could it be?"))
time.sleep(0.5)

print(patient_agent.process_query("What about ibuprofen and warfarin? Are they safe together?"))
time.sleep(0.5)

print(patient_agent.process_query("I still feel tired, and now have a headache. Any new thoughts?"))
time.sleep(0.5)

print(patient_agent.process_query("My stomach hurts. What's wrong?"))