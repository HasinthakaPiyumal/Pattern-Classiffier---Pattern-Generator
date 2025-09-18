import concurrent.futures
import time
import random

def check_prerequisites(student_id, course_id):
    print(f"  [Prereq] Checking prerequisites for student {student_id} in {course_id}...")
    time.sleep(random.uniform(0.5, 1.5))
    is_qualified = random.choice([True, True, False])
    print(f"  [Prereq] Student {student_id} qualified for {course_id}: {is_qualified}.")
    return is_qualified

def verify_payment(student_id, course_id, amount):
    print(f"  [Payment] Verifying payment for student {student_id} for {course_id} (Amount: ${amount})...")
    time.sleep(random.uniform(0.8, 2.0))
    is_paid = random.choice([True, True, True, False])
    print(f"  [Payment] Payment status for {student_id} in {course_id}: {is_paid}.")
    return is_paid

def allocate_seat_in_course(student_id, course_id):
    print(f"  [Enroll] Attempting to allocate seat for student {student_id} in {course_id}...")
    time.sleep(random.uniform(0.7, 1.8))
    seat_allocated = random.choice([True, True, False])
    if seat_allocated:
        print(f"  [Enroll] Seat allocated for {student_id} in {course_id}.")
    else:
        print(f"  [Enroll] Failed to allocate seat for {student_id} in {course_id}: Course full or error.")
    return seat_allocated

def update_student_transcript(student_id, course_id, status):
    print(f"  [Transcript] Updating transcript for student {student_id} with {course_id} ({status})...")
    time.sleep(random.uniform(0.6, 1.5))
    print(f"  [Transcript] Transcript for {student_id} updated.")
    return True

def send_enrollment_confirmation(student_id, course_id, payment_status, seat_status):
    print(f"[Confirmation] Sending enrollment confirmation to {student_id} for {course_id}...")
    if payment_status and seat_status:
        time.sleep(0.5)
        print(f"[Confirmation] Enrollment confirmed for {student_id} in {course_id}.")
        return True
    else:
        print(f"[Confirmation] Enrollment confirmation failed for {student_id} in {course_id}.")
        return False

def notify_instructor(instructor_email, student_id, course_id):
    print(f"[Instructor Notify] Notifying instructor {instructor_email} about {student_id} enrollment in {course_id}...")
    time.sleep(0.5)
    print(f"[Instructor Notify] Instructor {instructor_email} notified.")
    return True

def enroll_student_in_course(enrollment_data):
    student_id = enrollment_data["student_id"]
    course_id = enrollment_data["course_id"]
    tuition_amount = enrollment_data["tuition_amount"]
    instructor_email = enrollment_data["instructor_email"]

    print(f"--- Starting enrollment for Student {student_id} in Course {course_id} ---")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_prereq = executor.submit(check_prerequisites, student_id, course_id)
        future_payment = executor.submit(verify_payment, student_id, course_id, tuition_amount)
        future_seat_allocation = executor.submit(allocate_seat_in_course, student_id, course_id)

        is_qualified = future_prereq.result()
        is_paid = future_payment.result()
        seat_allocated = future_seat_allocation.result()

    print(f"\n--- Parallel checks for Student {student_id} in Course {course_id} completed ---")
    print(f"  Qualified: {is_qualified}")
    print(f"  Payment Status: {is_paid}")
    print(f"  Seat Allocated: {seat_allocated}")

    overall_enrollment_success = False
    if is_qualified and is_paid and seat_allocated:
        print("\nAll initial checks passed. Proceeding with finalization.")
        transcript_updated = update_student_transcript(student_id, course_id, "Enrolled")
        confirmation_sent = send_enrollment_confirmation(student_id, course_id, is_paid, seat_allocated)
        
        if confirmation_sent and transcript_updated:
            notify_instructor(instructor_email, student_id, course_id)
            overall_enrollment_success = True
            print(f"Enrollment for {student_id} in {course_id} successfully finalized.")
        else:
            print(f"Enrollment for {student_id} in {course_id} failed during finalization.")
    else:
        print(f"Enrollment for {student_id} in {course_id} failed due to initial checks.")

    print(f"--- Finished enrollment for Student {student_id} in Course {course_id}. Overall Success: {overall_enrollment_success} ---\n")
    return overall_enrollment_success

if __name__ == "__main__":
    enrollment_info = {
        "student_id": "STU101",
        "course_id": "CS101",
        "tuition_amount": 500,
        "instructor_email": "prof.jones@university.edu"
    }
    enroll_student_in_course(enrollment_info)

    enrollment_info_2 = {
        "student_id": "STU102",
        "course_id": "MA201",
        "tuition_amount": 450,
        "instructor_email": "prof.smith@university.edu"
    }
    enroll_student_in_course(enrollment_info_2)
