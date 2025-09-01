import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from books.models import Book

# Update books with cover images
book_images = {
    '1984': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1532714506i/40961427.jpg',
    'Animal Farm': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1424037542i/7613.jpg',
    'To Kill a Mockingbird': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1553383690i/2657.jpg',
    'The Great Gatsby': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1490528560i/4671.jpg',
    'Pride and Prejudice': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1320399351i/1885.jpg',
    'The Adventures of Tom Sawyer': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1347652377i/24583.jpg',
    'Great Expectations': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1327920219i/2623.jpg',
    'A Tale of Two Cities': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1344922523i/1953.jpg',
    'The Old Man and the Sea': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1329189714i/2165.jpg',
    'Murder on the Orient Express': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1486131451i/853510.jpg',
    'The Shining': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1353277730i/11588.jpg',
    'It': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1334416842i/830502.jpg',
    'The Da Vinci Code': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1579621267i/968.jpg',
    'Angels & Demons': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1303390735i/960.jpg',
    'Harry Potter and the Sorcerer\'s Stone': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1474154022i/3.jpg'
}

for title, image_url in book_images.items():
    try:
        book = Book.objects.get(title=title)
        book.image_url = image_url
        book.save()
        print(f"Updated image for: {title}")
    except Book.DoesNotExist:
        print(f"Book not found: {title}")

print("Book images updated!")