import concurrent.futures
import time
import random

def register_patient_demographics(patient_data):
    print(f"[{time.time():.2f}] Registering patient demographics for {patient_data['name']}...")
    time.sleep(random.uniform(1.0, 2.0)) # Simulate database write
    patient_id = f"PAT{random.randint(10000, 99999)}"
    print(f"[{time.time():.2f}] Patient {patient_data['name']} registered with ID: {patient_id}.")
    return {"status": "success", "patient_id": patient_id, "name": patient_data['name']}

def collect_medical_history(patient_id):
    print(f"[{time.time():.2f}] Collecting medical history for patient {patient_id}...")
    time.sleep(random.uniform(2.0, 4.0)) # Simulate patient questionnaire or nurse interview
    print(f"[{time.time():.2f}] Medical history collected for patient {patient_id}.")
    return {"status": "success", "history": "Completed"}

def verify_insurance(patient_id, insurance_info):
    print(f"[{time.time():.2f}] Verifying insurance for patient {patient_id} (Provider: {insurance_info['provider']})...")
    time.sleep(random.uniform(1.5, 3.0)) # Simulate external API call to insurance provider
    is_active = random.choice([True, True, True, False]) # Simulate occasional insurance issues
    if is_active:
        print(f"[{time.time():.2f}] Insurance verified for patient {patient_id}. Status: Active.")
        return {"status": "success", "coverage": "Active"}
    else:
        print(f"[{time.time():.2f}] Insurance verification failed for patient {patient_id}. Status: Inactive/Problem.")
        return {"status": "failed", "coverage": "Inactive", "reason": "Verification failed"}

def schedule_initial_consultation(patient_id, preferred_date):
    print(f"[{time.time():.2f}] Scheduling initial consultation for patient {patient_id} on {preferred_date}...")
    time.sleep(random.uniform(1.0, 2.5)) # Simulate calendar system interaction
    appointment_time = f"{preferred_date} {random.randint(9, 16)}:00"
    print(f"[{time.time():.2f}] Initial consultation scheduled for patient {patient_id} at {appointment_time}.")
    return {"status": "success", "appointment": appointment_time}

def prepare_patient_chart(patient_id, demographics, history, insurance, appointment):
    print(f"[{time.time():.2f}] Preparing patient chart for {demographics['name']} (ID: {patient_id})...")
    time.sleep(random.uniform(1.0, 2.0)) # Simulate compiling data into EHR
    print(f"[{time.time():.2f}] Patient chart for {demographics['name']} prepared.")
    return {"status": "success", "chart_ready": True}

def process_patient_intake(patient_input):
    print(f"\n[{time.time():.2f}] --- Starting patient intake for {patient_input['name']} ---")

    # Step 1: Sequential - Register patient demographics (essential first step)
    demographics_result = register_patient_demographics(patient_input)
    if demographics_result['status'] == 'failed':
        print(f"[{time.time():.2f}] Patient intake failed: Demographics registration failed.")
        return {"intake_status": "failed", "reason": "demographics_failed"}
    patient_id = demographics_result['patient_id']

    # Step 2: Parallel execution of independent tasks
    # Medical history collection, insurance verification, and appointment scheduling can happen concurrently
    print(f"[{time.time():.2f}] Initiating parallel tasks for patient {patient_id}...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        history_future = executor.submit(collect_medical_history, patient_id)
        insurance_future = executor.submit(verify_insurance, patient_id, patient_input['insurance'])
        appointment_future = executor.submit(schedule_initial_consultation, patient_id, patient_input['preferred_date'])

        medical_history_result = history_future.result()
        insurance_result = insurance_future.result()
        appointment_result = appointment_future.result()

    if insurance_result['status'] == 'failed':
        print(f"[{time.time():.2f}] Patient intake for {patient_id} has issues: Insurance verification failed. Proceeding with caution...")
        # In a real system, this might halt or trigger a manual review process

    # Step 3: Sequential dependent task - Prepare patient chart (requires all prior info)
    print(f"[{time.time():.2f}] All parallel tasks completed for patient {patient_id}. Preparing patient chart.")
    chart_result = prepare_patient_chart(patient_id, demographics_result, medical_history_result, insurance_result, appointment_result)

    print(f"[{time.time():.2f}] --- Patient intake for {demographics_result['name']} complete ---")
    return {
        "intake_status": "completed",
        "patient_id": patient_id,
        "demographics": demographics_result,
        "medical_history": medical_history_result,
        "insurance": insurance_result,
        "appointment": appointment_result,
        "chart": chart_result
    }

if __name__ == "__main__":
    patient1_data = {
        'name': 'Jane Doe',
        'dob': '1990-01-15',
        'address': '789 Pine Ln',
        'insurance': {'provider': 'HealthCo', 'policy_number': 'ABC12345'},
        'preferred_date': '2024-07-20'
    }
    intake_status = process_patient_intake(patient1_data)
    print(f"\nFinal Intake Status for {patient1_data['name']}: {intake_status['intake_status']}")

    patient2_data = {
        'name': 'John Smith',
        'dob': '1985-05-22',
        'address': '101 Birch St',
        'insurance': {'provider': 'CarePlus', 'policy_number': 'XYZ67890'},
        'preferred_date': '2024-07-25'
    }
    print("\n--- Simulating a patient with potential insurance issues ---")
    random.seed(2) # Make insurance fail for the next call for demonstration
    intake_status = process_patient_intake(patient2_data)
    print(f"\nFinal Intake Status for {patient2_data['name']}: {intake_status['intake_status']}")
