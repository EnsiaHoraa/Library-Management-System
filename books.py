import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    isbn TEXT,
    category TEXT,
    available INTEGER DEFAULT 1
)
""")

# Students Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT
)
""")

# Issued Books Table
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