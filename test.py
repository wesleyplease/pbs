import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
import random
from collections import defaultdict

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.availability = {}  # Key: day, Value: list of available hours
        self.preferences = {}  # Key: day, Value: list of preferred hours with weights

    def set_availability(self, day, hours):
        self.availability[day] = hours

    def set_preference(self, day, hours_with_weights):
        self.preferences[day] = hours_with_weights

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
    def __init__(self, class_id, name, schedule_date, hour):
        self.class_id = class_id
        self.name = name
        self.students = []
        self.teacher = None
        self.schedule_date = schedule_date
        self.hour = hour

    def add_student(self, student):
        self.students.append(student)

    def set_teacher(self, teacher):
        self.teacher = teacher

class RecurringClass(Class):
    def __init__(self, class_id, name, start_date, hour, frequency):
        super().__init__(class_id, name, start_date, hour)
        self.frequency = frequency  # Frequency can be daily, weekly, etc.
        self.recurring_dates = self.generate_recurring_dates(start_date, frequency)

    def generate_recurring_dates(self, start_date, frequency):
        dates = [start_date]
        current_date = start_date
        while len(dates) < 10:  # Let's assume we generate 10 instances for simplicity
            if frequency == 'weekly':
                current_date = (current_date + datetime.timedelta(weeks=1))
            elif frequency == 'daily':
                current_date = (current_date + datetime.timedelta(days=1))
            dates.append(current_date)
        return dates

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

    def add_recurring_class(self, recurring_class):
        for date in recurring_class.recurring_dates:
            class_instance = Class(recurring_class.class_id, recurring_class.name, date, recurring_class.hour)
            self.add_class(class_instance)

    def assign_teachers_to_classes(self):
        for class_instance in self.classes.values():
            available_teachers = [
                teacher for teacher in self.teachers.values()
                if class_instance.schedule_date in teacher.availability and class_instance.hour in teacher.availability[class_instance.schedule_date]
            ]
            if available_teachers:
                teacher = max(available_teachers, key=lambda t: t.preferences.get(class_instance.schedule_date, {}).get(class_instance.hour, 0))
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

    def handle_teacher_call_out(self, teacher_id):
        teacher = self.teachers.get(teacher_id)
        if not teacher:
            messagebox.showerror("Error", "Invalid teacher ID")
            return

        for class_instance in teacher.assigned_classes:
            substitutes = [
                t for t in self.teachers.values() if t.user_id != teacher_id and 
                class_instance.schedule_date in t.availability and class_instance.hour in t.availability[class_instance.schedule_date]
            ]
            if substitutes:
                substitute = max(substitutes, key=lambda t: t.preferences.get(class_instance.schedule_date, {}).get(class_instance.hour, 0))
                class_instance.set_teacher(substitute)
                substitute.assign_class(class_instance)
                messagebox.showinfo("Substitute Assigned", f"Class {class_instance.name} reassigned to {substitute.name}")
            else:
                messagebox.showwarning("No Substitute", f"No available substitute for class {class_instance.name} at {class_instance.schedule_date} {class_instance.hour}")

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

        # Handle Teacher Call-Out Button
        self.teacher_call_out_button = tk.Button(self.frame, text="Handle Teacher Call-Out", command=self.handle_teacher_call_out, bg="#FFD700", fg="#000000")
        self.teacher_call_out_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        # Calendar Frame
        self.calendar_frame = tk.Frame(root, bg="#87CEEB")
        self.calendar_frame.pack(pady=10)
        self.calendar_label = tk.Label(self.calendar_frame, text="Class Schedule", font=("Helvetica", 14), bg="#87CEEB", fg="#FFD700")
        self.calendar_label.pack()
        self.calendar = Calendar(self.calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=10)

        # Display Classes Button
        self.display_classes_button = tk.Button(self.calendar_frame, text="Display Classes", command=self.display_classes, bg="#FFD700", fg="#000000")
        self.display_classes_button.pack(pady=5)

        # Listbox for displaying classes
        self.class_listbox = tk.Listbox(self.calendar_frame, width=50, height=10)
        self.class_listbox.pack(pady=10)

        # Mouse events for drag and drop
        self.calendar.bind("<Button-1>", self.on_click)
        self.calendar.bind("<B1-Motion>", self.on_drag)
        self.calendar.bind("<ButtonRelease-1>", self.on_release)

        self.drag_data = {"x": 0, "y": 0, "item": None}

    def add_student(self):
        self.input_popup("Add Student", "Student ID:", "Name:", self.admin.add_student, Student)

    def add_teacher(self):
        self.input_popup("Add Teacher", "Teacher ID:", "Name:", self.admin.add_teacher, Teacher)

    def add_class(self):
        self.input_popup("Add Class", "Class ID:", "Name:", self.admin.add_class, Class, with_date=True, with_hour=True)

    def process_bids(self):
        self.admin.process_bids()
        messagebox.showinfo("Success", "Bids have been processed")

    def assign_teachers(self):
        self.admin.assign_teachers_to_classes()
        messagebox.showinfo("Success", "Teachers have been assigned")

    def last_minute_changes(self):
        self.input_popup("Last Minute Changes", "Student ID:", "New Class ID:", self.admin.handle_last_minute_changes, None, False)

    def handle_teacher_call_out(self):
        self.input_popup("Teacher Call-Out", "Teacher ID:", "", self.admin.handle_teacher_call_out, None, False, with_teacher_call_out=True)

    def display_classes(self):
        selected_date = self.calendar.get_date()
        self.class_listbox.delete(0, tk.END)
        for class_instance in self.admin.classes.values():
            if class_instance.schedule_date == selected_date:
                self.class_listbox.insert(tk.END, f"{class_instance.name} (Teacher: {class_instance.teacher.name if class_instance.teacher else 'TBD'}) at {class_instance.hour}:00")

    def input_popup(self, title, label1_text, label2_text, callback, cls, has_name=True, with_date=False, with_hour=False, with_teacher_call_out=False):
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

        if with_date:
            date_label = tk.Label(popup, text="Date (YYYY-MM-DD):", bg="#87CEEB", fg="#000000")
            date_label.grid(row=2, column=0, padx=10, pady=5)
            date_entry = DateEntry(popup, date_pattern='yyyy-mm-dd')
            date_entry.grid(row=2, column=1, padx=10, pady=5)
        else:
            date_entry = None

        if with_hour:
            hour_label = tk.Label(popup, text="Hour (0-23):", bg="#87CEEB", fg="#000000")
            hour_label.grid(row=3, column=0, padx=10, pady=5)
            hour_entry = tk.Entry(popup)
            hour_entry.grid(row=3, column=1, padx=10, pady=5)
        else:
            hour_entry = None

        def on_submit():
            if has_name:
                if with_date and with_hour:
                    instance = cls(entry1.get(), entry2.get(), date_entry.get_date(), int(hour_entry.get()))
                elif with_date:
                    instance = cls(entry1.get(), entry2.get(), date_entry.get_date())
                else:
                    instance = cls(entry1.get(), entry2.get())
                callback(instance)
            elif with_teacher_call_out:
                callback(entry1.get())
            else:
                callback(entry1.get(), entry2.get())
            popup.destroy()
            messagebox.showinfo("Success", f"{title} has been processed")

        submit_button = tk.Button(popup, text="Submit", command=on_submit, bg="#FFD700", fg="#000000")
        submit_button.grid(row=4 if with_hour else 3 if with_date else 2, column=0, columnspan=2, pady=10)

    def on_click(self, event):
        # Record the item and its location
        self.drag_data["item"] = self.calendar.get_calevent_selection()
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag(self, event):
        # Calculate the distance moved
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        # Move the item
        self.calendar.move(self.drag_data["item"], dx, dy)
        # Record the new position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_release(self, event):
        # Reset the drag data
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolGUI(root)
    root.mainloop()
