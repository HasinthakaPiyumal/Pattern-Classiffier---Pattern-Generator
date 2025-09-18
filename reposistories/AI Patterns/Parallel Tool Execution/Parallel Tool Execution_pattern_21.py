import time
import concurrent.futures

def verify_insurance(patient_id: str, policy_number: str) -> dict:
    time.sleep(1.8) # Simulate external API call to insurance provider
    # print(f"  Verifying insurance for {patient_id} (policy: {policy_number})...")
    if "INVALID" not in policy_number:
        return {"task": "insurance_verification", "success": True, "message": "Insurance verified"}
    return {"task": "insurance_verification", "success": False, "message": "Insurance verification failed"}

def create_patient_record(patient_data: dict) -> dict:
    time.sleep(1.2) # Simulate database write and data processing
    # print(f"  Creating patient record for {patient_data['name']}...")
    if patient_data.get('name') and patient_data.get('date_of_birth'):
        return {"task": "patient_record_creation", "success": True, "patient_id": f"PID-{int(time.time())}", "message": "Patient record created"}
    return {"task": "patient_record_creation", "success": False, "patient_id": None, "message": "Failed to create patient record"}

def schedule_initial_consultation(patient_id: str, doctor_id: str, preferred_date: str) -> dict:
    time.sleep(1.5) # Simulate scheduling system interaction
    # print(f"  Scheduling consultation for {patient_id} with Dr. {doctor_id} on {preferred_date}...")
    return {"task": "consultation_scheduling", "success": True, "appointment_id": f"APP-{int(time.time())}", "message": "Consultation scheduled"}

def send_welcome_packet(patient_id: str, email: str) -> dict:
    time.sleep(0.7) # Simulate email/postal service dispatch
    # print(f"  Sending welcome packet to {patient_id} at {email}...")
    return {"task": "welcome_packet_dispatch", "success": True, "message": "Welcome packet dispatched"}

def onboard_new_patient(patient_details: dict):
    print(f"\n--- Onboarding Patient: {patient_details['name']} ---")
    start_time = time.perf_counter()

    patient_name = patient_details['name']
    patient_dob = patient_details['date_of_birth']
    patient_email = patient_details['email']
    policy_number = patient_details['insurance_policy']

    # Independent tasks: Insurance verification and Patient record creation
    # These can often happen concurrently. Insurance doesn't need a full record to start, and vice-versa.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_insurance = executor.submit(verify_insurance, patient_name, policy_number)
        future_record = executor.submit(create_patient_record, patient_details)

        insurance_result = future_insurance.result()
        record_result = future_record.result()

    print(f"[Parallel Step 1 Results]:")
    print(f"  - {insurance_result['message']}")
    print(f"  - {record_result['message']}")

    # Dependent tasks: Scheduling and Welcome Packet
    # These depend on the successful creation of the patient record.
    final_status = "Failed"
    if record_result['success'] and insurance_result['success']:
        patient_id = record_result['patient_id']
        print("[Sequential Step 2: Post-Onboarding Actions]")
        
        # These two could potentially be parallelized if no strict dependency, but often scheduling depends on record ID.
        schedule_result = schedule_initial_consultation(patient_id, "Dr. Smith", "2023-11-15")
        welcome_result = send_welcome_packet(patient_id, patient_email)

        print(f"  - {schedule_result['message']} (Appointment ID: {schedule_result['appointment_id']})")
        print(f"  - {welcome_result['message']}")
        final_status = "Successfully Onboarded"
    else:
        print("  Patient onboarding halted due to initial failures.")
        if not insurance_result['success']:
             send_welcome_packet("N/A", patient_email) # Send an apology/instruction email

    end_time = time.perf_counter()
    print(f"--- Patient {patient_name} Onboarding {final_status} in {end_time - start_time:.2f} seconds ---")

if __name__ == "__main__":
    patient1 = {
        "name": "Jane Doe",
        "date_of_birth": "1990-05-15",
        "email": "jane.doe@example.com",
        "insurance_policy": "ABC12345"
    }
    patient2 = {
        "name": "John Smith",
        "date_of_birth": "1985-11-20",
        "email": "john.smith@example.com",
        "insurance_policy": "INVALID-POLICY"
    }

    onboard_new_patient(patient1)
    onboard_new_patient(patient2)
