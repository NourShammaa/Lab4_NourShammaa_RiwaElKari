# Lab4_NourShammaa_RiwaElKari
A project combining Tkinter and PyQt documented implementations
# School Management System

Two desktop UIs that use the same database helper:
- **PyQt** app: `pyqt_app_database.py`
- **Tkinter** app: `tkinter_app_database.py`
- **DB helper** used by both: `database.py` (or `school_gui_db.py` in the PyQt version; keep only one final helper and update imports accordingly)


---

## How to Run

### Run the Tkinter UI
```bash
python tkinter_app_database.py
```

### Run the PyQt UI
```bash
python pyqt_app_database.py
```

Both UIs connect to the same DB helper and support:
- add/edit/delete/search for students, instructors, and courses
- saving/loading/exporting


