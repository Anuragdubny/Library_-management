import os
import sys
import django

os.chdir('library_project')
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from django.contrib.auth.models import User
from books.models import Member, BorrowRecord

print("=== USER CHECK ===")
users = User.objects.all()
for user in users:
    print(f"User: {user.username}")
    try:
        member = Member.objects.get(user=user)
        active_records = BorrowRecord.objects.filter(member=member, return_date__isnull=True)
        print(f"  - Active borrowed books: {active_records.count()}")
        for record in active_records:
            print(f"    * {record.book.title}")
    except Member.DoesNotExist:
        print(f"  - No member record")
    print()

print("=== SOLUTION ===")
print("1. Make sure you're logged in as 'admin' or 'dubey'")
print("2. Go to: http://127.0.0.1:8000/my-books/")
print("3. If still empty, borrow a book first from the main page")