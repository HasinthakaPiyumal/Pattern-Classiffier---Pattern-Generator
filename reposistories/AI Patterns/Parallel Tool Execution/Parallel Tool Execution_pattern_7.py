import time
import concurrent.futures

def review_academic_records(applicant_id, transcript_link):
    time.sleep(2.2) # Simulate human review or external API for transcript validation
    print(f"Applicant {applicant_id}: Academic records from {transcript_link} reviewed.")
    return True

def verify_personal_details(applicant_id, identity_doc_id):
    time.sleep(1.5) # Simulate identity verification service
    print(f"Applicant {applicant_id}: Personal details verified with ID {identity_doc_id}.")
    return True

def check_admission_requirements(applicant_id, program_code):
    time.sleep(1.0) # Simulate database lookup for program requirements
    print(f"Applicant {applicant_id}: Admission requirements for {program_code} checked.")
    return True

def assign_student_id(applicant_id):
    time.sleep(0.8) # Simulate internal database operation
    student_id = f"STU-{int(time.time()) % 1000}"
    print(f"Applicant {applicant_id}: Assigned Student ID {student_id}.")
    return student_id

def generate_initial_fee_invoice(student_id, program_code):
    time.sleep(1.7) # Simulate financial system API call
    invoice_amount = 5000.00 if program_code == 'CS101' else 4500.00
    print(f"Student {student_id}: Initial fee invoice generated for ${invoice_amount}.")
    return invoice_amount

def enroll_in_orientation_session(student_id):
    time.sleep(1.2) # Simulate calendar/enrollment system
    orientation_date = "2023-11-15"
    print(f"Student {student_id}: Enrolled in orientation session on {orientation_date}.")
    return orientation_date

def send_enrollment_confirmation(student_id, email_address, invoice_amount, orientation_date):
    time.sleep(0.6) # Simulate email service
    print(f"Student {student_id}: Enrollment confirmation email sent to {email_address} with invoice ${invoice_amount} and orientation on {orientation_date}.")
    return True

def process_student_enrollment(applicant_data):
    applicant_id = applicant_data['applicant_id']
    program_code = applicant_data['program']
    email = applicant_data['email']
    transcript_link = applicant_data['transcript_link']
    identity_doc_id = applicant_data['identity_doc_id']

    print(f"\n--- Starting enrollment process for Applicant {applicant_id} ---")

    # Step 1: Initial sequential application reception
    time.sleep(0.3)
    print(f"Applicant {applicant_id}: Application received and logged.")

    # Step 2: Parallel execution for initial checks
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        records_future = executor.submit(review_academic_records, applicant_id, transcript_link)
        details_future = executor.submit(verify_personal_details, applicant_id, identity_doc_id)
        requirements_future = executor.submit(check_admission_requirements, applicant_id, program_code)

        concurrent.futures.wait([records_future, details_future, requirements_future])

        records_ok = records_future.result()
        details_ok = details_future.result()
        requirements_met = requirements_future.result()

    if records_ok and details_ok and requirements_met:
        print(f"Applicant {applicant_id}: All initial checks passed. Proceeding to admission.")
        # Step 3: Dependent sequential task - Admission Approval
        time.sleep(0.5) # Simulate admission approval logic
        print(f"Applicant {applicant_id}: Admission approved.")

        # Step 4: Dependent sequential task - Assign Student ID (must happen before other tasks that need it)
        new_student_id = assign_student_id(applicant_id)

        if new_student_id:
            print(f"Student {new_student_id}: Student ID successfully assigned.")
            # Step 5: Parallel execution for post-ID tasks
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                invoice_future = executor.submit(generate_initial_fee_invoice, new_student_id, program_code)
                orientation_future = executor.submit(enroll_in_orientation_session, new_student_id)

                concurrent.futures.wait([invoice_future, orientation_future])

                initial_invoice_amount = invoice_future.result()
                orientation_date = orientation_future.result()

            if initial_invoice_amount and orientation_date:
                print(f"Student {new_student_id}: Invoice generated and orientation enrolled.")
                # Step 6: Final dependent sequential task
                send_enrollment_confirmation(new_student_id, email, initial_invoice_amount, orientation_date)
                print(f"--- Student {new_student_id} enrollment complete ---")
                return True
    print(f"--- Applicant {applicant_id} enrollment failed ---")
    return False

if __name__ == "__main__":
    applicant1 = {
        'applicant_id': 'APP789',
        'program': 'CS101',
        'email': 'applicant1@university.edu',
        'transcript_link': 'http://uni.edu/transcripts/app789',
        'identity_doc_id': 'ID987654'
    }
    applicant2 = {
        'applicant_id': 'APP101',
        'program': 'BIO202',
        'email': 'applicant2@university.edu',
        'transcript_link': 'http://uni.edu/transcripts/app101',
        'identity_doc_id': 'ID123456'
    }
    process_student_enrollment(applicant1)
    process_student_enrollment(applicant2)