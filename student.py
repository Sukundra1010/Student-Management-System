"""Student records and academic calculations."""

from datetime import date


class Student:
    """A student and their course grades."""

    _next_id = 1

    def __init__(
        self,
        name,
        age,
        student_id=None,
        email="",
        phone="",
        courses=None,
        enrollment_date=None,
    ):
        self._name = self._validate_name(name)
        self._age = self._validate_age(age)
        self._email = str(email).strip()
        self._phone = str(phone).strip()
        self._student_id = student_id or self.generate_id()
        self._courses = dict(courses or {})
        self._enrollment_date = enrollment_date or date.today().isoformat()
        self._sync_id_counter(self._student_id)

    @classmethod
    def generate_id(cls):
        student_id = f"STU{Student._next_id:04d}"
        Student._next_id += 1
        return student_id

    @classmethod
    def _sync_id_counter(cls, student_id):
        suffix = str(student_id).removeprefix("STU")
        if suffix.isdigit():
            Student._next_id = max(Student._next_id, int(suffix) + 1)

    @staticmethod
    def _validate_name(value):
        name = str(value).strip()
        if not name:
            raise ValueError("Student name is required.")
        return name

    @staticmethod
    def _validate_age(value):
        if isinstance(value, float) and not value.is_integer():
            raise ValueError("Age must be a whole number.")
        try:
            age = int(value)
        except (TypeError, ValueError) as error:
            raise ValueError("Age must be a whole number.") from error
        if not 3 <= age <= 120:
            raise ValueError("Age must be between 3 and 120.")
        return age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self._validate_name(value)

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = self._validate_age(value)

    @property
    def student_id(self):
        return self._student_id

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = str(value).strip()

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = str(value).strip()

    @property
    def enrollment_date(self):
        return self._enrollment_date

    @property
    def courses(self):
        return self._courses.copy()

    def enroll(self, course):
        course_key = course.course_id or course.name
        if course_key not in self._courses:
            if not course.add_student(self):
                raise ValueError(f"{course.name} has reached its capacity.")
            self._courses[course_key] = None

    def set_grade(self, course_name, grade):
        course_key = course_name
        if course_key not in self._courses:
            course_key = next(
                (
                    key
                    for key in self._courses
                    if getattr(key, "name", None) == course_name
                ),
                course_name,
            )
        if course_key not in self._courses:
            raise ValueError("The student is not enrolled in this course.")
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise ValueError("Grade must be a number from 0 to 100.")
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100.")
        self._courses[course_key] = float(grade)

    def clear_grade(self, course_name):
        course_key = course_name
        if course_key not in self._courses:
            course_key = next(
                (
                    key
                    for key in self._courses
                    if getattr(key, "name", None) == course_name
                ),
                course_name,
            )
        if course_key not in self._courses:
            raise ValueError("The student is not enrolled in this course.")
        if self._courses[course_key] is None:
            raise ValueError("This course does not have a grade to delete.")
        self._courses[course_key] = None

    def remove_course(self, course_id):
        self._courses.pop(course_id, None)

    @property
    def gpa(self):
        grades = [grade for grade in self._courses.values() if grade is not None]
        if not grades:
            return 0.0
        average = sum(grades) / len(grades)
        if average >= 90:
            return 4.0
        if average >= 80:
            return 3.0
        if average >= 70:
            return 2.0
        if average >= 60:
            return 1.0
        return 0.0

    @property
    def academic_level(self):
        return "Student"

    def to_dict(self):
        return {
            "type": "student",
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "phone": self.phone,
            "enrollment_date": self.enrollment_date,
            "courses": self._courses,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            age=data["age"],
            student_id=data["student_id"],
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            courses=data.get("courses", {}),
            enrollment_date=data.get("enrollment_date"),
        )

    def __str__(self):
        return f"{self.student_id}: {self.name} (GPA: {self.gpa:.1f})"