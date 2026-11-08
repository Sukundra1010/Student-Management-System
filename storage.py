"""JSON persistence and CSV export using the Python standard library."""

import csv
import json
import os
import tempfile


class Storage:
    def __init__(self, json_path):
        self.json_path = os.path.abspath(json_path)

    def load(self):
        if not os.path.exists(self.json_path):
            return {}
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            raise RuntimeError(f"Could not load school data: {error}") from error
        if not isinstance(data, dict):
            raise RuntimeError("The school data file must contain a JSON object.")
        return data

    def save(self, data):
        directory = os.path.dirname(self.json_path)
        os.makedirs(directory, exist_ok=True)
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=directory,
                delete=False,
                suffix=".tmp",
            ) as file:
                temporary_path = file.name
                json.dump(data, file, indent=2, ensure_ascii=False)
                file.write("\n")
            os.replace(temporary_path, self.json_path)
        except OSError as error:
            if temporary_path and os.path.exists(temporary_path):
                os.remove(temporary_path)
            raise RuntimeError(f"Could not save school data: {error}") from error

    @staticmethod
    def export_students_csv(path, students):
        try:
            with open(path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=(
                        "student_id",
                        "name",
                        "age",
                        "email",
                        "phone",
                        "academic_level",
                        "gpa",
                        "enrollment_date",
                    ),
                )
                writer.writeheader()
                for student in students:
                    writer.writerow(
                        {
                            "student_id": student.student_id,
                            "name": student.name,
                            "age": student.age,
                            "email": student.email,
                            "phone": student.phone,
                            "academic_level": student.academic_level,
                            "gpa": f"{student.gpa:.2f}",
                            "enrollment_date": student.enrollment_date,
                        }
                    )
        except OSError as error:
            raise RuntimeError(f"Could not export students: {error}") from error
