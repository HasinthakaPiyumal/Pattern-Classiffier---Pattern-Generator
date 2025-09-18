import datetime

def require_admin_access(func):
    def wrapper(patient_id, user_role):
        print(f"Checking access for user role: {user_role}...")
        if user_role not in ["admin", "doctor"]:
            print(f"Access DENIED for user role '{user_role}'. Only 'admin' or 'doctor' can view records.")
            return None
        print(f"Access GRANTED for user role '{user_role}'.")
        return func(patient_id, user_role)
    return wrapper

def audit_record_access(func):
    def wrapper(patient_id, user_role):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"AUDIT: User '{user_role}' attempting to access patient '{patient_id}' at {timestamp}.")
        result = func(patient_id, user_role)
        if result:
            print(f"AUDIT: Access to patient '{patient_id}' by '{user_role}' was successful.")
        else:
            print(f"AUDIT: Access to patient '{patient_id}' by '{user_role}' was denied.")
        return result
    return wrapper

def encrypt_data_on_access(func):
    def wrapper(patient_id, user_role):
        print(f"Encrypting patient data for secure viewing...")
        data = func(patient_id, user_role)
        if data:
            encrypted_data = f"Encrypted({data})"
            print(f"Data encrypted.")
            return encrypted_data
        return data
    return wrapper

@audit_record_access
@require_admin_access
@encrypt_data_on_access
def get_patient_details(patient_id, user_role):
    patient_data = {
        "P001": {"name": "Alice Smith", "dob": "1980-05-15", "condition": "Hypertension"},
        "P002": {"name": "Bob Johnson", "dob": "1992-11-22", "condition": "Asthma"}
    }
    details = patient_data.get(patient_id)
    if details:
        print(f"Retrieved details for patient {patient_id}: {details}")
    else:
        print(f"Patient {patient_id} not found.")
    return details

if __name__ == "__main__":
    print("--- Doctor accessing P001 ---")
    details1 = get_patient_details("P001", "doctor")
    print(f"Result: {details1}\n")

    print("--- Nurse accessing P002 (should be denied) ---")
    details2 = get_patient_details("P002", "nurse")
    print(f"Result: {details2}\n")

    print("--- Admin accessing P001 ---")
    details3 = get_patient_details("P001", "admin")
    print(f"Result: {details3}\n")