import time
import concurrent.futures

def collect_demographics(patient_id, data):
    print(f"[Patient {patient_id}] Collecting demographics: {data['name']}...")
    time.sleep(1.2)
    print(f"[Patient {patient_id}] Demographics collected.")
    return {"patient_id": patient_id, "name": data['name'], "dob": data['dob']}

def prepare_medical_history_forms(patient_id):
    print(f"[Patient {patient_id}] Preparing medical history forms...")
    time.sleep(0.8)
    print(f"[Patient {patient_id}] Medical history forms ready.")
    return {"patient_id": patient_id, "forms_generated": True}

def process_initial_patient_data(patient_id, demographics, forms_status):
    print(f"[Patient {patient_id}] Consolidating initial data and preparing for next steps...")
    time.sleep(0.5)
    if demographics and forms_status["forms_generated"]:
        print(f"[Patient {patient_id}] Initial data processed for {demographics['name']}.")
        return True
    print(f"[Patient {patient_id}] Failed to process initial data.")
    return False

def verify_insurance(patient_id, policy_info):
    print(f"[Patient {patient_id}] Verifying insurance for policy: {policy_info['provider']}...")
    time.sleep(2.5)
    if "invalid" in policy_info['provider'].lower():
        print(f"[Patient {patient_id}] Insurance verification failed.")
        return False
    print(f"[Patient {patient_id}] Insurance verified successfully.")
    return True

def schedule_initial_consultation(patient_id, doctor_id, preferred_date):
    print(f"[Patient {patient_id}] Scheduling initial consultation with Dr. {doctor_id} for {preferred_date}...")
    time.sleep(1.8)
    print(f"[Patient {patient_id}] Consultation scheduled.")
    return True

def setup_patient_portal_access(patient_id, email):
    print(f"[Patient {patient_id}] Setting up patient portal access for {email}...")
    time.sleep(1.0)
    print(f"[Patient {patient_id}] Patient portal access set up.")
    return True

def finalize_onboarding_record(patient_id):
    print(f"[Patient {patient_id}] Finalizing patient onboarding record.")
    time.sleep(0.7)
    print(f"[Patient {patient_id}] Patient onboarding complete.")
    return True

def onboard_new_patient(patient_id, patient_data):
    print(f"\n--- Starting onboarding for Patient {patient_id} ({patient_data['name']}) ---")

    print(f"[Patient {patient_id}] Phase 1: Collecting basic info in parallel.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_demographics = executor.submit(collect_demographics, patient_id, patient_data['demographics'])
        future_forms = executor.submit(prepare_medical_history_forms, patient_id)

        demographics_result = future_demographics.result()
        forms_result = future_forms.result()

    print(f"[Patient {patient_id}] Phase 2: Processing initial collected data (sequential).")
    initial_data_processed = process_initial_patient_data(patient_id, demographics_result, forms_result)

    if not initial_data_processed:
        print(f"[Patient {patient_id}] Initial data processing failed. Aborting onboarding.")
        return

    print(f"[Patient {patient_id}] Phase 3: Initiating parallel tasks: Insurance, Scheduling, Portal Setup.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_insurance = executor.submit(verify_insurance, patient_id, patient_data['insurance'])
        future_consultation = executor.submit(schedule_initial_consultation, patient_id, patient_data['doctor_id'], patient_data['preferred_date'])
        future_portal = executor.submit(setup_patient_portal_access, patient_id, patient_data['email'])

        insurance_status = future_insurance.result()
        consultation_status = future_consultation.result()
        portal_status = future_portal.result()

    print(f"[Patient {patient_id}] Phase 4: Finalizing onboarding record (sequential).")
    if insurance_status and consultation_status and portal_status:
        finalize_onboarding_record(patient_id)
    else:
        print(f"[Patient {patient_id}] One or more critical Phase 3 tasks failed. Onboarding incomplete.")

    print(f"--- Finished onboarding for Patient {patient_id} ---")

if __name__ == "__main__":
    patients_to_onboard = [
        {
            "id": "P001",
            "name": "Alice Smith",
            "demographics": {"name": "Alice Smith", "dob": "1990-01-15"},
            "insurance": {"provider": "BlueCross", "policy_number": "ABC12345"},
            "doctor_id": "Dr. Jones",
            "preferred_date": "2024-07-20",
            "email": "alice.s@example.com"
        },
        {
            "id": "P002",
            "name": "Bob Johnson",
            "demographics": {"name": "Bob Johnson", "dob": "1985-05-22"},
            "insurance": {"provider": "InvalidInsurance", "policy_number": "XYZ98765"},
            "doctor_id": "Dr. Green",
            "preferred_date": "2024-07-25",
            "email": "bob.j@example.com"
        }
    ]

    for patient in patients_to_onboard:
        onboard_new_patient(patient["id"], patient)
