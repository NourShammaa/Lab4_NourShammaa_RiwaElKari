import json
import re
from abc import ABC, abstractmethod
#this person
class Person(ABC):
  def __init__(self, name: str, age: int, email: str):
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        if age < 0:
            raise ValueError("Age cannot be negative")
        self.name = name
        self.age = age
        self._email = email

  def introduce(self):
        return f"Hi, I am {self.name}, {self.age} years old."
  @staticmethod
  def _validate_email(email: str) -> bool:
    """Return True if email looks real email address."""
    email = (email or "").strip()
    if not email or " " in email or email.count("@") != 1:#if 
        return False

    local, domain = email.split("@", 1)
    allowed_local = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'*+/=?^_`{|}~.-")
    if local[0] == "." or local[-1] == "." or ".." in local:
        return False
    if any(ch not in allowed_local for ch in local):
        return False
    if domain[0] == "." or domain[-1] == "." or ".." in domain:
        return False
    return True

# this for student
class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []
    def register_course(self, course):
        self.registered_courses.append(course)
# the following  is for the instructor
class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []
    def assign_course(self, course):
        self.assigned_courses.append(course)
# this course
class Course:
    def __init__(self, course_id, course_name, instructor=None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []
    def add_student(self, student):
        self.enrolled_students.append(student)
class DataManager:
    @staticmethod
    def save(data, filename="school_data.json"):
        with open(filename, "w") as f:
            json.dump(data, f, default=lambda o: o.__dict__, indent=4)

    @staticmethod
    def load(filename="school_data.json"):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
