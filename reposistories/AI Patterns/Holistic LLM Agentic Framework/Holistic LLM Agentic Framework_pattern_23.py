import datetime

class SimulatedLLM:
    def process_query(self, query, context=None):
        if "schedule appointment" in query.lower():
            return "ACTION:SCHEDULE_APPOINTMENT(patient_name='John Doe', reason='flu symptoms', date='tomorrow')"
        elif "medication interaction" in query.lower():
            return "ACTION:CHECK_MEDICATION_INTERACTION(med1='Amoxicillin', med2='Ibuprofen')"
        elif "patient history" in query.lower():
            return "QUERY:RETRIEVE_PATIENT_HISTORY(patient_id='P101')"
        elif "diagnose" in query.lower():
            return f"REASONING: Based on symptoms, considering common cold or mild flu. Need more data. Context: {context}"
        return f"I'm not sure how to respond to '{query}'. Please clarify."

class KnowledgeBase:
    def __init__(self):
        self._data = {
            "med_interaction": {
                "Amoxicillin-Ibuprofen": "Generally safe, but Ibuprofen can reduce Amoxicillin's effectiveness in some cases.",
                "Warfarin-Aspirin": "High risk of bleeding. Contraindicated."
            },
            "medical_facts": {
                "flu_symptoms": "Fever, cough, sore throat, body aches, fatigue.",
                "common_cold_symptoms": "Runny nose, sneezing, mild sore throat, cough."
            }
        }

    def retrieve(self, query_type, key):
        return self._data.get(query_type, {}).get(key, "Information not found.")

class PatientMemory:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []
        self.semantic_memory = {
            'P101': {
                'name': 'John Doe',
                'age': 45,
                'conditions': ['Hypertension'],
                'medications': ['Lisinopril'],
                'allergies': ['Penicillin']
            }
        }

    def update_working_memory(self, key, value):
        self.working_memory[key] = value

    def add_episodic_event(self, event):
        self.episodic_memory.append(event)

    def get_patient_profile(self, patient_id):
        return self.semantic_memory.get(patient_id, {})

class MedicalAssistantAgent:
    def __init__(self, patient_id):
        self.llm = SimulatedLLM()
        self.knowledge_base = KnowledgeBase()
        self.memory = PatientMemory()
        self.patient_id = patient_id
        self.memory.update_working_memory('current_patient_id', patient_id)

    def _schedule_appointment(self, patient_name, reason, date):
        print(f"TOOL_EXEC: Scheduling appointment for {patient_name} for {reason} on {date}.\n")
        self.memory.add_episodic_event(f"Appointment scheduled for {patient_name} on {date} for {reason}.")
        return f"Appointment for {patient_name} confirmed for {date}."

    def _check_medication_interaction(self, med1, med2):
        interaction_key = f"{med1}-{med2}"
        result = self.knowledge_base.retrieve("med_interaction", interaction_key)
        print(f"TOOL_EXEC: Checking interaction between {med1} and {med2}. Result: {result}\n")
        self.memory.add_episodic_event(f"Checked med interaction: {med1} & {med2}.")
        return result

    def _retrieve_patient_history(self, patient_id):
        profile = self.memory.get_patient_profile(patient_id)
        print(f"TOOL_EXEC: Retrieving patient history for {patient_id}. Profile: {profile}\n")
        return profile

    def _verify_knowledge(self, statement, context):
        # Simulate factual verification against KB or context
        if "common cold" in statement and "runny nose" in context:
            return True, "Consistent with common cold symptoms."
        return False, "Needs more verification."

    def run(self, user_query):
        print(f"USER: {user_query}")
        patient_profile = self.memory.get_patient_profile(self.patient_id)
        context = f"Patient ID: {self.patient_id}, Profile: {patient_profile}"
        self.memory.update_working_memory('current_context', context)

        llm_response = self.llm.process_query(user_query, context)
        print(f"LLM_ORCHESTRATOR: {llm_response}")

        if llm_response.startswith("ACTION:"):
            action_str = llm_response[len("ACTION:"):]
            try:
                # Simple parsing for demonstration
                action_name = action_str.split('(')[0]
                params_str = action_str.split('(')[1][:-1]
                params = dict(item.split('=', 1) for item in params_str.split(', '))
                
                for k, v in params.items():
                    params[k] = v.strip("'")

                if action_name == "SCHEDULE_APPOINTMENT":
                    tool_output = self._schedule_appointment(**params)
                elif action_name == "CHECK_MEDICATION_INTERACTION":
                    tool_output = self._check_medication_interaction(**params)
                else:
                    tool_output = "Unknown action."
                print(f"AGENT_RESPONSE: {tool_output}")
                self.memory.add_episodic_event(f"Agent executed {action_name} with result: {tool_output}")
            except Exception as e:
                print(f"TOOL_ERROR: Failed to execute action {action_str}. Error: {e}")
                print("AGENT_RESPONSE: I encountered an error while trying to perform that action.")
        elif llm_response.startswith("QUERY:"):
            query_str = llm_response[len("QUERY:"):]
            if query_str.startswith("RETRIEVE_PATIENT_HISTORY"):
                patient_id = query_str.split("(")[1].split("=")[1].strip("')")
                history = self._retrieve_patient_history(patient_id)
                print(f"AGENT_RESPONSE: Patient history for {patient_id}: {history}")
                self.memory.add_episodic_event(f"Retrieved patient history for {patient_id}.")
        elif llm_response.startswith("REASONING:"):
            reasoning = llm_response[len("REASONING:"):]
            is_verified, verification_msg = self._verify_knowledge(reasoning, context)
            print(f"AGENT_THOUGHT: {reasoning} -- Verification: {verification_msg}\n")
            print(f"AGENT_RESPONSE: {reasoning.split('Context:')[0].strip()} {verification_msg}")
            self.memory.add_episodic_event(f"Agent reasoned: {reasoning} and verified: {verification_msg}")
        else:
            print(f"AGENT_RESPONSE: {llm_response}")
        print("\n" + "-" * 50 + "\n")

# Real-world usage simulation: Medical Assistant for patient queries
medical_agent = MedicalAssistantAgent(patient_id='P101')
medical_agent.run("I feel sick, I think I have the flu. Can you schedule an appointment for me for tomorrow?")
medical_agent.run("What medications am I on? And can I take Amoxicillin with Ibuprofen?")
medical_agent.run("Can you tell me more about common cold symptoms?")