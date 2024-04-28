import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to MySQL database
connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='Project'
)
cursor = connect.cursor(buffered=True)

# Create a table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  title VARCHAR(255) NOT NULL,
                  author VARCHAR(255) NOT NULL)''')

class LibraryManagement:
    def __init__(self, master):
        self.main = master
        self.main.title("Library Management System")
        self.main.geometry("600x420")
        self.main.config(bg='#ECECEC')

        self.books = []
        self.fetch_books()

        # Title Label
        self.title_label = tk.Label(self.main, text="Library Management System", font=("Helvetica", 24, "bold"), bg='#4CAF50', fg='white', border=5, relief=tk.GROOVE)
        self.title_label.pack(side="top", fill="x")

        # Entry Labels
        self.title_entry_label = tk.Label(self.main, text="Title:", font=("Helvetica", 14), bg='#ECECEC', fg='black')
        self.title_entry_label.pack(pady=(10, 0))

        self.title_entry = tk.Entry(self.main, font=("Helvetica", 12))
        self.title_entry.pack(ipadx=100, ipady=5)

        self.author_entry_label = tk.Label(self.main, text="Author:", font=("Helvetica", 14), bg='#ECECEC', fg='black')
        self.author_entry_label.pack(pady=(10, 0))

        self.author_entry = tk.Entry(self.main, font=("Helvetica", 12))
        self.author_entry.pack(ipadx=100, ipady=5)

        # Add Book Button
        self.add_book_button = tk.Button(self.main, text="Add Book", command=self.add_book, font=("Helvetica", 12), bg='#4CAF50', fg='white', width=20)
        self.add_book_button.pack(pady=10)

        # Remove Book Section
        self.remove_book_label = tk.Label(self.main, text="Remove Book", font=("Helvetica", 16), bg='#ECECEC', fg='black')
        self.remove_book_label.pack()

        self.remove_book_entry = tk.Entry(self.main, font=("Helvetica", 12))
        self.remove_book_entry.pack(ipadx=100, ipady=5)

        self.remove_book_button = tk.Button(self.main, text="Remove Book", command=self.remove_book, font=("Helvetica", 12), bg='#FF5733', fg='white', width=20)
        self.remove_book_button.pack(pady=10)

        # View Books Button
        self.view_books_button = tk.Button(self.main, text="View Books", command=self.view_books, font=("Helvetica", 12), bg='#2980B9', fg='white', width=20)
        self.view_books_button.pack(pady=10)

    def fetch_books(self):
        # Fetch books from the database
        cursor.execute("SELECT title FROM Books")
        result = cursor.fetchall()
        self.books = [book[0] for book in result]

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        if title and author:
            try:
                # Insert book into the database
                cursor.execute("INSERT INTO Books (title, author) VALUES (%s, %s)", (title, author))
                connect.commit()
                self.books.append(title)
                messagebox.showinfo("Success", "Book added successfully!")
                self.clear_entry_fields()  # Clear entry fields after adding
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error occurred: {err}")
        else:
            messagebox.showerror("Error", "Please enter both title and author")

    def remove_book(self):
        title = self.remove_book_entry.get()
        if title in self.books:
            try:
                # Delete book from the database
                cursor.execute("DELETE FROM Books WHERE title = %s", (title,))
                connect.commit()
                self.books.remove(title)
                messagebox.showinfo("Success", "Book removed successfully!")
                self.clear_entry_fields()  # Clear entry fields after removing
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error occurred: {err}")
        else:
            messagebox.showerror("Error", "Book not found")

    def view_books(self):
        message = "\n".join(self.books)
        messagebox.showinfo("Books", message)

    def clear_entry_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.remove_book_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagement(root)
    root.mainloop()
