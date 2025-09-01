import os
import sys
import django

os.chdir('library_project')
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from books.models import BorrowRecord, Member
from django.contrib.auth.models import User
from django.test import RequestFactory
from books.views import my_books

# Test the my_books view
user = User.objects.get(username='admin')
factory = RequestFactory()
request = factory.get('/my-books/')
request.user = user

try:
    response = my_books(request)
    print(f"View response status: {response.status_code}")
    
    # Check what data is being passed to template
    member = Member.objects.get(user=user)
    borrowed_books = BorrowRecord.objects.filter(member=member, return_date__isnull=True)
    print(f"Borrowed books count: {borrowed_books.count()}")
    
    for book in borrowed_books:
        print(f"Book: {book.book.title}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()