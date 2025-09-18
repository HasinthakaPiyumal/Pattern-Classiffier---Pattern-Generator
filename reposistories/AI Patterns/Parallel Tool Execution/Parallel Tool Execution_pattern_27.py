import time
import concurrent.futures

def collect_demographics(patient_id, data):
    time.sleep(1)
    return f"Patient {patient_id}: Demographics collected: {data['name']}."

def verify_insurance(patient_id, insurance_info):
    time.sleep(2.5)
    return f"Patient {patient_id}: Insurance verification for {insurance_info['provider']} completed."

def schedule_initial_consultation(patient_id, preferred_date):
    time.sleep(1.8)
    return f"Patient {patient_id}: Initial consultation scheduled for {preferred_date}."

def create_medical_record(patient_id, basic_info):
    time.sleep(2.2)
    return f"Patient {patient_id}: Medical record created with DOB {basic_info['dob']}."

def assign_primary_care_physician(patient_id, record_status):
    time.sleep(1.5)
    if "Medical record created" in record_status:
        return f"Patient {patient_id}: Primary Care Physician assigned."
    return f"Patient {patient_id}: Failed to assign PCP due to record status."

def send_welcome_kit(patient_id, address):
    time.sleep(1.0)
    return f"Patient {patient_id}: Welcome kit dispatched to {address}."

def finalize_onboarding(patient_id):
    time.sleep(0.5)
    return f"Patient {patient_id}: Onboarding finalized."

def onboard_new_patient(patient_data):
    patient_id = patient_data["patient_id"]
    demographics = patient_data["demographics"]
    insurance = patient_data["insurance"]
    consult_date = patient_data["consultation_date"]
    address = patient_data["address"]

    print(f"--- Starting onboarding for Patient {patient_id} ---")

    demographics_result = collect_demographics(patient_id, demographics)
    print(demographics_result)
    time.sleep(0.3)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_insurance = executor.submit(verify_insurance, patient_id, insurance)
        future_consultation = executor.submit(schedule_initial_consultation, patient_id, consult_date)
        future_medical_record = executor.submit(create_medical_record, patient_id, demographics)
        future_welcome_kit = executor.submit(send_welcome_kit, patient_id, address)

        medical_record_result = future_medical_record.result()
        print(medical_record_result)

        other_parallel_results = []
        for future in concurrent.futures.as_completed([future_insurance, future_consultation, future_welcome_kit]):
            other_parallel_results.append(future.result())
        for res in other_parallel_results:
            print(res)

    pcp_assignment_result = assign_primary_care_physician(patient_id, medical_record_result)
    print(pcp_assignment_result)

    final_status = finalize_onboarding(patient_id)
    print(final_status)
    print(f"--- Finished onboarding for Patient {patient_id} ---")

if __name__ == "__main__":
    patient_details = {
        "patient_id": "P-789012",
        "demographics": {"name": "Jane Doe", "dob": "1990-05-15", "gender": "Female"},
        "insurance": {"provider": "HealthCare Inc.", "policy_id": "HCI-5678"},
        "consultation_date": "2023-10-26",
        "address": "456 Oak Ave, Healthville, USA"
    }
    onboard_new_patient(patient_details)