import json

class HealthcareLLM:
    def __init__(self, medical_knowledge_graph, tools, agents):
        self.medical_knowledge_graph = medical_knowledge_graph
        self.tools = tools
        self.agents = agents
        self.patient_profile = {"name": "John Doe", "conditions": [], "preferences": {"language": "en"}}
        self.working_memory = {}
        self.episodic_memory = []

    def _query_knowledge_graph(self, topic):
        if topic in self.medical_knowledge_graph:
            return self.medical_knowledge_graph[topic]
        for condition, details in self.medical_knowledge_graph.items():
            if "symptoms" in details and topic in details["symptoms"]:
                return details
            if "specialists" in details and topic in details["specialists"]:
                return details
        return {"description": "Information not found in medical knowledge graph."}

    def _understand_intent(self, query):
        query_lower = query.lower()
        if "symptoms" in query_lower or "diagnose" in query_lower or "cough" in query_lower or "fever" in query_lower:
            return "analyze_symptoms", {"symptoms_query": query}
        elif "find doctor" in query_lower or "specialist" in query_lower or "appointment" in query_lower:
            return "schedule_appointment", {"appointment_query": query}
        elif "explain" in query_lower or "what is" in query_lower:
            return "explain_condition", {"condition_query": query}
        return "general_inquiry", {"query": query}

    def _orchestrate_agents_and_tools(self, intent, params):
        if intent == "analyze_symptoms":
            return self.agents["symptom_analyzer"].process(params["symptoms_query"], self.patient_profile)
        elif intent == "schedule_appointment":
            return self.agents["appointment_scheduler"].process(params["appointment_query"], self.patient_profile, self.tools)
        elif intent == "explain_condition":
            condition_info = self._query_knowledge_graph(params["condition_query"].replace("explain ", "").replace("what is ", "").strip("?. "))
            return f"Based on our medical knowledge: {condition_info.get('description', 'Could not find details.')} Common symptoms: {', '.join(condition_info.get('symptoms', []))}. Recommended specialists: {', '.join(condition_info.get('specialists', []))}."
        return "I'm here to help with your healthcare needs. How can I assist you further?"

    def process_query(self, user_query):
        intent, params = self._understand_intent(user_query)
        self.working_memory["last_intent"] = intent
        self.working_memory["last_params"] = params
        self.episodic_memory.append({"query": user_query, "intent": intent, "params": params})

        response = self._orchestrate_agents_and_tools(intent, params)

        if "diagnosed with" in response.lower() and "condition" in self.working_memory:
            condition = self.working_memory["condition"]
            if condition not in self.patient_profile["conditions"]:
                self.patient_profile["conditions"].append(condition)
                response += f"\nI've added '{condition}' to your patient profile for future reference."

        return response

class HealthcareTools:
    def find_specialist(self, specialty, location="near you"):
        specialists = {
            "dermatologist": ["Dr. Emily Chen (Dermatology Clinic)", "Dr. Alex Lee (Skin Health Center)"],
            "cardiologist": ["Dr. Sarah Miller (Heart Institute)"],
            "general practitioner": ["Dr. David Green (Family Care)"]
        }
        found = specialists.get(specialty.lower(), [])
        return f"Found {len(found)} {specialty} specialist(s) {location}: {', '.join(found) if found else 'None'}"

    def schedule_appointment(self, doctor, date, time):
        if "booked" in date:
            return False, f"Sorry, {doctor} is fully booked on {date}. Please try another date."
        return True, f"Appointment with {doctor} scheduled for {date} at {time}."

class SymptomAnalyzerAgent:
    def __init__(self, medical_knowledge_graph):
        self.medical_knowledge_graph = medical_knowledge_graph

    def process(self, symptoms_query, patient_profile):
        symptoms_query_lower = symptoms_query.lower()
        if "cough" in symptoms_query_lower and "fever" in symptoms_query_lower:
            possible_condition = "Flu"
            self.medical_knowledge_graph["flu"]["description"] = "Influenza (flu) is a contagious respiratory illness caused by flu viruses." 
            return f"Based on your symptoms (cough, fever), it sounds like you might have the {possible_condition}. It's often accompanied by body aches and fatigue. I recommend resting and consulting a General Practitioner."
        elif "skin rash" in symptoms_query_lower:
            possible_condition = "Eczema"
            return f"A persistent skin rash could indicate {possible_condition} or an allergic reaction. A Dermatologist would be the best specialist to consult."
        return "I need more specific symptoms to provide a potential analysis. Please describe them in more detail."

class AppointmentSchedulerAgent:
    def __init__(self, llm_core):
        self.llm_core = llm_core

    def process(self, appointment_query, patient_profile, tools):
        query_lower = appointment_query.lower()
        specialty = "general practitioner"
        doctor_name = "Dr. David Green"
        date = "tomorrow"
        time = "10 AM"

        if "dermatologist" in query_lower:
            specialty = "dermatologist"
            doctor_name = "Dr. Emily Chen"
        elif "cardiologist" in query_lower:
            specialty = "cardiologist"
            doctor_name = "Dr. Sarah Miller"

        if "next Tuesday" in query_lower:
            date = "next Tuesday"
        elif "fully booked" in query_lower:
            date = "fully booked"

        specialist_info = tools.find_specialist(specialty)
        if "None" in specialist_info:
            return f"I couldn't find a {specialty} specialist. Can you provide more details?"

        success, message = tools.schedule_appointment(doctor_name, date, time)
        if success:
            return f"Okay, I've scheduled your appointment with {doctor_name} for {date} at {time}. {specialist_info}"
        else:
            return f"{message} Would you like me to try another date or specialist?"

if __name__ == "__main__" :
    medical_knowledge_graph = {
        "flu": {
            "description": "Influenza (flu) is a contagious respiratory illness caused by flu viruses. It can cause mild to severe illness, and at times can lead to death.",
            "symptoms": ["fever", "cough", "sore throat", "body aches", "fatigue"],
            "specialists": ["general practitioner"]
        },
        "eczema": {
            "description": "Eczema is a condition that causes dry, itchy, inflamed skin. It's common in children but can occur at any age.",
            "symptoms": ["skin rash", "itchiness", "dry skin"],
            "specialists": ["dermatologist"]
        },
        "diabetes": {
            "description": "Diabetes is a chronic disease that occurs either when the pancreas does not produce enough insulin or when the body cannot effectively use the insulin it produces.",
            "symptoms": ["frequent urination", "increased thirst", "unexplained weight loss"],
            "specialists": ["endocrinologist", "general practitioner"]
        }
    }

    healthcare_tools = HealthcareTools()

    symptom_analyzer_agent = SymptomAnalyzerAgent(medical_knowledge_graph)
    appointment_scheduler_agent = AppointmentSchedulerAgent(None)

    healthcare_agent = HealthcareLLM(
        medical_knowledge_graph,
        healthcare_tools,
        {"symptom_analyzer": symptom_analyzer_agent, "appointment_scheduler": appointment_scheduler_agent}
    )

    print("--- Healthcare Navigator Simulation ---")

    user_query = "I have a persistent cough and a fever. What could it be?"
    print(f"\nUser: {user_query}")
    response = healthcare_agent.process_query(user_query)
    print(f"Agent: {response}")
    print(f"Patient Profile (after): {healthcare_agent.patient_profile}")

    user_query = "I need to find a dermatologist and book an appointment for next Tuesday."
    print(f"\nUser: {user_query}")
    response = healthcare_agent.process_query(user_query)
    print(f"Agent: {response}")

    user_query = "Can you explain what diabetes is?"
    print(f"\nUser: {user_query}")
    response = healthcare_agent.process_query(user_query)
    print(f"Agent: {response}")

    user_query = "Book an appointment with Dr. Emily Chen, but she's fully booked."
    print(f"\nUser: {user_query}")
    response = healthcare_agent.process_query(user_query)
    print(f"Agent: {response}")

    print("\n--- Agent Memory Snapshot ---")
    print(f"Working Memory: {healthcare_agent.working_memory}")
    print(f"Episodic Memory (last 2): {healthcare_agent.episodic_memory[-2:]}")