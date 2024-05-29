import tkinter as tk
from tkinter import messagebox
import random
from collections import defaultdict

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class Student(User):
    def __init__(self, student_id, name):
        super().__init__(student_id, name)
        self.bids = []

    def place_bid(self, class_bid):
        self.bids.append(class_bid)

class Teacher(User):
    def __init__(self, teacher_id, name):
        super().__init__(teacher_id, name)
        self.assigned_classes = []

    def assign_class(self, class_instance):
        self.assigned_classes.append(class_instance)

class Class:
    def __init__(self, class_id, name):
        self.class_id = class_id
        self.name = name
        self.students = []
        self.teacher = None

    def add_student(self, student):
        self.students.append(student)

    def set_teacher(self, teacher):
        self.teacher = teacher

class ClassBid:
    def __init__(self, student, class_instance):
        self.student = student
        self.class_instance = class_instance

class Admin:
    def __init__(self):
        self.students = {}
        self.teachers = {}
        self.classes = {}

    def add_student(self, student):
        self.students[student.user_id] = student

    def add_teacher(self, teacher):
        self.teachers[teacher.user_id] = teacher

    def add_class(self, class_instance):
        self.classes[class_instance.class_id] = class_instance

    def assign_teachers_to_classes(self):
        for class_instance in self.classes.values():
            teacher = random.choice(list(self.teachers.values()))
            class_instance.set_teacher(teacher)
            teacher.assign_class(class_instance)

    def process_bids(self):
        class_bids = defaultdict(list)
        for student in self.students.values():
            for bid in student.bids:
                class_bids[bid.class_instance].append(bid.student)

        for class_instance, students in class_bids.items():
            for student in students:
                class_instance.add_student(student)

    def handle_last_minute_changes(self, student_id, new_class_id):
        student = self.students.get(student_id)
        new_class = self.classes.get(new_class_id)
        
        if student and new_class:
            for class_instance in self.classes.values():
                if student in class_instance.students:
                    class_instance.students.remove(student)

            new_class.add_student(student)
        else:
            print("Invalid student ID or class ID")

# GUI Implementation
class SchoolGUI:
    def __init__(self, root):
        self.admin = Admin()

        self.root = root
        self.root.title("School Scheduling System")
        self.root.configure(bg="#87CEEB")

        # Title
        self.title_label = tk.Label(root, text="School Scheduling System", font=("Helvetica", 16), bg="#87CEEB", fg="#FFD700")
        self.title_label.pack(pady=10)

        # Frame for buttons
        self.frame = tk.Frame(root, bg="#87CEEB")
        self.frame.pack(pady=10)

        # Add Student Button
        self.add_student_button = tk.Button(self.frame, text="Add Student", command=self.add_student, bg="#FFD700", fg="#000000")
        self.add_student_button.grid(row=0, column=0, padx=10, pady=5)

        # Add Teacher Button
        self.add_teacher_button = tk.Button(self.frame, text="Add Teacher", command=self.add_teacher, bg="#FFD700", fg="#000000")
        self.add_teacher_button.grid(row=0, column=1, padx=10, pady=5)

        # Add Class Button
        self.add_class_button = tk.Button(self.frame, text="Add Class", command=self.add_class, bg="#FFD700", fg="#000000")
        self.add_class_button.grid(row=0, column=2, padx=10, pady=5)

        # Process Bids Button
        self.process_bids_button = tk.Button(self.frame, text="Process Bids", command=self.process_bids, bg="#FFD700", fg="#000000")
        self.process_bids_button.grid(row=1, column=0, padx=10, pady=5)

        # Assign Teachers Button
        self.assign_teachers_button = tk.Button(self.frame, text="Assign Teachers", command=self.assign_teachers, bg="#FFD700", fg="#000000")
        self.assign_teachers_button.grid(row=1, column=1, padx=10, pady=5)

        # Handle Last Minute Changes Button
        self.last_minute_changes_button = tk.Button(self.frame, text="Last Minute Changes", command=self.last_minute_changes, bg="#FFD700", fg="#000000")
        self.last_minute_changes_button.grid(row=1, column=2, padx=10, pady=5)

    def add_student(self):
        self.input_popup("Add Student", "Student ID:", "Name:", self.admin.add_student, Student)

    def add_teacher(self):
        self.input_popup("Add Teacher", "Teacher ID:", "Name:", self.admin.add_teacher, Teacher)

    def add_class(self):
        self.input_popup("Add Class", "Class ID:", "Name:", self.admin.add_class, Class)

    def process_bids(self):
        self.admin.process_bids()
        messagebox.showinfo("Success", "Bids have been processed")

    def assign_teachers(self):
        self.admin.assign_teachers_to_classes()
        messagebox.showinfo("Success", "Teachers have been assigned")

    def last_minute_changes(self):
        self.input_popup("Last Minute Changes", "Student ID:", "New Class ID:", self.admin.handle_last_minute_changes, None, False)

    def input_popup(self, title, label1_text, label2_text, callback, cls, has_name=True):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="#87CEEB")

        label1 = tk.Label(popup, text=label1_text, bg="#87CEEB", fg="#000000")
        label1.grid(row=0, column=0, padx=10, pady=5)
        entry1 = tk.Entry(popup)
        entry1.grid(row=0, column=1, padx=10, pady=5)

        if has_name:
            label2 = tk.Label(popup, text=label2_text, bg="#87CEEB", fg="#000000")
            label2.grid(row=1, column=0, padx=10, pady=5)
            entry2 = tk.Entry(popup)
            entry2.grid(row=1, column=1, padx=10, pady=5)
        else:
            entry2 = None

        def on_submit():
            if has_name:
                instance = cls(entry1.get(), entry2.get())
                callback(instance)
            else:
                callback(entry1.get(), entry2.get())
            popup.destroy()
            messagebox.showinfo("Success", f"{title} has been processed")

        submit_button = tk.Button(popup, text="Submit", command=lambda: on_submit(), bg="#FFD700", fg="#000000")
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolGUI(root)
    root.mainloop()
