import mysql.connector
from datetime import datetime

# ✅ 1️⃣ --- Connection setup (یہاں آپ اپنا existing connection code رکھیں)
conn = mysql.connector.connect(
    host="localhost",
    user="myuser",          # نیا user جو آپ نے بنایا
    password="mypassword",  # نیا password
    database="Library-db"   # آپ کا existing database
)
cursor = conn.cursor()

# ✅ 2️⃣ --- Create tables (یہ صرف پہلی بار چلائیں، بعد میں comment کر دیں)
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    year_published INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    member_id INT,
    issue_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
)
""")

# ✅ 3️⃣ --- Functions

def add_book(title, author, year_published):
    sql = "INSERT INTO books (title, author, year_published) VALUES (%s, %s, %s)"
    val = (title, author, year_published)
    cursor.execute(sql, val)
    conn.commit()
    print("✅ Book added successfully.")

def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("📚 All Books:")
    for book in books:
        print(book)

def update_book(book_id, title, author, year_published):
    sql = "UPDATE books SET title=%s, author=%s, year_published=%s WHERE id=%s"
    val = (title, author, year_published, book_id)
    cursor.execute(sql, val)
    conn.commit()
    print("✅ Book updated successfully.")

def delete_book(book_id):
    sql = "DELETE FROM books WHERE id=%s"
    val = (book_id,)
    cursor.execute(sql, val)
    conn.commit()
    print("✅ Book deleted successfully.")

def add_member(name, email, phone):
    sql = "INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)"
    val = (name, email, phone)
    cursor.execute(sql, val)
    conn.commit()
    print("✅ Member added successfully.")

def view_members():
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    print("👥 All Members:")
    for member in members:
        print(member)

def issue_book(book_id, member_id):
    issue_date = datetime.now().date()
    sql = "INSERT INTO issued_books (book_id, member_id, issue_date, return_date) VALUES (%s, %s, %s, NULL)"
    val = (book_id, member_id, issue_date)
    cursor.execute(sql, val)
    conn.commit()
    print("✅ Book issued successfully.")

def return_book(issue_id):
    return_date = datetime.now().date()
    sql = "UPDATE issued_books SET return_date=%s WHERE id=%s"
    val = (return_date, issue_id)
    cursor.execute(sql, val)
    conn.commit()
    print("✅ Book returned successfully.")

def view_issued_books():
    cursor.execute("""
    SELECT issued_books.id, books.title, members.name, issued_books.issue_date, issued_books.return_date
    FROM issued_books
    JOIN books ON issued_books.book_id = books.id
    JOIN members ON issued_books.member_id = members.id
    """)
    issued = cursor.fetchall()
    print("📖 Issued Books:")
    for record in issued:
        print(record)

# ✅ 4️⃣ --- Test your functions here

# Add book test
# add_book("Python Basics", "John Doe", 2024)

# View all books
# view_books()

# Update book test
# update_book(1, "Advanced Python", "John Doe", 2025)

# Delete book test
# delete_book(1)

# Add member test
# add_member("Alice Smith", "alice@example.com", "03001234567")

# View members
# view_members()

# Issue book
# issue_book(1, 1)

# Return book
# return_book(1)

# View issued books
# view_issued_books()

# ✅ 5️⃣ --- Close connection at the end
#Test case for my library management system
def test_invalid_book_id_for_issue():
    try:
        issue_book(999, 1)  # Assuming 999 is an invalid book_id
    except Exception as e:
        assert str(e) == "Invalid book ID", "Test failed: No error for invalid book ID."
        print("Test passed: Error for invalid book ID.")
def test_invalid_member_id_for_issue():
    try:
        issue_book(1, 999)  # Assuming 999 is an invalid member_id
    except Exception as e:
        assert str(e) == "Invalid member ID", "Test failed: No error for invalid member ID."
        print("Test passed: Error for invalid member ID.")
def test_search_book_by_title():
    search_results = search_book_by_title("The Python Handbook")
    assert len(search_results) > 0, "Test failed: Book not found."
    print("Test passed: Book search by title successful.")
def test_return_book():
    # Assuming book_id=1 is valid and the book has been issued
    return_book(1)
    cursor.execute("SELECT * FROM issued_books WHERE book_id = 1")
    result = cursor.fetchone()
    assert result is None, "Test failed: Book not returned."
    print("Test passed: Book returned successfully.")
def test_view_books():
    books = view_books()
    assert len(books) > 0, "Test failed: No books found."
    print("Test passed: Books displayed successfully.")
def test_issue_book():
    # Assuming book_id=1 and member_id=1 are valid
    issue_book(1, 1)
    cursor.execute("SELECT * FROM issued_books WHERE book_id = 1 AND member_id = 1")
    result = cursor.fetchone()
    assert result is not None, "Test failed: Book not issued."
    print("Test passed: Book issued successfully.")
def test_add_member():
    add_member("John Doe", "john.doe@example.com", "123456789")
    cursor.execute("SELECT * FROM members WHERE name = 'John Doe'")
    result = cursor.fetchone()
    assert result is not None, "Test failed: Member not added."
    print("Test passed: Member added successfully.")
def test_add_book():
    add_book("The Python Handbook", "Guido van Rossum", 2024)
    cursor.execute("SELECT * FROM books WHERE title = 'The Python Handbook'")
    result = cursor.fetchone()
    assert result is not None, "Test failed: Book not added."
    print("Test passed: Book added successfully.")
