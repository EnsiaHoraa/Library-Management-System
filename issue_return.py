import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

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


def issue_book():

    book_id = int(input("Book ID: "))
    student_id = int(input("Student ID: "))
    issue_date = input("Issue Date: ")
    due_date = input("Due Date: ")

    cursor.execute("""
    SELECT available
    FROM books
    WHERE id=?
    """,(book_id,))

    book = cursor.fetchone()

    if book and book[0] == 1:

        cursor.execute("""
        INSERT INTO issued_books
        (book_id, student_id, issue_date, due_date)
        VALUES(?,?,?,?)
        """,(book_id, student_id, issue_date, due_date))

        cursor.execute("""
        UPDATE books
        SET available=0
        WHERE id=?
        """,(book_id,))

        conn.commit()

        print("Book Issued Successfully")

    else:
        print("Book Not Available")


def return_book():

    issue_id = int(input("Issue ID: "))

    cursor.execute("""
    SELECT book_id
    FROM issued_books
    WHERE issue_id=?
    """,(issue_id,))

    result = cursor.fetchone()

    if result:

        book_id = result[0]

        cursor.execute("""
        UPDATE issued_books
        SET return_status='Returned'
        WHERE issue_id=?
        """,(issue_id,))

        cursor.execute("""
        UPDATE books
        SET available=1
        WHERE id=?
        """,(book_id,))

        conn.commit()

        print("Book Returned Successfully")

    else:
        print("Issue Record Not Found")


def available_books():

    cursor.execute("""
    SELECT * FROM books
    WHERE available=1
    """)

    books = cursor.fetchall()

    print("\nAvailable Books\n")

    for book in books:
        print(book)


def issued_books_report():

    cursor.execute("""
    SELECT * FROM issued_books
    WHERE return_status='Not Returned'
    """)

    data = cursor.fetchall()

    print("\nIssued Books\n")

    for row in data:
        print(row)


while True:

    print("\n===== ISSUE & RETURN =====")
    print("1. Issue Book")
    print("2. Return Book")
    print("3. Available Books")
    print("4. Issued Books Report")
    print("5. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        issue_book()

    elif choice == "2":
        return_book()

    elif choice == "3":
        available_books()

    elif choice == "4":
        issued_books_report()

    elif choice == "5":
        break

    else:
        print("Invalid Choice")