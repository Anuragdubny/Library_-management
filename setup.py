#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
sys.path.append('library_project')
django.setup()

# Import models after Django setup
from books.models import Author, Book

def setup_sample_data():
    # Create sample authors
    author1, _ = Author.objects.get_or_create(
        name="J.K. Rowling",
        defaults={'email': 'jk@example.com'}
    )
    author2, _ = Author.objects.get_or_create(
        name="George Orwell",
        defaults={'email': 'orwell@example.com'}
    )
    
    # Create sample books
    Book.objects.get_or_create(
        isbn="9780439708180",
        defaults={
            'title': "Harry Potter and the Sorcerer's Stone",
            'author': author1,
            'publication_date': '1997-06-26'
        }
    )
    Book.objects.get_or_create(
        isbn="9780451524935",
        defaults={
            'title': "1984",
            'author': author2,
            'publication_date': '1949-06-08'
        }
    )
    
    print("Sample data created successfully!")

if __name__ == '__main__':
    os.chdir('library_project')
    
    print("Setting up Django Library Management System...")
    
    # Run migrations
    execute_from_command_line(['manage.py', 'makemigrations', 'books'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Setup sample data
    setup_sample_data()
    
    print("\nTo create an admin user, run: python manage.py createsuperuser")
    print("\nSetup complete! Run 'python manage.py runserver' to start the application.")