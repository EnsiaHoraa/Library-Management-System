import sqlite3

# Database Connection
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE,
    category TEXT,
    available INTEGER DEFAULT 1
)
""")

conn.commit()


# Add Book
def add_book():
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    isbn = input("Enter ISBN: ")
    category = input("Enter Category: ")

    cursor.execute("""
    INSERT INTO books(title, author, isbn, category)
    VALUES (?, ?, ?, ?)
    """, (title, author, isbn, category))

    conn.commit()
    print("Book Added Successfully!")


# View All Books
def view_books():

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if len(books) == 0:
        print("No Books Found")
    else:
        print("\n--- BOOK LIST ---")
        for book in books:
            print(book)


# Search Book
def search_book():

    keyword = input("Enter Title or Author: ")

    cursor.execute("""
    SELECT * FROM books
    WHERE title LIKE ? OR author LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%'))

    books = cursor.fetchall()

    if books:
        for book in books:
            print(book)
    else:
        print("Book Not Found")


# Update Book
def update_book():

    book_id = int(input("Enter Book ID: "))

    title = input("New Title: ")
    author = input("New Author: ")
    isbn = input("New ISBN: ")
    category = input("New Category: ")

    cursor.execute("""
    UPDATE books
    SET title=?, author=?, isbn=?, category=?
    WHERE id=?
    """, (title, author, isbn, category, book_id))

    conn.commit()

    print("Book Updated Successfully")


# Delete Book
def delete_book():

    book_id = int(input("Enter Book ID To Delete: "))

    cursor.execute("""
    DELETE FROM books
    WHERE id=?
    """, (book_id,))

    conn.commit()

    print("Book Deleted Successfully")


# Testing Menu
while True:

    print("\n===== BOOK MANAGEMENT =====")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_book()

    elif choice == "2":
        view_books()

    elif choice == "3":
        search_book()

    elif choice == "4":
        update_book()

    elif choice == "5":
        delete_book()

    elif choice == "6":
        break

    else:
        print("Invalid Choice")