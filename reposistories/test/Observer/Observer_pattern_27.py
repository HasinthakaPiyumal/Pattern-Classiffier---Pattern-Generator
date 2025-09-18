class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)

class Patient(Subject):
    def __init__(self, patient_id, name):
        super().__init__()
        self._patient_id = patient_id
        self._name = name
        self._heart_rate = 70
        self._temperature = 98.6
        print(f"Patient '{self._name}' (ID: {self._patient_id}) admitted.")

    @property
    def patient_id(self):
        return self._patient_id

    @property
    def name(self):
        return self._name

    @property
    def heart_rate(self):
        return self._heart_rate

    @heart_rate.setter
    def heart_rate(self, new_hr):
        if self._heart_rate != new_hr:
            old_hr = self._heart_rate
            self._heart_rate = new_hr
            print(f"Patient {self._name}'s heart rate changed from {old_hr} to {new_hr} bpm.")
            self.notify("vitals_update", vital_type="heart_rate", value=new_hr)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, new_temp):
        if self._temperature != new_temp:
            old_temp = self._temperature
            self._temperature = new_temp
            print(f"Patient {self._name}'s temperature changed from {old_temp:.1f} to {new_temp:.1f}°F.")
            self.notify("vitals_update", vital_type="temperature", value=new_temp)

class NurseStationDisplay:
    def __init__(self, station_id):
        self.station_id = station_id

    def update(self, subject, event_type, **kwargs):
        if event_type == "vitals_update":
            vital_type = kwargs["vital_type"]
            value = kwargs["value"]
            if vital_type == "heart_rate":
                print(f"Nurse Station {self.station_id}: Displaying {subject.name} (ID:{subject.patient_id}) - Heart Rate: {value} bpm")
            elif vital_type == "temperature":
                print(f"Nurse Station {self.station_id}: Displaying {subject.name} (ID:{subject.patient_id}) - Temperature: {value:.1f}°F")

class DoctorAlertSystem:
    def __init__(self):
        self.critical_hr_low = 50
        self.critical_hr_high = 100
        self.critical_temp_high = 101.0

    def update(self, subject, event_type, **kwargs):
        if event_type == "vitals_update":
            vital_type = kwargs["vital_type"]
            value = kwargs["value"]
            alert_triggered = False
            message = ""

            if vital_type == "heart_rate":
                if value < self.critical_hr_low:
                    message = f"CRITICAL ALERT! Doctor needed for {subject.name} (ID:{subject.patient_id}): Heart Rate {value} bpm (Too Low!)"
                    alert_triggered = True
                elif value > self.critical_hr_high:
                    message = f"CRITICAL ALERT! Doctor needed for {subject.name} (ID:{subject.patient_id}): Heart Rate {value} bpm (Too High!)"
                    alert_triggered = True
            elif vital_type == "temperature":
                if value > self.critical_temp_high:
                    message = f"CRITICAL ALERT! Doctor needed for {subject.name} (ID:{subject.patient_id}): Temperature {value:.1f}°F (Fever!)"
                    alert_triggered = True

            if alert_triggered:
                print(f"*** Doctor Alert System: {message} ***")

class MedicalRecordSystem:
    def __init__(self):
        pass

    def update(self, subject, event_type, **kwargs):
        if event_type == "vitals_update":
            vital_type = kwargs["vital_type"]
            value = kwargs["value"]
            print(f"Medical Record System: Logging vital for {subject.name} (ID:{subject.patient_id}) - {vital_type.replace('_', ' ').title()}: {value}")

# Simulation of a Healthcare patient monitoring system
print("--- Healthcare Patient Monitoring Simulation ---")
patient_john = Patient("P001", "John Doe")

nurse_display = NurseStationDisplay("NS1")
doctor_alert = DoctorAlertSystem()
medical_record = MedicalRecordSystem()

patient_john.attach(nurse_display)
patient_john.attach(doctor_alert)
patient_john.attach(medical_record)

print("\n--- Scenario 1: Normal Vitals ---")
patient_john.heart_rate = 72
patient_john.temperature = 98.8

print("\n--- Scenario 2: High Heart Rate ---")
patient_john.heart_rate = 110 

print("\n--- Scenario 3: Fever ---")
patient_john.temperature = 102.5 

print("\n--- Scenario 4: Low Heart Rate (after detaching an observer) ---")
patient_john.detach(nurse_display)
patient_john.heart_rate = 45 
