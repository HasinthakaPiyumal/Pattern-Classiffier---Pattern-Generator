import abc
import random

class TriageStrategy(abc.ABC):
    @abc.abstractmethod
    def assess_patient(self, patient_info):
        pass

class EmergencyTriage(TriageStrategy):
    def assess_patient(self, patient_info):
        condition = patient_info.get("condition", "unknown").lower()
        if "cardiac arrest" in condition or "severe trauma" in condition or "unresponsive" in condition:
            print(f"Patient {patient_info['id']}: IMMEDIATE ATTENTION (Emergency Triage - Critical).")
            return "Critical"
        elif "difficulty breathing" in condition or "severe pain" in condition:
            print(f"Patient {patient_info['id']}: URGENT ATTENTION (Emergency Triage - Urgent).")
            return "Urgent"
        else:
            print(f"Patient {patient_info['id']}: Standard Emergency Queue (Emergency Triage - Stable).")
            return "Stable"

class PediatricTriage(TriageStrategy):
    def assess_patient(self, patient_info):
        age = patient_info.get("age", 0)
        condition = patient_info.get("condition", "unknown").lower()
        if age < 2 and ("fever" in condition or "lethargy" in condition):
            print(f"Patient {patient_info['id']} (Age {age}): URGENT PEDIATRIC ATTENTION (Pediatric Triage - High Risk Infant).")
            return "Urgent Pediatric"
        elif age < 12 and ("fracture" in condition or "high fever" in condition):
            print(f"Patient {patient_info['id']} (Age {age}): Standard Pediatric Queue (Pediatric Triage - Moderate).")
            return "Moderate Pediatric"
        else:
            print(f"Patient {patient_info['id']} (Age {age}): Routine Pediatric Check (Pediatric Triage - Routine).")
            return "Routine Pediatric"

class GeneralPracticeTriage(TriageStrategy):
    def assess_patient(self, patient_info):
        condition = patient_info.get("condition", "unknown").lower()
        if "cold symptoms" in condition or "rash" in condition:
            print(f"Patient {patient_info['id']}: Routine appointment recommended (General Practice Triage - Minor).")
            return "Minor"
        elif "chronic pain" in condition or "follow-up" in condition:
            print(f"Patient {patient_info['id']}: Scheduled appointment (General Practice Triage - Managed).")
            return "Managed"
        else:
            print(f"Patient {patient_info['id']}: General consultation (General Practice Triage - General).")
            return "General"

class TriageSystem:
    def __init__(self, default_strategy: TriageStrategy):
        self._strategy = default_strategy
        self._patients_queue = []

    def set_triage_strategy(self, strategy: TriageStrategy):
        self._strategy = strategy

    def add_patient(self, patient_id, age, condition):
        patient_info = {"id": patient_id, "age": age, "condition": condition}
        self._patients_queue.append(patient_info)
        print(f"\nAdded patient {patient_id} (Age: {age}, Condition: '{condition}')")

    def process_patient(self):
        if not self._patients_queue:
            print("No patients in queue.")
            return

        patient = self._patients_queue.pop(0)
        self._strategy.assess_patient(patient)

if __name__ == "__main__":
    triage_system = TriageSystem(GeneralPracticeTriage())

    triage_system.add_patient("P001", 35, "Severe Trauma")
    triage_system.add_patient("P002", 7, "High Fever")
    triage_system.add_patient("P003", 60, "Cold Symptoms")
    triage_system.add_patient("P004", 1, "Lethargy and Fever")
    triage_system.add_patient("P005", 45, "Difficulty Breathing")

    print("\n--- Processing patients with initial General Practice Triage ---")
    triage_system.process_patient()

    triage_system.set_triage_strategy(EmergencyTriage())
    print("\n--- Processing patients with Emergency Triage ---")
    triage_system.process_patient()
    triage_system.process_patient()
    triage_system.add_patient("P006", 55, "Cardiac Arrest")
    triage_system.process_patient()

    triage_system.set_triage_strategy(PediatricTriage())
    print("\n--- Processing patients with Pediatric Triage ---")
    triage_system.process_patient()
    triage_system.process_patient()