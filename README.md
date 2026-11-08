# Northstar Student Management System

A modular desktop student-management application built with Python's standard
library and Tkinter. It does not use a browser, web framework, database engine,
or third-party package. `styles.css` documents the visual tokens; `dashboard.py`
translates those colors, typography, and spacing into Tkinter/ttk configuration
because Tkinter does not parse CSS.

## Requirements and launch

- Python 3.9 or newer
- Tkinter (included with most standard Python distributions)

Run from this project directory:

```text
python main.py
```

The app creates `data/school_data.json` automatically when the first record is
saved. Student records can also be exported from the Students page as CSV.

## Features

- Add, edit, search, delete, and view student profiles and report cards
- Generate student IDs and distinguish graduate students
- Create, edit, delete, and capacity-manage courses; enroll students
- Add, edit, and delete grades; GPA recalculates automatically from graded
  courses, with gradebooks and honor roll views
- Mark present/absent and calculate each student's attendance percentage
- Switch between light and dark dashboard themes
- Automatically persist students, courses, teachers, and attendance to JSON
- Export student directory data to CSV
- Also expose simple `register_student`, `register_graduate`, `create_course`,
  `enroll_student`, `assign_grade`, and `get_honor_roll` methods for direct use

## Project layout

- `main.py` starts the app and chooses the data-file location.
- `dashboard.py` contains Tkinter views, forms, navigation, and theme mapping.
- `student.py` defines student data, enrollment, and GPA behavior.
- `graduate_student.py` specializes `Student` and overrides academic level.
- `course.py` enforces course capacity and maintains enrollment membership.
- `teacher.py` and `attendance.py` define teacher and attendance records.
- `school_system.py` coordinates validation, application operations, and storage.
- `storage.py` handles JSON persistence and CSV export.
- `styles.css` holds the CSS-inspired design specification.

## OOP concepts

- **Encapsulation and properties:** model fields are private and exposed through
  properties with validation where appropriate.
- **Inheritance and overriding:** `GraduateStudent` extends `Student` and
  overrides `academic_level` and serialization behavior.
- **Polymorphism:** regular and graduate students share an interface; reports
  use each object's overridden `academic_level`.
- **Abstraction:** `SchoolSystem` exposes school operations without requiring
  the interface to manage JSON details.
- **Composition:** `SchoolSystem` owns collections of student, course, teacher,
  and attendance objects; students and courses are linked by enrollment IDs.
- **Constructors and exception handling:** constructors establish valid model
  state; invalid values and storage errors are reported explicitly.

## Data and GPA

The JSON file is the source of truth. Student records retain course IDs and
grades, and course records retain enrolled student IDs. GPA follows the
provided sample's grading bands: 90+ = 4.0, 80–89.99 = 3.0, 70–79.99 = 2.0,
60–69.99 = 1.0, and below 60 = 0.0. GPA is calculated from graded courses only.
Graduate students use the stricter sample scale (93+ = 4.0, 85+ = 3.5, 80+ =
3.0, 75+ = 2.5, 70+ = 2.0, otherwise 0.0) and can track thesis completion.

## Tests

Run the standard-library tests from this directory:

```text
python -m unittest discover -s tests
```
