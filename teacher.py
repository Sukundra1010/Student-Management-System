"""Teacher model."""


class Teacher:
    def __init__(self, name, teacher_id, email=""):
        self.name = name
        self.teacher_id = teacher_id
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        name = str(value).strip()
        if not name:
            raise ValueError("Teacher name is required.")
        self._name = name

    @property
    def teacher_id(self):
        return self._teacher_id

    @teacher_id.setter
    def teacher_id(self, value):
        teacher_id = str(value).strip()
        if not teacher_id:
            raise ValueError("Teacher ID is required.")
        self._teacher_id = teacher_id

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = str(value).strip()

    def to_dict(self):
        return {
            "teacher_id": self.teacher_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
