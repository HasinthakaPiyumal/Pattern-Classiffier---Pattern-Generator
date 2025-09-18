import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def validate_prerequisites(student_id, course_code):
    print(f"Student {student_id}: Validating prerequisites for {course_code}...")
    time.sleep(random.uniform(0.7, 1.5))
    if random.random() < 0.1:
        print(f"Student {student_id}: Prerequisite validation failed for {course_code}!")
        return False
    print(f"Student {student_id}: Prerequisites validated for {course_code}.")
    return True

def register_course(student_id, course_code):
    print(f"Student {student_id}: Registering for course {course_code}...")
    time.sleep(random.uniform(1.0, 2.0))
    if random.random() < 0.05:
        print(f"Student {student_id}: Course registration failed for {course_code}!")
        return False
    print(f"Student {student_id}: Registered for course {course_code}.")
    return True

def assign_student_id_card(student_id):
    print(f"Student {student_id}: Assigning student ID card number...")
    time.sleep(random.uniform(0.5, 1.2))
    print(f"Student {student_id}: Student ID card assigned.")
    return True

def generate_invoice(student_id, course_code, tuition_fee):
    print(f"Student {student_id}: Generating invoice for {course_code} (Fee: ${tuition_fee})...")
    time.sleep(random.uniform(1.0, 2.0))
    print(f"Student {student_id}: Invoice generated.")
    return True

def send_welcome_email(student_id, course_code, student_email):
    print(f"Student {student_id}: Sending welcome email for {course_code} to {student_email}...")
    time.sleep(random.uniform(0.8, 1.8))
    print(f"Student {student_id}: Welcome email sent.")
    return True

def enroll_student_in_course(student_id, student_name, student_email, course_code, tuition_fee):
    print(f"\n--- Starting enrollment for Student {student_id} ({student_name}) in {course_code} ---")
    prereqs_met = validate_prerequisites(student_id, course_code)
    if not prereqs_met:
        print(f"Student {student_id}: Enrollment failed: Prerequisites not met.")
        return False
    course_registered = register_course(student_id, course_code)
    if not course_registered:
        print(f"Student {student_id}: Enrollment failed: Course registration error.")
        return False
    print(f"Student {student_id}: Course registered, executing parallel post-enrollment tasks...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(assign_student_id_card, student_id): "Assign Student ID Card",
            executor.submit(generate_invoice, student_id, course_code, tuition_fee): "Generate Invoice",
            executor.submit(send_welcome_email, student_id, course_code, student_email): "Send Welcome Email"
        }
        results = {}
        for future in as_completed(futures):
            task_name = futures[future]
            try:
                result = future.result()
                results[task_name] = result
                print(f"Student {student_id}: Task '{task_name}' completed with result: {result}")
            except Exception as exc:
                results[task_name] = f"Failed: {exc}"
                print(f"Student {student_id}: Task '{task_name}' generated an exception: {exc}")
    all_parallel_tasks_successful = all(results.values())
    if all_parallel_tasks_successful:
        print(f"--- Student {student_id} enrollment in {course_code} completed successfully! ---")
    else:
        print(f"--- Student {student_id} enrollment in {course_code} completed with some issues! ---")
    return all_parallel_tasks_successful

if __name__ == "__main__":
    student_data = [
        {"id": "S101", "name": "Charlie Brown", "email": "charlie@example.com", "course": "CS101", "fee": 500.00},
        {"id": "S102", "name": "Lucy Van Pelt", "email": "lucy@example.com", "course": "MA201", "fee": 450.00}
    ]
    for student in student_data:
        enroll_student_in_course(student["id"], student["name"], student["email"], student["course"], student["fee"])
