"""
School Management System (PyQt5)
================================

This file builds a GUI-based school management system using PyQt5.
It handles students, instructors, and courses, allowing the user
to add, edit, delete, search, assign, and register records.
Data can also be saved, loaded, exported, and backed up.

The app interacts with the SQLite database through `database.py`
and with helper classes defined in `models.py`.

Usage
-----
Run this file directly with::

    python pyqt_app_database.py
"""

import sys 
import csv
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QMessageBox, QFileDialog, QDialog, QFormLayout, QDialogButtonBox
)
from models import Student, Instructor, Course, DataManager
import database as db


THEME_RED = "#A31F34"
THEME_RED_HOVER = "#7f1626"
THEME_CREAM = "#fffdd0"


class SimpleEditDialog(QDialog):
    """Popup dialog used to edit Students, Instructors, or Courses."""

    def __init__(self, title, fields):
        """Build a simple edit dialog.

        :param title: Window title
        :param fields: List of (label, default_value) pairs
        """
        super().__init__()
        self.setWindowTitle(title)
        self.setModal(True)
        form = QFormLayout(self)
        self._edits = []
        for label, default in fields:
            lab = QLabel(label)
            edit = QLineEdit(str(default))
            form.addRow(lab, edit)
            self._edits.append(edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def values(self):
        """Return the values entered in the edit fields."""
        return [e.text().strip() for e in self._edits]


class SchoolApp(QMainWindow):
    """The main application window for the School Management System."""

    def __init__(self):
        """Initialize the main GUI and sync data from the database."""
        super().__init__()
        self.setWindowTitle("School Management System (PyQt5)")
        self.setGeometry(200, 100, 1100, 650)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {THEME_CREAM};
                font-family: Segoe UI, Arial;
                font-size: 13px;
            }}
            QLineEdit, QComboBox, QTableWidget {{
                background-color: #ffffff;
                border: 1px solid #d3cbb8;
                padding: 4px;
                border-radius: 4px;
            }}
            QLabel {{
                color: #333333;
            }}
            QPushButton {{
                background-color: {THEME_RED};
                color: #ffffff;
                padding: 6px 12px;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {THEME_RED_HOVER};
            }}
            QTableWidget {{
                gridline-color: #d3cbb8;
                alternate-background-color: #fdf6ec;
            }}
            QHeaderView::section {{
                background-color: {THEME_RED};
                color: white;
                padding: 6px;
                border: none;
            }}
        """)

        self.students = []
        self.instructors = []
        self.courses = []

        db.init_db()

        container = QWidget()
        layout = QVBoxLayout()
        layout.addLayout(self._build_form(
            specs=[("Student Name", "student_name_input"), ("Age", "student_age_input"),
                   ("Email", "student_email_input"), ("Student ID", "student_id_input")],
            button_text="Add Student",
            handler=self.add_student
        ))
        layout.addLayout(self._build_form(
            specs=[("Instructor Name", "instructor_name_input"), ("Age", "instructor_age_input"),
                   ("Email", "instructor_email_input"), ("Instructor ID", "instructor_id_input")],
            button_text="Add Instructor",
            handler=self.add_instructor
        ))
        layout.addLayout(self._build_form(
            specs=[("Course Name", "course_title_input"), ("Course ID", "course_id_input")],
            button_text="Add Course",
            handler=self.add_course
        ))
        layout.addLayout(self._build_registration_row())
        layout.addLayout(self._build_assignment_row())
        layout.addLayout(self._build_search_row())
        self._build_table(layout)
        layout.addLayout(self._build_controls_row())
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.sync_from_db()

    def _build_form(self, specs, button_text, handler):
        """Generic builder for student, instructor, and course forms."""
        row = QHBoxLayout()
        for label_text, attr_name in specs:
            box = QHBoxLayout()
            lab = QLabel(label_text)
            edit = QLineEdit()
            box.addWidget(lab)
            box.addWidget(edit)
            row.addLayout(box)
            setattr(self, attr_name, edit)
        btn = QPushButton(button_text)
        btn.clicked.connect(handler)
        row.addWidget(btn)
        return row

    def _build_registration_row(self):
        """Build the row that lets you register a student to a course."""
        row = QHBoxLayout()
        row.addWidget(QLabel("Student"))
        self.student_selector = QComboBox()
        self.student_selector.addItem("Select Student")
        row.addWidget(self.student_selector)
        row.addWidget(QLabel("Course"))
        self.course_selector = QComboBox()
        self.course_selector.addItem("Select Course")
        row.addWidget(self.course_selector)
        self.register_button = QPushButton("Register Student")
        self.register_button.clicked.connect(self.register_student)
        row.addWidget(self.register_button)
        return row

    def _build_assignment_row(self):
        """Build the row that lets you assign an instructor to a course."""
        row = QHBoxLayout()
        row.addWidget(QLabel("Instructor"))
        self.instructor_selector = QComboBox()
        self.instructor_selector.addItem("Select Instructor")
        row.addWidget(self.instructor_selector)
        row.addWidget(QLabel("Course"))
        self.assignment_course_selector = QComboBox()
        self.assignment_course_selector.addItem("Select Course")
        row.addWidget(self.assignment_course_selector)
        self.assign_button = QPushButton("Assign Instructor")
        self.assign_button.clicked.connect(self.assign_instructor)
        row.addWidget(self.assign_button)
        return row

    def _build_search_row(self):
        """Builds the row for searching records (students, instructors, courses)."""
        row = QHBoxLayout()
        row.addWidget(QLabel("Search"))
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Search by name, ID, or course")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_records)
        self.show_all_button = QPushButton("Show All")
        self.show_all_button.clicked.connect(self.update_table)
        row.addWidget(self.query_input)
        row.addWidget(self.search_button)
        row.addWidget(self.show_all_button)
        return row

    def _build_table(self, parent_layout):
        """Create the main table widget for displaying all records."""
        self.records_table = QTableWidget()
        self.records_table.setAlternatingRowColors(True)
        self.records_table.setColumnCount(6)
        self.records_table.setHorizontalHeaderLabels(
            ["Type", "ID", "Name", "Age", "Email", "Courses/Students"]
        )
        parent_layout.addWidget(self.records_table)

    def _build_controls_row(self):
        """Build the row of control buttons (edit, delete, save, load, export, backup)."""
        row = QHBoxLayout()
        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.clicked.connect(self.edit_record)
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_record)
        self.save_button = QPushButton("Save Data")
        self.save_button.clicked.connect(self.save_data)
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        self.export_button = QPushButton("Export CSV")
        self.export_button.clicked.connect(self.export_csv)
        self.backup_button = QPushButton("Backup DB")
        self.backup_button.clicked.connect(self.backup_database)
        row.addWidget(self.edit_button)
        row.addWidget(self.delete_button)
        row.addWidget(self.save_button)
        row.addWidget(self.load_button)
        row.addWidget(self.export_button)
        row.addWidget(self.backup_button)
        return row

    def _msg(self, kind, title, text):
        """Helper for showing info/warning message boxes."""
        if kind == "warn":
            QMessageBox.warning(self, title, text)
        elif kind == "info":
            QMessageBox.information(self, title, text)

    def _focus(self, widget):
        """Set focus and select all text in the widget."""
        widget.setFocus()
        widget.selectAll()

    def _is_valid_email(self, value):
        """Check if a string looks like a valid email address."""
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))

    def _id_exists(self, kind, identifier, exclude_id=None):
        """Check if an ID already exists (student, instructor, or course)."""
        if kind == "student":
            return any((s.student_id == identifier) and (exclude_id is None or s.student_id != exclude_id) for s in self.students)
        if kind == "instructor":
            return any((i.instructor_id == identifier) and (exclude_id is None or i.instructor_id != exclude_id) for i in self.instructors)
        if kind == "course":
            return any((c.course_id == identifier) and (exclude_id is None or c.course_id != exclude_id) for c in self.courses)
        return False

    def _student_by_id(self, sid):
        """Find a Student object by ID."""
        return next((s for s in self.students if s.student_id == sid), None)

    def _instructor_by_id(self, iid):
        """Find an Instructor object by ID."""
        return next((i for i in self.instructors if i.instructor_id == iid), None)

    def _course_by_id(self, cid):
        """Find a Course object by ID."""
        return next((c for c in self.courses if c.course_id == cid), None)

    def _clear(self, *widgets):
        """Clear the contents of one or more widgets."""
        for w in widgets:
            w.clear()

    def _require(self, label_to_value):
        """Check that required values are present, else show error."""
        for label, value in label_to_value.items():
            if not value:
                self._msg("warn", "Error", f"{label} required")
                return False
        return True

    def sync_from_db(self):
        """Sync all students, instructors, and courses from the database."""
        self.students.clear()
        self.instructors.clear()
        self.courses.clear()

        stu_rows = db.fetch_students()
        inst_rows = db.get_instructors()
        course_rows = db.list_courses()
        reg_rows = db.get_registrations()

        inst_map = {}
        for iid, name, age, email in inst_rows:
            i = Instructor(name, int(age) if str(age).isdigit() else age, email, iid)
            self.instructors.append(i)
            inst_map[i.instructor_id] = i

        stu_map = {}
        for sid, name, age, email in stu_rows:
            s = Student(name, int(age) if str(age).isdigit() else age, email, sid)
            self.students.append(s)
            stu_map[s.student_id] = s

        course_map = {}
        for cid, name, instructor_id in course_rows:
            course = Course(cid, name if name is not None else "(unnamed)", inst_map.get(instructor_id))
            if course.instructor:
                course.instructor.assign_course(course)
            self.courses.append(course)
            course_map[course.course_id] = course

        for sid, cid in reg_rows:
            s = stu_map.get(sid)
            c = course_map.get(cid)
            if s and c:
                s.register_course(c)
                c.add_student(s)

        self.refresh_dropdowns()
        self.update_table()

    def add_student(self):
        """Add a new student after validating fields."""
        name = self.student_name_input.text().strip()
        age = self.student_age_input.text().strip()
        email = self.student_email_input.text().strip()
        sid = self.student_id_input.text().strip()
        if not self._require({"All fields": name and age and email and sid}):
            return
        if not age.isdigit():
            self._msg("warn", "Error", "Age must be a number")
            self._focus(self.student_age_input)
            return
        if not self._is_valid_email(email):
            self._msg("warn", "Error", "Invalid email format")
            self._focus(self.student_email_input)
            return
        if self._id_exists("student", sid):
            self._msg("warn", "Error", "Student ID already exists")
            self._focus(self.student_id_input)
            return
        db.add_student(sid, name, int(age), email)
        self._clear(self.student_name_input, self.student_age_input, self.student_email_input, self.student_id_input)
        self._focus(self.student_name_input)
        self.sync_from_db()
        self._msg("info", "Added", f"Student {name} added")

    def add_instructor(self):
        """Add a new instructor after validating fields."""
        name = self.instructor_name_input.text().strip()
        age = self.instructor_age_input.text().strip()
        email = self.instructor_email_input.text().strip()
        iid = self.instructor_id_input.text().strip()
        if not self._require({"All fields": name and age and email and iid}):
            return
        if not age.isdigit():
            self._msg("warn", "Error", "Age must be a number")
            self._focus(self.instructor_age_input)
            return
        if not self._is_valid_email(email):
            self._msg("warn", "Error", "Invalid email format")
            self._focus(self.instructor_email_input)
            return
        if self._id_exists("instructor", iid):
            self._msg("warn", "Error", "Instructor ID already exists")
            self._focus(self.instructor_id_input)
            return
        db.add_instructor(iid, name, int(age), email)
        self._clear(self.instructor_name_input, self.instructor_age_input, self.instructor_email_input, self.instructor_id_input)
        self._focus(self.instructor_name_input)
        self.sync_from_db()
        self._msg("info", "Added", f"Instructor {name} added")

    def add_course(self):
        """Add a new course into the database."""
        cname = self.course_title_input.text().strip()
        cid = self.course_id_input.text().strip()
        if not self._require({"Course ID and Name": cid and cname}):
            return
        if self._id_exists("course", cid):
            self._msg("warn", "Error", "Course ID already exists")
            self._focus(self.course_id_input)
            return
        db.add_course(cid, cname, None)
        self._clear(self.course_title_input, self.course_id_input)
        self._focus(self.course_title_input)
        self.sync_from_db()
        self._msg("info", "Added", f"Course {cname} added")

    def register_student(self):
        """Register a student for a course."""
        sid = self.student_selector.currentText()
        cid = self.course_selector.currentText()
        if sid == "Select Student" or cid == "Select Course":
            self._msg("warn", "Error", "Please select both a student and a course")
            return
        existing = {(s, c) for s, c in db.get_registrations()}
        if (sid, cid) in existing:
            self._msg("info", "Info", "Student is already registered in that course")
            return
        db.register_student(sid, cid)
        self.sync_from_db()
        self._msg("info", "Registered", f"{sid} registered in {cid}")

    def assign_instructor(self):
        """Assign an instructor to a course."""
        iid = self.instructor_selector.currentText()
        cid = self.assignment_course_selector.currentText()
        if iid == "Select Instructor" or cid == "Select Course":
            self._msg("warn", "Error", "Please select both an instructor and a course")
            return
        course_row = next((r for r in db.list_courses() if r[0] == cid), None)
        if not course_row:
            self._msg("warn", "Error", "Course not found")
            return
        db.update_course(cid, course_row[1], iid)
        self.sync_from_db()
        self._msg("info", "Assigned", f"{iid} assigned to {cid}")

    def update_table(self):
        """Refresh the main table with current records."""
        self.records_table.setRowCount(0)
        for entity in self.students + self.instructors + self.courses:
            self._add_row(entity)

    def refresh_dropdowns(self):
        """Update all dropdown menus with latest data."""
        self.student_selector.clear()
        self.student_selector.addItem("Select Student")
        self.student_selector.addItems([s.student_id for s in self.students])

        self.course_selector.clear()
        self.course_selector.addItem("Select Course")
        self.course_selector.addItems([c.course_id for c in self.courses])

        self.instructor_selector.clear()
        self.instructor_selector.addItem("Select Instructor")
        self.instructor_selector.addItems([i.instructor_id for i in self.instructors])

        self.assignment_course_selector.clear()
        self.assignment_course_selector.addItem("Select Course")
        self.assignment_course_selector.addItems([c.course_id for c in self.courses])

    def _row_values(self, obj):
        """Return row values for a Student, Instructor, or Course."""
        if isinstance(obj, Student):
            course_names = [c.course_name for c in obj.registered_courses if c and c.course_name]
            return [
                "Student", obj.student_id, obj.name or "-", str(obj.age),
                obj._email or "-", ", ".join(course_names) if course_names else "-"
            ]
        if isinstance(obj, Instructor):
            assigned = [c.course_name for c in obj.assigned_courses if c and c.course_name]
            return [
                "Instructor", obj.instructor_id, obj.name or "-", str(obj.age),
                obj._email or "-", ", ".join(assigned) if assigned else "-"
            ]
        if isinstance(obj, Course):
            students = [s.name for s in obj.enrolled_students if s and s.name]
            return [
                "Course", obj.course_id, obj.course_name or "-",
                obj.instructor.name if obj.instructor and obj.instructor.name else "-",
                "-", ", ".join(students) if students else "-"
            ]
        return ["-", "-", "-", "-", "-", "-"]

    def _add_row(self, obj):
        """Insert a row for an entity into the table."""
        r = self.records_table.rowCount()
        self.records_table.insertRow(r)
        for idx, val in enumerate(self._row_values(obj)):
            self.records_table.setItem(r, idx, QTableWidgetItem(val))

    def search_records(self):
        """Search for records matching the query and update table."""
        q = self.query_input.text().lower().strip()
        self.records_table.setRowCount(0)
        matched_courses = {c for c in self.courses if q and (q in (c.course_name or "").lower() or q in c.course_id.lower())}
        for s in self.students:
            cond = q in (s.name or "").lower() or q in s.student_id.lower()
            if not cond and matched_courses:
                cond = any(c in matched_courses for c in s.registered_courses)
            if cond:
                self._add_row(s)
        for i in self.instructors:
            cond = q in (i.name or "").lower() or q in i.instructor_id.lower()
            if not cond and matched_courses:
                cond = any(c in matched_courses for c in i.assigned_courses)
            if cond:
                self._add_row(i)
        for c in self.courses:
            if q in (c.course_name or "").lower() or q in c.course_id.lower():
                self._add_row(c)

    def edit_record(self):
        """Edit the currently selected record in the table."""
        row = self.records_table.currentRow()
        if row < 0:
            return
        type_item = self.records_table.item(row, 0)
        id_item = self.records_table.item(row, 1)
        if not type_item or not id_item:
            return
        rtype = type_item.text()
        rid = id_item.text()
        target = None
        if rtype == "Student":
            target = self._student_by_id(rid)
        elif rtype == "Instructor":
            target = self._instructor_by_id(rid)
        elif rtype == "Course":
            target = self._course_by_id(rid)
        if target:
            # opens SimpleEditDialog and applies changes
            if self._edit_entity(target):
                self.sync_from_db()
                self._msg("info", "Updated", "Record updated")

    def delete_record(self):
        """Delete the currently selected record from the database."""
        row = self.records_table.currentRow()
        if row < 0:
            return
        id_item = self.records_table.item(row, 1)
        type_item = self.records_table.item(row, 0)
        if not id_item or not type_item:
            return
        rid = id_item.text()
        rtype = type_item.text()
        if rtype == "Student":
            db.remove_student(rid)
        elif rtype == "Instructor":
            db.remove_instructor(rid)
        elif rtype == "Course":
            db.delete_course(rid)
        self.sync_from_db()
        self._msg("info", "Deleted", "Record deleted")

    def save_data(self):
        """Save all current records to a JSON file via DataManager."""
        data = {
            "students": [
                {
                    "student_id": s.student_id,
                    "name": s.name,
                    "age": s.age,
                    "_email": s._email,
                    "registered_courses": [c.course_id for c in s.registered_courses],
                }
                for s in self.students
            ],
            "instructors": [
                {
                    "instructor_id": i.instructor_id,
                    "name": i.name,
                    "age": i.age,
                    "_email": i._email,
                    "assigned_courses": [c.course_id for c in i.assigned_courses],
                }
                for i in self.instructors
            ],
            "courses": [
                {
                    "course_id": c.course_id,
                    "course_name": c.course_name,
                    "instructor": c.instructor.instructor_id if c.instructor else None,
                    "enrolled_students": [s.student_id for s in c.enrolled_students],
                }
                for c in self.courses
            ],
        }
        DataManager.save(data)
        self._msg("info", "Saved", "Data saved to file")

    def load_data(self):
        """Load records from a JSON file via DataManager."""
        data = DataManager.load()

        for i in data.get("instructors", []):
            db.add_instructor(i["instructor_id"], i["name"], i["age"], i["_email"])

        for s in data.get("students", []):
            db.add_student(s["student_id"], s["name"], s["age"], s["_email"])

        existing_courses = {cid: (name, inst) for cid, name, inst in db.list_courses()}
        for c in data.get("courses", []):
            cid = c["course_id"]
            name = c.get("course_name")
            inst_id = c.get("instructor")
            if cid in existing_courses:
                current_name, _ = existing_courses[cid]
                final_name = name or current_name or "(unnamed)"
            else:
                final_name = name or "(unnamed)"
            db.add_course(cid, final_name, inst_id)

        for s in data.get("students", []):
            sid = s["student_id"]
            for cid in s.get("registered_courses", []):
                db.register_student(sid, cid)

        existing_courses = {cid: (name, inst) for cid, name, inst in db.list_courses()}
        for i in data.get("instructors", []):
            iid = i["instructor_id"]
            for cid in i.get("assigned_courses", []):
                if cid in existing_courses:
                    cname, _ = existing_courses[cid]
                    db.update_course(cid, cname or "(unnamed)", iid)

        self.sync_from_db()
        self._msg("info", "Loaded", "Data loaded from file")

    def export_csv(self):
        """Export all current records to a CSV file."""
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "ID", "Name", "Age/Instructor", "Courses/Students"])
            for row in range(self.records_table.rowCount()):
                writer.writerow(
                    [
                        self.records_table.item(row, col).text() if self.records_table.item(row, col) else ""
                        for col in range(5)
                    ]
                )
        self._msg("info", "Export", f"Data exported to {path}")

    def backup_database(self):
        """Create a backup of the database via db.backup_db()."""
        try:
            result = db.backup_db()
            self._msg("info", "Backup", result)
        except Exception as e:
            self._msg("warn", "Backup Failed", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SchoolApp()
    win.show()
    sys.exit(app.exec_())
