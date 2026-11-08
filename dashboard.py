"""Tkinter dashboard for the Student Management System."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from graduate_student import GraduateStudent
from storage import Storage


LIGHT = {
    "navy": "#12233f",
    "navy_deep": "#0b172b",
    "blue": "#3c63f5",
    "blue_soft": "#e9efff",
    "background": "#f3f6fb",
    "surface": "#ffffff",
    "text": "#18263d",
    "muted": "#78869b",
    "border": "#e4eaf2",
    "danger": "#d84b5b",
    "teal": "#12a88a",
    "amber": "#e2a53a",
    "violet": "#8065df",
    "banner": "#e51f2b",
    "sidebar": "#edf7ef",
    "sidebar_text": "#3e584a",
    "sidebar_active": "#c9efd2",
    "orange": "#ff9800",
    "green": "#42ad58",
    "red": "#df3542",
}

DARK = {
    "navy": "#111d32",
    "navy_deep": "#091321",
    "blue": "#7892ff",
    "blue_soft": "#293958",
    "background": "#111927",
    "surface": "#1b2739",
    "text": "#edf2fc",
    "muted": "#9eacc1",
    "border": "#334157",
    "danger": "#ff7d8a",
    "teal": "#40c9aa",
    "amber": "#edbd65",
    "violet": "#a28af4",
    "banner": "#c92734",
    "sidebar": "#17251f",
    "sidebar_text": "#c1d5c8",
    "sidebar_active": "#28543a",
    "orange": "#f0a332",
    "green": "#4cba69",
    "red": "#ed5963",
}


class StudentManagementApp(tk.Tk):
    """Window, navigation, and forms for the school management system."""

    PAGES = ("Overview", "Students", "Courses", "Academics", "Attendance")

    def __init__(self, system):
        super().__init__()
        self.system = system
        self.dark_mode = False
        self.colors = LIGHT
        self.current_page = "Overview"
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_students())
        self.title(f"Northstar | {self.system.school_name}")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = min(1280, screen_width - 48)
        height = min(800, screen_height - 72)
        self.geometry(
            f"{width}x{height}+{(screen_width - width) // 2}+{(screen_height - height) // 2}"
        )
        self.minsize(1000, 650)
        self.configure(bg=self.colors["background"])
        self._configure_styles()
        self._build_shell()
        self.show_page("Overview")

    def _configure_styles(self):
        colors = self.colors
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure(
            ".",
            font=("Segoe UI", 10),
            background=colors["background"],
            foreground=colors["text"],
        )
        self.style.configure("TFrame", background=colors["background"])
        self.style.configure("Surface.TFrame", background=colors["surface"])
        self.style.configure(
            "TLabel", background=colors["background"], foreground=colors["text"]
        )
        self.style.configure(
            "Surface.TLabel",
            background=colors["surface"],
            foreground=colors["text"],
        )
        self.style.configure(
            "Muted.TLabel",
            background=colors["background"],
            foreground=colors["muted"],
        )
        self.style.configure(
            "CardTitle.TLabel",
            background=colors["surface"],
            foreground=colors["muted"],
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "CardValue.TLabel",
            background=colors["surface"],
            foreground=colors["text"],
            font=("Segoe UI", 24, "bold"),
        )
        self.style.configure(
            "Title.TLabel",
            background=colors["background"],
            foreground=colors["text"],
            font=("Segoe UI", 22, "bold"),
        )
        self.style.configure(
            "Subtitle.TLabel",
            background=colors["background"],
            foreground=colors["muted"],
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "TButton",
            padding=(13, 9),
            background=colors["surface"],
            foreground=colors["text"],
            bordercolor=colors["border"],
            focusthickness=0,
            font=("Segoe UI", 9, "bold"),
        )
        self.style.map(
            "TButton",
            background=[
                ("pressed", colors["blue_soft"]),
                ("active", colors["blue_soft"]),
            ],
            bordercolor=[("focus", colors["blue"])],
        )
        self.style.configure(
            "Primary.TButton",
            padding=(14, 10),
            background=colors["blue"],
            foreground="#ffffff",
            bordercolor=colors["blue"],
            font=("Segoe UI", 10, "bold"),
            focusthickness=0,
        )
        self.style.map(
            "Primary.TButton",
            background=[
                ("pressed", colors["navy"]),
                ("active", colors["navy"]),
            ],
            foreground=[("active", "#ffffff")],
        )
        self.style.configure(
            "Danger.TButton",
            padding=(13, 9),
            background=colors["danger"],
            foreground="#ffffff",
            bordercolor=colors["danger"],
            font=("Segoe UI", 9, "bold"),
            focusthickness=0,
        )
        self.style.map(
            "Danger.TButton",
            background=[
                ("pressed", colors["navy"]),
                ("active", colors["danger"]),
            ],
            foreground=[("active", "#ffffff")],
        )
        self.style.configure(
            "Treeview",
            rowheight=40,
            background=colors["surface"],
            fieldbackground=colors["surface"],
            foreground=colors["text"],
            bordercolor=colors["border"],
            lightcolor=colors["border"],
            darkcolor=colors["border"],
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Treeview.Heading",
            background=colors["blue_soft"],
            foreground=colors["muted"],
            font=("Segoe UI", 9, "bold"),
            padding=(12, 12),
        )
        self.style.map(
            "Treeview",
            background=[("selected", colors["blue_soft"])],
            foreground=[("selected", colors["text"])],
        )
        self.style.configure(
            "Vertical.TScrollbar",
            background=colors["surface"],
            troughcolor=colors["background"],
            bordercolor=colors["background"],
            arrowcolor=colors["muted"],
        )
        self.style.configure(
            "Horizontal.TScrollbar",
            background=colors["surface"],
            troughcolor=colors["background"],
            bordercolor=colors["background"],
            arrowcolor=colors["muted"],
        )
        self.style.configure(
            "TEntry",
            padding=(10, 9),
            fieldbackground=colors["surface"],
            foreground=colors["text"],
            bordercolor=colors["border"],
            insertcolor=colors["text"],
            font=("Segoe UI", 10),
        )
        self.style.map(
            "TEntry",
            bordercolor=[("focus", colors["blue"])],
            lightcolor=[("focus", colors["blue"])],
        )
        self.style.configure(
            "TCombobox",
            padding=(10, 8),
            fieldbackground=colors["surface"],
            foreground=colors["text"],
            bordercolor=colors["border"],
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", colors["surface"])],
            selectbackground=[("readonly", colors["blue_soft"])],
            selectforeground=[("readonly", colors["text"])],
        )
        self.style.configure(
            "TCheckbutton",
            background=colors["background"],
            foreground=colors["text"],
            font=("Segoe UI", 10),
        )
        self.style.map(
            "TCheckbutton",
            background=[("active", colors["background"])],
            foreground=[("active", colors["text"])],
        )

    def _build_shell(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.banner = tk.Frame(self, bg=self.colors["banner"], height=68)
        self.banner.grid(row=0, column=0, sticky="ew")
        self.banner.grid_propagate(False)
        tk.Label(
            self.banner,
            text="STUDENT MANAGEMENT SYSTEM",
            bg=self.colors["banner"],
            fg="#ffffff",
            font=("Segoe UI", 25, "bold"),
        ).pack(expand=True)

        self.workspace = tk.Frame(self, bg=self.colors["background"])
        self.workspace.grid(row=1, column=0, sticky="nsew")
        self.workspace.grid_columnconfigure(1, weight=1)
        self.workspace.grid_rowconfigure(0, weight=1)
        self.sidebar = tk.Frame(
            self.workspace,
            bg=self.colors["sidebar"],
            width=190,
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        tk.Label(
            self.sidebar,
            text="MENU",
            bg=self.colors["sidebar"],
            fg=self.colors["muted"],
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=16, pady=(20, 10))
        self.nav_buttons = {}
        for page in self.PAGES:
            labels = {
                "Overview": "Dashboard",
                "Students": "Students",
                "Courses": "Class",
                "Academics": "Reports",
                "Attendance": "Attendance",
            }
            button = tk.Button(
                self.sidebar,
                text=f"  {self._page_icon(page)}   {labels[page]}",
                anchor="w",
                relief="flat",
                bd=0,
                padx=13,
                pady=10,
                bg=self.colors["sidebar"],
                fg=self.colors["sidebar_text"],
                activebackground=self.colors["sidebar_active"],
                activeforeground=self.colors["text"],
                font=("Segoe UI", 9, "bold"),
                command=lambda selected=page: self.show_page(selected),
            )
            button.pack(fill="x", padx=8, pady=2)
            self.nav_buttons[page] = button

        footer = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        footer.pack(side="bottom", fill="x", padx=12, pady=14)
        tk.Label(
            footer,
            text=self.system.school_name,
            bg=self.colors["sidebar"],
            fg=self.colors["sidebar_text"],
            font=("Segoe UI", 9, "bold"),
            anchor="w",
            wraplength=160,
            justify="left",
        ).pack(anchor="w", pady=(0, 8))
        self.theme_button = tk.Button(
            footer,
            text="◐  Dark mode",
            anchor="w",
            relief="flat",
            bd=0,
            padx=8,
            pady=8,
            bg=self.colors["sidebar_active"],
            fg=self.colors["sidebar_text"],
            activebackground=self.colors["sidebar_active"],
            activeforeground=self.colors["text"],
            font=("Segoe UI", 9),
            command=self.toggle_theme,
        )
        self.theme_button.pack(fill="x")

        self.main_area = ttk.Frame(self.workspace, padding=(24, 18, 24, 22))
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)
        self.header = ttk.Frame(self.main_area)
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.header.grid_columnconfigure(0, weight=1)
        self.heading_box = ttk.Frame(self.header)
        self.heading_box.grid(row=0, column=0, sticky="w")
        self.page_title = ttk.Label(self.heading_box, text="", style="Title.TLabel")
        self.page_title.pack(anchor="w")
        self.page_subtitle = ttk.Label(
            self.heading_box, text="", style="Subtitle.TLabel"
        )
        self.page_subtitle.pack(anchor="w", pady=(4, 0))
        self.school_badge = ttk.Label(
            self.header,
            text=self.system.school_name,
            style="Subtitle.TLabel",
        )
        self.school_badge.grid(row=0, column=1, sticky="e", padx=(10, 14))
        self.header_actions = ttk.Frame(self.header)
        self.header_actions.grid(row=0, column=2, sticky="e")
        self.content = ttk.Frame(self.main_area)
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    @staticmethod
    def _page_icon(page):
        return {
            "Overview": "⌂",
            "Students": "♙",
            "Courses": "▤",
            "Academics": "◈",
            "Attendance": "◷",
        }[page]

    def show_page(self, page):
        self.current_page = page
        page_titles = {
            "Overview": "Dashboard",
            "Students": "Students",
            "Courses": "Class",
            "Academics": "Reports",
            "Attendance": "Attendance",
        }
        self.page_title.configure(text=page_titles[page])
        subtitles = {
            "Overview": "A clear view of your school, all in one place.",
            "Students": "Manage student records and individual profiles.",
            "Courses": "Build your curriculum and manage enrollment.",
            "Academics": "Assign grades and review student performance.",
            "Attendance": "Record attendance and monitor participation.",
        }
        self.page_subtitle.configure(text=subtitles[page])
        for name, button in self.nav_buttons.items():
            active = name == page
            button.configure(
                bg=self.colors["sidebar_active"] if active else self.colors["sidebar"],
                fg=self.colors["text"] if active else self.colors["sidebar_text"],
            )
        for child in self.content.winfo_children():
            child.destroy()
        for child in self.header_actions.winfo_children():
            child.destroy()
        builders = {
            "Overview": self._build_overview,
            "Students": self._build_students,
            "Courses": self._build_courses,
            "Academics": self._build_academics,
            "Attendance": self._build_attendance,
        }
        if page == "Students":
            ttk.Button(
                self.header_actions,
                text="Delete",
                command=self._delete_student,
            ).pack(side="left", padx=(0, 8))
            ttk.Button(
                self.header_actions,
                text="＋  Add / edit student",
                style="Primary.TButton",
                command=self._add_or_edit_student,
            ).pack(side="left")
        elif page == "Courses":
            ttk.Button(
                self.header_actions,
                text="Delete",
                command=self._delete_course,
            ).pack(side="left", padx=(0, 8))
            ttk.Button(
                self.header_actions,
                text="＋  Add / edit class",
                style="Primary.TButton",
                command=self._add_or_edit_course,
            ).pack(side="left")
        builders[page]()

    def _surface(self, parent, padding=18):
        return ttk.Frame(parent, style="Surface.TFrame", padding=padding)

    def _card(self, parent, label, value, note):
        accent_colors = (
            self.colors["blue"],
            self.colors["orange"],
            self.colors["green"],
            self.colors["red"],
        )
        accent_index = max(0, len(parent.winfo_children()) - 1)
        accent = accent_colors[accent_index % len(accent_colors)]
        card = tk.Frame(parent, bg=accent, padx=14, pady=12)
        tk.Label(
            card,
            text=label,
            bg=accent,
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            card,
            text=str(value),
            bg=accent,
            fg="#ffffff",
            font=("Segoe UI", 23, "bold"),
        ).pack(anchor="w", pady=(7, 1))
        tk.Label(
            card,
            text=note,
            bg=accent,
            fg="#f2f5ff",
            font=("Segoe UI", 8),
        ).pack(anchor="w")
        return card

    def _section_heading(self, parent, title, subtitle=""):
        ttk.Label(
            parent,
            text=title,
            style="Surface.TLabel",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")
        if subtitle:
            ttk.Label(parent, text=subtitle, style="CardTitle.TLabel").pack(
                anchor="w", pady=(4, 0)
            )

    def _tree(self, parent, columns, headings, widths, height=12):
        frame = ttk.Frame(parent, style="Surface.TFrame")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=height,
            selectmode="browse",
        )
        for column, heading, width in zip(columns, headings, widths):
            tree.heading(column, text=heading)
            tree.column(column, width=width, minwidth=60, anchor="w")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        horizontal_scrollbar = ttk.Scrollbar(
            frame, orient="horizontal", command=tree.xview
        )
        tree.configure(
            yscrollcommand=scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set,
        )
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
        return frame, tree

    def _build_overview(self):
        for column in range(4):
            self.content.grid_columnconfigure(column, weight=1)
        self.content.grid_rowconfigure(1, weight=1)
        students = list(self.system.students.values())
        courses = list(self.system.courses.values())
        today = self.system.attendance_for_date()
        cards = (
            ("Total class", len(courses), "View classes"),
            ("Total students", len(students), "View students"),
            ("Academic honors", len(self.system.honor_roll()), "Honor roll"),
            (
                "Present today",
                sum(status == "Present" for status in today.values()),
                "View attendance",
            ),
        )
        for column, (label, value, note) in enumerate(cards):
            self._card(self.content, label, value, note).grid(
                row=0,
                column=column,
                sticky="ew",
                padx=(0 if column == 0 else 7, 0),
                pady=(0, 18),
            )

        chart_card = self._surface(self.content, padding=(18, 15, 18, 12))
        chart_card.grid(
            row=1, column=0, columnspan=4, sticky="nsew", padx=0, pady=(0, 4)
        )
        chart_header = ttk.Frame(chart_card, style="Surface.TFrame")
        chart_header.pack(fill="x")
        title_box = ttk.Frame(chart_header, style="Surface.TFrame")
        title_box.pack(side="left", fill="x", expand=True)
        self._section_heading(
            title_box,
            "My Daily Activities",
            "Course enrollment at a glance",
        )
        ttk.Button(
            chart_header,
            text="＋ Add student",
            style="Primary.TButton",
            command=lambda: self._student_form(),
        ).pack(side="right", padx=(8, 0))
        ttk.Button(
            chart_header,
            text="＋ Add class",
            command=lambda: self._course_form(),
        ).pack(side="right")
        self.activity_chart = tk.Canvas(
            chart_card,
            height=300,
            bg=self.colors["surface"],
            highlightthickness=0,
            bd=0,
        )
        self.activity_chart.pack(fill="both", expand=True, pady=(12, 0))
        self.activity_chart.bind("<Configure>", self._draw_activity_chart)
        self._draw_activity_chart()

    def _draw_activity_chart(self, _event=None):
        if not hasattr(self, "activity_chart"):
            return
        canvas = self.activity_chart
        canvas.delete("all")
        width = max(canvas.winfo_width(), 420)
        height = max(canvas.winfo_height(), 230)
        left, right, top, bottom = 42, width - 18, 20, height - 46
        chart_height = bottom - top
        courses = sorted(
            self.system.courses.values(),
            key=lambda item: item.name.casefold(),
        )[:8]
        maximum = max((course.enrollment for course in courses), default=0)
        scale_max = max(4, ((maximum + 3) // 4) * 4)
        colors = self.colors

        for tick in range(5):
            value = round(scale_max * tick / 4)
            y = bottom - chart_height * tick / 4
            canvas.create_line(left, y, right, y, fill=colors["border"])
            canvas.create_text(
                left - 12,
                y,
                text=str(value),
                anchor="e",
                fill=colors["muted"],
                font=("Segoe UI", 9),
            )
        canvas.create_line(left, top, left, bottom, fill=colors["border"])
        canvas.create_line(left, bottom, right, bottom, fill=colors["border"])

        if not courses:
            canvas.create_text(
                (left + right) / 2,
                (top + bottom) / 2,
                text="Create a class to see enrollment activity here.",
                fill=colors["muted"],
                font=("Segoe UI", 11),
            )
            return

        slot_width = (right - left) / len(courses)
        bar_width = min(58, slot_width * 0.52)
        bar_colors = (
            colors["blue"],
            colors["orange"],
            colors["green"],
            colors["red"],
        )
        for index, course in enumerate(courses):
            center = left + slot_width * (index + 0.5)
            bar_height = chart_height * course.enrollment / scale_max
            x0 = center - bar_width / 2
            x1 = center + bar_width / 2
            y0 = bottom - bar_height
            color = bar_colors[index % len(bar_colors)]
            canvas.create_rectangle(
                x0,
                y0,
                x1,
                bottom,
                fill=color,
                outline="",
            )
            canvas.create_text(
                center,
                y0 - 11,
                text=str(course.enrollment),
                fill=colors["text"],
                font=("Segoe UI", 9, "bold"),
            )
            label = course.name
            if len(label) > 15:
                label = f"{label[:13]}..."
            canvas.create_text(
                center,
                bottom + 20,
                text=label,
                fill=colors["muted"],
                font=("Segoe UI", 9),
            )

    def _build_students(self):
        self.content.grid_rowconfigure(1, weight=1)
        toolbar = ttk.Frame(self.content)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        toolbar.grid_columnconfigure(0, weight=1)
        search_box = ttk.Frame(toolbar, style="Surface.TFrame", padding=(10, 2))
        search_box.grid(row=0, column=0, sticky="ew")
        ttk.Label(
            search_box,
            text="⌕",
            style="CardTitle.TLabel",
            font=("Segoe UI", 16),
        ).pack(side="left", padx=(0, 6))
        ttk.Entry(search_box, textvariable=self.search_var).pack(
            side="left", fill="x", expand=True, ipady=2
        )
        actions = ttk.Frame(toolbar)
        actions.grid(row=0, column=1, sticky="e")
        ttk.Button(actions, text="Export CSV", command=self._export_students).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(actions, text="View profile", command=self._view_student).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(actions, text="Edit student", command=self._edit_student).pack(
            side="left", padx=(0, 8)
        )
        table_card = self._surface(self.content)
        table_card.grid(row=1, column=0, sticky="nsew")
        self._section_heading(
            table_card, "Student directory", "Search by name, ID, or email"
        )
        tree_frame, self.student_tree = self._tree(
            table_card,
            ("student_id", "name", "level", "age", "email", "courses", "gpa"),
            ("Student ID", "Student", "Level", "Age", "Email", "Courses", "GPA"),
            (115, 170, 95, 55, 190, 75, 65),
            height=15,
        )
        tree_frame.pack(fill="both", expand=True, pady=(14, 0))
        self.student_tree.bind("<Double-1>", lambda _event: self._view_student())
        self.student_tree.bind("<Delete>", lambda _event: self._delete_student())
        self._refresh_students()

    def _refresh_students(self):
        if not hasattr(self, "student_tree") or not self.student_tree.winfo_exists():
            return
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        for student in self.system.search_students(self.search_var.get()):
            self.student_tree.insert(
                "",
                "end",
                iid=student.student_id,
                values=(
                    student.student_id,
                    student.name,
                    student.academic_level,
                    student.age,
                    student.email or "—",
                    len(student.courses),
                    f"{student.gpa:.1f}",
                ),
            )

    def _build_courses(self):
        self.content.grid_rowconfigure(1, weight=1)
        toolbar = ttk.Frame(self.content)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        toolbar.grid_columnconfigure(0, weight=1)
        ttk.Label(
            toolbar,
            text="Manage course catalog and student enrollment.",
            style="Muted.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(toolbar, text="Enroll student", command=self._enroll_student).grid(
            row=0, column=1, padx=(8, 0)
        )
        card = self._surface(self.content)
        card.grid(row=1, column=0, sticky="nsew")
        self._section_heading(card, "Course catalog", "Capacity and enrollment at a glance")
        tree_frame, self.course_tree = self._tree(
            card,
            ("course_id", "name", "teacher", "enrollment", "capacity", "description"),
            ("Course ID", "Course", "Teacher", "Enrolled", "Capacity", "Description"),
            (110, 190, 160, 90, 90, 250),
            height=15,
        )
        tree_frame.pack(fill="both", expand=True, pady=(14, 0))
        self.course_tree.bind("<Delete>", lambda _event: self._delete_course())
        self._refresh_courses()

    def _refresh_courses(self):
        if not hasattr(self, "course_tree") or not self.course_tree.winfo_exists():
            return
        for row in self.course_tree.get_children():
            self.course_tree.delete(row)
        for course in sorted(
            self.system.courses.values(), key=lambda item: item.name.casefold()
        ):
            self.course_tree.insert(
                "",
                "end",
                iid=course.course_id,
                values=(
                    course.course_id,
                    course.name,
                    course.teacher or "—",
                    course.enrollment,
                    course.capacity,
                    course.description or "—",
                ),
            )

    def _build_academics(self):
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        ttk.Button(
            self.header_actions,
            text="Delete grade",
            command=self._delete_selected_grade,
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            self.header_actions,
            text="＋  Add / edit grade",
            style="Primary.TButton",
            command=self._grade_form,
        ).pack(side="left")
        summary = self._surface(self.content)
        summary.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self._section_heading(
            summary,
            "Academic performance",
            "Grade students in courses they are enrolled in.",
        )
        ttk.Label(
            summary,
            text=f"{len(self.system.honor_roll())} student(s) currently on the honor roll (GPA 3.5+).",
            style="CardTitle.TLabel",
        ).pack(anchor="w", pady=(10, 0))
        card = self._surface(self.content)
        card.grid(row=1, column=0, sticky="nsew")
        self._section_heading(
            card,
            "Gradebook",
            "Add or edit course grades; each student's GPA updates automatically.",
        )
        tree_frame, self.grade_tree = self._tree(
            card,
            ("student", "student_id", "course", "grade", "gpa"),
            ("Student", "Student ID", "Course", "Grade", "GPA"),
            (200, 125, 220, 100, 75),
            height=14,
        )
        tree_frame.pack(fill="both", expand=True, pady=(14, 0))
        for student in self.system.search_students():
            if not student.courses:
                self.grade_tree.insert(
                    "",
                    "end",
                    values=(student.name, student.student_id, "—", "Not enrolled", f"{student.gpa:.1f}"),
                )
            for course_id, grade in student.courses.items():
                course = self.system.courses.get(course_id)
                self.grade_tree.insert(
                    "",
                    "end",
                    iid=f"{student.student_id}::{course_id}",
                    values=(
                        student.name,
                        student.student_id,
                        course.name if course else course_id,
                        f"{grade:.1f}" if grade is not None else "Not graded",
                        f"{student.gpa:.1f}",
                    ),
                )

    def _build_attendance(self):
        self.content.grid_rowconfigure(1, weight=1)
        toolbar = ttk.Frame(self.content)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        toolbar.grid_columnconfigure(0, weight=1)
        ttk.Label(toolbar, text="Today’s attendance", style="Muted.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Button(
            toolbar,
            text="Mark absent",
            command=lambda: self._mark_selected("Absent"),
        ).grid(row=0, column=1, padx=(8, 0))
        ttk.Button(
            toolbar,
            text="Mark present",
            style="Primary.TButton",
            command=lambda: self._mark_selected("Present"),
        ).grid(row=0, column=2, padx=(8, 0))
        card = self._surface(self.content)
        card.grid(row=1, column=0, sticky="nsew")
        self._section_heading(
            card,
            "Attendance register",
            "Marking a student again updates today’s record.",
        )
        tree_frame, self.attendance_tree = self._tree(
            card,
            ("student_id", "name", "status", "percentage"),
            ("Student ID", "Student", "Today", "Attendance rate"),
            (140, 260, 140, 160),
            height=15,
        )
        tree_frame.pack(fill="both", expand=True, pady=(14, 0))
        today = self.system.attendance_for_date()
        for student in self.system.search_students():
            self.attendance_tree.insert(
                "",
                "end",
                iid=student.student_id,
                values=(
                    student.student_id,
                    student.name,
                    today.get(student.student_id, "Not marked"),
                    f"{self.system.attendance_percentage(student.student_id):.0f}%",
                ),
            )

    def _selected_id(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Select a record", "Choose a row first.", parent=self)
            return None
        return selected[0]

    def _student_form(self, student=None):
        dialog = tk.Toplevel(self)
        dialog.title("Edit student" if student else "Add student")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(bg=self.colors["background"])
        dialog.resizable(False, False)
        frame = ttk.Frame(dialog, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(
            frame,
            text="Edit student" if student else "Add a student",
            style="Title.TLabel",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 17))
        fields = {}
        values = (
            ("Full name", student.name if student else ""),
            ("Age", str(student.age) if student else ""),
            ("Email", student.email if student else ""),
            ("Phone", student.phone if student else ""),
        )
        for row, (label, value) in enumerate(values, start=1):
            ttk.Label(frame, text=label).grid(
                row=row, column=0, sticky="w", pady=6, padx=(0, 16)
            )
            entry = ttk.Entry(frame, width=34)
            entry.insert(0, value)
            entry.grid(row=row, column=1, sticky="ew", pady=6)
            fields[label] = entry

        graduate_var = tk.BooleanVar(value=isinstance(student, GraduateStudent))
        ttk.Checkbutton(
            frame,
            text="Graduate student",
            variable=graduate_var,
            state="disabled" if student else "normal",
        ).grid(row=5, column=1, sticky="w", pady=7)
        program = ttk.Entry(frame, width=34)
        thesis = ttk.Entry(frame, width=34)
        if isinstance(student, GraduateStudent):
            program.insert(0, student.program)
            thesis.insert(0, student.thesis_title)
        ttk.Label(frame, text="Program").grid(
            row=6, column=0, sticky="w", pady=6, padx=(0, 16)
        )
        program.grid(row=6, column=1, sticky="ew", pady=6)
        ttk.Label(frame, text="Thesis title").grid(
            row=7, column=0, sticky="w", pady=6, padx=(0, 16)
        )
        thesis.grid(row=7, column=1, sticky="ew", pady=6)
        frame.grid_columnconfigure(1, weight=1)

        def save():
            try:
                values = {
                    "name": fields["Full name"].get(),
                    "age": fields["Age"].get(),
                    "email": fields["Email"].get(),
                    "phone": fields["Phone"].get(),
                }
                if student:
                    self.system.update_student(student.student_id, **values)
                    if isinstance(student, GraduateStudent):
                        self.system.update_graduate_details(
                            student.student_id, program.get(), thesis.get()
                        )
                else:
                    self.system.add_student(
                        **values,
                        graduate=graduate_var.get(),
                        program=program.get(),
                        thesis_title=thesis.get(),
                    )
                dialog.destroy()
                self._refresh_after_change()
            except (ValueError, RuntimeError) as error:
                messagebox.showerror("Could not save student", str(error), parent=dialog)

        actions = ttk.Frame(frame)
        actions.grid(row=8, column=0, columnspan=2, sticky="e", pady=(17, 0))
        ttk.Button(actions, text="Cancel", command=dialog.destroy).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(
            actions,
            text="Save student",
            style="Primary.TButton",
            command=save,
        ).pack(side="left")

    def _edit_student(self):
        student_id = self._selected_id(self.student_tree)
        if student_id:
            self._student_form(self.system.get_student(student_id))

    def _add_or_edit_student(self):
        selected = self.student_tree.selection()
        if selected:
            self._student_form(self.system.get_student(selected[0]))
        else:
            self._student_form()

    def _delete_student(self):
        student_id = self._selected_id(self.student_tree)
        if student_id and messagebox.askyesno(
            "Delete student",
            "Delete this student and their attendance records?",
            parent=self,
        ):
            try:
                self.system.delete_student(student_id)
                self._refresh_after_change()
            except (ValueError, RuntimeError) as error:
                messagebox.showerror("Could not delete student", str(error), parent=self)

    def _view_student(self):
        student_id = self._selected_id(self.student_tree)
        if not student_id:
            return
        report = self.system.report_card(student_id)
        student = report["student"]
        details = [
            f"{student.name}  ·  {student.academic_level}",
            f"Student ID: {student.student_id}",
            f"Age: {student.age}",
            f"Email: {student.email or 'Not provided'}",
            f"Phone: {student.phone or 'Not provided'}",
            f"Enrolled: {student.enrollment_date}",
            f"GPA: {report['gpa']:.2f}",
            "",
            "COURSES",
        ]
        details.extend(
            f"{item['course']}: {item['grade']:.1f}"
            if item["grade"] is not None
            else f"{item['course']}: Not graded"
            for item in report["courses"]
        )
        if not report["courses"]:
            details.append("No courses enrolled.")
        if isinstance(student, GraduateStudent):
            details.extend(
                (
                    "",
                    f"Program: {student.program or '—'}",
                    f"Thesis: {student.thesis_title or '—'}",
                )
            )
        messagebox.showinfo(
            "Student profile and report card", "\n".join(details), parent=self
        )

    def _course_form(self, course=None):
        dialog = tk.Toplevel(self)
        dialog.title("Edit course" if course else "Create course")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(bg=self.colors["background"])
        dialog.resizable(False, False)
        frame = ttk.Frame(dialog, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Course details", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 17)
        )
        values = (
            ("Course name", course.name if course else ""),
            ("Teacher", course.teacher if course else ""),
            ("Capacity", str(course.capacity) if course else "30"),
            ("Description", course.description if course else ""),
        )
        entries = {}
        for row, (label, value) in enumerate(values, start=1):
            ttk.Label(frame, text=label).grid(
                row=row, column=0, sticky="w", padx=(0, 16), pady=6
            )
            entry = ttk.Entry(frame, width=34)
            entry.insert(0, value)
            entry.grid(row=row, column=1, sticky="ew", pady=6)
            entries[label] = entry
        frame.grid_columnconfigure(1, weight=1)

        def save():
            try:
                values = (
                    entries["Course name"].get(),
                    entries["Teacher"].get(),
                    entries["Capacity"].get(),
                    entries["Description"].get(),
                )
                if course:
                    self.system.update_course(course.course_id, *values)
                else:
                    self.system.add_course(
                        values[0], values[1], values[2], values[3]
                    )
                dialog.destroy()
                self._refresh_after_change()
            except (ValueError, RuntimeError) as error:
                messagebox.showerror("Could not save course", str(error), parent=dialog)

        actions = ttk.Frame(frame)
        actions.grid(row=5, column=0, columnspan=2, sticky="e", pady=(17, 0))
        ttk.Button(actions, text="Cancel", command=dialog.destroy).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(
            actions,
            text="Save course",
            style="Primary.TButton",
            command=save,
        ).pack(side="left")

    def _edit_course(self):
        course_id = self._selected_id(self.course_tree)
        if course_id:
            self._course_form(self.system.get_course(course_id))

    def _add_or_edit_course(self):
        selected = self.course_tree.selection()
        if selected:
            self._course_form(self.system.get_course(selected[0]))
        else:
            self._course_form()

    def _delete_course(self):
        course_id = self._selected_id(self.course_tree)
        if course_id and messagebox.askyesno(
            "Delete course",
            "Delete this course and remove its grades from student records?",
            parent=self,
        ):
            try:
                self.system.delete_course(course_id)
                self._refresh_after_change()
            except (ValueError, RuntimeError) as error:
                messagebox.showerror("Could not delete course", str(error), parent=self)

    def _enroll_student(self):
        if not self.system.students or not self.system.courses:
            messagebox.showinfo(
                "Enrollment",
                "Add at least one student and one course first.",
                parent=self,
            )
            return
        self._choice_dialog(
            "Enroll student",
            [
                f"{student.student_id} — {student.name}"
                for student in self.system.search_students()
            ],
            [
                f"{course.course_id} — {course.name}"
                for course in self.system.courses.values()
            ],
            self._complete_enrollment,
        )

    def _complete_enrollment(self, student_label, course_label):
        student_id = student_label.split(" — ", 1)[0]
        course_id = course_label.split(" — ", 1)[0]
        self.system.enroll_student(student_id, course_id)

    def _grade_form(self):
        if not self.system.students or not self.system.courses:
            messagebox.showinfo(
                "Gradebook",
                "Add at least one student and one course before assigning grades.",
                parent=self,
            )
            return
        self._choice_dialog(
            "Assign grade",
            [
                f"{student.student_id} — {student.name}"
                for student in self.system.search_students()
            ],
            [
                f"{course.course_id} — {course.name}"
                for course in self.system.courses.values()
            ],
            self._complete_grade,
            include_grade=True,
        )

    def _complete_grade(self, student_label, course_label, grade):
        student_id = student_label.split(" — ", 1)[0]
        course_id = course_label.split(" — ", 1)[0]
        self.system.assign_grade(student_id, course_id, grade)

    def _delete_selected_grade(self):
        selected = self.grade_tree.selection()
        if not selected:
            messagebox.showinfo(
                "Select a grade",
                "Choose a graded course row from the gradebook first.",
                parent=self,
            )
            return
        if "::" not in selected[0]:
            messagebox.showinfo(
                "No grade selected",
                "Choose a course row that has an assigned grade.",
                parent=self,
            )
            return
        student_id, course_id = selected[0].split("::", 1)
        student = self.system.get_student(student_id)
        if student.courses.get(course_id) is None:
            messagebox.showinfo(
                "No grade to delete",
                "This course does not have an assigned grade.",
                parent=self,
            )
            return
        if messagebox.askyesno(
            "Delete grade",
            f"Remove {student.name}'s grade for "
            f"{self.system.get_course(course_id).name}?\n"
            "The student's GPA will be recalculated.",
            parent=self,
        ):
            try:
                self.system.delete_grade(student_id, course_id)
                self._refresh_after_change()
            except (ValueError, RuntimeError) as error:
                messagebox.showerror("Could not delete grade", str(error), parent=self)

    def _choice_dialog(
        self, title, student_choices, course_choices, callback, include_grade=False
    ):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.transient(self)
        dialog.grab_set()
        frame = ttk.Frame(dialog, padding=22)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=title, style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )
        ttk.Label(frame, text="Student").grid(
            row=1, column=0, sticky="w", pady=7, padx=(0, 12)
        )
        student_var = tk.StringVar(value=student_choices[0])
        ttk.Combobox(
            frame,
            textvariable=student_var,
            values=student_choices,
            state="readonly",
            width=33,
        ).grid(row=1, column=1, sticky="ew", pady=7)
        ttk.Label(frame, text="Course").grid(
            row=2, column=0, sticky="w", pady=7, padx=(0, 12)
        )
        course_var = tk.StringVar(value=course_choices[0])
        ttk.Combobox(
            frame,
            textvariable=course_var,
            values=course_choices,
            state="readonly",
            width=33,
        ).grid(row=2, column=1, sticky="ew", pady=7)
        grade_entry = None
        if include_grade:
            ttk.Label(frame, text="Grade (0–100)").grid(
                row=3, column=0, sticky="w", pady=7, padx=(0, 12)
            )
            grade_entry = ttk.Entry(frame)
            grade_entry.grid(row=3, column=1, sticky="ew", pady=7)

        def submit():
            try:
                if include_grade:
                    callback(student_var.get(), course_var.get(), grade_entry.get())
                else:
                    callback(student_var.get(), course_var.get())
                dialog.destroy()
                self._refresh_after_change()
            except (ValueError, RuntimeError) as error:
                messagebox.showerror(title, str(error), parent=dialog)

        actions = ttk.Frame(frame)
        actions.grid(
            row=4 if include_grade else 3,
            column=0,
            columnspan=2,
            sticky="e",
            pady=(14, 0),
        )
        ttk.Button(actions, text="Cancel", command=dialog.destroy).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(actions, text="Save", style="Primary.TButton", command=submit).pack(
            side="left"
        )

    def _mark_selected(self, status):
        student_id = self._selected_id(self.attendance_tree)
        if student_id:
            try:
                self.system.mark_attendance(student_id, status)
                self.show_page("Attendance")
            except (ValueError, RuntimeError) as error:
                messagebox.showerror("Could not mark attendance", str(error), parent=self)

    def _export_students(self):
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Export student list",
            defaultextension=".csv",
            filetypes=(("CSV files", "*.csv"),),
        )
        if not path:
            return
        try:
            Storage.export_students_csv(path, self.system.search_students())
            messagebox.showinfo(
                "Export complete", f"Student list exported to:\n{path}", parent=self
            )
        except RuntimeError as error:
            messagebox.showerror("Export failed", str(error), parent=self)

    def _refresh_after_change(self):
        self.show_page(self.current_page)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.colors = DARK if self.dark_mode else LIGHT
        current_page = self.current_page
        self.banner.destroy()
        self.workspace.destroy()
        self.configure(bg=self.colors["background"])
        self._configure_styles()
        self._build_shell()
        self.show_page(current_page)
        self.theme_button.configure(
            text=(
                "◐  Light mode"
                if self.dark_mode
                else "◐  Dark mode"
            )
        )
