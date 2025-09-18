import asyncio
import time
import random

async def verify_student_eligibility(student_id):
    print(f"[{time.time():.2f}] Verifying eligibility for student {student_id}...")
    await asyncio.sleep(random.uniform(1.0, 2.0)) # Simulate database lookup for academic standing, prerequisites
    is_eligible = random.choice([True, True, True, False]) # Simulate occasional eligibility issues
    if is_eligible:
        print(f"[{time.time():.2f}] Student {student_id} is eligible for enrollment.")
        return {"status": "success", "eligible": True}
    else:
        print(f"[{time.time():.2f}] Student {student_id} is NOT eligible for enrollment (e.g., holds, low GPA).")
        return {"status": "failed", "eligible": False, "reason": "Eligibility criteria not met"}

async def check_course_availability(course_code):
    print(f"[{time.time():.2f}] Checking availability for course {course_code}...")
    await asyncio.sleep(random.uniform(0.8, 1.8)) # Simulate querying course catalog/seats database
    seats_available = random.randint(0, 10)
    if seats_available > 0:
        print(f"[{time.time():.2f}] Course {course_code} has {seats_available} seats available.")
        return {"status": "success", "available": True, "seats": seats_available}
    else:
        print(f"[{time.time():.2f}] Course {course_code} is full. No seats available.")
        return {"status": "failed", "available": False, "reason": "Course full"}

async def process_payment_details(student_id, amount):
    print(f"[{time.time():.2f}] Processing payment of ${amount} for student {student_id}...")
    await asyncio.sleep(random.uniform(1.5, 3.0)) # Simulate external payment gateway call
    payment_successful = random.choice([True, True, True, False]) # Simulate occasional payment failure
    if payment_successful:
        print(f"[{time.time():.2f}] Payment for student {student_id} successful.")
        return {"status": "success", "transaction_id": f"PAY{random.randint(100000, 999999)}"}
    else:
        print(f"[{time.time():.2f}] Payment for student {student_id} failed.")
        return {"status": "failed", "reason": "Payment declined or error"}

async def assign_course_materials(student_id, course_code):
    print(f"[{time.time():.2f}] Assigning course materials for student {student_id} in {course_code}...")
    await asyncio.sleep(random.uniform(0.7, 1.5)) # Simulate LMS update, e-book access provisioning
    print(f"[{time.time():.2f}] Course materials assigned for student {student_id} in {course_code}.")
    return {"status": "success"}

async def update_student_record(student_id, course_code):
    print(f"[{time.time():.2f}] Updating academic record for student {student_id} with {course_code}...")
    await asyncio.sleep(random.uniform(0.6, 1.2)) # Simulate SIS update
    print(f"[{time.time():.2f}] Student record for {student_id} updated with {course_code}.")
    return {"status": "success"}

async def enroll_student_in_course(enrollment_data):
    student_id = enrollment_data['student_id']
    course_code = enrollment_data['course_code']
    course_fee = enrollment_data['course_fee']

    print(f"\n[{time.time():.2f}] --- Starting enrollment for student {student_id} in {course_code} ---")

    # Step 1: Sequential - Verify student eligibility (must pass first)
    eligibility_result = await verify_student_eligibility(student_id)
    if not eligibility_result['eligible']:
        print(f"[{time.time():.2f}] Enrollment failed: Student {student_id} not eligible. Reason: {eligibility_result['reason']}")
        return {"enrollment_status": "failed", "reason": "student_not_eligible"}

    # Step 2: Parallel execution of independent tasks
    # Course availability check and payment processing can happen concurrently
    print(f"[{time.time():.2f}] Student {student_id} eligible. Initiating parallel checks: course availability and payment.")
    availability_task = check_course_availability(course_code)
    payment_task = process_payment_details(student_id, course_fee)

    availability_result, payment_result = await asyncio.gather(availability_task, payment_task)

    if availability_result['status'] == 'failed':
        print(f"[{time.time():.2f}] Enrollment failed: {availability_result['reason']}")
        return {"enrollment_status": "failed", "reason": "course_unavailable"}

    if payment_result['status'] == 'failed':
        print(f"[{time.time():.2f}] Enrollment failed: {payment_result['reason']}")
        return {"enrollment_status": "failed", "reason": "payment_failed"}

    # Step 3: Parallel execution of dependent tasks (only if previous steps succeed)
    # Assigning materials and updating student record can happen concurrently after successful enrollment
    print(f"[{time.time():.2f}] All checks passed for student {student_id}. Finalizing enrollment: assigning materials and updating record.")
    assign_materials_task = assign_course_materials(student_id, course_code)
    update_record_task = update_student_record(student_id, course_code)

    await asyncio.gather(assign_materials_task, update_record_task)

    print(f"[{time.time():.2f}] --- Enrollment for student {student_id} in {course_code} complete ---")
    return {
        "enrollment_status": "completed",
        "student_id": student_id,
        "course_code": course_code,
        "eligibility": eligibility_result,
        "availability": availability_result,
        "payment": payment_result
    }

if __name__ == "__main__":
    enrollment1 = {
        'student_id': 'S001',
        'course_code': 'CS101',
        'course_fee': 500.00
    }
    asyncio.run(enroll_student_in_course(enrollment1))

    enrollment2 = {
        'student_id': 'S002',
        'course_code': 'MA201',
        'course_fee': 350.00
    }
    print("\n--- Simulating an enrollment with potential course full issue ---")
    random.seed(1) # Make course availability fail for the next call for demonstration
    asyncio.run(enroll_student_in_course(enrollment2))

    enrollment3 = {
        'student_id': 'S003',
        'course_code': 'EN305',
        'course_fee': 400.00
    }
    print("\n--- Simulating an enrollment with potential payment failure ---")
    random.seed(2) # Make payment fail for the next call for demonstration
    asyncio.run(enroll_student_in_course(enrollment3))
