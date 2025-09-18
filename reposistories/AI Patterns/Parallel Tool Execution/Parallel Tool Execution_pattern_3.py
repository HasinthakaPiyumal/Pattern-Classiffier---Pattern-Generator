import concurrent.futures
import time
import random

def create_patient_record(patient_id, name, dob):
    print(f"  [Records] Creating record for {name} (ID: {patient_id})...")
    time.sleep(random.uniform(0.6, 1.8))
    print(f"  [Records] Record for {patient_id} created.")
    return {"patient_id": patient_id, "status": "active"}

def schedule_initial_consultation(patient_id, doctor_type):
    print(f"  [Scheduling] Scheduling consultation for {patient_id} with {doctor_type}...")
    time.sleep(random.uniform(1.0, 2.5))
    appointment_id = f"APP-{patient_id}-{random.randint(1000,9999)}"
    print(f"  [Scheduling] Consultation {appointment_id} scheduled for {patient_id}.")
    return appointment_id

def send_welcome_packet(patient_id, address):
    print(f"  [Mail] Preparing and sending welcome packet to {address} for {patient_id}...")
    time.sleep(random.uniform(0.8, 2.0))
    print(f"  [Mail] Welcome packet sent for {patient_id}.")
    return True

def verify_insurance(patient_id, policy_number):
    print(f"  [Insurance] Verifying insurance for {patient_id} (Policy: {policy_number})...")
    time.sleep(random.uniform(1.2, 2.8))
    is_verified = random.choice([True, False])
    print(f"  [Insurance] Insurance for {patient_id} verification status: {is_verified}.")
    return is_verified

def assign_primary_care_physician(patient_record_details):
    patient_id = patient_record_details["patient_id"]
    if patient_record_details["status"] == "active":
        print(f"[PCP Assign] Assigning PCP for patient {patient_id}...")
        time.sleep(random.uniform(0.5, 1.0))
        pcp_name = f"Dr. Smith (ID: DOC{random.randint(100,999)})"
        print(f"[PCP Assign] PCP {pcp_name} assigned for {patient_id}.")
        return pcp_name
    else:
        print(f"[PCP Assign] Cannot assign PCP for {patient_id}: record not active.")
        return None

def finalize_onboarding(patient_id, assigned_pcp, appointment_id, packet_sent, insurance_verified):
    print(f"\n[Onboarding] Finalizing onboarding for patient {patient_id}...")
    if assigned_pcp and appointment_id and packet_sent and insurance_verified:
        time.sleep(0.7)
        print(f"[Onboarding] Patient {patient_id} successfully onboarded with PCP {assigned_pcp} and appointment {appointment_id}.")
        return True
    else:
        print(f"[Onboarding] Onboarding for patient {patient_id} failed. Missing components.")
        return False

def onboard_new_patient(patient_data):
    patient_id = patient_data["patient_id"]
    patient_name = patient_data["name"]
    patient_dob = patient_data["dob"]
    patient_address = patient_data["address"]
    patient_insurance = patient_data["insurance_policy"]

    print(f"--- Starting onboarding for Patient ID: {patient_id} ---")

    patient_record = create_patient_record(patient_id, patient_name, patient_dob)
    if not patient_record:
        print(f"Failed to create patient record for {patient_id}. Aborting onboarding.")
        return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_consultation = executor.submit(schedule_initial_consultation, patient_id, "General Practitioner")
        future_welcome_packet = executor.submit(send_welcome_packet, patient_id, patient_address)
        future_insurance = executor.submit(verify_insurance, patient_id, patient_insurance)

        future_pcp = executor.submit(assign_primary_care_physician, patient_record)

        appointment_id = future_consultation.result()
        packet_sent = future_welcome_packet.result()
        insurance_verified = future_insurance.result()
        assigned_pcp = future_pcp.result()

    print(f"\n--- Parallel tasks for Patient {patient_id} completed ---")
    print(f"  Appointment ID: {appointment_id}")
    print(f"  Welcome Packet Sent: {packet_sent}")
    print(f"  Insurance Verified: {insurance_verified}")
    print(f"  Assigned PCP: {assigned_pcp}")

    onboarding_success = finalize_onboarding(patient_id, assigned_pcp, appointment_id, packet_sent, insurance_verified)

    print(f"--- Finished onboarding for Patient ID: {patient_id}. Overall Success: {onboarding_success} ---\n")
    return onboarding_success

if __name__ == "__main__":
    patient_info = {
        "patient_id": "PAT001",
        "name": "Jane Doe",
        "dob": "1990-05-15",
        "address": "789 Pine Ln, Healthburg, USA",
        "insurance_policy": "INS123456"
    }
    onboard_new_patient(patient_info)

    patient_info_2 = {
        "patient_id": "PAT002",
        "name": "John Smith",
        "dob": "1985-11-22",
        "address": "101 Elm St, Medtown, USA",
        "insurance_policy": "INS789012"
    }
    onboard_new_patient(patient_info_2)
