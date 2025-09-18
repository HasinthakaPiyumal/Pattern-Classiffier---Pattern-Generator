class PatientRecord:
    def __init__(self, patient_id, name, diagnosis, sensitive_info=""):
        self._patient_id = patient_id
        self._name = name
        self._diagnosis = diagnosis
        self._sensitive_info = sensitive_info

    def get_patient_id(self):
        return self._patient_id

    def get_name(self):
        return self._name

    def get_diagnosis(self):
        return self._diagnosis

    def get_sensitive_info(self):
        return "Access Denied: Sensitive Info" # Default restricted access

    def display_record(self):
        return f"Patient ID: {self.get_patient_id()}, Name: {self.get_name()}, Diagnosis: {self.get_diagnosis()}"

class RecordAccessDecorator:
    def __init__(self, decorated_record):
        self._decorated_record = decorated_record

    def get_patient_id(self):
        return self._decorated_record.get_patient_id()

    def get_name(self):
        return self._decorated_record.get_name()

    def get_diagnosis(self):
        return self._decorated_record.get_diagnosis()

    def get_sensitive_info(self):
        return self._decorated_record.get_sensitive_info()

    def display_record(self):
        return self._decorated_record.display_record()

class DoctorAccessDecorator(RecordAccessDecorator):
    def get_sensitive_info(self):
        return f"Sensitive Info (Doctor View): {self._decorated_record._sensitive_info}"

    def display_record(self):
        base_display = super().display_record()
        return f"{base_display}, {self.get_sensitive_info()}"

class NurseAccessDecorator(RecordAccessDecorator):
    def get_diagnosis(self):
        return f"Diagnosis (Nurse View): {self._decorated_record._diagnosis} (limited details)"

    def display_record(self):
        base_display = f"Patient ID: {self.get_patient_id()}, Name: {self.get_name()}, {self.get_diagnosis()}"
        return base_display

class AdminAccessDecorator(RecordAccessDecorator):
    def get_patient_id(self):
        return f"Admin ID: {self._decorated_record._patient_id}"

    def get_name(self):
        return f"Admin Name: {self._decorated_record._name}"

    def get_diagnosis(self):
        return f"Admin Diagnosis: {self._decorated_record._diagnosis}"

    def get_sensitive_info(self):
        return f"Admin Sensitive Info: {self._decorated_record._sensitive_info}"

    def display_record(self):
        return (f"{self.get_patient_id()}, {self.get_name()}, {self.get_diagnosis()}, "
                f"{self.get_sensitive_info()}")

if __name__ == "__main__":
    patient_data = PatientRecord("P101", "Alice Smith", "Flu", "Prescribed Tamiflu, allergic to Penicillin")

    print("--- Base Record Access ---")
    print(patient_data.display_record())
    print(f"Sensitive info attempt: {patient_data.get_sensitive_info()}")

    print("\n--- Nurse Access ---")
    nurse_view = NurseAccessDecorator(patient_data)
    print(nurse_view.display_record())
    print(f"Sensitive info attempt by nurse: {nurse_view.get_sensitive_info()}")

    print("\n--- Doctor Access ---")
    doctor_view = DoctorAccessDecorator(patient_data)
    print(doctor_view.display_record())
    print(f"Sensitive info attempt by doctor: {doctor_view.get_sensitive_info()}")

    print("\n--- Admin Access ---")
    admin_view = AdminAccessDecorator(patient_data)
    print(admin_view.display_record())
    print(f"Sensitive info attempt by admin: {admin_view.get_sensitive_info()}")

    print("\n--- Chained Access (Doctor on Nurse view) ---")
    chained_view = DoctorAccessDecorator(NurseAccessDecorator(patient_data))
    print(chained_view.display_record())
    print(f"Sensitive info attempt by chained view: {chained_view.get_sensitive_info()}")