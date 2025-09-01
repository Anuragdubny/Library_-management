import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from books.models import Author, Book
from datetime import date

# Add more authors
authors_data = [
    {'name': 'George Orwell', 'email': 'george@orwell.com'},
    {'name': 'Harper Lee', 'email': 'harper@lee.com'},
    {'name': 'F. Scott Fitzgerald', 'email': 'scott@fitzgerald.com'},
    {'name': 'Jane Austen', 'email': 'jane@austen.com'},
    {'name': 'Mark Twain', 'email': 'mark@twain.com'},
    {'name': 'Charles Dickens', 'email': 'charles@dickens.com'},
    {'name': 'Ernest Hemingway', 'email': 'ernest@hemingway.com'},
    {'name': 'Agatha Christie', 'email': 'agatha@christie.com'},
    {'name': 'Stephen King', 'email': 'stephen@king.com'},
    {'name': 'Dan Brown', 'email': 'dan@brown.com'},
]

# Create authors
for author_data in authors_data:
    author, created = Author.objects.get_or_create(
        name=author_data['name'],
        defaults={'email': author_data['email']}
    )
    if created:
        print(f"Created author: {author.name}")

# Add more books
books_data = [
    {'title': '1984', 'author': 'George Orwell', 'isbn': '9780451524935', 'date': date(1949, 6, 8)},
    {'title': 'Animal Farm', 'author': 'George Orwell', 'isbn': '9780451526342', 'date': date(1945, 8, 17)},
    {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'isbn': '9780061120084', 'date': date(1960, 7, 11)},
    {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '9780743273565', 'date': date(1925, 4, 10)},
    {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'isbn': '9780141439518', 'date': date(1813, 1, 28)},
    {'title': 'The Adventures of Tom Sawyer', 'author': 'Mark Twain', 'isbn': '9780486400778', 'date': date(1876, 6, 1)},
    {'title': 'Great Expectations', 'author': 'Charles Dickens', 'isbn': '9780141439563', 'date': date(1861, 8, 1)},
    {'title': 'A Tale of Two Cities', 'author': 'Charles Dickens', 'isbn': '9780486406510', 'date': date(1859, 11, 26)},
    {'title': 'The Old Man and the Sea', 'author': 'Ernest Hemingway', 'isbn': '9780684801223', 'date': date(1952, 9, 1)},
    {'title': 'Murder on the Orient Express', 'author': 'Agatha Christie', 'isbn': '9780062693662', 'date': date(1934, 1, 1)},
    {'title': 'The Shining', 'author': 'Stephen King', 'isbn': '9780307743657', 'date': date(1977, 1, 28)},
    {'title': 'It', 'author': 'Stephen King', 'isbn': '9781501142970', 'date': date(1986, 9, 15)},
    {'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'isbn': '9780307474278', 'date': date(2003, 3, 18)},
    {'title': 'Angels & Demons', 'author': 'Dan Brown', 'isbn': '9780671027360', 'date': date(2000, 5, 1)},
]

# Create books
for book_data in books_data:
    author = Author.objects.get(name=book_data['author'])
    book, created = Book.objects.get_or_create(
        isbn=book_data['isbn'],
        defaults={
            'title': book_data['title'],
            'author': author,
            'publication_date': book_data['date'],
            'available': True
        }
    )
    if created:
        print(f"Created book: {book.title}")

print("Books added successfully!")