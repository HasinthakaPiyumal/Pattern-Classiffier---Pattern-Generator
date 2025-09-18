import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def tool_register_patient_demographics(patient_data):
    patient_id = patient_data['id']
    print(f"[{time.time():.2f}] Registering patient demographics for {patient_id} ({patient_data['name']})...")
    time.sleep(random.uniform(1.0, 2.0))
    if random.random() < 0.05:
        print(f"[{time.time():.2f}] Patient registration FAILED for {patient_id}.")
        return None
    print(f"[{time.time():.2f}] Patient {patient_id} demographics registered.")
    return f"PAT-{patient_id}"

def tool_verify_insurance(patient_internal_id, insurance_info):
    print(f"[{time.time():.2f}] Verifying insurance for {patient_internal_id} (Policy: {insurance_info['policy_number']})...")
    time.sleep(random.uniform(1.5, 2.5))
    if random.random() < 0.15:
        print(f"[{time.time():.2f}] Insurance verification FAILED for {patient_internal_id}.")
        return False
    print(f"[{time.time():.2f}] Insurance verified for {patient_internal_id}.")
    return True

def tool_schedule_initial_appointment(patient_internal_id, preferred_date):
    print(f"[{time.time():.2f}] Scheduling initial appointment for {patient_internal_id} (Preferred: {preferred_date})...")
    time.sleep(random.uniform(1.0, 2.0))
    appointment_time = (time.time() + random.randint(86400, 259200))
    print(f"[{time.time():.2f}] Appointment scheduled for {patient_internal_id} on {time.ctime(appointment_time)}.")
    return True

def tool_prepare_medical_history_forms(patient_internal_id):
    print(f"[{time.time():.2f}] Preparing medical history forms for {patient_internal_id}...")
    time.sleep(random.uniform(0.8, 1.8))
    print(f"[{time.time():.2f}] Medical history forms prepared for {patient_internal_id}.")
    return True

def onboard_patient(patient_details):
    patient_id = patient_details['id']
    patient_name = patient_details['name']
    insurance_info = patient_details['insurance']
    preferred_appointment_date = patient_details['preferred_appointment_date']

    print(f"\n[{time.time():.2f}] Starting onboarding for Patient {patient_name} (ID: {patient_id})...")

    internal_patient_id = tool_register_patient_demographics(patient_details)
    if not internal_patient_id:
        print(f"[{time.time():.2f}] Patient {patient_name} onboarding halted due to registration failure.")
        return False

    print(f"[{time.time():.2f}] Demographics registered. Initiating parallel tasks for {patient_name}...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(tool_verify_insurance, internal_patient_id, insurance_info): "Insurance Verification",
            executor.submit(tool_schedule_initial_appointment, internal_patient_id, preferred_appointment_date): "Appointment Scheduling",
            executor.submit(tool_prepare_medical_history_forms, internal_patient_id): "Forms Preparation"
        }

        results = {}
        for future in as_completed(futures):
            task_name = futures[future]
            try:
                result = future.result()
                results[task_name] = "SUCCESS" if result else "FAILURE"
            except Exception as exc:
                results[task_name] = f"ERROR: {exc}"
            print(f"[{time.time():.2f}] Task '{task_name}' completed with result: {results[task_name]}")

    overall_success = all(res == "SUCCESS" for res in results.values())
    print(f"[{time.time():.2f}] All parallel tasks for Patient {patient_name} completed. Overall success: {overall_success}")
    return overall_success

if __name__ == "__main__":
    patient_1 = {
        'id': 'P-001',
        'name': 'Alice Smith',
        'dob': '1985-03-15',
        'insurance': {'provider': 'HealthCo', 'policy_number': 'ABC12345'},
        'preferred_appointment_date': '2024-07-20'
    }
    patient_2 = {
        'id': 'P-002',
        'name': 'Bob Johnson',
        'dob': '1990-11-22',
        'insurance': {'provider': 'CareCorp', 'policy_number': 'XYZ98765'},
        'preferred_appointment_date': '2024-07-25'
    }

    onboard_patient(patient_1)
    print("-" * 50)
    onboard_patient(patient_2)