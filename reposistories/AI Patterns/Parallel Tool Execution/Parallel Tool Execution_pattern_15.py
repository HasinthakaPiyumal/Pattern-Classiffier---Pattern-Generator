import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def collect_personal_info(patient_id, data):
    time.sleep(random.uniform(0.5, 1.5))
    if not data.get("name") or not data.get("dob"):
        return {"patient_id": patient_id, "status": "failed", "reason": "Missing essential personal info"}
    return {"patient_id": patient_id, "status": "success", "personal_info_ok": True, "collected_data": data}

def verify_insurance(patient_id, policy_number):
    time.sleep(random.uniform(0.7, 2.0))
    if random.random() < 0.15:
        return {"patient_id": patient_id, "status": "failed", "reason": "Insurance verification failed"}
    return {"patient_id": patient_id, "status": "success", "insurance_ok": True}

def schedule_initial_consultation(patient_id, preferred_date):
    time.sleep(random.uniform(0.3, 1.0))
    if random.random() < 0.05:
        return {"patient_id": patient_id, "status": "failed", "reason": "No slots available for preferred date"}
    scheduled_date = "2024-08-15"
    return {"patient_id": patient_id, "status": "success", "consultation_scheduled": True, "scheduled_date": scheduled_date}

def create_patient_record(patient_id, personal_data):
    time.sleep(random.uniform(0.5, 1.5))
    if not personal_data:
        return {"patient_id": patient_id, "status": "failed", "reason": "Cannot create record without personal data"}
    record_id = f"PATREC{patient_id}"
    return {"patient_id": patient_id, "status": "success", "record_id": record_id}

def send_welcome_pack(patient_id, patient_name, scheduled_date):
    time.sleep(random.uniform(0.5, 1.5))
    if random.random() < 0.02:
        return {"patient_id": patient_id, "status": "failed", "reason": "Failed to send welcome pack"}
    return {"patient_id": patient_id, "status": "success"}

def onboard_patient(patient_data):
    patient_id = patient_data["id"]
    personal_info = patient_data["personal_info"]
    insurance_policy = patient_data["insurance_policy"]
    preferred_consultation_date = patient_data["preferred_consultation_date"]

    print(f"\n--- Starting patient onboarding for Patient {patient_id} ---")

    results = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_personal_info = executor.submit(collect_personal_info, patient_id, personal_info)
        future_insurance = executor.submit(verify_insurance, patient_id, insurance_policy)
        future_consultation = executor.submit(schedule_initial_consultation, patient_id, preferred_consultation_date)

        for future in as_completed([future_personal_info, future_insurance, future_consultation]):
            result = future.result()
            if result["status"] == "failed":
                print(f"[{patient_id}] Critical failure during initial step: {result['reason']}. Aborting.")
                return {"patient_id": patient_id, "overall_status": "failed", "reason": result["reason"]}
            results.update(result)

    if not (results.get("personal_info_ok") and results.get("insurance_ok") and results.get("consultation_scheduled")):
        print(f"[{patient_id}] Initial onboarding steps failed. Overall status: Failed.")
        return {"patient_id": patient_id, "overall_status": "failed", "reason": "Pre-onboarding checks failed"}

    print(f"[{patient_id}] All initial parallel onboarding steps completed successfully.")

    patient_record_result = create_patient_record(patient_id, results.get("collected_data"))
    if patient_record_result["status"] == "failed":
        print(f"[{patient_id}] Failed to create patient record: {patient_record_result['reason']}. Aborting.")
        return {"patient_id": patient_id, "overall_status": "failed", "reason": "Failed to create patient record"}
    else:
        results["record_creation_status"] = "success"
        results["patient_record_id"] = patient_record_result["record_id"]

    welcome_pack_result = send_welcome_pack(patient_id, personal_info.get("name", "N/A"), results.get("scheduled_date"))
    if welcome_pack_result["status"] == "failed":
        results["welcome_pack_status"] = "failed"

    print(f"--- Finished patient onboarding for Patient {patient_id}. Overall status: Success ---")
    results["overall_status"] = "success"
    return results

if __name__ == "__main__":
    patients = [
        {"id": "PAT001", "personal_info": {"name": "Alice Smith", "dob": "1990-01-15"}, "insurance_policy": "INS12345", "preferred_consultation_date": "2024-08-10"},
        {"id": "PAT002", "personal_info": {"name": "Bob Johnson", "dob": "1985-05-20"}, "insurance_policy": "INS67890", "preferred_consultation_date": "2024-08-12"},
        {"id": "PAT003", "personal_info": {"name": "Charlie Brown"}, "insurance_policy": "INS00112", "preferred_consultation_date": "2024-08-14"},
        {"id": "PAT004", "personal_info": {"name": "Diana Prince", "dob": "1970-12-01"}, "insurance_policy": "BADPOLICY", "preferred_consultation_date": "2024-08-16"}
    ]

    for patient in patients:
        final_status = onboard_patient(patient)
        print(f"Final result for {patient['id']}: {final_status['overall_status']}")
        time.sleep(1)
