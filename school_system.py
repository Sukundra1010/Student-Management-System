"""Application services and in-memory school records."""

import os
from datetime import date

from attendance import Attendance
from course import Course
from graduate_student import GraduateStudent
from storage import Storage
from student import Student
from teacher import Teacher


class SchoolSystem:
    """Coordinates school records and persists each successful change."""

    def __init__(self, school_name="Student Management System", storage_path=None):
        if storage_path is None and isinstance(school_name, os.PathLike):
            storage_path = os.fspath(school_name)
            school_name = "Student Management System"
        elif (
            storage_path is None
            and isinstance(school_name, str)
            and (school_name.lower().endswith(".json") or os.path.sep in school_name)
        ):
            storage_path = school_name
            school_name = "Student Management System"
        self.school_name = str(school_name).strip() or "Student Management System"
        self.storage = Storage(storage_path) if storage_path else None
        self.students = {}
        self.courses = {}
        self._students = self.students
        self._courses = self.courses
        self.teachers = {}
        self.attendance_records = []
        self._load()

    def _load(self):
        if self.storage is None:
            return
        data = self.storage.load()
        for item in data.get("students", []):
            student_class = GraduateStudent if item.get("type") == "graduate" else Student
            student = student_class.from_dict(item)
            self.students[student.student_id] = student
        for item in data.get("courses", []):
            course = Course.from_dict(item)
            self.courses[course.course_id] = course
        for item in data.get("teachers", []):
            teacher = Teacher.from_dict(item)
            self.teachers[teacher.teacher_id] = teacher
        self.attendance_records = [
            Attendance.from_dict(item) for item in data.get("attendance", [])
        ]
        for course in self.courses.values():
            for student_id in course.student_ids:
                student = self.students.get(student_id)
                if student is not None:
                    course.add_student(student)

    def _save(self):
        if self.storage is None:
            return
        self.storage.save(
            {
                "students": [student.to_dict() for student in self.students.values()],
                "courses": [course.to_dict() for course in self.courses.values()],
                "teachers": [teacher.to_dict() for teacher in self.teachers.values()],
                "attendance": [record.to_dict() for record in self.attendance_records],
            }
        )

    @staticmethod
    def _next_id(prefix, records):
        largest = 0
        for record_id in records:
            suffix = str(record_id).removeprefix(prefix)
            if suffix.isdigit():
                largest = max(largest, int(suffix))
        return f"{prefix}{largest + 1:04d}"

    def add_student(
        self,
        name,
        age,
        email="",
        phone="",
        graduate=False,
        program="",
        thesis_title="",
        thesis_topic="",
    ):
        student_id = self._next_id("STU", self.students)
        student_class = GraduateStudent if graduate else Student
        extra = (
            {
                "program": program,
                "thesis_title": thesis_title,
                "thesis_topic": thesis_topic,
            }
            if graduate
            else {}
        )
        student = student_class(
            name,
            age,
            student_id=student_id,
            email=email,
            phone=phone,
            **extra,
        )
        self.students[student_id] = student
        self._save()
        return student

    def register_student(self, name, age):
        return self.add_student(name, age)

    def register_graduate(self, name, age, thesis=""):
        return self.add_student(
            name,
            age,
            graduate=True,
            thesis_topic=thesis,
            thesis_title=thesis,
        )

    def update_student(self, student_id, name, age, email="", phone=""):
        student = self.get_student(student_id)
        validated_name = Student._validate_name(name)
        validated_age = Student._validate_age(age)
        student.name = validated_name
        student.age = validated_age
        student.email = email
        student.phone = phone
        self._save()
        return student

    def delete_student(self, student_id):
        if student_id not in self.students:
            raise ValueError("Student was not found.")
        del self.students[student_id]
        for course in self.courses.values():
            course.remove_student(student_id)
        self.attendance_records = [
            record
            for record in self.attendance_records
            if record.student_id != student_id
        ]
        self._save()

    def get_student(self, student_id):
        try:
            return self.students[student_id]
        except KeyError as error:
            raise ValueError("Student was not found.") from error

    def search_students(self, query=""):
        query = str(query).strip().casefold()
        students = sorted(self.students.values(), key=lambda item: item.name.casefold())
        if not query:
            return students
        return [
            student
            for student in students
            if query in student.name.casefold()
            or query in student.student_id.casefold()
            or query in student.email.casefold()
        ]

    def add_course(self, name, teacher="", capacity=30, description=""):
        course_id = self._next_id("CRS", self.courses)
        course = Course(
            name,
            teacher,
            capacity,
            course_id=course_id,
            description=description,
        )
        self.courses[course_id] = course
        self._save()
        return course

    def create_course(self, name, instructor, max_students=30):
        return self.add_course(name, instructor, max_students)

    def update_course(self, course_id, name, teacher="", capacity=30, description=""):
        course = self.get_course(course_id)
        updated_course = Course(
            name,
            teacher,
            capacity,
            course_id=course_id,
            description=description,
            student_ids=course.student_ids,
        )
        self.courses[course_id] = updated_course
        for student_id in updated_course.student_ids:
            student = self.students.get(student_id)
            if student is not None:
                updated_course.add_student(student)
        self._save()
        return updated_course

    def delete_course(self, course_id):
        self.get_course(course_id)
        del self.courses[course_id]
        for student in self.students.values():
            student.remove_course(course_id)
        self._save()

    def get_course(self, course_id):
        try:
            return self.courses[course_id]
        except KeyError as error:
            raise ValueError("Course was not found.") from error

    def _find_course(self, course_reference):
        course = self.courses.get(course_reference)
        if course is not None:
            return course
        return next(
            (
                item
                for item in self.courses.values()
                if item.name == course_reference
            ),
            None,
        )

    def enroll_student(self, student_id, course_id):
        student = self.students.get(student_id)
        course = self._find_course(course_id)
        if student is None or course is None:
            return False
        if course.course_id in student.courses or course.name in student.courses:
            return True
        student.enroll(course)
        self._save()
        return True

    def assign_grade(self, student_id, course_id, grade):
        student = self.students.get(student_id)
        course = self._find_course(course_id)
        if student is None or course is None:
            return False
        grade_key = course.course_id or course.name
        if grade_key not in student.courses and course.name not in student.courses:
            raise ValueError("Enroll the student in this course before assigning a grade.")
        try:
            numeric_grade = float(grade)
        except (TypeError, ValueError) as error:
            raise ValueError("Grade must be a number from 0 to 100.") from error
        student.set_grade(grade_key, numeric_grade)
        self._save()
        return numeric_grade

    def delete_grade(self, student_id, course_id):
        student = self.get_student(student_id)
        course = self._find_course(course_id)
        if course is None:
            raise ValueError("Course was not found.")
        grade_key = course.course_id or course.name
        if grade_key not in student.courses and course.name in student.courses:
            grade_key = course.name
        student.clear_grade(grade_key)
        self._save()

    def report_card(self, student_id):
        student = self.get_student(student_id)
        courses = []
        for course_id, grade in student.courses.items():
            course = self.courses.get(course_id)
            courses.append(
                {
                    "course": course.name if course else course_id,
                    "grade": grade,
                    "course_id": course_id,
                }
            )
        return {"student": student, "courses": courses, "gpa": student.gpa}

    def honor_roll(self, minimum_gpa=3.5):
        return sorted(
            (
                student
                for student in self.students.values()
                if student.gpa >= minimum_gpa
                and any(grade is not None for grade in student.courses.values())
            ),
            key=lambda student: (-student.gpa, student.name.casefold()),
        )

    def get_honor_roll(self, min_gpa=3.0):
        return self.honor_roll(min_gpa)

    def mark_attendance(self, student_id, status, attendance_date=None):
        self.get_student(student_id)
        day = attendance_date or date.today().isoformat()
        record = Attendance(student_id, status, day)
        self.attendance_records = [
            existing
            for existing in self.attendance_records
            if not (existing.student_id == student_id and existing.date == day)
        ]
        self.attendance_records.append(record)
        self._save()
        return record

    def attendance_percentage(self, student_id):
        self.get_student(student_id)
        records = [
            record
            for record in self.attendance_records
            if record.student_id == student_id
        ]
        if not records:
            return 0.0
        present = sum(record.status == "Present" for record in records)
        return present * 100.0 / len(records)

    def attendance_for_date(self, attendance_date=None):
        day = attendance_date or date.today().isoformat()
        return {
            record.student_id: record.status
            for record in self.attendance_records
            if record.date == day
        }

    def add_teacher(self, name, email=""):
        teacher_id = self._next_id("TCH", self.teachers)
        teacher = Teacher(name, teacher_id, email)
        self.teachers[teacher_id] = teacher
        self._save()
        return teacher

    def update_graduate_details(self, student_id, program, thesis_title):
        student = self.get_student(student_id)
        if not isinstance(student, GraduateStudent):
            raise ValueError("Graduate details can only be updated for graduate students.")
        student.program = program
        student.thesis_title = thesis_title
        self._save()
        return student

    def __str__(self):
        return (
            f"{self.school_name}: {len(self.students)} students, "
            f"{len(self.courses)} courses"
        )
