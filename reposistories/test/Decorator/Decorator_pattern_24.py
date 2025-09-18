class Course:
    def __init__(self, course_code, course_name, capacity):
        self._course_code = course_code
        self._course_name = course_name
        self._capacity = capacity
        self._enrolled_students = []

    def enroll_student(self, student_id):
        if len(self._enrolled_students) < self._capacity:
            self._enrolled_students.append(student_id)
            print(f"Successfully enrolled student {student_id} in {self._course_name} ({self._course_code}).")
            return True
        else:
            print(f"Enrollment failed for student {student_id}: {self._course_name} is full.")
            return False

    def get_course_info(self):
        return f"{self._course_name} ({self._course_code}) - Enrolled: {len(self._enrolled_students)}/{self._capacity}"

    def get_enrolled_students(self):
        return self._enrolled_students

class CourseEnrollmentDecorator:
    def __init__(self, decorated_course):
        self._decorated_course = decorated_course

    def enroll_student(self, student_id):
        return self._decorated_course.enroll_student(student_id)

    def get_course_info(self):
        return self._decorated_course.get_course_info()

    def get_enrolled_students(self):
        return self._decorated_course.get_enrolled_students()

class PrerequisiteCheckDecorator(CourseEnrollmentDecorator):
    def __init__(self, decorated_course, required_courses):
        super().__init__(decorated_course)
        self._required_courses = required_courses # List of course codes

    def enroll_student(self, student_id, completed_courses=None):
        if completed_courses is None:
            completed_courses = []

        if all(rc in completed_courses for rc in self._required_courses):
            print(f"PREREQ CHECK: Student {student_id} meets prerequisites for {self._decorated_course._course_name}.")
            return super().enroll_student(student_id)
        else:
            print(f"PREREQ CHECK FAILED: Student {student_id} missing prerequisites {self._required_courses} for {self._decorated_course._course_name}.")
            return False

class EmailNotificationDecorator(CourseEnrollmentDecorator):
    def enroll_student(self, student_id):
        result = super().enroll_student(student_id)
        if result:
            print(f"EMAIL NOTIFICATION: Sending enrollment confirmation to student {student_id} for {self._decorated_course._course_name}.")
        else:
            print(f"EMAIL NOTIFICATION: Sending enrollment failure notification to student {student_id} for {self._decorated_course._course_name}.")
        return result

if __name__ == "__main__":
    math_course = Course("MATH101", "Introduction to Math", 2)
    cs_course = Course("CS201", "Data Structures", 1)

    print("--- Basic Enrollment ---")
    math_course.enroll_student("S001")
    math_course.enroll_student("S002")
    math_course.enroll_student("S003") # Will fail due to capacity
    print(math_course.get_course_info())

    print("\n--- Enrollment with Prerequisite Check and Email Notification ---")
    advanced_cs_course = PrerequisiteCheckDecorator(
        EmailNotificationDecorator(Course("CS301", "Algorithms", 2)),
        ["CS201", "MATH101"]
    )

    student_a_completed = ["MATH101"]
    student_b_completed = ["MATH101", "CS201"]

    print(f"\nAttempting enrollment for Student A (completed: {student_a_completed})")
    advanced_cs_course.enroll_student("S004", student_a_completed)

    print(f"\nAttempting enrollment for Student B (completed: {student_b_completed})")
    advanced_cs_course.enroll_student("S005", student_b_completed)
    advanced_cs_course.enroll_student("S006", student_b_completed)
    advanced_cs_course.enroll_student("S007", student_b_completed) # Will fail due to capacity

    print(advanced_cs_course.get_course_info())