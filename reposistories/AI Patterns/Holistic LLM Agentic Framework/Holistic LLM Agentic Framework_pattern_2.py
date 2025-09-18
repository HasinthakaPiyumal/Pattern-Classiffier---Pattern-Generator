import random

class SimulatedLLM:
    def __init__(self, name="CoreMedLLM"):
        self.name = name
        self.reasoning_trace = []

    def _simulate_reasoning(self, prompt, context):
        self.reasoning_trace.append(f"LLM: Analyzing prompt '{prompt}' with context: {context}")
        if "symptoms" in context:
            if "fever" in context["symptoms"] and "cough" in context["symptoms"]:
                return "potential respiratory infection"
            elif "headache" in context["symptoms"] and "nausea" in context["symptoms"]:
                return "migraine or other neurological concern"
        if "diagnostic_result" in context:
            if "positive for influenza" in context["diagnostic_result"]:
                return "influenza treatment plan"
        return "general health advice"

    def understand_intent_and_orchestrate(self, user_query, current_state):
        self.reasoning_trace = []
        self.reasoning_trace.append(f"LLM: Understanding intent for query: '{user_query}'")
        query_lower = user_query.lower()
        if "symptoms" in query_lower or "feel unwell" in query_lower:
            intent = "diagnose_symptoms"
            self.reasoning_trace.append("LLM: Intent identified: Diagnose Symptoms.")
        elif "treatment for" in query_lower or "how to cure" in query_lower:
            intent = "propose_treatment"
            self.reasoning_trace.append("LLM: Intent identified: Propose Treatment.")
        elif "explain" in query_lower or "what is" in query_lower:
            intent = "explain_condition"
            self.reasoning_trace.append("LLM: Intent identified: Explain Condition.")
        else:
            intent = "general_inquiry"
            self.reasoning_trace.append("LLM: Intent identified: General Inquiry.")

        context = {"user_query": user_query, "current_state": current_state, "intent": intent}
        reasoning_output = self._simulate_reasoning(user_query, context)
        self.reasoning_trace.append(f"LLM: Core reasoning output: {reasoning_output}")
        return {"intent": intent, "reasoning_output": reasoning_output, "trace": self.reasoning_trace}

    def generate_response(self, context):
        response_template = f"Based on your query and our analysis ({context.get('intent', 'unknown intent')} leading to {context.get('reasoning_output', 'no specific conclusion')}): "
        if context["intent"] == "diagnose_symptoms":
            return response_template + "We need to run some diagnostics. Please describe your symptoms in more detail."
        elif context["intent"] == "propose_treatment":
            return response_template + f"For {context['reasoning_output']}, consider rest and hydration. We might suggest specific medication after a doctor's consultation."
        elif context["intent"] == "explain_condition":
            return response_template + f"A {context['reasoning_output']} is a common ailment often caused by viruses."
        else:
            return response_template + "I'm here to help with your health questions. How can I assist you further?"

class KnowledgeBase:
    def __init__(self, data):
        self.data = data

    def retrieve(self, query, strategy="simple"):
        retrieved_info = []
        for key, value in self.data.items():
            if query.lower() in key.lower() or query.lower() in value.lower():
                retrieved_info.append(f"{key}: {value}")
        return " ".join(retrieved_info) if retrieved_info else "No specific information found."

class PatientMemory:
    def __init__(self):
        self.working_memory = {} 
        self.episodic_memory = [] 
        self.semantic_memory = {
            "patient_id": "P101",
            "allergies": ["penicillin"],
            "conditions": ["hypertension"],
            "medications": ["lisinopril"]
        }
        self.procedural_memory = {
            "diagnose_symptoms": "Run DiagnosticTool, then ProposeTreatment.",
            "propose_treatment": "Consult MedicalKnowledgeBase, then PrescriptionTool."
        }

    def update_working_memory(self, key, value):
        self.working_memory[key] = value

    def add_episodic_memory(self, interaction):
        self.episodic_memory.append(interaction)

    def get_patient_profile(self):
        return self.semantic_memory

    def get_procedural_guidance(self, task):
        return self.procedural_memory.get(task, "No specific procedure known.")

class DiagnosticTool:
    def execute(self, symptoms):
        print(f"Executing Diagnostic Tool for symptoms: {symptoms}")
        if "fever" in symptoms and "cough" in symptoms:
            return {"result": "positive for influenza", "confidence": 0.85}
        elif "headache" in symptoms:
            return {"result": "migraine suspected", "confidence": 0.7}
        return {"result": "inconclusive", "confidence": 0.5}

class PrescriptionTool:
    def execute(self, condition, patient_profile):
        print(f"Executing Prescription Tool for condition: {condition}, patient: {patient_profile['patient_id']}")
        if "influenza" in condition.lower() and "penicillin" in patient_profile.get("allergies", []):
            print("Guardrail triggered: Patient is allergic to penicillin. Suggesting alternative.")
            return "Recommend Tamiflu (non-penicillin based) and rest."
        elif "influenza" in condition.lower():
            return "Recommend rest, fluids, and potentially antiviral medication (e.g., Tamiflu) if early."
        return "Consult a doctor for specific medication."

class HealthcareAgent:
    def __init__(self):
        self.llm = SimulatedLLM()
        self.knowledge_base = KnowledgeBase({
            "influenza": "Influenza is a viral infection that attacks your respiratory system.",
            "migraine": "A migraine is a severe headache often accompanied by nausea and sensitivity to light/sound.",
            "treatment for influenza": "Rest, fluids, antiviral drugs (e.g., Tamiflu), pain relievers."
        })
        self.patient_memory = PatientMemory()
        self.diagnostic_tool = DiagnosticTool()
        self.prescription_tool = PrescriptionTool()
        self.current_state = {}

    def process_query(self, user_query):
        self.patient_memory.update_working_memory("last_query", user_query)
        self.patient_memory.add_episodic_memory({"query": user_query, "timestamp": "now"})

        llm_analysis = self.llm.understand_intent_and_orchestrate(user_query, self.current_state)
        intent = llm_analysis["intent"]
        reasoning_output = llm_analysis["reasoning_output"]
        print("\n--- LLM Orchestration & Reasoning Trace ---")
        for step in llm_analysis["trace"]:
            print(step)
        print("------------------------------------------")

        response_context = {"intent": intent, "reasoning_output": reasoning_output}

        retrieved_info = self.knowledge_base.retrieve(user_query)
        self.patient_memory.update_working_memory("retrieved_kb", retrieved_info)
        response_context["retrieved_info"] = retrieved_info
        print(f"Memory: Retrieved knowledge for '{user_query}': {retrieved_info}")
        print(f"Memory: Patient profile: {self.patient_memory.get_patient_profile()}")

        if intent == "diagnose_symptoms":
            symptoms_str = user_query.replace("my symptoms are ", "").replace("i feel unwell with ", "")
            self.patient_memory.update_working_memory("current_symptoms", symptoms_str)
            diagnostic_result = self.diagnostic_tool.execute(symptoms_str)
            self.patient_memory.update_working_memory("diagnostic_result", diagnostic_result)
            response_context["diagnostic_result"] = diagnostic_result
            response_context["reasoning_output"] = diagnostic_result["result"]
            print(f"Tool: Diagnostic result: {diagnostic_result}")
            llm_analysis_after_tool = self.llm.understand_intent_and_orchestrate(
                f"Based on diagnostic result: {diagnostic_result['result']}",
                {"symptoms": symptoms_str, "diagnostic_result": diagnostic_result["result"]}
            )
            response_context["intent"] = llm_analysis_after_tool["intent"]
            response_context["reasoning_output"] = llm_analysis_after_tool["reasoning_output"]
            print("--- LLM Re-orchestration Trace after Tool ---")
            for step in llm_analysis_after_tool["trace"]:
                print(step)
            print("------------------------------------------")

        if intent == "propose_treatment" or (intent == "diagnose_symptoms" and "result" in response_context.get("diagnostic_result", {})):
            condition_for_treatment = response_context.get("diagnostic_result", {}).get("result", reasoning_output)
            if condition_for_treatment and condition_for_treatment != "inconclusive":
                treatment_advice = self.prescription_tool.execute(condition_for_treatment, self.patient_memory.get_patient_profile())
                response_context["treatment_advice"] = treatment_advice
                response_context["reasoning_output"] = treatment_advice
                print(f"Tool: Treatment advice: {treatment_advice}")
            else:
                response_context["treatment_advice"] = "Cannot propose specific treatment without a clear diagnosis."
                print("Tool: No specific treatment proposed due to inconclusive diagnosis.")

        self.patient_memory.add_episodic_memory({"response_context": response_context, "timestamp": "now"})

        explanation = f"We've analyzed your request using our medical intelligence ({response_context['reasoning_output']})."
        if "diagnostic_result" in response_context:
            explanation += f" Our diagnostic tool indicated: {response_context['diagnostic_result']['result']}."
        if "treatment_advice" in response_context:
            explanation += f" Our prescription guidance suggests: {response_context['treatment_advice']}."
        explanation += f" Retrieved knowledge: {response_context['retrieved_info']}"
        response_context["explanation"] = explanation
        print(f"Explainability: {explanation}")

        final_response = self.llm.generate_response(response_context)
        return final_response, self.patient_memory.working_memory

if __name__ == "__main__":
    agent = HealthcareAgent()
    print("Healthcare Agent Activated. Type 'exit' to quit.")

    queries = [
        "I feel unwell, my symptoms are fever and a cough.",
        "What is influenza?",
        "What is the treatment for influenza?",
        "I have a headache and nausea."
    ]

    for query in queries:
        print(f"\n--- User Query: {query} ---")
        response, state = agent.process_query(query)
        print(f"\nAgent Response: {response}")
        print(f"Current Agent State (Working Memory): {state}")
