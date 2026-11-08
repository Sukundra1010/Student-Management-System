"""Attendance records."""

from datetime import date


class Attendance:
    STATUSES = ("Present", "Absent")

    def __init__(self, student_id, status, attendance_date=None):
        self._student_id = str(student_id).strip()
        if not self._student_id:
            raise ValueError("Student ID is required.")
        normalized_status = str(status).strip().title()
        if normalized_status not in self.STATUSES:
            raise ValueError("Attendance status must be Present or Absent.")
        self._status = normalized_status
        self._date = str(attendance_date or date.today().isoformat())
        try:
            date.fromisoformat(self._date)
        except ValueError as error:
            raise ValueError("Attendance date must use YYYY-MM-DD format.") from error

    @property
    def student_id(self):
        return self._student_id

    @property
    def status(self):
        return self._status

    @property
    def date(self):
        return self._date

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "status": self.status,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["status"], data.get("date"))