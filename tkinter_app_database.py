
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import csv
import database as db

class SchoolApp:
    """
    A Tkinter-based School Management System.
    This class builds a tkinter based GUI for managing students, instructors, and courses by allowing users use it by adding, editing, deleting, registering, assigning,
    searching, exporting to CSV, and backing up the database..
    It relies on ``database.py`` module for storage and general databasae operations.

    :param root: Root Tkinter window for attaching the application.
    :type root: tk.Tk
    """
    def __init__(self, root):
        """
    Constructor method
        """
        db.init_db()

        self.root = root
        self.root.title("School Management System")
        self.root.configure(bg="#fff5e6")

        style = ttk.Style()
        style.configure("Treeview", background="#fff5e6", fieldbackground="#fff5e6", foreground="black")
        style.map("Treeview", background=[("selected", "#a52a2a")], foreground=[("selected", "white")])

        tk.Label(root, text="student name", bg="#fff5e6", fg="#a52a2a").grid(row=0, column=0, sticky="w")
        self.stuName = tk.Entry(root); self.stuName.grid(row=0, column=1)
        tk.Label(root, text="age", bg="#fff5e6", fg="#a52a2a").grid(row=1, column=0, sticky="w")
        self.stuAge = tk.Entry(root); self.stuAge.grid(row=1, column=1)
        tk.Label(root, text="email", bg="#fff5e6", fg="#a52a2a").grid(row=2, column=0, sticky="w")
        self.stuEmail = tk.Entry(root); self.stuEmail.grid(row=2, column=1)
        tk.Label(root, text="student id", bg="#fff5e6", fg="#a52a2a").grid(row=3, column=0, sticky="w")
        self.stuId = tk.Entry(root); self.stuId.grid(row=3, column=1)
        tk.Button(root, text="add student", bg="#a52a2a", fg="white", command=self.add_student).grid(row=4, column=0, columnspan=2)

        tk.Label(root, text="instructor name", bg="#fff5e6", fg="#a52a2a").grid(row=0, column=2, sticky="w")
        self.instructorName = tk.Entry(root); self.instructorName.grid(row=0, column=3)
        tk.Label(root, text="age", bg="#fff5e6", fg="#a52a2a").grid(row=1, column=2, sticky="w")
        self.instructorAge = tk.Entry(root); self.instructorAge.grid(row=1, column=3)
        tk.Label(root, text="email", bg="#fff5e6", fg="#a52a2a").grid(row=2, column=2, sticky="w")
        self.instructorEmail = tk.Entry(root); self.instructorEmail.grid(row=2, column=3)
        tk.Label(root, text="instructor id", bg="#fff5e6", fg="#a52a2a").grid(row=3, column=2, sticky="w")
        self.instructorId = tk.Entry(root); self.instructorId.grid(row=3, column=3)
        tk.Button(root, text="add instructor", bg="#a52a2a", fg="white", command=self.add_instructor).grid(row=4, column=2, columnspan=2)

        tk.Label(root, text="course name", bg="#fff5e6", fg="#a52a2a").grid(row=5, column=0, sticky="w")
        self.courseName = tk.Entry(root); self.courseName.grid(row=5, column=1)
        tk.Label(root, text="course id", bg="#fff5e6", fg="#a52a2a").grid(row=6, column=0, sticky="w")
        self.courseId = tk.Entry(root); self.courseId.grid(row=6, column=1)
        tk.Button(root, text="add course", bg="#a52a2a", fg="white", command=self.add_course).grid(row=7, column=0, columnspan=2)

        tk.Label(root, text="select student", bg="#fff5e6", fg="#a52a2a").grid(row=8, column=0)
        self.studentBox = ttk.Combobox(root); self.studentBox.grid(row=8, column=1)
        tk.Label(root, text="select course", bg="#fff5e6", fg="#a52a2a").grid(row=9, column=0)
        self.courseBox = ttk.Combobox(root); self.courseBox.grid(row=9, column=1)
        tk.Button(root, text="register student", bg="#a52a2a", fg="white", command=self.register_student).grid(row=10, column=0, columnspan=2)

        tk.Label(root, text="select instructor", bg="#fff5e6", fg="#a52a2a").grid(row=8, column=2)
        self.instructorBox = ttk.Combobox(root); self.instructorBox.grid(row=8, column=3)
        tk.Label(root, text="select course", bg="#fff5e6", fg="#a52a2a").grid(row=9, column=2)
        self.courseBox2 = ttk.Combobox(root); self.courseBox2.grid(row=9, column=3)
        tk.Button(root, text="assign instructor", bg="#a52a2a", fg="white", command=self.assign_instructor).grid(row=10, column=2, columnspan=2)

        tk.Label(root, text="search", bg="#fff5e6", fg="#a52a2a").grid(row=11, column=0)
        self.searchBox = tk.Entry(root); self.searchBox.grid(row=11, column=1)
        tk.Button(root, text="search", bg="#a52a2a", fg="white", command=self.search_records).grid(row=11, column=2)

        cols = ("type", "id", "name", "age", "email", "courses/students")
        self.tree = ttk.Treeview(root, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.grid(row=12, column=0, columnspan=6, sticky="nsew")

        tk.Button(root, text="edit selected", bg="#a52a2a", fg="white", command=self.edit_record).grid(row=13, column=0)
        tk.Button(root, text="delete selected", bg="#a52a2a", fg="white", command=self.delete_record).grid(row=13, column=1)
        tk.Button(root, text="export csv", bg="#a52a2a", fg="white", command=self.export_csv).grid(row=13, column=2)
        tk.Button(root, text="backup db", bg="#a52a2a", fg="white", command=self.backup_db).grid(row=13, column=3)
        tk.Button(root, text="refresh", bg="#a52a2a", fg="white", command=lambda: (self.update_tree(), self.refresh_dropdowns())).grid(row=13, column=4)

        self.refresh_dropdowns()
        self.update_tree()

    def add_student(self):
        """
        Add a new student to the database and validates that all required fields are filled and that age is numeric value.
        when it works and succeeds, it updates where it inserts its new record.

        :raises ValueError: If any field is missing or age is not numeric.
        :return: None
        :rtype: None
        """
        sid, name, age, email = self.stuId.get().strip(), self.stuName.get().strip(), self.stuAge.get().strip(), self.stuEmail.get().strip()
        if not (sid and name and age and email): return messagebox.showerror("error", "all student fields required")
        if not age.isdigit(): return messagebox.showerror("error", "age must be number")
        db.add_student(sid, name, int(age), email)
        self.update_tree(); self.refresh_dropdowns()
        self.stuId.delete(0, tk.END); self.stuName.delete(0, tk.END); self.stuAge.delete(0, tk.END); self.stuEmail.delete(0, tk.END)

    def add_instructor(self):
        """
        Add a new instructor to the database.
        Reads ID, name, age, and email from the entry fields, checks
        that all are valid, and stores the record.

        :raises ValueError: If required fields are missing or age is not numeric.
        :return: None
        :rtype: None
        """
        iid, name, age, email = self.instructorId.get().strip(), self.instructorName.get().strip(), self.instructorAge.get().strip(), self.instructorEmail.get().strip()
        if not (iid and name and age and email): return messagebox.showerror("error", "all instructor fields required")
        if not age.isdigit(): return messagebox.showerror("error", "age must be number")
        db.add_instructor(iid, name, int(age), email)
        self.update_tree(); self.refresh_dropdowns()
        self.instructorId.delete(0, tk.END); self.instructorName.delete(0, tk.END); self.instructorAge.delete(0, tk.END); self.instructorEmail.delete(0, tk.END)

    def add_course(self):
        """
        Create a new course using the ID and name that the user adds.
        The instructor is npt set until later on. After adding, the
        table and dropdowns are refreshed.
        :raises ValueError: If course ID or name is empty.
        :return: None
        :rtype: None
        """
        cid, cname = self.courseId.get().strip(), self.courseName.get().strip()
        if not cid or not cname: return messagebox.showerror("error", "course id and name are required")
        db.add_course(cid, cname, None)
        self.update_tree(); self.refresh_dropdowns()
        self.courseId.delete(0, tk.END); self.courseName.delete(0, tk.END)

    def register_student(self):
        """
        Register the selected student to the selected course.
        Uses the selected values from the student and course dropdowns.

        :param sid: Student ID to register.
        :type sid: str
        :param cid: Course ID selected in the combobox.
        :type cid: str
        :return: None
        :rtype: None
        """
        sid, cid = self.studentBox.get(), self.courseBox.get()
        if sid and cid:
            db.register_student(sid, cid)
            self.update_tree()

    def assign_instructor(self):
        """
        Assign the selected instructor to the selected course.

        If the course has no name, asks the user to provide one
        :param iid: Instructor ID.
        :type iid: str
        :param cid: Course ID.
        :type cid: str
        :raises ValueError: If course name is missing when required.
        :return: None
        :rtype: None
        """

        iid, cid = self.instructorBox.get(), self.courseBox2.get()
        if not (iid and cid): return
        course_rows = [c for c in db.list_courses() if c[0] == cid]
        if not course_rows: return
        current_name = course_rows[0][1]
        if not current_name or str(current_name).strip() == "":
            ask = simpledialog.askstring("course name", "enter course name for this course id")
            if not ask or ask.strip() == "":
                return messagebox.showerror("error", "course name required")
            current_name = ask.strip()
        db.update_course(cid, current_name, iid)
        self.update_tree()
########################################################################################3
    def delete_record(self):

        """
        Delete the selected record.
        Determines if the selected row is a student or instructor,
        or course, and removes it.

        :raises LookupError: If no record is selected.
        :return: None
        :rtype: None
        """
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], "values"); kind, rid = vals[0], vals[1]
        if kind == "student": db.remove_student(rid)
        elif kind == "instructor": db.remove_instructor(rid)
        elif kind == "course": db.delete_course(rid)
        self.update_tree(); self.refresh_dropdowns()

    def edit_record(self):
        """
        Edit a selected record.
        Opens a popup window with editable fields and then also saves the record back
        after validation.

        :raises LookupError: If no record is selected.
        :raises ValueError: If inputs are invalid (for example non-numeric age).
        :return: None
        :rtype: None
        """
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], "values"); kind, rid = vals[0], vals[1]

        win = tk.Toplevel(self.root); win.title(f"edit {kind}")
        entries = {}
        if kind in ("student","instructor"):
            for idx, field in enumerate(["name","age","email"]):
                tk.Label(win, text=field).grid(row=idx, column=0)
                e = tk.Entry(win); e.grid(row=idx, column=1); e.insert(0, vals[idx+2])
                entries[field] = e
        elif kind == "course":
            tk.Label(win, text="course name").grid(row=0, column=0)
            e = tk.Entry(win); e.grid(row=0, column=1); e.insert(0, vals[2])
            entries["name"] = e

        def save():
            if kind == "student":
                age_val = entries["age"].get().strip()
                if not age_val.isdigit(): return messagebox.showerror("error", "age must be number")
                db.update_student(rid, entries["name"].get().strip(), int(age_val), entries["email"].get().strip())
            elif kind == "instructor":
                age_val = entries["age"].get().strip()
                if not age_val.isdigit(): return messagebox.showerror("error", "age must be number")
                db.update_instructor(rid, entries["name"].get().strip(), int(age_val), entries["email"].get().strip())
            elif kind == "course":
                name_new = entries["name"].get().strip()
                if not name_new: return messagebox.showerror("error", "course name required")
                row = [c for c in db.list_courses() if c[0]==rid]
                current_inst = row[0][2] if row else None
                db.update_course(rid, name_new, current_inst)
            self.update_tree(); win.destroy()
        tk.Button(win, text="save", bg="#a52a2a", fg="white", command=save).grid(row=5, column=0, columnspan=2)

    def search_records(self):
        """
        Search for records by ID or name.
        Reads the search box text and updates the table accordingly.

        :param q: Search string typed by the user.
        :type q: str
        :return: None
        :rtype: None
        """
        q = self.searchBox.get().lower()
        self.update_tree(q)

    def update_tree(self, q=""):
        """
        Refresh the main table view, it clears and reloads students and instructors and courses. If a query
        string is provided, filters by ID or name.

        :param q: Optional search string, defaults to "".
        :type q: str, optional
        :return: None
        :rtype: None
        """
        for i in self.tree.get_children(): self.tree.delete(i)
        q = str(q).lower() if q else ""

        for s in db.fetch_students():
            sid, name, age, email = s[0], s[1], s[2], s[3]
            if q in str(name).lower() or q in str(sid).lower():
                reg_course_ids = [r[1] for r in db.get_registrations() if r[0]==sid]
                course_names = [c[1] for c in db.list_courses() if c[0] in reg_course_ids]
                courses_str = ", ".join(str(x) for x in course_names if x) or "-"
                self.tree.insert("", "end", values=("student", sid, name, age, email, courses_str))

        for i in db.get_instructors():
            iid, name, age, email = i[0], i[1], i[2], i[3]
            if q in str(name).lower() or q in str(iid).lower():
                teaching = [c[1] for c in db.list_courses() if c[2]==iid]
                teaching_str = ", ".join(str(x) for x in teaching if x) or "-"
                self.tree.insert("", "end", values=("instructor", iid, name, age, email, teaching_str))

        for c in db.list_courses():
            cid, cname, inst_id = c[0], c[1], c[2]
            if q in str(cname).lower() or q in str(cid).lower():
                inst_name = "-"
                if inst_id:
                    ins = [i for i in db.get_instructors() if i[0]==inst_id]
                    if ins: inst_name = ins[0][1]
                enrolled_names = [s[1] for s in db.fetch_students() if (s[0], cid) in db.get_registrations()]
                enrolled_str = ", ".join(str(x) for x in enrolled_names if x) or "-"
                self.tree.insert("", "end", values=("course", cid, cname, inst_name, "-", enrolled_str))

    def refresh_dropdowns(self):
        """
        refresh all dropdown menus. it updates student, instructor, and course boxes from database.

        :return: None
        :rtype: None
        """
        self.studentBox["values"] = [s[0] for s in db.fetch_students()]
        self.instructorBox["values"] = [i[0] for i in db.get_instructors()]
        self.courseBox["values"] = [c[0] for c in db.list_courses()]
        self.courseBox2["values"] = [c[0] for c in db.list_courses()]

    def export_csv(self):
        """
        Export records to a CSV file. it writes students, instructors, and courses to ``school_data.csv``.

        :return: None
        :rtype: None
        """
        with open("school_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["type","id","name","age","email","courses/students"])
            for s in db.fetch_students():
                reg_course_ids = [r[1] for r in db.get_registrations() if r[0]==s[0]]
                reg_course_names = [c[1] for c in db.list_courses() if c[0] in reg_course_ids]
                regs_str = ", ".join(str(x) for x in reg_course_names if x) or "-"
                writer.writerow(["student", s[0], s[1], s[2], s[3], regs_str])
            for i in db.get_instructors():
                teaching_names = [c[1] for c in db.list_courses() if c[2]==i[0]]
                teaching_str = ", ".join(str(x) for x in teaching_names if x) or "-"
                writer.writerow(["instructor", i[0], i[1], i[2], i[3], teaching_str])
            for c in db.list_courses():
                inst_name = "-"
                if c[2]:
                    ins = [i for i in db.get_instructors() if i[0]==c[2]]
                    if ins: inst_name = ins[0][1]
                enrolled_names = [s[1] for s in db.fetch_students() if (s[0], c[0]) in db.get_registrations()]
                enrolled_str = ", ".join(str(x) for x in enrolled_names if x) or "-"
                writer.writerow(["course", c[0], c[1], inst_name, "-", enrolled_str])
        messagebox.showinfo("done","data exported to school_data.csv")

    def backup_db(self):
        """
        Backups the database. Triggers the backup operation in the database module and shows
        the result.

        :return: Backup status message.
        :rtype: str
        """
        msg = db.backup_db()
        messagebox.showinfo("backup", msg)

if __name__=="__main__":
    root = tk.Tk()
    app = SchoolApp(root)
    root.mainloop()
