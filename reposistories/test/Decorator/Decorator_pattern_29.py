def check_course_prerequisites(func):
    def wrapper(student_id, course_id):
        prerequisites = {
            "CS201": ["CS101"],
            "MA301": ["MA201", "PH101"]
        }
        student_completed_courses = {
            "S001": ["CS101", "MA201"],
            "S002": ["MA201"]
        }

        required = prerequisites.get(course_id, [])
        if not required:
            print(f"No prerequisites for {course_id}.")
            return func(student_id, course_id)

        student_courses = set(student_completed_courses.get(student_id, []))
        missing_prereqs = [p for p in required if p not in student_courses]

        if missing_prereqs:
            print(f"Prerequisite check FAILED for {student_id} enrolling in {course_id}.")
            print(f"Missing prerequisites: {', '.join(missing_prereqs)}")
            return False
        print(f"Prerequisite check PASSED for {student_id} enrolling in {course_id}.")
        return func(student_id, course_id)
    return wrapper

def send_enrollment_confirmation(func):
    def wrapper(student_id, course_id):
        success = func(student_id, course_id)
        if success:
            print(f"Sending enrollment confirmation to {student_id} for {course_id} via email.")
        else:
            print(f"Enrollment failed, no confirmation sent for {student_id} in {course_id}.")
        return success
    return wrapper

def check_course_capacity(func):
    course_capacities = {"CS201": 2, "MA301": 1}
    current_enrollments = {"CS201": ["S001"], "MA301": []}

    def wrapper(student_id, course_id):
        if course_id in course_capacities:
            if len(current_enrollments.get(course_id, [])) >= course_capacities[course_id]:
                print(f"Course {course_id} is full. Cannot enroll {student_id}.")
                return False
            print(f"Course {course_id} has available capacity.")
            result = func(student_id, course_id)
            if result:
                current_enrollments.setdefault(course_id, []).append(student_id)
            return result
        return func(student_id, course_id)
    return wrapper

@send_enrollment_confirmation
@check_course_prerequisites
@check_course_capacity
def enroll_student_in_course(student_id, course_id):
    print(f"Attempting to enroll student {student_id} in course {course_id}.")
    print(f"Student {student_id} successfully enrolled in {course_id}.")
    return True

if __name__ == "__main__":
    print("--- Student S001 enrolling in CS201 (should pass) ---")
    enrollment1 = enroll_student_in_course("S001", "CS201")
    print(f"Enrollment 1 success: {enrollment1}\n")

    print("--- Student S002 enrolling in CS201 (no prereq CS101, but course full) ---")
    enrollment2 = enroll_student_in_course("S002", "CS201")
    print(f"Enrollment 2 success: {enrollment2}\n")

    print("--- Student S001 enrolling in MA301 (missing prereq PH101) ---")
    enrollment3 = enroll_student_in_course("S001", "MA301")
    print(f"Enrollment 3 success: {enrollment3}\n")

    print("--- Student S002 enrolling in MA301 (missing prereq PH101) ---")
    enrollment4 = enroll_student_in_course("S002", "MA301")
    print(f"Enrollment 4 success: {enrollment4}\n")