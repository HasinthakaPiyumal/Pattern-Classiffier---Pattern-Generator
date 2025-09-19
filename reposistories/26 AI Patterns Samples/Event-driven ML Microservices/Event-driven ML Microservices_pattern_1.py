import uuid
import time
import random

class Event:
    def __init__(self, type, payload):
        self.type = type
        self.payload = payload
        self.timestamp = time.time()
        self.id = str(uuid.uuid4())

class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event):
        if event.type in self._subscribers:
            for callback in self._subscribers[event.type]:
                callback(event)

class PatientDataIngestionService:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def ingest_patient_data(self, patient_record):
        print(f"Ingestion: Receiving patient record {patient_record['patient_id']}")
        event = Event("NewPatientDataEvent", patient_record)
        self.event_bus.publish(event)

class DataPreprocessingService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        event_bus.subscribe("NewPatientDataEvent", self.preprocess_data)

    def preprocess_data(self, event):
        patient_data = event.payload
        patient_id = patient_data['patient_id']
        processed_data = patient_data.copy()
        processed_data['heart_rate'] = float(patient_data.get('heart_rate', 70))
        processed_data['temperature'] = float(patient_data.get('temperature', 98.6))
        processed_data['blood_pressure_sys'] = float(patient_data.get('blood_pressure_sys', 120))
        processed_data['blood_pressure_dia'] = float(patient_data.get('blood_pressure_dia', 80))
        processed_data['lab_results_normalized'] = {
            'white_blood_cell_count': float(patient_data.get('lab_results', {}).get('wbc', 7.0)) / 10.0,
            'creatinine': float(patient_data.get('lab_results', {}).get('creatinine', 0.8)) / 1.5
        }
        print(f"Preprocessing: Cleaned and normalized data for patient {patient_id}")
        self.event_bus.publish(Event("ProcessedPatientDataEvent", processed_data))

class RiskScoreCalculationService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        event_bus.subscribe("ProcessedPatientDataEvent", self.calculate_risk_score)

    def calculate_risk_score(self, event):
        processed_data = event.payload
        patient_id = processed_data['patient_id']
        risk_score = 0.0
        if processed_data['heart_rate'] > 100 or processed_data['heart_rate'] < 50:
            risk_score += 0.3
        if processed_data['temperature'] > 100.4 or processed_data['temperature'] < 96.8:
            risk_score += 0.4
        if processed_data['blood_pressure_sys'] > 140 or processed_data['blood_pressure_sys'] < 90:
            risk_score += 0.2
        if processed_data['lab_results_normalized']['white_blood_cell_count'] > 1.2:
            risk_score += 0.5
        if processed_data['lab_results_normalized']['creatinine'] > 1.0:
            risk_score += 0.3

        risk_level = "Low"
        if risk_score > 0.8:
            risk_level = "High"
        elif risk_score > 0.4:
            risk_level = "Medium"
        
        risk_assessment = {
            "patient_id": patient_id,
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "timestamp": time.time()
        }
        print(f"RiskCalculation: Calculated risk for patient {patient_id}: {risk_level} (Score: {risk_assessment['risk_score']})")
        self.event_bus.publish(Event("RiskScoreCalculatedEvent", risk_assessment))

class RecommendationService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        event_bus.subscribe("RiskScoreCalculatedEvent", self.generate_recommendations)

    def generate_recommendations(self, event):
        risk_assessment = event.payload
        patient_id = risk_assessment['patient_id']
        recommendations = []
        if risk_assessment['risk_level'] == "High":
            recommendations.append("Immediate physician review required.")
            recommendations.append("Consider blood cultures and broad-spectrum antibiotics.")
        elif risk_assessment['risk_level'] == "Medium":
            recommendations.append("Monitor vitals closely every 4 hours.")
            recommendations.append("Consult with specialist if no improvement in 24 hours.")
        else:
            recommendations.append("Continue routine monitoring.")

        print(f"Recommendation: For patient {patient_id} ({risk_assessment['risk_level']} risk): {', '.join(recommendations)}")

event_bus = EventBus()

ingestion_service = PatientDataIngestionService(event_bus)
preprocessing_service = DataPreprocessingService(event_bus)
risk_calculation_service = RiskScoreCalculationService(event_bus)
recommendation_service = RecommendationService(event_bus)

print("--- Simulating Healthcare Patient Risk Assessment Pipeline ---")
patient_records_to_simulate = [
    {"patient_id": "P001", "heart_rate": 72, "temperature": 98.2, "blood_pressure_sys": 120, "blood_pressure_dia": 80, "lab_results": {"wbc": 6.5, "creatinine": 0.7}},
    {"patient_id": "P002", "heart_rate": 110, "temperature": 101.5, "blood_pressure_sys": 100, "blood_pressure_dia": 60, "lab_results": {"wbc": 15.0, "creatinine": 1.1}},
    {"patient_id": "P003", "heart_rate": 85, "temperature": 99.0, "blood_pressure_sys": 135, "blood_pressure_dia": 85, "lab_results": {"wbc": 9.0, "creatinine": 0.9}},
    {"patient_id": "P004", "heart_rate": 60, "temperature": 97.0, "blood_pressure_sys": 110, "blood_pressure_dia": 70, "lab_results": {"wbc": 5.0, "creatinine": 0.6}},
]

for i, record in enumerate(patient_records_to_simulate):
    print(f"\n--- Processing Patient Record {i+1} ---")
    ingestion_service.ingest_patient_data(record)
    time.sleep(0.1)
print("\n--- Simulation Complete ---")