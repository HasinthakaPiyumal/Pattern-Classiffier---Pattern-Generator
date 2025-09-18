import concurrent.futures
import time
import random

def receive_application_data(app_id, applicant_details):
    print(f"[App {app_id}] Receiving and validating application data for {applicant_details['name']}...")
    time.sleep(random.uniform(0.5, 1.0)) # Simulate data intake and initial validation
    print(f"[App {app_id}] Application data received.")
    return {"status": "success", "applicant_info": applicant_details}

def perform_credit_check(app_id, ssn):
    print(f"[App {app_id}] Performing credit check for SSN: {ssn[:3]}***...")
    time.sleep(random.uniform(1.5, 2.5)) # Simulate external credit bureau API call
    credit_score = random.randint(300, 850)
    print(f"[App {app_id}] Credit check complete. Score: {credit_score}.")
    return {"status": "success", "credit_score": credit_score}

def verify_identity(app_id, name, dob):
    print(f"[App {app_id}] Verifying identity for {name} (DOB: {dob})...")
    time.sleep(random.uniform(1.0, 2.0)) # Simulate external identity verification service (KYC)
    is_verified = random.choice([True, True, True, False])
    if is_verified:
        print(f"[App {app_id}] Identity verified.")
    else:
        print(f"[App {app_id}] Identity verification failed.")
    return {"status": "success" if is_verified else "failed", "verified": is_verified}

def validate_income(app_id, income_details):
    print(f"[App {app_id}] Validating income of ${income_details['annual_income']}...")
    time.sleep(random.uniform(1.2, 2.2)) # Simulate bank statement analysis, employer verification
    is_sufficient = income_details['annual_income'] > 50000 and random.choice([True, True, True, False])
    if is_sufficient:
        print(f"[App {app_id}] Income validated as sufficient.")
    else:
        print(f"[App {app_id}] Income deemed insufficient or verification failed.")
    return {"status": "success" if is_sufficient else "failed", "sufficient": is_sufficient}

def conduct_risk_assessment(app_id, credit_score, identity_verified, income_sufficient):
    print(f"[App {app_id}] Conducting comprehensive risk assessment...")
    time.sleep(random.uniform(1.5, 2.5)) # Simulate complex internal risk model calculation
    risk_score = 0
    if credit_score < 600: risk_score += 30
    elif credit_score < 700: risk_score += 15
    if not identity_verified: risk_score += 50
    if not income_sufficient: risk_score += 40

    overall_risk = "High" if risk_score > 60 else ("Medium" if risk_score > 20 else "Low")
    print(f"[App {app_id}] Risk assessment complete. Overall risk: {overall_risk}.")
    return {"status": "success", "overall_risk": overall_risk, "risk_score": risk_score}

def generate_offer_letter(app_id, loan_amount, overall_risk):
    print(f"[App {app_id}] Generating loan offer letter for ${loan_amount} with {overall_risk} risk...")
    time.sleep(random.uniform(0.8, 1.5)) # Simulate document generation system
    if overall_risk == "High":
        offer = "Declined"
    elif overall_risk == "Medium":
        offer = f"Approved for ${loan_amount * 0.8:.2f} at 8% APR"
    else: # Low risk
        offer = f"Approved for ${loan_amount} at 4% APR"
    print(f"[App {app_id}] Offer letter generated: {offer}.")
    return {"status": "success", "offer": offer}

def notify_applicant_status(app_id, applicant_email, offer_status):
    print(f"[App {app_id}] Notifying applicant {applicant_email} of application status...")
    time.sleep(random.uniform(0.6, 1.0)) # Simulate email notification service
    print(f"[App {app_id}] Applicant notified: {offer_status}.")
    return {"status": "success"}

def archive_application(app_id):
    print(f"[App {app_id}] Archiving application documents...")
    time.sleep(random.uniform(0.4, 0.8)) # Simulate document management system write
    print(f"[App {app_id}] Application archived.")
    return {"status": "success"}

def process_loan_application(app_id, applicant_details, income_details, loan_amount):
    print(f"--- Starting loan application processing for Application {app_id} ---")

    # Step 1: Sequential - Receive and validate initial data
    app_data_result = receive_application_data(app_id, applicant_details)
    if app_data_result["status"] != "success":
        print(f"[App {app_id}] Application data reception failed. Aborting.")
        return False
    print(f"[App {app_id}] Initial data step complete.")

    # Step 2: Parallel - Perform independent checks
    print(f"[App {app_id}] Starting parallel execution for credit, identity, and income checks...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_credit = executor.submit(perform_credit_check, app_id, applicant_details['ssn'])
        future_identity = executor.submit(verify_identity, app_id, applicant_details['name'], applicant_details['dob'])
        future_income = executor.submit(validate_income, app_id, income_details)

        credit_result = future_credit.result()
        identity_result = future_identity.result()
        income_result = future_income.result()

    if identity_result["status"] == "failed" or income_result["status"] == "failed":
        print(f"[App {app_id}] Critical checks failed (Identity or Income). Declining application.")
        return False
    print(f"[App {app_id}] All initial parallel checks completed.")

    # Step 3: Sequential - Conduct risk assessment (depends on all parallel checks)
    risk_result = conduct_risk_assessment(
        app_id,
        credit_result["credit_score"],
        identity_result["verified"],
        income_result["sufficient"]
    )
    if risk_result["status"] != "success":
        print(f"[App {app_id}] Risk assessment failed. Aborting.")
        return False
    overall_risk = risk_result["overall_risk"]
    print(f"[App {app_id}] Risk assessment step complete.")

    # Step 4: Sequential - Generate offer letter (depends on risk assessment)
    offer_result = generate_offer_letter(app_id, loan_amount, overall_risk)
    if offer_result["status"] != "success":
        print(f"[App {app_id}] Offer generation failed. Aborting.")
        return False
    offer_status_for_notification = offer_result["offer"]
    print(f"[App {app_id}] Offer generation step complete.")

    # Step 5: Parallel - Post-offer tasks (notification, archiving)
    print(f"[App {app_id}] Starting parallel execution for applicant notification and archiving...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_notify = executor.submit(notify_applicant_status, app_id, applicant_details['email'], offer_status_for_notification)
        future_archive = executor.submit(archive_application, app_id)

        future_notify.result()
        future_archive.result()
    print(f"[App {app_id}] Notification and archiving steps complete.")

    print(f"--- Loan application {app_id} processing complete ---")
    return True

if __name__ == "__main__":
    app_id = "LOAN-001"
    applicant_details = {
        "name": "John Smith",
        "dob": "1985-03-15",
        "ssn": "123-45-6789",
        "email": "john.smith@example.com"
    }
    income_details = {"employer": "TechCorp", "annual_income": 75000}
    loan_amount = 25000.00

    start_time = time.time()
    process_loan_application(app_id, applicant_details, income_details, loan_amount)
    end_time = time.time()
    print(f"Total processing time: {end_time - start_time:.2f} seconds")
