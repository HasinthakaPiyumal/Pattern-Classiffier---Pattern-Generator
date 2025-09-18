import json
import time

class SimulatedLLM:
    def __init__(self):
        self.medical_knowledge_base = {
            "symptoms_conditions": {
                "fever": ["Flu", "Common Cold", "Infection"],
                "cough": ["Flu", "Common Cold", "Bronchitis", "Allergies"],
                "sore throat": ["Common Cold", "Strep Throat", "Tonsillitis"],
                "headache": ["Migraine", "Tension Headache", "Sinusitis"],
                "fatigue": ["Flu", "Common Cold", "Anemia", "Chronic Fatigue Syndrome"]
            },
            "condition_details": {
                "Flu": {"description": "Viral infection, often with fever, cough, body aches.", "severity": "moderate", "recommendation": "Rest, fluids, consult doctor if severe.", "related_symptoms": ["fever", "cough", "fatigue", "body aches"]},
                "Common Cold": {"description": "Mild viral infection, runny nose, sore throat.", "severity": "mild", "recommendation": "Rest, fluids, OTC meds.", "related_symptoms": ["cough", "sore throat", "runny nose"]},
                "Migraine": {"description": "Severe headache, often with throbbing pain, sensitivity to light/sound.", "severity": "severe", "recommendation": "Consult doctor for diagnosis and treatment.", "related_symptoms": ["headache", "nausea", "light sensitivity"]}
            },
            "drug_interactions": {
                "ibuprofen_aspirin": "Increased risk of gastrointestinal bleeding.",
                "antibiotics_antacids": "Reduced absorption of antibiotics."
            }
        }

    def generate_response(self, prompt, context=None):
        if "symptoms" in prompt.lower() and context and "symptoms" in context:
            symptoms = context["symptoms"]
            possible_conditions = []
            for symptom in symptoms:
                if symptom.lower() in self.medical_knowledge_base["symptoms_conditions"]:
                    possible_conditions.extend(self.medical_knowledge_base["symptoms_conditions"][symptom.lower()])
            
            if possible_conditions:
                # Simple frequency count for plausible conditions
                condition_counts = {cond: possible_conditions.count(cond) for cond in set(possible_conditions)}
                sorted_conditions = sorted(condition_counts.items(), key=lambda item: item[1], reverse=True)
                top_conditions = [cond for cond, count in sorted_conditions if count > 0]

                if top_conditions:
                    response = f"Based on your symptoms ({', '.join(symptoms)}), potential conditions could include: {', '.join(top_conditions[:3])}.\n"
                    if top_conditions[0] in self.medical_knowledge_base["condition_details"]:
                        details = self.medical_knowledge_base["condition_details"][top_conditions[0]]
                        response += f"For instance, {top_conditions[0]} is described as: {details['description']}. Recommendation: {details['recommendation']}"
                    response += "\nThis is not a substitute for professional medical advice. Please consult a doctor for diagnosis."
                    return response
            return "I couldn't identify specific conditions based on these symptoms. Please consult a medical professional."
        
        if "condition details" in prompt.lower() and context and "condition" in context:
            condition = context["condition"]
            if condition in self.medical_knowledge_base["condition_details"]:
                details = self.medical_knowledge_base["condition_details"][condition]
                return f"Details for {condition}: {details['description']} Severity: {details['severity']}. Recommendation: {details['recommendation']}"
            return f"I don't have detailed information for {condition}."

        if "drug interaction" in prompt.lower() and context and "drugs" in context:
            drug1, drug2 = context["drugs"]
            interaction_key = f"{drug1.lower()}_{drug2.lower()}"
            reverse_interaction_key = f"{drug2.lower()}_{drug1.lower()}"
            if interaction_key in self.medical_knowledge_base["drug_interactions"]:
                return f"Interaction between {drug1} and {drug2}: {self.medical_knowledge_base['drug_interactions'][interaction_key]}"
            elif reverse_interaction_key in self.medical_knowledge_base["drug_interactions"]:
                return f"Interaction between {drug1} and {drug2}: {self.medical_knowledge_base['drug_interactions'][reverse_interaction_key]}"
            return f"No known significant interaction found between {drug1} and {drug2} in my current knowledge base. Always consult a pharmacist or doctor."

        return "I'm a medical assistant. Please describe your symptoms or ask about a medical condition or drug interaction."

class MemorySystem:
    def __init__(self):
        self.working_memory = {}
        self.episodic_memory = [] # Past patient queries and agent responses
        self.semantic_memory = {
            "medical_glossary": {"fever": "elevated body temperature", "analgesic": "pain reliever"},
            "common_illnesses": ["flu", "cold", "allergies"]
        }
        self.procedural_memory = {
            "symptom_analysis_flow": ["Collect symptoms", "Search knowledge base", "Suggest conditions", "Recommend actions"],
            "drug_interaction_check_flow": ["Identify drugs", "Query interaction database", "Report findings"]
        }
        self.knowledge_graph_nodes = {
            "Fever": {"type": "symptom", "related_to": ["Flu", "Infection"]},
            "Flu": {"type": "condition", "causes": ["Influenza Virus"], "treatments": ["Rest", "Antivirals"]}
        }

    def store_working_memory(self, key, value):
        self.working_memory[key] = value

    def retrieve_working_memory(self, key):
        return self.working_memory.get(key)

    def add_episodic_memory(self, interaction):
        self.episodic_memory.append((time.time(), interaction))

    def get_semantic_info(self, query):
        for term, desc in self.semantic_memory["medical_glossary"].items():
            if query.lower() in term.lower():
                return f"Semantic info for '{term}': {desc}"
        return None
    
    def get_procedural_info(self, skill_name):
        return self.procedural_memory.get(skill_name)

    def reason_on_knowledge_graph(self, query_node):
        # Simulate simple KG reasoning
        if query_node in self.knowledge_graph_nodes:
            node_info = self.knowledge_graph_nodes[query_node]
            return f"Knowledge Graph info for {query_node}: Type: {node_info['type']}, Related: {node_info.get('related_to', [])}, Causes: {node_info.get('causes', [])}"
        return "Node not found in KG."

class ToolKit:
    def search_medical_database(self, query_terms):
        # Simulate retrieving information from a medical database (RAG)
        time.sleep(0.1)
        found_info = []
        llm_kb = SimulatedLLM().medical_knowledge_base
        for term in query_terms:
            if term.lower() in llm_kb["symptoms_conditions"]:
                found_info.append(f"Symptom '{term}' linked to conditions: {llm_kb['symptoms_conditions'][term.lower()]}")
            if term in llm_kb["condition_details"]:
                details = llm_kb["condition_details"][term]
                found_info.append(f"Condition '{term}': {details['description']}")
        return {"success": True, "data": found_info if found_info else "No relevant information found.", "query": query_terms}

    def check_drug_interactions(self, drug1, drug2):
        # Simulate an API call to a drug interaction checker
        time.sleep(0.1)
        llm_kb = SimulatedLLM().medical_knowledge_base
        interaction_key = f"{drug1.lower()}_{drug2.lower()}"
        reverse_interaction_key = f"{drug2.lower()}_{drug1.lower()}"
        if interaction_key in llm_kb["drug_interactions"] or reverse_interaction_key in llm_kb["drug_interactions"]:
            return {"success": True, "interaction_found": True, "drugs": [drug1, drug2]}
        return {"success": True, "interaction_found": False, "drugs": [drug1, drug2]}

    def find_nearest_clinic(self, location="user_location_simulated"):
        # Simulate finding a clinic based on location
        time.sleep(0.2)
        return {"success": True, "data": f"Nearest clinic: General Health Clinic, 123 Main St, open until 5 PM. (Simulated for {location})"}

class MedicalAssistantAgent:
    def __init__(self):
        self.llm = SimulatedLLM()
        self.memory = MemorySystem()
        self.toolkit = ToolKit()
        self.current_plan = []

    def _orchestrate_tools(self, tool_name, *args, **kwargs):
        tool_func = getattr(self.toolkit, tool_name, None)
        if tool_func:
            try:
                result = tool_func(*args, **kwargs)
                if not result.get("success"): 
                    self.memory.add_episodic_memory(f"Tool {tool_name} failed: {result.get('error')}")
                return result
            except Exception as e:
                self.memory.add_episodic_memory(f"Error executing tool {tool_name}: {e}")
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Tool not found"}

    def _parse_symptoms_from_query(self, query):
        known_symptoms = list(self.llm.medical_knowledge_base["symptoms_conditions"].keys())
        found_symptoms = [symptom for symptom in known_symptoms if symptom in query.lower()]
        return found_symptoms if found_symptoms else None

    def _parse_drugs_from_query(self, query):
        # Simple parser for two drugs
        query_lower = query.lower()
        if "ibuprofen" in query_lower and "aspirin" in query_lower:
            return "ibuprofen", "aspirin"
        if "antibiotics" in query_lower and "antacids" in query_lower:
            return "antibiotics", "antacids"
        return None, None

    def _plan_and_execute(self, user_query):
        response = ""
        symptoms = self._parse_symptoms_from_query(user_query)
        drug1, drug2 = self._parse_drugs_from_query(user_query)

        if symptoms:
            self.current_plan = ["analyze_symptoms", "provide_condition_info"]
            self.memory.store_working_memory("current_symptoms", symptoms)
        elif drug1 and drug2:
            self.current_plan = ["check_drug_interactions"]
            self.memory.store_working_memory("current_drugs", (drug1, drug2))
        elif "nearest clinic" in user_query.lower() or "find a doctor" in user_query.lower():
            self.current_plan = ["find_clinic"]
        elif "what is" in user_query.lower() or "tell me about" in user_query.lower():
            # Example of LLM clarifying intent or extracting entity
            condition_keywords = [k.lower() for k in self.llm.medical_knowledge_base["condition_details"].keys()]
            found_condition = next((c for c in condition_keywords if c in user_query.lower()), None)
            if found_condition:
                self.current_plan = ["get_condition_details"]
                self.memory.store_working_memory("current_condition", found_condition.capitalize())
            else:
                self.current_plan = ["direct_llm_response"]
        else:
            self.current_plan = ["direct_llm_response"]

        for step in self.current_plan:
            if step == "analyze_symptoms":
                current_symptoms = self.memory.retrieve_working_memory("current_symptoms")
                rag_output = self._orchestrate_tools("search_medical_database", current_symptoms)
                self.memory.store_working_memory("rag_symptom_data", rag_output["data"])
                llm_context = {"symptoms": current_symptoms, "rag_data": rag_output["data"]}
                response = self.llm.generate_response(f"Analyze symptoms: {', '.join(current_symptoms)}", context=llm_context)
                # Example of KG reasoning for additional context
                if "fever" in current_symptoms:
                    kg_info = self.memory.reason_on_knowledge_graph("Fever")
                    response += f"\nAdditional context from medical knowledge graph: {kg_info}"
            
            elif step == "provide_condition_info":
                # This step is often integrated within the LLM's initial symptom analysis for brevity.
                pass # LLM already handled this in 'analyze_symptoms' step

            elif step == "check_drug_interactions":
                drug1, drug2 = self.memory.retrieve_working_memory("current_drugs")
                tool_output = self._orchestrate_tools("check_drug_interactions", drug1, drug2)
                llm_context = {"drugs": [drug1, drug2], "interaction_result": tool_output}
                response = self.llm.generate_response(f"Check interaction between {drug1} and {drug2}", context=llm_context)
            
            elif step == "get_condition_details":
                condition = self.memory.retrieve_working_memory("current_condition")
                llm_context = {"condition": condition}
                response = self.llm.generate_response(f"Tell me about {condition}", context=llm_context)

            elif step == "find_clinic":
                tool_output = self._orchestrate_tools("find_nearest_clinic")
                if tool_output["success"]:
                    response = tool_output["data"]
                else:
                    response = "Could not find a clinic at this time."

            elif step == "direct_llm_response":
                response = self.llm.generate_response(user_query)

        return response

    def process_query(self, user_query):
        self.memory.add_episodic_memory(f"User Query: {user_query}")
        print(f"\nUser: {user_query}")

        response = self._plan_and_execute(user_query)

        self.memory.add_episodic_memory(f"Agent Response: {response}")
        return response

# Real-world Usage Simulation: Healthcare Medical Assistant
medical_agent = MedicalAssistantAgent()

print(medical_agent.process_query("I have a fever and cough."))
print(medical_agent.process_query("What are the details of Migraine?"))
print(medical_agent.process_query("Check drug interactions between Ibuprofen and Aspirin."))
print(medical_agent.process_query("Where is the nearest clinic?"))

# Simulation Pattern: Handling a more generic query or unknown symptom
print(medical_agent.process_query("My stomach hurts.")) # Symptom not in simplified KB
