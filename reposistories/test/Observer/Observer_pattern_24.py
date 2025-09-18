class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, student_id, course_name, grade):
        for observer in self._observers:
            observer.update(student_id, course_name, grade)

class Course(Subject):
    def __init__(self, course_name):
        super().__init__()
        self.course_name = course_name
        self._grades = {}

    def post_grade(self, student_id, student_name, grade):
        if student_id not in self._grades:
            self._grades[student_id] = {'name': student_name, 'grade': grade}
            print(f"Education: {self.course_name}: Grade posted for {student_name} ({student_id}): {grade}")
            self.notify(student_id, self.course_name, grade)
        elif self._grades[student_id]['grade'] != grade:
            self._grades[student_id]['grade'] = grade
            print(f"Education: {self.course_name}: Grade updated for {student_name} ({student_id}): {grade}")
            self.notify(student_id, self.course_name, grade)
        else:
            print(f"Education: {self.course_name}: Grade for {student_name} ({student_id}) is already {grade}. No change.")

class StudentPortal:
    def __init__(self, portal_id):
        self.portal_id = portal_id

    def update(self, student_id, course_name, grade):
        print(f"Education: Student Portal ({self.portal_id}): Displaying new grade for Student {student_id} in {course_name}: {grade}")

class ParentNotifier:
    def __init__(self, parent_email):
        self.parent_email = parent_email

    def update(self, student_id, course_name, grade):
        if grade < 'C': # Example condition for parent notification
            print(f"Education: Parent Notifier: Email to {self.parent_email} for Student {student_id} in {course_name}: Grade {grade} (Below expectation)")
        else:
            print(f"Education: Parent Notifier: Email to {self.parent_email} for Student {student_id} in {course_name}: Grade {grade}")

class AcademicAdvisor:
    def update(self, student_id, course_name, grade):
        if grade == 'F':
            print(f"Education: Academic Advisor: Alert! Student {student_id} received 'F' in {course_name}. Scheduling follow-up.")
        else:
            print(f"Education: Academic Advisor: Noted grade {grade} for Student {student_id} in {course_name}.")

math_course = Course("Calculus I")

student_portal_s1 = StudentPortal("SP-001")
parent_notifier_s1 = ParentNotifier("parent1@example.com")
academic_advisor = AcademicAdvisor()

math_course.attach(student_portal_s1)
math_course.attach(parent_notifier_s1)
math_course.attach(academic_advisor)

print("--- Education Simulation: Post initial grades ---")
math_course.post_grade("S001", "Alice", 'B')
math_course.post_grade("S002", "Bob", 'D')

print("\n--- Education Simulation: Update a grade ---")
math_course.post_grade("S001", "Alice", 'A')

print("\n--- Education Simulation: Post a failing grade ---")
math_course.post_grade("S003", "Charlie", 'F')

print("\n--- Education Simulation: Detach parent notifier for S002 ---")
math_course.detach(parent_notifier_s1)
math_course.post_grade("S002", "Bob", 'C')