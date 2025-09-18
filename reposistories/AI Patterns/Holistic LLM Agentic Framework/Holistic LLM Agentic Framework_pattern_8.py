import json
import time

class MockLLM:
    def __init__(self):
        self.knowledge_base = {
            "common_cold": "Symptoms: runny nose, sore throat, cough, congestion. Treatment: rest, fluids, OTC meds.",
            "influenza": "Symptoms: fever, body aches, fatigue, cough. Treatment: antiviral meds (Tamiflu), rest, fluids.",
            "migraine": "Symptoms: severe throbbing headache, sensitivity to light/sound, nausea. Treatment: pain relievers, triptans.",
            "diabetes_type2": "Symptoms: increased thirst, frequent urination, fatigue, blurred vision. Management: diet, exercise, medication.",
            "hypertension": "Symptoms: often none ('silent killer'). Can cause headaches, shortness of breath. Management: lifestyle changes, medication."
        }
        self.tool_descriptions = {
            "symptom_checker": "Checks a list of symptoms against known conditions and provides a likely diagnosis.",
            "medication_info": "Retrieves information about a specific medication, including dosage and side effects.",
            "schedule_appointment": "Schedules a virtual or in-person doctor's appointment."
        }

    def infer(self, prompt, context=None, persona="medical_assistant"):
        if "diagnose" in prompt.lower() and "symptoms:" in prompt.lower():
            symptoms_str = prompt.split("symptoms:", 1)[1].strip().lower()
            if "fever" in symptoms_str and "body aches" in symptoms_str:
                return {"action": "tool_use", "tool": "symptom_checker", "params": {"symptoms": symptoms_str, "likely_condition": "influenza"}, "thought": "Based on fever and body aches, I should check for influenza."}
            elif "runny nose" in symptoms_str and "sore throat" in symptoms_str:
                return {"action": "tool_use", "tool": "symptom_checker", "params": {"symptoms": symptoms_str, "likely_condition": "common_cold"}, "thought": "Runny nose and sore throat suggest a common cold."}
            elif "headache" in symptoms_str and "light sensitivity" in symptoms_str:
                return {"action": "tool_use", "tool": "symptom_checker", "params": {"symptoms": symptoms_str, "likely_condition": "migraine"}, "thought": "Severe headache with light sensitivity points to migraine."}
            else:
                return {"action": "generate", "response": "I need more information about your symptoms to provide a precise diagnosis. Could you elaborate?", "thought": "Symptoms are too vague for a direct diagnosis."}
        
        if "medication info for" in prompt.lower():
            med_name = prompt.split("medication info for", 1)[1].strip().replace("?", "").capitalize()
            return {"action": "tool_use", "tool": "medication_info", "params": {"medication": med_name}, "thought": f"User asked for info on {med_name}."}

        if "schedule appointment" in prompt.lower():
            return {"action": "tool_use", "tool": "schedule_appointment", "params": {"type": "general"}, "thought": "User wants to schedule an appointment."}

        if "recommendation for" in prompt.lower():
            condition = prompt.split("recommendation for", 1)[1].strip().replace("?", "").lower()
            if condition in self.knowledge_base:
                return {"action": "generate", "response": f"Based on your query about {condition}, here's what I know: {self.knowledge_base[condition]}. Please consult a doctor for personalized advice.", "thought": f"Directly generating info for {condition}."}
            else:
                return {"action": "generate", "response": "I don't have specific recommendations for that condition in my current knowledge base. Please consult a medical professional.", "thought": "Condition not found in KB."}

        return {"action": "generate", "response": "Hello! How can I assist you with your health today?", "thought": "Initial greeting or fallback."}

class MedicalAgent:
    def __init__(self):
        self.llm = MockLLM()
        self.working_memory = {}
        self.episodic_memory = [] # Patient history, past interactions
        self.semantic_memory = self.llm.knowledge_base.copy() # Medical facts
        self.procedural_memory = {
            "symptom_checker": self._tool_symptom_checker,
            "medication_info": self._tool_medication_info,
            "schedule_appointment": self._tool_schedule_appointment,
        }
        self.tools = self.procedural_memory # Alias for clarity
        self.patient_profile = {}

    def _tool_symptom_checker(self, symptoms, likely_condition):
        time.sleep(0.5) # Simulate database lookup
        if likely_condition in self.semantic_memory:
            info = self.semantic_memory[likely_condition]
            self.working_memory['diagnosis'] = likely_condition
            return f"Based on your symptoms, a likely condition is {likely_condition}. {info} For a definitive diagnosis, please consult a doctor."
        return "Could not find detailed information for the suggested condition."

    def _tool_medication_info(self, medication):
        time.sleep(0.3) # Simulate API call
        mock_med_db = {
            "Paracetamol": "Common pain reliever. Dosage: 500mg-1000mg every 4-6 hrs. Side effects: rare, liver damage in overdose.",
            "Ibuprofen": "NSAID for pain/inflammation. Dosage: 200mg-400mg every 4-6 hrs. Side effects: stomach upset, kidney issues.",
            "Tamiflu": "Antiviral for influenza. Dosage: 75mg twice daily for 5 days. Side effects: nausea, vomiting."
        }
        info = mock_med_db.get(medication, "Information not found for this medication.")
        self.working_memory['last_med_query'] = medication
        return f"Medication info for {medication}: {info}"

    def _tool_schedule_appointment(self, appt_type, patient_id="current_user"):
        time.sleep(1) # Simulate scheduling system
        appointment_id = f"APP-{int(time.time())}"
        self.episodic_memory.append(f"Scheduled {appt_type} appointment for {patient_id} with ID {appointment_id}")
        self.working_memory['last_appointment'] = appointment_id
        return f"Appointment of type '{appt_type}' scheduled successfully. Your appointment ID is {appointment_id}."

    def _reflect_on_outcome(self, user_query, llm_response, tool_output=None):
        if "diagnosis" in self.working_memory and "I need more information" not in llm_response.get("response", ""):
            self.patient_profile['last_diagnosis'] = self.working_memory['diagnosis']
            self.episodic_memory.append(f"Reflected on query: '{user_query}', outcome: '{self.working_memory['diagnosis']}'")
        elif "appointment" in user_query.lower() and tool_output and "scheduled successfully" in tool_output:
            self.patient_profile['last_action'] = "appointment_scheduled"
            self.episodic_memory.append(f"Reflected on query: '{user_query}', action: 'appointment_scheduled'")
        # Simulate learning: If a diagnosis was confirmed, add it to a 'learned' section
        if 'diagnosis' in self.working_memory and self.working_memory['diagnosis'] not in self.semantic_memory:
            print(f"[AGENT LEARNS] New diagnosis pattern for '{self.working_memory['diagnosis']}' added to semantic memory.")
            self.semantic_memory[self.working_memory['diagnosis']] = "Learned new diagnostic pattern."

    def _verify_facts(self, statement):
        # Simple verification: check if statement is directly in semantic memory
        for k, v in self.semantic_memory.items():
            if k.lower() in statement.lower() and k.lower() in v.lower():
                return True, f"Verified against semantic memory for '{k}'."
        return False, "Could not directly verify statement against semantic memory."

    def process_query(self, user_query):
        print(f"\n[USER]: {user_query}")
        self.working_memory = {"user_query": user_query}
        
        # 1. LLM as Central Intelligence & Orchestrator
        llm_decision = self.llm.infer(user_query, context=self.working_memory)
        
        tool_output = None
        response = ""
        thought = llm_decision.get("thought", "No specific thought.")
        print(f"[LLM Thought]: {thought}")

        if llm_decision.get("action") == "tool_use":
            tool_name = llm_decision["tool"]
            params = llm_decision["params"]
            print(f"[AGENT ACTION]: Using tool '{tool_name}' with params: {params}")
            if tool_name in self.tools:
                try:
                    tool_output = self.tools[tool_name](**params)
                    response = tool_output
                    # 4. Adaptive Planning & Decision-Making (Grounded & Iterative Planning)
                    if "likely_condition" in params and "influenza" in params["likely_condition"]:
                         # Simulate a follow-up action based on diagnosis
                         print("[AGENT PLANNING]: Influenza suspected, considering medication info next.")
                         med_info_decision = self.llm.infer(f"medication info for Tamiflu")
                         if med_info_decision.get("action") == "tool_use":
                             tool_output_med = self.tools[med_info_decision["tool"]](**med_info_decision["params"])
                             response += f"\nAlso, given the potential for influenza, here is information on a common antiviral: {tool_output_med}"

                except Exception as e:
                    response = f"Error executing tool {tool_name}: {e}"
                    print(f"[ERROR]: {response}")
            else:
                response = f"LLM suggested unknown tool: {tool_name}"
        elif llm_decision.get("action") == "generate":
            response = llm_decision["response"]
        else:
            response = "I'm not sure how to respond to that."
        
        # 7. Verification, Grounding & Explainability
        if "diagnosis" in self.working_memory:
            verified, trace = self._verify_facts(response)
            print(f"[VERIFICATION]: Diagnosis '{self.working_memory['diagnosis']}' - {verified} ({trace})")

        # 5. Continuous Learning & Self-Improvement (Automated Feedback & Reflection)
        self._reflect_on_outcome(user_query, llm_decision, tool_output)

        # 8. Output Generation & Integration
        final_output = f"[AGENT RESPONSE]: {response}"
        print(final_output)
        return final_output

# Real-world Usage: Virtual Medical Assistant
# Simulation Pattern: User interacts with the agent asking for diagnosis, medication info, and scheduling appointments.
medical_agent = MedicalAgent()

medical_agent.process_query("I have a runny nose and a sore throat. Can you diagnose me?")
medical_agent.process_query("What are the symptoms and treatment for migraine?")
medical_agent.process_query("I have fever and body aches. Please diagnose me.")
medical_agent.process_query("Can you tell me medication info for Paracetamol?")
medical_agent.process_query("I need to schedule an appointment with a doctor.")
medical_agent.process_query("My symptoms are vague. Just a bit tired. What could it be?")
