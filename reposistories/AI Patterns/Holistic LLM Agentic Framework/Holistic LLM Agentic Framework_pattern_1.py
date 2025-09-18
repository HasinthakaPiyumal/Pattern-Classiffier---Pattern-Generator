import json
import datetime

class LLMCore:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.reasoning_strategies = ["Chain-of-Thought", "Plan-and-Solve"]

    def _simulate_reasoning(self, prompt, context):
        if "diagnose" in prompt.lower() and "symptoms" in context:
            symptoms = context.get("symptoms", [])
            patient_history = context.get("history", [])
            retrieved_info = self.knowledge_base.retrieve_info(f"diagnosis for {', '.join(symptoms)}")
            
            diagnosis_candidates = []
            if "fever" in symptoms and "cough" in symptoms:
                diagnosis_candidates.append("Common Cold")
            if "chest pain" in symptoms and "shortness of breath" in symptoms:
                diagnosis_candidates.append("Potential Cardiac Issue")
            if "diabetes" in patient_history and "high blood sugar" in context.get("lab_results", []):
                diagnosis_candidates.append("Diabetes Management")
            
            if retrieved_info:
                diagnosis_candidates.extend([item for item in retrieved_info.split(', ') if item not in diagnosis_candidates])

            if diagnosis_candidates:
                return f"Considering the symptoms ({', '.join(symptoms)}) and history, potential diagnoses include: {', '.join(diagnosis_candidates)}. Further investigation needed."
            return "Unable to determine a specific diagnosis from provided information."
        elif "clarify" in prompt.lower():
            return "Please provide more details about your discomfort. When did it start? What exactly do you feel?"
        elif "recommend treatment" in prompt.lower():
            diagnosis = context.get("diagnosis", "unknown condition")
            retrieved_treatment = self.knowledge_base.retrieve_info(f"treatment for {diagnosis}")
            if retrieved_treatment:
                return f"Based on {diagnosis}, recommended treatments might include: {retrieved_treatment}. Consult a doctor for personalized advice."
            return f"No specific treatment found for {diagnosis}. General recommendations apply."
        return "Understood. How can I assist further?"

    def process_query(self, user_query, current_context):
        print(f"LLM: Processing query '{user_query}' with context: {current_context}")
        if "feel unwell" in user_query.lower() or "not feeling good" in user_query.lower():
            if not current_context.get("symptoms"):
                return self._simulate_reasoning("clarify intent", current_context)
            else:
                return self._simulate_reasoning("diagnose", current_context)
        elif "diagnose me" in user_query.lower() or "what's wrong" in user_query.lower():
            return self._simulate_reasoning("diagnose", current_context)
        elif "what treatment" in user_query.lower():
            return self._simulate_reasoning("recommend treatment", current_context)
        elif "schedule" in user_query.lower():
            return "Intent: Schedule Appointment"
        
        return self._simulate_reasoning(user_query, current_context)

class MultiTieredMemory:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = []
        self.semantic_memory = {
            "Common Cold": "Viral infection, symptoms include fever, cough, runny nose. Treatment: rest, fluids.",
            "Potential Cardiac Issue": "Symptoms: chest pain, shortness of breath. Requires immediate medical attention. Diagnostic: ECG, blood tests.",
            "Diabetes Management": "Chronic condition, requires diet control, exercise, medication (e.g., insulin). Monitoring blood sugar is key.",
            "Ibuprofen": "Pain reliever, anti-inflammatory. Side effects: stomach upset. Interactions: blood thinners.",
            "Acetaminophen": "Pain reliever, fever reducer. Side effects: liver damage in high doses.",
            "appointment availability": ["Monday 10 AM", "Wednesday 2 PM"]
        }
        self.procedural_memory = {
            "diagnose_protocol": ["gather_symptoms", "check_history", "order_labs", "consult_KB", "propose_diagnosis"],
            "schedule_protocol": ["check_availability", "confirm_booking"]
        }

    def update_working_memory(self, key, value):
        self.working_memory[key] = value

    def get_working_memory(self, key=None):
        return self.working_memory if key is None else self.working_memory.get(key)

    def add_episodic_event(self, event):
        self.episodic_memory.append(event)

    def get_episodic_history(self, patient_id=None):
        if patient_id:
            return [e for e in self.episodic_memory if e.get("patient_id") == patient_id]
        return self.episodic_memory

class KnowledgeBase:
    def __init__(self, semantic_memory):
        self.semantic_memory = semantic_memory
        self.external_docs = {
            "fever cough": "Common Cold, Bronchitis, Flu",
            "chest pain shortness of breath": "Angina, Myocardial Infarction, Anxiety",
            "diabetes high blood sugar": "Diabetic Ketoacidosis, Hyperglycemic Hyperosmolar State",
            "Common Cold treatment": "Rest, fluids, OTC cold medicine (e.g., decongestants, pain relievers like Acetaminophen or Ibuprofen).",
            "Potential Cardiac Issue treatment": "Emergency medical care, aspirin, nitroglycerin. Definitive treatment depends on diagnosis.",
            "Diabetes Management treatment": "Insulin, oral medications, diet, exercise."
        }
        
    def retrieve_info(self, query):
        query_lower = query.lower()
        if query_lower in self.semantic_memory:
            return self.semantic_memory[query_lower]
        
        for key, value in self.external_docs.items():
            if all(word in query_lower for word in key.split()):
                return value
        
        return None

class Tool:
    def execute(self, params):
        raise NotImplementedError

class SymptomChecker(Tool):
    def execute(self, params):
        symptoms = params.get("symptoms", [])
        print(f"Tool: Running SymptomChecker with symptoms: {symptoms}")
        if "fever" in symptoms and "cough" in symptoms:
            return {"possible_conditions": ["Common Cold", "Flu"], "severity": "mild"}
        elif "chest pain" in symptoms and "shortness of breath" in symptoms:
            return {"possible_conditions": ["Angina", "Heart Attack"], "severity": "critical", "action_required": "emergency"}
        return {"possible_conditions": ["Unspecified Illness"], "severity": "unknown"}

class DrugInteractionChecker(Tool):
    def execute(self, params):
        drugs = params.get("drugs", [])
        print(f"Tool: Running DrugInteractionChecker for drugs: {drugs}")
        if "Ibuprofen" in drugs and "blood thinner" in drugs:
            return {"interaction": "High risk of bleeding", "severity": "severe"}
        return {"interaction": "No significant interactions found", "severity": "none"}

class EHRInterface(Tool):
    def execute(self, params):
        action = params.get("action")
        patient_id = params.get("patient_id")
        data = params.get("data", {})
        print(f"Tool: Interacting with EHR for patient {patient_id}, action: {action}")
        if action == "get_history":
            return {"history": ["diagnosed with diabetes 5 years ago", "allergic to penicillin"], "last_visit": "2023-10-26"}
        elif action == "record_diagnosis":
            print(f"EHR: Recorded diagnosis for patient {patient_id}: {data.get('diagnosis')}")
            return {"status": "success", "record_id": f"diag_{patient_id}_{datetime.datetime.now().timestamp()}"}
        elif action == "schedule_appointment":
            date_time = data.get("date_time")
            if date_time in self.available_slots:
                self.available_slots.remove(date_time)
                print(f"EHR: Scheduled appointment for patient {patient_id} on {date_time}")
                return {"status": "success", "appointment_id": f"app_{patient_id}_{date_time}"}
            return {"status": "failed", "reason": "slot unavailable"}
        return {"status": "failed", "reason": "unsupported EHR action"}

    def __init__(self):
        self.available_slots = ["Monday 10 AM", "Wednesday 2 PM"]

class HealthcareAgent:
    def __init__(self):
        self.memory = MultiTieredMemory()
        self.knowledge_base = KnowledgeBase(self.memory.semantic_memory)
        self.llm_core = LLMCore(self.knowledge_base)
        self.tools = {
            "symptom_checker": SymptomChecker(),
            "drug_interaction_checker": DrugInteractionChecker(),
            "ehr_interface": EHRInterface()
        }
        self.patient_context = {}

    def _tool_orchestration(self, tool_name, params):
        if tool_name in self.tools:
            try:
                result = self.tools[tool_name].execute(params)
                print(f"Tool '{tool_name}' executed. Result: {result}")
                return result
            except Exception as e:
                print(f"Error executing tool '{tool_name}': {e}")
                return {"status": "error", "message": str(e)}
        return {"status": "error", "message": f"Tool '{tool_name}' not found."}

    def _update_patient_context(self, patient_id, key, value):
        if patient_id not in self.patient_context:
            self.patient_context[patient_id] = {}
        self.patient_context[patient_id][key] = value
        self.memory.update_working_memory(f"{patient_id}_{key}", value)
        
    def _get_patient_context(self, patient_id):
        patient_specific_context = self.patient_context.get(patient_id, {})
        for k, v in self.memory.working_memory.items():
            if k.startswith(f"{patient_id}_") and k.replace(f"{patient_id}_", "") not in patient_specific_context:
                patient_specific_context[k.replace(f"{patient_id}_", "")] = v
        
        patient_specific_context["history"] = self.memory.get_episodic_history(patient_id)
        return patient_specific_context

    def handle_patient_query(self, patient_id, user_query):
        print(f"\nAgent: Handling query for Patient {patient_id}: '{user_query}'")
        
        current_context = self._get_patient_context(patient_id)
        
        llm_response = self.llm_core.process_query(user_query, current_context)
        
        final_response_parts = [f"Agent Initial Thought: {llm_response}"]
        
        if "Intent: Schedule Appointment" in llm_response:
            print("Agent: Detected intent to schedule appointment. Using EHR tool.")
            available_slots = self.knowledge_base.retrieve_info("appointment availability")
            if available_slots:
                final_response_parts.append(f"Available slots: {', '.join(available_slots)}. Please specify your preferred time.")
                self._update_patient_context(patient_id, "available_slots", available_slots)
            else:
                final_response_parts.append("No appointment slots currently available.")
            
            if "schedule for" in user_query.lower():
                slot = user_query.lower().split("schedule for ")[-1].strip()
                if slot in available_slots:
                    ehr_result = self._tool_orchestration("ehr_interface", {"action": "schedule_appointment", "patient_id": patient_id, "data": {"date_time": slot}})
                    if ehr_result.get("status") == "success":
                        final_response_parts.append(f"Appointment confirmed for {slot}. Appointment ID: {ehr_result.get('appointment_id')}")
                    else:
                        final_response_parts.append(f"Failed to schedule appointment: {ehr_result.get('reason')}")
                else:
                    final_response_parts.append(f"Slot '{slot}' is not available.")
            
        elif "clarify" in llm_response.lower() or "more details" in llm_response.lower():
            final_response_parts.append(llm_response)
            
            if "my symptoms are" in user_query.lower():
                symptoms_str = user_query.lower().split("my symptoms are ")[-1].strip().split(", ")
                self._update_patient_context(patient_id, "symptoms", symptoms_str)
                final_response_parts.append(f"Agent: Noted symptoms: {', '.join(symptoms_str)}.")
                
                current_context_with_symptoms = self._get_patient_context(patient_id)
                llm_rerun_response = self.llm_core.process_query("diagnose me", current_context_with_symptoms)
                final_response_parts.append(f"Agent Refined Thought: {llm_rerun_response}")

                print("Agent: Consulting SymptomChecker tool...")
                checker_result = self._tool_orchestration("symptom_checker", {"symptoms": symptoms_str})
                final_response_parts.append(f"Symptom Checker Tool Output: {checker_result}")
                
                rag_info = self.knowledge_base.retrieve_info(f"diagnosis for {', '.join(symptoms_str)}")
                if rag_info:
                    final_response_parts.append(f"Knowledge Base (RAG) says: {rag_info}")
                
                self._update_patient_context(patient_id, "diagnosis_candidates", checker_result.get("possible_conditions", []))
                self._update_patient_context(patient_id, "rag_info", rag_info)
                
                synthesis_prompt = f"Synthesize diagnosis for patient with symptoms: {', '.join(symptoms_str)}. Symptom checker suggested: {checker_result.get('possible_conditions')}. RAG suggested: {rag_info}. Patient history: {current_context.get('history')}. Provide a preliminary diagnosis and next steps, explaining the reasoning."
                final_diagnosis_llm = self.llm_core.process_query(synthesis_prompt, self._get_patient_context(patient_id))
                final_response_parts.append(f"Agent Final Diagnosis Proposal (LLM Synthesis): {final_diagnosis_llm}")
                
                final_response_parts.append("\n--- Human-AI Collaboration ---")
                final_response_parts.append("This diagnosis is a preliminary AI assessment and requires review and confirmation by a medical professional.")
                self.memory.add_episodic_event({"patient_id": patient_id, "timestamp": str(datetime.datetime.now()), "query": user_query, "agent_response": final_diagnosis_llm})
                
                if "diagnosis" in final_diagnosis_llm.lower():
                    ehr_diagnosis = "Preliminary Assessment"
                    if "Common Cold" in final_diagnosis_llm: ehr_diagnosis = "Common Cold"
                    elif "Cardiac Issue" in final_diagnosis_llm: ehr_diagnosis = "Suspected Cardiac Issue"

                    ehr_record_result = self._tool_orchestration("ehr_interface", {"action": "record_diagnosis", "patient_id": patient_id, "data": {"diagnosis": ehr_diagnosis, "details": final_diagnosis_llm}})
                    final_response_parts.append(f"EHR Record Status: {ehr_record_result.get('status')}")

        else:
            final_response_parts.append(llm_response)

        integrated_response = "\n".join(final_response_parts)
        print(f"\nAgent: Final Integrated Response for Patient {patient_id}:\n{integrated_response}")
        return integrated_response

def run_healthcare_simulation():
    agent = HealthcareAgent()
    patient_id = "P101"

    print("--- Healthcare Agent Simulation Start ---")

    response1 = agent.handle_patient_query(patient_id, "I don't feel good.")

    response2 = agent.handle_patient_query(patient_id, "My symptoms are fever, cough, and a runny nose.")

    agent._update_patient_context(patient_id, "diagnosis", "Common Cold")
    response3 = agent.handle_patient_query(patient_id, "What's the best treatment for Common Cold?")

    response4 = agent.handle_patient_query(patient_id, "Can I schedule an appointment?")

    response5 = agent.handle_patient_query(patient_id, "I want to schedule for Monday 10 AM.")

    agent._update_patient_context(patient_id, "current_meds", ["Ibuprofen", "Warfarin (blood thinner)"])
    response6 = agent.handle_patient_query(patient_id, "Are there any interactions between Ibuprofen and Warfarin?")
    
    print("\n--- Healthcare Agent Simulation End ---")
    print("\n--- Agent's Episodic History ---")
    for event in agent.memory.get_episodic_history(patient_id):
        print(f"[{event['timestamp']}] Query: '{event['query']}' | Response: '{event['agent_response'][:70]}...'\n")

import io
import sys
old_stdout = sys.stdout
redirected_output = io.StringIO()
sys.stdout = redirected_output

run_healthcare_simulation()

sys.stdout = old_stdout

program_output = [redirected_output.getvalue()]

print(json.dumps(program_output))