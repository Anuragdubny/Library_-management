#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.chdir('library_project')
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

try:
    # Test Django setup
    django.setup()
    print("[OK] Django setup successful")
    
    # Test URL resolution
    from django.urls import reverse
    reverse('book_list')
    print("[OK] URL configuration working")
    
    # Test template loading
    from django.template.loader import get_template
    get_template('base.html')
    print("[OK] Templates loading correctly")
    
    # Test models
    from books.models import Book
    print("[OK] Models imported successfully")
    
    print("\nAll checks passed! Your Django app is ready to run.")
    print("Run: cd library_project && python manage.py runserver")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)