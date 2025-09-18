import abc

class GradingStrategy(abc.ABC):
    @abc.abstractmethod
    def calculate_grade(self, score):
        pass

class NumericGrading(GradingStrategy):
    def calculate_grade(self, score):
        print(f"Calculated numeric grade: {score:.1f}/100")
        return f"{score:.1f}/100"

class LetterGrading(GradingStrategy):
    def calculate_grade(self, score):
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        print(f"Calculated letter grade: {grade} (Score: {score:.1f})")
        return grade

class PassFailGrading(GradingStrategy):
    def calculate_grade(self, score):
        if score >= 70:
            grade = "Pass"
        else:
            grade = "Fail"
        print(f"Calculated Pass/Fail grade: {grade} (Score: {score:.1f})")
        return grade

class Student:
    def __init__(self, student_id, name):
        self._student_id = student_id
        self._name = name
        self._grades = {}

    def add_score(self, course_id, score):
        if not (0 <= score <= 100):
            raise ValueError("Score must be between 0 and 100.")
        self._grades[course_id] = score

    def get_grade_report(self, course_id, grading_strategy: GradingStrategy):
        if course_id not in self._grades:
            return f"No score recorded for {course_id} for student {self._name}."
        score = self._grades[course_id]
        print(f"--- Student: {self._name}, Course: {course_id} ---")
        return grading_strategy.calculate_grade(score)

class Course:
    def __init__(self, course_id, name, default_grading_strategy: GradingStrategy):
        self._course_id = course_id
        self._name = name
        self._grading_strategy = default_grading_strategy
        self._students_scores = {}

    def set_grading_strategy(self, strategy: GradingStrategy):
        self._grading_strategy = strategy

    def enroll_student_with_score(self, student_id, score):
        if not (0 <= score <= 100):
            raise ValueError("Score must be between 0 and 100.")
        self._students_scores[student_id] = score

    def get_course_grades(self):
        print(f"\n--- Grades for Course: {self._name} ({self._course_id}) ---")
        for student_id, score in self._students_scores.items():
            print(f"Student {student_id}: ", end="")
            self._grading_strategy.calculate_grade(score)

if __name__ == "__main__":
    student1 = Student("S001", "Alice")
    student2 = Student("S002", "Bob")
    student3 = Student("S003", "Charlie")

    student1.add_score("CS101", 88.5)
    student2.add_score("CS101", 62.0)
    student3.add_score("CS101", 95.0)

    student1.add_score("ENG200", 71.0)
    student2.add_score("ENG200", 45.0)

    print("\n*** Student-centric grading ***")
    print(student1.get_grade_report("CS101", LetterGrading()))
    print(student2.get_grade_report("CS101", PassFailGrading()))
    print(student3.get_grade_report("ENG200", NumericGrading()))

    cs_course = Course("CS101", "Intro to Programming", LetterGrading())
    cs_course.enroll_student_with_score("S001", 88.5)
    cs_course.enroll_student_with_score("S002", 62.0)
    cs_course.enroll_student_with_score("S003", 95.0)
    cs_course.get_course_grades()

    eng_course = Course("ENG200", "Literature Analysis", PassFailGrading())
    eng_course.enroll_student_with_score("S001", 71.0)
    eng_course.enroll_student_with_score("S002", 45.0)
    eng_course.get_course_grades()

    eng_course.set_grading_strategy(LetterGrading())
    eng_course.get_course_grades()