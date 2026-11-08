"""Tests for student, course, grade, attendance, and file operations."""

import csv
import os
import tempfile
import unittest

from course import Course
from graduate_student import GraduateStudent
from school_system import SchoolSystem
from storage import Storage


class SchoolSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_path = os.path.join(self.temp_dir.name, "school_data.json")
        self.system = SchoolSystem(storage_path=self.data_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_student_course_grade_gpa_and_report_card(self):
        student = self.system.add_student("Ada Lovelace", 18)
        course = self.system.add_course("Mathematics", "Dr. Curie", 30)
        self.system.enroll_student(student.student_id, course.course_id)
        self.system.assign_grade(student.student_id, course.course_id, "96")

        self.assertEqual(student.student_id, "STU0001")
        self.assertEqual(student.gpa, 4.0)
        self.assertEqual(
            self.system.report_card(student.student_id)["courses"][0]["course"],
            "Mathematics",
        )
        self.assertEqual(course.enrollment, 1)

    def test_grade_can_be_added_updated_and_deleted_with_gpa_recalculation(self):
        student = self.system.add_student("Ada Lovelace", 18)
        first_course = self.system.add_course("Mathematics")
        second_course = self.system.add_course("Computing")
        self.system.enroll_student(student.student_id, first_course.course_id)
        self.system.enroll_student(student.student_id, second_course.course_id)
        self.system.assign_grade(student.student_id, first_course.course_id, 100)
        self.system.assign_grade(student.student_id, second_course.course_id, 60)
        self.assertEqual(student.gpa, 3.0)

        self.system.assign_grade(student.student_id, second_course.course_id, 90)
        self.assertEqual(student.gpa, 4.0)

        self.system.delete_grade(student.student_id, second_course.course_id)
        self.assertEqual(student.courses[second_course.course_id], None)
        self.assertEqual(student.gpa, 4.0)
        reloaded = SchoolSystem(storage_path=self.data_path)
        reloaded_student = reloaded.get_student(student.student_id)
        self.assertEqual(reloaded_student.courses[second_course.course_id], None)
        self.assertEqual(reloaded_student.gpa, 4.0)

    def test_example_api_supports_courses_rosters_and_graduate_gpa(self):
        school = SchoolSystem("Python Academy")
        alice = school.register_student("Alice", 20)
        charlie = school.register_graduate(
            "Charlie", 25, "Machine Learning in Python"
        )
        python = school.create_course("Python 101", "Dr. Smith", 2)

        self.assertTrue(school.enroll_student(alice.student_id, "Python 101"))
        self.assertTrue(school.enroll_student(charlie.student_id, "Python 101"))
        self.assertFalse(school.enroll_student(alice.student_id, "Missing course"))
        school.assign_grade(alice.student_id, "Python 101", 92)
        school.assign_grade(charlie.student_id, "Python 101", 85)

        self.assertEqual(python.instructor, "Dr. Smith")
        self.assertEqual(python.enrollment_count, 2)
        self.assertTrue(python.is_full)
        self.assertEqual(charlie.gpa, 3.5)
        self.assertTrue(charlie.complete_thesis())
        self.assertEqual([item.name for item in school.get_honor_roll()], ["Alice", "Charlie"])
        self.assertIn("Python Academy", str(school))
        self.assertEqual(len(python.get_roster()), 2)

    def test_course_sample_constructor_and_full_result(self):
        course = Course("OOP Concepts", "Prof. Jones", 1)
        student = self.system.register_student("Grace Hopper", 20)

        self.assertTrue(course.add_student(student))
        self.assertFalse(course.add_student("STU9999"))
        self.assertEqual(course.max_students, 1)
        self.assertIn("Prof. Jones", str(course))

    def test_search_honor_roll_and_academic_records_persist(self):
        top_student = self.system.add_student(
            "Ada Lovelace", 18, email="ada@example.test"
        )
        other_student = self.system.add_student("Grace Hopper", 20)
        course = self.system.add_course("Mathematics")
        for student, grade in ((top_student, 95), (other_student, 85)):
            self.system.enroll_student(student.student_id, course.course_id)
            self.system.assign_grade(student.student_id, course.course_id, grade)

        self.assertEqual(
            [student.student_id for student in self.system.search_students("ada@")],
            [top_student.student_id],
        )
        self.assertEqual(
            [student.student_id for student in self.system.honor_roll()],
            [top_student.student_id],
        )
        reloaded = SchoolSystem(storage_path=self.data_path)
        self.assertEqual(
            reloaded.get_student(top_student.student_id).gpa,
            4.0,
        )
        self.assertEqual(
            reloaded.get_course(course.course_id).enrollment,
            2,
        )

    def test_capacity_is_enforced_and_invalid_student_update_is_safe(self):
        student = self.system.add_student("Grace Hopper", 20)
        other = self.system.add_student("Katherine Johnson", 19)
        course = self.system.add_course("Computing", capacity=1)
        self.system.enroll_student(student.student_id, course.course_id)

        with self.assertRaises(ValueError):
            self.system.enroll_student(other.student_id, course.course_id)
        with self.assertRaises(ValueError):
            self.system.update_student(student.student_id, "", 21)
        self.assertEqual(self.system.get_student(student.student_id).name, "Grace Hopper")

    def test_graduate_student_persists_with_subclass_fields(self):
        student = self.system.add_student(
            "Alan Turing",
            25,
            graduate=True,
            program="Computer Science",
            thesis_title="Computing Machinery",
        )
        reloaded = SchoolSystem(storage_path=self.data_path).get_student(
            student.student_id
        )

        self.assertIsInstance(reloaded, GraduateStudent)
        self.assertEqual(reloaded.academic_level, "Graduate")
        self.assertEqual(reloaded.program, "Computer Science")

    def test_graduate_thesis_completion_and_gpa_persist(self):
        student = self.system.add_student(
            "Alan Turing",
            25,
            graduate=True,
            thesis_topic="Computing Machinery",
        )
        course = self.system.add_course("Research")
        self.system.enroll_student(student.student_id, course.course_id)
        self.system.assign_grade(student.student_id, course.course_id, 85)
        student.complete_thesis()
        self.system._save()

        reloaded = SchoolSystem(storage_path=self.data_path).get_student(
            student.student_id
        )
        self.assertEqual(reloaded.gpa, 3.5)
        self.assertTrue(reloaded.thesis_completed)
        self.assertEqual(reloaded.thesis_topic, "Computing Machinery")

    def test_course_capacity_cannot_be_reduced_below_enrollment(self):
        student = self.system.add_student("Dorothy Vaughan", 22)
        course = self.system.add_course("Physics", capacity=2)
        self.system.enroll_student(student.student_id, course.course_id)

        with self.assertRaises(ValueError):
            self.system.update_course(course.course_id, "Physics", capacity=0)
        self.assertEqual(self.system.get_course(course.course_id).capacity, 2)

    def test_attendance_is_upserted_and_percentage_calculated(self):
        student = self.system.add_student("Mary Jackson", 21)
        self.system.mark_attendance(student.student_id, "Present", "2026-01-01")
        self.system.mark_attendance(student.student_id, "Absent", "2026-01-02")
        self.system.mark_attendance(student.student_id, "Present", "2026-01-02")

        self.assertEqual(self.system.attendance_percentage(student.student_id), 100.0)
        self.assertEqual(len(self.system.attendance_records), 2)

    def test_delete_student_removes_enrollment_and_attendance(self):
        student = self.system.add_student("Joan Clarke", 20)
        course = self.system.add_course("Cryptography")
        self.system.enroll_student(student.student_id, course.course_id)
        self.system.mark_attendance(student.student_id, "Present")

        self.system.delete_student(student.student_id)

        self.assertEqual(self.system.get_course(course.course_id).enrollment, 0)
        self.assertEqual(self.system.attendance_records, [])

    def test_delete_course_removes_student_grade(self):
        student = self.system.add_student("Joan Clarke", 20)
        course = self.system.add_course("Cryptography")
        self.system.enroll_student(student.student_id, course.course_id)
        self.system.assign_grade(student.student_id, course.course_id, 95)

        self.system.delete_course(course.course_id)

        self.assertNotIn(course.course_id, student.courses)
        self.assertEqual(student.gpa, 0.0)

    def test_student_csv_export(self):
        student = self.system.add_student("Edsger Dijkstra", 19, email="ed@example.test")
        csv_path = os.path.join(self.temp_dir.name, "students.csv")
        Storage.export_students_csv(csv_path, [student])

        with open(csv_path, newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(rows[0]["student_id"], student.student_id)
        self.assertEqual(rows[0]["email"], "ed@example.test")


if __name__ == "__main__":
    unittest.main()
