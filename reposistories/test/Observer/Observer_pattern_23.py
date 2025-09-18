class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

class Patient(Subject):
    def __init__(self, name, patient_id):
        super().__init__()
        self.name = name
        self.patient_id = patient_id
        self._heart_rate = 70
        self._temperature = 37.0

    @property
    def heart_rate(self):
        return self._heart_rate

    @heart_rate.setter
    def heart_rate(self, value):
        if self._heart_rate != value:
            self._heart_rate = value
            self.notify()

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if self._temperature != value:
            self._temperature = value
            self.notify()

class NurseStationDisplay:
    def update(self, patient):
        print(f"Healthcare: Nurse Station: Displaying patient {patient.name} ({patient.patient_id}): HR={patient.heart_rate}, Temp={patient.temperature}°C")
        if patient.heart_rate > 100 or patient.temperature > 38.5:
            print(f"Healthcare: Nurse Station: ALERT! {patient.name} requires immediate attention.")

class DoctorPager:
    def update(self, patient):
        if patient.heart_rate > 100 or patient.temperature > 38.5:
            print(f"Healthcare: Doctor Pager: Paging doctor for {patient.name} ({patient.patient_id}). Vitals abnormal: HR={patient.heart_rate}, Temp={patient.temperature}°C")

class MedicalRecordUpdater:
    def update(self, patient):
        print(f"Healthcare: Medical Records: Updating {patient.name}'s ({patient.patient_id}) record: HR={patient.heart_rate}, Temp={patient.temperature}°C")

patient_john = Patient("John Doe", "P101")

nurse_display = NurseStationDisplay()
doctor_pager = DoctorPager()
record_updater = MedicalRecordUpdater()

patient_john.attach(nurse_display)
patient_john.attach(doctor_pager)
patient_john.attach(record_updater)

print("--- Healthcare Simulation: Initial Vitals ---")
patient_john.heart_rate = 72
patient_john.temperature = 37.1

print("\n--- Healthcare Simulation: Vitals change (normal range) ---")
patient_john.heart_rate = 75
patient_john.temperature = 37.2

print("\n--- Healthcare Simulation: Vitals change (abnormal range) ---")
patient_john.heart_rate = 110
patient_john.temperature = 39.0

print("\n--- Healthcare Simulation: Doctor pager detached, vitals return to normal ---")
patient_john.detach(doctor_pager)
patient_john.heart_rate = 80
patient_john.temperature = 37.5