"""Course model and capacity management."""


class Course:
    def __init__(
        self,
        name,
        instructor="",
        max_students=30,
        *,
        course_id=None,
        capacity=None,
        description="",
        student_ids=None,
    ):
        self._course_id = str(course_id or "").strip()
        self._name = self._validate_name(name)
        self._teacher = str(instructor).strip()
        self._capacity = self._validate_capacity(
            max_students if capacity is None else capacity
        )
        self._description = str(description).strip()
        self._student_ids = set(student_ids or [])
        self._students = []
        if len(self._student_ids) > self._capacity:
            raise ValueError("Course capacity cannot be below current enrollment.")

    @staticmethod
    def _validate_name(value):
        name = str(value).strip()
        if not name:
            raise ValueError("Course name is required.")
        return name

    @staticmethod
    def _validate_capacity(value):
        if isinstance(value, float) and not value.is_integer():
            raise ValueError("Capacity must be a whole number.")
        try:
            capacity = int(value)
        except (TypeError, ValueError) as error:
            raise ValueError("Capacity must be a whole number.") from error
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")
        return capacity

    @property
    def course_id(self):
        return self._course_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self._validate_name(value)

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, value):
        self._teacher = str(value).strip()

    @property
    def instructor(self):
        return self.teacher

    @instructor.setter
    def instructor(self, value):
        self.teacher = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        capacity = self._validate_capacity(value)
        if capacity < self.enrollment:
            raise ValueError("Capacity cannot be below current enrollment.")
        self._capacity = capacity

    @property
    def max_students(self):
        return self.capacity

    @max_students.setter
    def max_students(self, value):
        self.capacity = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = str(value).strip()

    @property
    def student_ids(self):
        return frozenset(self._student_ids)

    @property
    def enrollment(self):
        return len(self._student_ids)

    def add_student(self, student_id):
        student = student_id if hasattr(student_id, "student_id") else None
        student_id = str(getattr(student_id, "student_id", student_id)).strip()
        if not student_id:
            raise ValueError("Student ID is required.")
        if student_id in self._student_ids:
            if student is not None:
                self._remember_student(student)
            return True
        if self.enrollment >= self.capacity:
            return False
        self._student_ids.add(student_id)
        if student is not None:
            self._remember_student(student)
        return True

    def _remember_student(self, student):
        if all(existing.student_id != student.student_id for existing in self._students):
            self._students.append(student)

    def remove_student(self, student_id):
        student_id = str(getattr(student_id, "student_id", student_id))
        self._student_ids.discard(student_id)
        self._students = [
            student for student in self._students if student.student_id != student_id
        ]

    @property
    def enrollment_count(self):
        return self.enrollment

    @property
    def is_full(self):
        return self.enrollment >= self.capacity

    def get_roster(self):
        """Print and return enrolled students, when their objects are available."""
        print(f"\n--- {self.name} Roster ---")
        print(f"Instructor: {self.instructor}")
        print(f"Enrolled: {self.enrollment_count}/{self.max_students}")
        known_students = {student.student_id: student for student in self._students}
        roster = []
        for student_id in sorted(self._student_ids):
            student = known_students.get(student_id)
            if student is None:
                print(f"  - {student_id}")
            else:
                print(f"  - {student.name} ({student.student_id})")
            roster.append(student if student is not None else student_id)
        return roster

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "name": self.name,
            "teacher": self.teacher,
            "capacity": self.capacity,
            "description": self.description,
            "student_ids": sorted(self._student_ids),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            instructor=data.get("instructor", data.get("teacher", "")),
            max_students=data.get("max_students", data.get("capacity", 30)),
            course_id=data.get("course_id"),
            description=data.get("description", ""),
            student_ids=data.get("student_ids", []),
        )

    def __str__(self):
        return (
            f"{self.name} by {self.instructor} "
            f"({self.enrollment_count}/{self.max_students})"
        )
