from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from pathlib import Path
import os

# -------------------- Main Window --------------------
root = Tk()
root.geometry("1200x600")
root.maxsize(1200, 600)
root.title("Student Management System")

# Avoid crashing if icon.png is not in the project folder
try:
    root.iconphoto(True, PhotoImage(file="icon1.png"))
except (TclError, FileNotFoundError):
    pass

# -------------------- Database --------------------

# Permanent database location on Windows
app_data = Path(os.environ.get("LOCALAPPDATA", Path.home()))
db_folder = app_data / "StudentManagementSystem"

# Create the folder if it doesn't exist
db_folder.mkdir(parents=True, exist_ok=True)

# The database file is created automatically beside this Python file.
DB_PATH = db_folder / "students.db"
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        roll_no TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age TEXT NOT NULL,
        total_marks TEXT NOT NULL,
        percentage TEXT NOT NULL,
        grade TEXT NOT NULL
    )
""")
connection.commit()

# -------------------- Header --------------------
f1 = Frame(root, bg="black", height=100, width=1200, relief=RIDGE)
f1.pack(fill=X)

l1 = Label(
    f1,
    text="Welcome to Student Management System!",
    font=("Castellar", 20, "bold"),
    bg="black",
    fg="white",
    relief=RIDGE
)
l1.pack(pady=20)

# -------------------- Student Details Form --------------------
details_frame = LabelFrame(
    root,
    text="Student Details",
    font=("Times New Roman", 14, "bold"),
    bg="gray",
    fg="black",
    bd=2,
    relief=GROOVE,
)
details_frame.place(y=79, width=400, height=521)

Label(details_frame, text="Name:- ", font=("Century", 12, "bold"),
      bg="grey").place(x=20, y=50)
Label(details_frame, text="Roll No:- ", font=("Century", 12, "bold"),
      bg="grey").place(x=20, y=90)
Label(details_frame, text="Age:- ", font=("Century", 12, "bold"),
      bg="grey").place(x=20, y=130)
Label(details_frame, text="Total Marks:- ", font=("Century", 12, "bold"),
      bg="grey").place(x=20, y=170)
Label(details_frame, text="Percentage:- ", font=("Century", 12, "bold"),
      bg="grey").place(x=20, y=210)
Label(details_frame, text="Grade:- ", font=("Century", 12, "bold"),
      bg="grey").place(x=20, y=250)

namevalv = StringVar()
rollvalv = StringVar()
agevalv = StringVar()
total_marksvalv = StringVar()
percentagevalv = StringVar()
gradevalv = StringVar()

e1 = Entry(details_frame, font=("Century", 12), bg="white",
           relief=SUNKEN, textvariable=namevalv)
e1.place(x=150, y=50)

e2 = Entry(details_frame, font=("Century", 12), bg="white",
           relief=SUNKEN, textvariable=rollvalv)
e2.place(x=150, y=90)

e3 = Entry(details_frame, font=("Century", 12), bg="white",
           relief=SUNKEN, textvariable=agevalv)
e3.place(x=150, y=130)

e4 = Entry(details_frame, font=("Century", 12), bg="white",
           relief=SUNKEN, textvariable=total_marksvalv)
e4.place(x=150, y=170)

e5 = Entry(details_frame, font=("Century", 12), bg="white",
           relief=SUNKEN, textvariable=percentagevalv)
e5.place(x=150, y=210)

e6 = Entry(details_frame, font=("Century", 12), bg="white",
           relief=SUNKEN, textvariable=gradevalv)
e6.place(x=150, y=250)

# -------------------- Student Records Table --------------------
records_frame = LabelFrame(
    root,
    text="Student Records",
    font=("Century", 12, "bold"),
    bg="grey",
    relief=RIDGE
)
records_frame.place(x=400, y=79, width=800, height=520)

table_frame = Frame(records_frame)
table_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

columns = ("Roll No", "Name", "Age", "Total Marks", "Percentage", "Grade")
student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

for col in columns:
    student_table.heading(col, text=col)

student_table.column("Roll No", width=90, anchor=CENTER)
student_table.column("Name", width=130, anchor=CENTER)
student_table.column("Age", width=60, anchor=CENTER)
student_table.column("Total Marks", width=100, anchor=CENTER)
student_table.column("Percentage", width=100, anchor=CENTER)
student_table.column("Grade", width=80, anchor=CENTER)

scroll_y.config(command=student_table.yview)
scroll_x.config(command=student_table.xview)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.pack(side=BOTTOM, fill=X)
student_table.pack(fill=BOTH, expand=True)

# -------------------- Helper Functions --------------------
def get_form_data():
    """Read the values exactly as entered; no marks/percentage/grade calculation."""
    data = {
        "name": namevalv.get().strip(),
        "roll_no": rollvalv.get().strip(),
        "age": agevalv.get().strip(),
        "total_marks": total_marksvalv.get().strip(),
        "percentage": percentagevalv.get().strip(),
        "grade": gradevalv.get().strip()
    }

    if not all(data.values()):
        messagebox.showwarning("Missing Details", "Please fill in all six fields.")
        return None

    return data


def clear_fields():
    namevalv.set("")
    rollvalv.set("")
    agevalv.set("")
    total_marksvalv.set("")
    percentagevalv.set("")
    gradevalv.set("")
    student_table.selection_remove(student_table.selection())
    e1.focus_set()


def show_records():
    """Reload all saved records into the table."""
    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute("""
        SELECT roll_no, name, age, total_marks, percentage, grade
        FROM students ORDER BY roll_no
    """)
    for record in cursor.fetchall():
        student_table.insert("", END, values=record)


def fill_form_from_record(event=None):
    """Put the selected table row into the form."""
    selected = student_table.selection()
    if not selected:
        return

    values = student_table.item(selected[0], "values")
    if not values:
        return

    rollvalv.set(values[0])
    namevalv.set(values[1])
    agevalv.set(values[2])
    total_marksvalv.set(values[3])
    percentagevalv.set(values[4])
    gradevalv.set(values[5])


# -------------------- Button Functions --------------------
def add_student():
    data = get_form_data()
    if data is None:
        return

    try:
        cursor.execute("""
            INSERT INTO students
            (roll_no, name, age, total_marks, percentage, grade)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["roll_no"], data["name"], data["age"],
            data["total_marks"], data["percentage"], data["grade"]
        ))
        connection.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Duplicate Roll No",
            "This Roll No already exists. Use Update to edit that student's details."
        )
        return
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))
        return

    show_records()
    clear_fields()
    messagebox.showinfo("Success", "Student record added successfully.")


def update_student():
    data = get_form_data()
    if data is None:
        return

    try:
        cursor.execute("""
            UPDATE students
            SET name = ?, age = ?, total_marks = ?, percentage = ?, grade = ?
            WHERE roll_no = ?
        """, (
            data["name"], data["age"], data["total_marks"],
            data["percentage"], data["grade"], data["roll_no"]
        ))
        connection.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning(
                "Not Found",
                "No student with this Roll No exists. Select a record or enter an existing Roll No."
            )
            return
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))
        return

    show_records()
    clear_fields()
    messagebox.showinfo("Success", "Student record updated successfully.")


def delete_student():
    roll = rollvalv.get().strip()

    selected = student_table.selection()
    if not roll and selected:
        values = student_table.item(selected[0], "values")
        roll = values[0] if values else ""

    if not roll:
        messagebox.showwarning(
            "Select Student",
            "Enter a Roll No or select a student record to delete."
        )
        return

    cursor.execute("SELECT name FROM students WHERE roll_no = ?", (roll,))
    record = cursor.fetchone()
    if record is None:
        messagebox.showwarning("Not Found", "No student found with this Roll No.")
        return

    if not messagebox.askyesno(
        "Confirm Delete",
        f"Delete the record for {record[0]} (Roll No: {roll})?"
    ):
        return

    try:
        cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll,))
        connection.commit()
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))
        return

    show_records()
    clear_fields()
    messagebox.showinfo("Success", "Student record deleted successfully.")


def search_student():
    roll = rollvalv.get().strip()
    if not roll:
        messagebox.showwarning("Enter Roll No", "Enter a Roll No to search.")
        e2.focus_set()
        return

    cursor.execute("""
        SELECT roll_no, name, age, total_marks, percentage, grade
        FROM students WHERE roll_no = ?
    """, (roll,))
    record = cursor.fetchone()

    if record is None:
        messagebox.showinfo("Not Found", "No student found with this Roll No.")
        return

    rollvalv.set(record[0])
    namevalv.set(record[1])
    agevalv.set(record[2])
    total_marksvalv.set(record[3])
    percentagevalv.set(record[4])
    gradevalv.set(record[5])

    student_table.selection_remove(student_table.selection())
    for item in student_table.get_children():
        if str(student_table.item(item, "values")[0]) == str(record[0]):
            student_table.selection_set(item)
            student_table.focus(item)
            student_table.see(item)
            break


# -------------------- Buttons --------------------
button1 = Button(
    details_frame, text="  Add  ", font=("Century", 12),
    bg="black", fg="white", relief=RAISED, command=add_student
)
button1.place(x=80, y=300)

button2 = Button(
    details_frame, text="  update  ", font=("Century", 12),
    bg="black", fg="white", relief=RAISED, command=update_student
)
button2.place(x=150, y=300)

button3 = Button(
    details_frame, text="  Delete  ", font=("Century", 12),
    bg="black", fg="white", relief=RAISED, command=delete_student
)
button3.place(x=70, y=350)

button4 = Button(
    details_frame, text="  Search  ", font=("Century", 12),
    bg="black", fg="white", relief=RAISED, command=search_student
)
button4.place(x=160, y=350)

button5 = Button(
    details_frame, text="  Clear  ", font=("Century", 12),
    bg="black", fg="white", relief=RAISED, command=clear_fields
)
button5.place(x=120, y=400)

# Clicking a row fills its details into the form.
student_table.bind("<<TreeviewSelect>>", fill_form_from_record)

# Load previously saved students whenever the app starts.
show_records()

def close_application():
    connection.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_application)

# Move to the next entry when Enter is pressed
e1.bind("<Return>", lambda event: e2.focus_set())
e2.bind("<Return>", lambda event: e3.focus_set())
e3.bind("<Return>", lambda event: e4.focus_set())
e4.bind("<Return>", lambda event: e5.focus_set())
e5.bind("<Return>", lambda event: e6.focus_set())

# After the last entry, move back to the first entry
e6.bind("<Return>", lambda event: e1.focus_set())

root.mainloop()
