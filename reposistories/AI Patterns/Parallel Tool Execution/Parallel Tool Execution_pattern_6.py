import time
import concurrent.futures

def verify_insurance_eligibility(patient_id, policy_number):
    time.sleep(2.5) # Simulate external insurance API call
    print(f"Patient {patient_id}: Insurance policy {policy_number} verified.")
    return True

def create_patient_record(patient_data):
    time.sleep(1.8) # Simulate database insertion
    new_patient_id = f"PAT-{int(time.time()) % 1000}" # Simulate ID generation
    print(f"Patient {patient_data['name']}: Basic record created with ID {new_patient_id}.")
    return new_patient_id

def assign_primary_care_physician(patient_id, location_pref):
    time.sleep(1.0) # Simulate internal logic/database lookup
    physician_name = f"Dr. Smith (for {location_pref})"
    print(f"Patient {patient_id}: Assigned to {physician_name}.")
    return physician_name

def schedule_initial_consultation(patient_id, physician_name):
    time.sleep(2.0) # Simulate calendar system interaction
    appointment_time = "2023-10-26 10:00 AM"
    print(f"Patient {patient_id}: Initial consultation scheduled with {physician_name} at {appointment_time}.")
    return appointment_time

def send_welcome_packet(patient_id, email_address, appointment_info):
    time.sleep(0.7) # Simulate email/document generation service
    print(f"Patient {patient_id}: Welcome packet sent to {email_address} with appointment details: {appointment_info}.")
    return True

def onboard_patient(patient_info):
    patient_name = patient_info['name']
    policy_number = patient_info['insurance_policy']
    email = patient_info['email']
    location = patient_info['location_preference']

    print(f"\n--- Starting patient onboarding for {patient_name} ---")

    # Step 1: Initial sequential data validation
    time.sleep(0.4)
    print(f"{patient_name}: Patient data validated.")

    # Step 2: Parallel execution for independent tasks
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        insurance_future = executor.submit(verify_insurance_eligibility, patient_name, policy_number) # Using name as temporary ID
        record_future = executor.submit(create_patient_record, patient_info)

        # Wait for these two to complete as subsequent steps depend on their results
        concurrent.futures.wait([insurance_future, record_future])

        insurance_verified = insurance_future.result()
        new_patient_id = record_future.result()

    if insurance_verified and new_patient_id:
        print(f"Patient {new_patient_id}: Insurance and record creation successful.")
        # Step 3: Dependent sequential task (needs new_patient_id)
        assigned_physician = assign_primary_care_physician(new_patient_id, location)

        if assigned_physician:
            print(f"Patient {new_patient_id}: Physician assigned successfully.")
            # Step 4: Another dependent sequential task
            appointment_details = schedule_initial_consultation(new_patient_id, assigned_physician)

            if appointment_details:
                print(f"Patient {new_patient_id}: Appointment scheduled.")
                # Step 5: Final dependent sequential task
                send_welcome_packet(new_patient_id, email, appointment_details)
                print(f"--- Patient {new_patient_id} onboarding complete ---")
                return True
    print(f"--- Patient {patient_name} onboarding failed ---")
    return False

if __name__ == "__main__":
    patient1 = {
        'name': 'Alice Johnson',
        'insurance_policy': 'INS00123',
        'email': 'alice.j@example.com',
        'location_preference': 'Downtown Clinic'
    }
    patient2 = {
        'name': 'Bob Williams',
        'insurance_policy': 'INS00456',
        'email': 'bob.w@example.com',
        'location_preference': 'Suburban Hospital'
    }
    onboard_patient(patient1)
    onboard_patient(patient2)