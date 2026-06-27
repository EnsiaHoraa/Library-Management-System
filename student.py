import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT
)
""")

conn.commit()

def add_student():
    name = input("Enter Student Name: ")
    contact = input("Enter Contact: ")

    cursor.execute("""
    INSERT INTO students(name, contact)
    VALUES(?,?)
    """,(name, contact))

    conn.commit()
    print("Student Added Successfully")


def view_students():

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if students:
        for student in students:
            print(student)
    else:
        print("No Students Found")


def delete_student():

    student_id = int(input("Enter Student ID: "))

    cursor.execute("""
    DELETE FROM students
    WHERE id=?
    """,(student_id,))

    conn.commit()

    print("Student Deleted Successfully")


while True:

    print("\n===== STUDENT MANAGEMENT =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Delete Student")
    print("4. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        delete_student()

    elif choice == "4":
        break

    else:
        print("Invalid Choice")