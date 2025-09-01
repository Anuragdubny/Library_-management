import os
import sys
import django

os.chdir('library_project')
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from books.models import Book, Member, BorrowRecord
from django.contrib.auth.models import User

# Test data flow
user = User.objects.get(username='admin')
books = Book.objects.all()

print(f"User: {user.username}")
print(f"Available books: {books.count()}")

# Check if member exists
try:
    member = Member.objects.get(user=user)
    print(f"Member exists: {member}")
except Member.DoesNotExist:
    print("No member record found")

# Check borrow records
records = BorrowRecord.objects.filter(member__user=user, return_date__isnull=True)
print(f"Active borrow records: {records.count()}")

for record in records:
    print(f"- {record.book.title} (borrowed: {record.borrow_date})")