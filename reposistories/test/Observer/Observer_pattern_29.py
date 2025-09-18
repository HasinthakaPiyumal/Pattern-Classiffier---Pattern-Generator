import abc

class SubjectHealthcare(abc.ABC):
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.receive_update(self)

class ObserverHealthcare(abc.ABC):
    @abc.abstractmethod
    def receive_update(self, subject):
        pass

class PatientVitalsMonitor(SubjectHealthcare):
    def __init__(self, patient_id):
        super().__init__()
        self._patient_id = patient_id
        self._heart_rate = 0
        self._temperature = 0.0
        self._blood_pressure = (0, 0)

    @property
    def patient_id(self):
        return self._patient_id

    @property
    def heart_rate(self):
        return self._heart_rate

    @heart_rate.setter
    def heart_rate(self, hr):
        if hr != self._heart_rate:
            self._heart_rate = hr
            self.notify_observers()

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temp):
        if temp != self._temperature:
            self._temperature = temp
            self.notify_observers()

    @property
    def blood_pressure(self):
        return self._blood_pressure

    @blood_pressure.setter
    def blood_pressure(self, bp):
        if bp != self._blood_pressure:
            self._blood_pressure = bp
            self.notify_observers()

class NurseStationDisplay(ObserverHealthcare):
    def receive_update(self, monitor):
        print(f"NURSE STATION: Patient {monitor.patient_id} - HR:{monitor.heart_rate}, Temp:{monitor.temperature:.1f}C, BP:{monitor.blood_pressure[0]}/{monitor.blood_pressure[1]}")

class DoctorAlertSystem(ObserverHealthcare):
    def receive_update(self, monitor):
        if monitor.heart_rate > 100 or monitor.heart_rate < 50:
            print(f"DOCTOR ALERT: Patient {monitor.patient_id} - Critical Heart Rate: {monitor.heart_rate} bpm!")
        if monitor.temperature > 38.5 or monitor.temperature < 35.0:
            print(f"DOCTOR ALERT: Patient {monitor.patient_id} - Abnormal Temperature: {monitor.temperature:.1f}C!")
        if monitor.blood_pressure[0] > 140 or monitor.blood_pressure[1] < 60:
            print(f"DOCTOR ALERT: Patient {monitor.patient_id} - Concerning Blood Pressure: {monitor.blood_pressure[0]}/{monitor.blood_pressure[1]}!")

class MedicalRecordUpdater(ObserverHealthcare):
    def receive_update(self, monitor):
        print(f"MEDICAL RECORDS: Patient {monitor.patient_id} vitals logged - HR:{monitor.heart_rate}, Temp:{monitor.temperature:.1f}C, BP:{monitor.blood_pressure[0]}/{monitor.blood_pressure[1]}")

if __name__ == "__main__":
    print("--- Healthcare Patient Vitals Monitoring Simulation ---")
    patient_a_monitor = PatientVitalsMonitor("P101")

    nurse_display = NurseStationDisplay()
    doctor_alert = DoctorAlertSystem()
    medical_recorder = MedicalRecordUpdater()

    patient_a_monitor.register_observer(nurse_display)
    patient_a_monitor.register_observer(doctor_alert)
    patient_a_monitor.register_observer(medical_recorder)

    print("\n--- Event 1: Initial Vitals ---")
    patient_a_monitor.heart_rate = 72
    patient_a_monitor.temperature = 36.8
    patient_a_monitor.blood_pressure = (120, 80)

    print("\n--- Event 2: Heart Rate Increase ---")
    patient_a_monitor.heart_rate = 95

    print("\n--- Event 3: Temperature Spike ---")
    patient_a_monitor.temperature = 39.2 # Doctor alert!

    print("\n--- Event 4: Blood Pressure Drop ---")
    patient_a_monitor.blood_pressure = (100, 55) # Doctor alert!

    print("\n--- Event 5: Vitals Stabilize ---")
    patient_a_monitor.heart_rate = 70
    patient_a_monitor.temperature = 37.0
    patient_a_monitor.blood_pressure = (115, 75)

    print("\n--- Event 6: Critical Heart Rate ---")
    patient_a_monitor.heart_rate = 110 # Doctor alert!

    print("\n--- Event 7: Unregister Medical Recorder ---")
    patient_a_monitor.unregister_observer(medical_recorder)
    patient_a_monitor.temperature = 36.9 # Only nurse and doctor react