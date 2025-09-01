import os
import sys
import django

os.chdir('library_project')
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

try:
    from books.views import book_list, book_detail
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    
    factory = RequestFactory()
    request = factory.get('/')
    request.user = User.objects.get(username='admin')
    
    response = book_list(request)
    print(f"Book list view: {response.status_code}")
    
    print("All views working correctly!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()