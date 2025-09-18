import concurrent.futures
import time
import random

def collect_demographics(patient_id, data):
    print(f"[Patient {patient_id}] Collecting demographics: {data['name']}...")
    time.sleep(random.uniform(0.8, 1.2)) # Simulate data entry/database write
    print(f"[Patient {patient_id}] Demographics collected.")
    return {"status": "success", "patient_info": data}

def verify_insurance(patient_id, insurance_info):
    print(f"[Patient {patient_id}] Verifying insurance for {insurance_info['provider']}...")
    time.sleep(random.uniform(1.5, 2.5)) # Simulate external insurance API call
    is_valid = random.choice([True, True, False]) # Simulate occasional rejection
    if is_valid:
        print(f"[Patient {patient_id}] Insurance verified successfully.")
    else:
        print(f"[Patient {patient_id}] Insurance verification failed.")
    return {"status": "success" if is_valid else "failed", "coverage": "active" if is_valid else "inactive"}

def create_ehr_entry(patient_id, patient_info):
    print(f"[Patient {patient_id}] Creating Electronic Health Record entry...")
    time.sleep(random.uniform(1.0, 2.0)) # Simulate EHR system API call/database write
    ehr_id = f"EHR-{patient_id}-{random.randint(100,999)}"
    print(f"[Patient {patient_id}] EHR entry created with ID: {ehr_id}.")
    return {"status": "success", "ehr_id": ehr_id}

def assign_primary_care_physician(patient_id, patient_info, insurance_status):
    print(f"[Patient {patient_id}] Assigning Primary Care Physician...")
    time.sleep(random.uniform(0.7, 1.0)) # Simulate internal logic/database lookup
    physician = "Dr. Alice Smith" if insurance_status == "active" else "Dr. John Doe (General)"
    print(f"[Patient {patient_id}] Assigned PCP: {physician}.")
    return {"status": "success", "pcp": physician}

def schedule_initial_consultation(patient_id, pcp):
    print(f"[Patient {patient_id}] Scheduling initial consultation with {pcp}...")
    time.sleep(random.uniform(1.2, 1.8)) # Simulate calendar system API call
    appointment_date = (time.time() + random.randint(7*24*3600, 14*24*3600)) # 1-2 weeks from now
    print(f"[Patient {patient_id}] Consultation scheduled for {time.ctime(appointment_date)}.")
    return {"status": "success", "appointment_date": appointment_date}

def send_welcome_packet(patient_id, patient_info):
    print(f"[Patient {patient_id}] Sending digital welcome packet...")
    time.sleep(random.uniform(0.6, 1.0)) # Simulate document generation/email service
    print(f"[Patient {patient_id}] Welcome packet sent.")
    return {"status": "success"}

def onboard_new_patient(patient_id, patient_data, insurance_data):
    print(f"--- Starting patient onboarding for Patient {patient_id} ---")

    # Step 1: Sequential - Collect core demographics
    demographics_result = collect_demographics(patient_id, patient_data)
    if demographics_result["status"] != "success":
        print(f"[Patient {patient_id}] Demographics collection failed. Aborting.")
        return False
    patient_info = demographics_result["patient_info"]
    print(f"[Patient {patient_id}] Demographics step complete.")

    # Step 2: Parallel - Verify insurance and create EHR entry (depend on demographics)
    print(f"[Patient {patient_id}] Starting parallel execution for insurance verification and EHR creation...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_insurance = executor.submit(verify_insurance, patient_id, insurance_data)
        future_ehr = executor.submit(create_ehr_entry, patient_id, patient_info)

        insurance_result = future_insurance.result()
        ehr_result = future_ehr.result()

    if insurance_result["status"] == "failed":
        print(f"[Patient {patient_id}] Insurance verification failed. Proceeding with limited services.")
    if ehr_result["status"] != "success":
        print(f"[Patient {patient_id}] EHR creation failed. Aborting further steps dependent on EHR.")
        return False
    print(f"[Patient {patient_id}] Insurance and EHR steps complete.")

    # Step 3: Sequential - Assign PCP (depends on insurance and patient info)
    pcp_result = assign_primary_care_physician(patient_id, patient_info, insurance_result["coverage"])
    if pcp_result["status"] != "success":
        print(f"[Patient {patient_id}] PCP assignment failed. Aborting.")
        return False
    pcp = pcp_result["pcp"]
    print(f"[Patient {patient_id}] PCP assignment step complete.")

    # Step 4: Parallel - Schedule consultation and send welcome packet (depend on PCP/patient info)
    print(f"[Patient {patient_id}] Starting parallel execution for scheduling and welcome packet...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_consultation = executor.submit(schedule_initial_consultation, patient_id, pcp)
        future_welcome = executor.submit(send_welcome_packet, patient_id, patient_info)

        future_consultation.result()
        future_welcome.result()
    print(f"[Patient {patient_id}] Scheduling and welcome packet steps complete.")

    print(f"--- Patient {patient_id} onboarding complete ---")
    return True

if __name__ == "__main__":
    patient_id = "PAT-001"
    patient_data = {"name": "Jane Doe", "dob": "1990-01-01", "address": "456 Oak Ave"}
    insurance_data = {"provider": "HealthCare Inc.", "policy_number": "ABC12345"}

    start_time = time.time()
    onboard_new_patient(patient_id, patient_data, insurance_data)
    end_time = time.time()
    print(f"Total onboarding time: {end_time - start_time:.2f} seconds")
