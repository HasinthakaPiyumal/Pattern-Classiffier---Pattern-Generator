import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def create_patient_record(patient_id, name):
    print(f"Patient {patient_id}: Creating patient record for {name}...")
    time.sleep(random.uniform(1.0, 2.0))
    if random.random() < 0.05:
        print(f"Patient {patient_id}: Failed to create patient record!")
        return False
    print(f"Patient {patient_id}: Patient record created.")
    return True

def verify_insurance(patient_id, insurance_info):
    print(f"Patient {patient_id}: Verifying insurance for {insurance_info['provider']}...")
    time.sleep(random.uniform(1.5, 3.0))
    if random.random() < 0.15:
        print(f"Patient {patient_id}: Insurance verification failed!")
        return False
    print(f"Patient {patient_id}: Insurance verified successfully.")
    return True

def schedule_initial_consultation(patient_id, doctor_id):
    print(f"Patient {patient_id}: Scheduling initial consultation with Doctor {doctor_id}...")
    time.sleep(random.uniform(1.0, 2.5))
    print(f"Patient {patient_id}: Initial consultation scheduled.")
    return True

def send_welcome_packet(patient_id, address):
    print(f"Patient {patient_id}: Preparing and sending welcome packet to {address}...")
    time.sleep(random.uniform(0.8, 1.8))
    print(f"Patient {patient_id}: Welcome packet sent.")
    return True

def onboard_new_patient(patient_id, name, insurance_info, doctor_id, address):
    print(f"\n--- Starting patient onboarding for Patient {patient_id} ({name}) ---")
    record_created = create_patient_record(patient_id, name)
    if not record_created:
        print(f"Patient {patient_id}: Onboarding failed due to record creation failure.")
        return False
    print(f"Patient {patient_id}: Record created, executing parallel onboarding tasks...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(verify_insurance, patient_id, insurance_info): "Insurance Verification",
            executor.submit(schedule_initial_consultation, patient_id, doctor_id): "Consultation Scheduling",
            executor.submit(send_welcome_packet, patient_id, address): "Welcome Packet Sending"
        }
        results = {}
        for future in as_completed(futures):
            task_name = futures[future]
            try:
                result = future.result()
                results[task_name] = result
                print(f"Patient {patient_id}: Task '{task_name}' completed with result: {result}")
            except Exception as exc:
                results[task_name] = f"Failed: {exc}"
                print(f"Patient {patient_id}: Task '{task_name}' generated an exception: {exc}")
    all_parallel_tasks_successful = all(results.values())
    if all_parallel_tasks_successful:
        print(f"--- Patient {patient_id} onboarding completed successfully! ---")
    else:
        print(f"--- Patient {patient_id} onboarding completed with some issues! ---")
    return all_parallel_tasks_successful

if __name__ == "__main__":
    patient_data = [
        {"id": "P001", "name": "Alice Smith", "insurance": {"provider": "BlueCare", "policy": "ABC123"}, "doctor": "Dr. Lee", "address": "101 Elm St"},
        {"id": "P002", "name": "Bob Johnson", "insurance": {"provider": "HealthNet", "policy": "XYZ789"}, "doctor": "Dr. Kim", "address": "202 Pine Ave"}
    ]
    for patient in patient_data:
        onboard_new_patient(patient["id"], patient["name"], patient["insurance"], patient["doctor"], patient["address"])
