"""Start the Student Management System desktop application."""

import os

from dashboard import StudentManagementApp
from school_system import SchoolSystem


def main():
    data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data",
        "school_data.json",
    )
    system = SchoolSystem(storage_path=data_path)
    app = StudentManagementApp(system)
    app.mainloop()


if __name__ == "__main__":
    main()
