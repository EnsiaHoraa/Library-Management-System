import sqlite3
from datetime import datetime

# Database Connection
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Create Issued Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books(
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    student_id INTEGER,
    issue_date TEXT,
    due_date TEXT,
    return_status TEXT DEFAULT 'Not Returned'
)
""")

conn.commit()


# ---------------- ISSUE BOOK ---------------- #

def issue_book():

    book_id = int(input("Enter Book ID: "))
    student_id = int(input("Enter Student ID: "))
    issue_date = input("Enter Issue Date (YYYY-MM-DD): ")
    due_date = input("Enter Due Date (YYYY-MM-DD): ")

    cursor.execute("SELECT available FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()

    if book and book[0] == 1:

        cursor.execute("""
        INSERT INTO issued_books(book_id, student_id, issue_date, due_date)
        VALUES(?,?,?,?)
        """, (book_id, student_id, issue_date, due_date))

        cursor.execute("""
        UPDATE books
        SET available = 0
        WHERE id = ?
        """, (book_id,))

        conn.commit()

        print("\nBook Issued Successfully!")

    else:
        print("\nBook Not Available.")


# ---------------- RETURN BOOK ---------------- #

def return_book():

    issue_id = int(input("Enter Issue ID: "))

    cursor.execute("""
    SELECT book_id
    FROM issued_books
    WHERE issue_id=?
    """, (issue_id,))

    result = cursor.fetchone()

    if result:

        book_id = result[0]

        cursor.execute("""
        UPDATE issued_books
        SET return_status='Returned'
        WHERE issue_id=?
        """, (issue_id,))

        cursor.execute("""
        UPDATE books
        SET available=1
        WHERE id=?
        """, (book_id,))

        conn.commit()

        print("\nBook Returned Successfully!")

    else:
        print("\nIssue Record Not Found.")


# ---------------- AVAILABLE BOOKS ---------------- #

def available_books():

    cursor.execute("""
    SELECT *
    FROM books
    WHERE available=1
    """)

    books = cursor.fetchall()

    print("\n===== AVAILABLE BOOKS =====")

    if books:

        for book in books:
            print(book)

    else:

        print("No Available Books")


# ---------------- ISSUED BOOK REPORT ---------------- #

def issued_books_report():

    cursor.execute("""
    SELECT *
    FROM issued_books
    WHERE return_status='Not Returned'
    """)

    data = cursor.fetchall()

    print("\n===== ISSUED BOOKS =====")

    if data:

        for row in data:
            print(row)

    else:

        print("No Issued Books")


# ---------------- FINE CALCULATOR ---------------- #

def calculate_fine():

    issue_id = int(input("Enter Issue ID: "))

    cursor.execute("""
    SELECT due_date, return_status
    FROM issued_books
    WHERE issue_id=?
    """, (issue_id,))

    record = cursor.fetchone()

    if record:

        due_date = record[0]
        status = record[1]

        if status == "Returned":

            print("\nBook is already returned.")
            return

        today = datetime.today()
        due = datetime.strptime(due_date, "%Y-%m-%d")

        if today > due:

            late_days = (today - due).days
            fine = late_days * 20

            print("\n===== FINE DETAILS =====")
            print("Late Days :", late_days)
            print("Fine Amount : Rs.", fine)

        else:

            print("\nNo Fine. Book is within Due Date.")

    else:

        print("\nIssue Record Not Found.")


# ---------------- MAIN MENU ---------------- #

while True:

    print("\n========== ISSUE & RETURN SYSTEM ==========")
    print("1. Issue Book")
    print("2. Return Book")
    print("3. Available Books")
    print("4. Issued Books Report")
    print("5. Calculate Fine")
    print("6. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        issue_book()

    elif choice == "2":
        return_book()

    elif choice == "3":
        available_books()

    elif choice == "4":
        issued_books_report()

    elif choice == "5":
        calculate_fine()

    elif choice == "6":
        print("Thank You!")
        break

    else:
        print("Invalid Choice! Please Try Again.")