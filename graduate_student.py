"""Graduate student specialization."""

from student import Student


class GraduateStudent(Student):
    """A student enrolled in a graduate program."""

    def __init__(
        self,
        name,
        age,
        thesis_topic="",
        program="",
        thesis_title="",
        *,
        thesis_completed=False,
        **student_data,
    ):
        super().__init__(name, age, **student_data)
        self._program = str(program).strip()
        self._thesis_topic = str(thesis_topic or thesis_title).strip()
        self._thesis_title = str(thesis_title or thesis_topic).strip()
        self._thesis_completed = bool(thesis_completed)

    @property
    def program(self):
        return self._program

    @program.setter
    def program(self, value):
        self._program = str(value).strip()

    @property
    def thesis_title(self):
        return self._thesis_title

    @thesis_title.setter
    def thesis_title(self, value):
        self._thesis_title = str(value).strip()
        self._thesis_topic = self._thesis_title

    @property
    def thesis_topic(self):
        return self._thesis_topic

    @thesis_topic.setter
    def thesis_topic(self, topic):
        self._thesis_topic = str(topic).strip()
        self._thesis_title = self._thesis_topic

    @property
    def thesis_completed(self):
        return self._thesis_completed

    def complete_thesis(self):
        if not self.thesis_topic:
            return False
        self._thesis_completed = True
        return True

    @property
    def gpa(self):
        grades = [grade for grade in self._courses.values() if grade is not None]
        if not grades:
            return 0.0
        average = sum(grades) / len(grades)
        if average >= 93:
            return 4.0
        if average >= 85:
            return 3.5
        if average >= 80:
            return 3.0
        if average >= 75:
            return 2.5
        if average >= 70:
            return 2.0
        return 0.0

    @property
    def academic_level(self):
        return "Graduate"

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "type": "graduate",
                "program": self.program,
                "thesis_title": self.thesis_title,
                "thesis_topic": self.thesis_topic,
                "thesis_completed": self.thesis_completed,
            }
        )
        return data

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
            program=data.get("program", ""),
            thesis_title=data.get("thesis_title", ""),
            thesis_topic=data.get("thesis_topic", ""),
            thesis_completed=data.get("thesis_completed", False),
        )

    def __str__(self):
        thesis = "Thesis Complete" if self.thesis_completed else "Thesis Pending"
        return (
            f"{self.student_id}: {self.name} [Grad] "
            f"(GPA: {self.gpa:.1f}, {thesis})"
        )
