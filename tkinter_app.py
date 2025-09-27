import tkinter as tk
from tkinter import ttk, messagebox
from models import Student, Instructor, Course, DataManager
import csv

class SchoolApp:
    def __init__(self, root):
        self.students, self.instructors, self.courses = [], [], []
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
        tk.Button(root, text="add student", bg="#a52a2a", fg="white",
                  command=lambda: self.add_record("student")).grid(row=4, column=0, columnspan=2)

        tk.Label(root, text="instructor name", bg="#fff5e6", fg="#a52a2a").grid(row=0, column=2, sticky="w")
        self.instructorName = tk.Entry(root); self.instructorName.grid(row=0, column=3)
        tk.Label(root, text="age", bg="#fff5e6", fg="#a52a2a").grid(row=1, column=2, sticky="w")
        self.instructorAge = tk.Entry(root); self.instructorAge.grid(row=1, column=3)
        tk.Label(root, text="email", bg="#fff5e6", fg="#a52a2a").grid(row=2, column=2, sticky="w")
        self.instructorEmail = tk.Entry(root); self.instructorEmail.grid(row=2, column=3)
        tk.Label(root, text="instructor id", bg="#fff5e6", fg="#a52a2a").grid(row=3, column=2, sticky="w")
        self.instructorId = tk.Entry(root); self.instructorId.grid(row=3, column=3)
        tk.Button(root, text="add instructor", bg="#a52a2a", fg="white",
                  command=lambda: self.add_record("instructor")).grid(row=4, column=2, columnspan=2)

        tk.Label(root, text="course name", bg="#fff5e6", fg="#a52a2a").grid(row=5, column=0, sticky="w")
        self.courseName = tk.Entry(root); self.courseName.grid(row=5, column=1)
        tk.Label(root, text="course id", bg="#fff5e6", fg="#a52a2a").grid(row=6, column=0, sticky="w")
        self.courseId = tk.Entry(root); self.courseId.grid(row=6, column=1)
        tk.Button(root, text="add course", bg="#a52a2a", fg="white",
                  command=lambda: self.add_record("course")).grid(row=7, column=0, columnspan=2)

        tk.Label(root, text="select student", bg="#fff5e6", fg="#a52a2a").grid(row=8, column=0)
        self.studentBox = ttk.Combobox(root); self.studentBox.grid(row=8, column=1)
        tk.Label(root, text="select course", bg="#fff5e6", fg="#a52a2a").grid(row=9, column=0)
        self.courseBox = ttk.Combobox(root); self.courseBox.grid(row=9, column=1)
        tk.Button(root, text="register student", bg="#a52a2a", fg="white",
                  command=self.register_student).grid(row=10, column=0, columnspan=2)

        tk.Label(root, text="select instructor", bg="#fff5e6", fg="#a52a2a").grid(row=8, column=2)
        self.instructorBox = ttk.Combobox(root); self.instructorBox.grid(row=8, column=3)
        tk.Label(root, text="select course", bg="#fff5e6", fg="#a52a2a").grid(row=9, column=2)
        self.courseBox2 = ttk.Combobox(root); self.courseBox2.grid(row=9, column=3)
        tk.Button(root, text="assign instructor", bg="#a52a2a", fg="white",
                  command=self.assign_instructor).grid(row=10, column=2, columnspan=2)

        tk.Label(root, text="search", bg="#fff5e6", fg="#a52a2a").grid(row=11, column=0)
        self.searchBox = tk.Entry(root); self.searchBox.grid(row=11, column=1)
        tk.Button(root, text="search", bg="#a52a2a", fg="white", command=self.search_records).grid(row=11, column=2)

        cols = ("type", "id", "name", "age", "email", "courses/students")
        self.tree = ttk.Treeview(root, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.grid(row=12, column=0, columnspan=5, sticky="nsew")

        tk.Button(root, text="edit selected", bg="#a52a2a", fg="white", command=self.edit_record).grid(row=13, column=0)
        tk.Button(root, text="delete selected", bg="#a52a2a", fg="white", command=self.delete_record).grid(row=13, column=1)
        tk.Button(root, text="save data", bg="#a52a2a", fg="white", command=self.save_data).grid(row=13, column=2)
        tk.Button(root, text="load data", bg="#a52a2a", fg="white", command=self.load_data).grid(row=13, column=3)
        tk.Button(root, text="export csv", bg="#a52a2a", fg="white", command=self.export_csv).grid(row=13, column=4)

    def add_record(self, kind):
        if kind == "student":
            name, age, email, sid = self.stuName.get().strip(), self.stuAge.get().strip(), self.stuEmail.get().strip(), self.stuId.get().strip()
            if not (name and age and email and sid): return messagebox.showerror("error", "fill all student fields")
            if not age.isdigit(): return messagebox.showerror("error", "age must be number")
            self.students.append(Student(name, int(age), email, sid))
            for e in (self.stuName, self.stuAge, self.stuEmail, self.stuId): e.delete(0, tk.END)

        elif kind == "instructor":
            name, age, email, iid = self.instructorName.get().strip(), self.instructorAge.get().strip(), self.instructorEmail.get().strip(), self.instructorId.get().strip()
            if not (name and age and email and iid): return messagebox.showerror("error", "fill all instructor fields")
            if not age.isdigit(): return messagebox.showerror("error", "age must be number")
            self.instructors.append(Instructor(name, int(age), email, iid))
            for e in (self.instructorName, self.instructorAge, self.instructorEmail, self.instructorId): e.delete(0, tk.END)

        elif kind == "course":
            cname, cid = self.courseName.get().strip(), self.courseId.get().strip()
            if not (cname and cid): return messagebox.showerror("error", "course fields required")
            self.courses.append(Course(cid, cname))
            for e in (self.courseName, self.courseId): e.delete(0, tk.END)

        self.update_tree(); self.refresh_dropdowns()

    def register_student(self):
        sid, cid = self.studentBox.get(), self.courseBox.get()
        stu = next((s for s in self.students if s.student_id == sid), None)
        course = next((c for c in self.courses if c.course_id == cid), None)
        if stu and course:
            stu.register_course(course); course.add_student(stu)
            messagebox.showinfo("done", f"{stu.name} registered in {course.course_name}")
            self.update_tree()

    def assign_instructor(self):
        iid, cid = self.instructorBox.get(), self.courseBox2.get()
        ins = next((i for i in self.instructors if i.instructor_id == iid), None)
        course = next((c for c in self.courses if c.course_id == cid), None)
        if ins and course:
            ins.assign_course(course); course.instructor = ins
            messagebox.showinfo("done", f"{ins.name} assigned to {course.course_name}")
            self.update_tree()

    def search_records(self):
        q = self.searchBox.get().lower()
        for i in self.tree.get_children(): self.tree.delete(i)
        for s in self.students:
            if q in s.name.lower() or q in s.student_id.lower():
                self.tree.insert("", "end", values=("student", s.student_id, s.name, s.age, getattr(s, "_email", getattr(s, "email", "")),
                                                    ", ".join(c.course_name for c in s.registered_courses) or "-"))
        for i in self.instructors:
            if q in i.name.lower() or q in i.instructor_id.lower():
                self.tree.insert("", "end", values=("instructor", i.instructor_id, i.name, i.age, getattr(i, "_email", getattr(i, "email", "")),
                                                    ", ".join(c.course_name for c in i.assigned_courses) or "-"))
        for c in self.courses:
            if q in c.course_name.lower() or q in c.course_id.lower():
                inst = c.instructor.name if c.instructor else "-"
                enrolled = ", ".join(s.name for s in c.enrolled_students) or "-"
                self.tree.insert("", "end", values=("course", c.course_id, c.course_name, inst, "-", enrolled))

    def delete_record(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showerror("error", "no record selected")
        vals = self.tree.item(sel[0], "values"); kind, rid = vals[0], vals[1]
        if kind == "student": self.students = [s for s in self.students if s.student_id != rid]
        elif kind == "instructor": self.instructors = [i for i in self.instructors if i.instructor_id != rid]
        elif kind == "course": self.courses = [c for c in self.courses if c.course_id != rid]
        self.update_tree(); self.refresh_dropdowns()

    def edit_record(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showerror("error", "no record selected")
        vals = self.tree.item(sel[0], "values"); kind, rid = vals[0], vals[1]

        obj = None
        if kind == "student":
            obj = next((s for s in self.students if s.student_id == rid), None)
        elif kind == "instructor":
            obj = next((i for i in self.instructors if i.instructor_id == rid), None)
        elif kind == "course":
            obj = next((c for c in self.courses if c.course_id == rid), None)
        if not obj: return

        win = tk.Toplevel(self.root)
        win.title(f"edit {kind}")

        entries = {}
        if kind != "course":
            current_email = getattr(obj, "_email", getattr(obj, "email", ""))
            for idx, field in enumerate(["name", "age", "email"]):
                tk.Label(win, text=field).grid(row=idx, column=0)
                e = tk.Entry(win); e.grid(row=idx, column=1)
                if field == "email":
                    e.insert(0, current_email)
                else:
                    e.insert(0, getattr(obj, field))
                entries[field] = e
        else:
            tk.Label(win, text="course name").grid(row=0, column=0)
            e = tk.Entry(win); e.grid(row=0, column=1)
            e.insert(0, obj.course_name)
            entries["course_name"] = e

        def save():
            for f, e in entries.items():
                val = e.get().strip()
                if f == "age":
                    if not val.isdigit(): return messagebox.showerror("error", "age must be number")
                    setattr(obj, "age", int(val))
                elif f == "name":
                    setattr(obj, "name", val)
                elif f == "email":
                    if hasattr(obj, "_email"):
                        setattr(obj, "_email", val)
                    else:
                        setattr(obj, "email", val)
                elif f == "course_name":
                    setattr(obj, "course_name", val)
            self.update_tree()
            win.destroy()

        tk.Button(win, text="save", bg="#a52a2a", fg="white", command=save).grid(row=5, column=0, columnspan=2)

    def save_data(self):
        data = {
            "students":[{"id":s.student_id,"name":s.name,"age":s.age,"email":getattr(s, "_email", getattr(s, "email", "")),
                         "courses":[c.course_id for c in s.registered_courses]} for s in self.students],
            "instructors":[{"id":i.instructor_id,"name":i.name,"age":i.age,"email":getattr(i, "_email", getattr(i, "email", "")),
                            "teaching":[c.course_id for c in i.assigned_courses]} for i in self.instructors],
            "courses":[{"id":c.course_id,"title":c.course_name,"instructor":c.instructor.instructor_id if c.instructor else None,
                        "students":[s.student_id for s in c.enrolled_students]} for c in self.courses]
        }
        DataManager.save(data); messagebox.showinfo("saved","data saved")

    def load_data(self):
        data = DataManager.load()
        self.students, self.instructors, self.courses = [], [], []
        sm, im, cm = {}, {}, {}

        for i in data.get("instructors", []):
            ins = Instructor(i["name"], i["age"], i["email"], i["id"])
            self.instructors.append(ins)
            im[ins.instructor_id] = ins

        for s in data.get("students", []):
            stu = Student(s["name"], s["age"], s["email"], s["id"])
            self.students.append(stu)
            sm[stu.student_id] = stu

        for c in data.get("courses", []):
            crs = Course(c["id"], c["title"], im.get(c.get("instructor")))
            self.courses.append(crs)
            cm[crs.course_id] = crs

        for sdata in data.get("students", []):
            stu = sm[sdata["id"]]
            for cid in sdata.get("courses", []):
                if cid in cm:
                    stu.register_course(cm[cid])
                    cm[cid].add_student(stu)

        for idata in data.get("instructors", []):
            ins = im[idata["id"]]
            for cid in idata.get("teaching", []):
                if cid in cm:
                    ins.assign_course(cm[cid])
                    cm[cid].instructor = ins

        self.update_tree(); self.refresh_dropdowns()

    def export_csv(self):
        try:
            with open("school_data.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["type","id","name","age","email","courses/students"])
                for s in self.students:
                    writer.writerow(["student", s.student_id, s.name, s.age,
                                     getattr(s, "_email", getattr(s, "email", "")),
                                     ", ".join(c.course_name for c in s.registered_courses) or "-"])
                for i in self.instructors:
                    writer.writerow(["instructor", i.instructor_id, i.name, i.age,
                                     getattr(i, "_email", getattr(i, "email", "")),
                                     ", ".join(c.course_name for c in i.assigned_courses) or "-"])
                for c in self.courses:
                    inst = c.instructor.name if c.instructor else "-"
                    enrolled = ", ".join(s.name for s in c.enrolled_students) or "-"
                    writer.writerow(["course", c.course_id, c.course_name, inst, "-", enrolled])
            messagebox.showinfo("exported", "data exported to school_data.csv")
        except Exception as e:
            messagebox.showerror("error", f"could not export: {e}")

    def update_tree(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for s in self.students:
            self.tree.insert("", "end", values=(
                "student", s.student_id, s.name, s.age, getattr(s, "_email", getattr(s, "email", "")),
                ", ".join(c.course_name for c in s.registered_courses) or "-"
            ))
        for i in self.instructors:
            self.tree.insert("", "end", values=(
                "instructor", i.instructor_id, i.name, i.age, getattr(i, "_email", getattr(i, "email", "")),
                ", ".join(c.course_name for c in i.assigned_courses) or "-"
            ))
        for c in self.courses:
            inst = c.instructor.name if c.instructor else "-"
            enrolled = ", ".join(s.name for s in c.enrolled_students) or "-"
            self.tree.insert("", "end", values=("course", c.course_id, c.course_name, inst, "-", enrolled))

    def refresh_dropdowns(self):
        self.studentBox["values"] = [s.student_id for s in self.students]
        self.courseBox["values"] = [c.course_id for c in self.courses]
        self.instructorBox["values"] = [i.instructor_id for i in self.instructors]
        self.courseBox2["values"] = [c.course_id for c in self.courses]

if __name__=="__main__":
    root = tk.Tk(); app = SchoolApp(root); root.mainloop()
