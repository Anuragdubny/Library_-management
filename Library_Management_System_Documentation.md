# Library Management System - Complete Documentation

## Project Overview

A Django-based library management system with modern UI, user authentication, book borrowing/returning functionality, and shopping cart features.

## Features

- **User Authentication**: Login, logout, and registration
- **Book Management**: Browse books with cover images
- **Borrowing System**: Borrow and return books
- **Shopping Cart**: Add books to cart before borrowing
- **Admin Interface**: Manage books, authors, and borrow records
- **Modern UI**: Tailwind CSS with creative background and animations

## Project Structure

```
library_project/
├── library/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/
│   ├── migrations/
│   ├── static/books/
│   │   └── style.css
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── books/
│   │   ├── book_detail.html
│   │   ├── book_list.html
│   │   ├── cart.html
│   │   └── my_books.html
│   ├── registration/
│   │   ├── login.html
│   │   └── register.html
│   └── base.html
├── manage.py
├── setup.py
├── create_admin.py
├── add_books.py
├── update_book_images.py
└── requirements.txt
```

## Installation & Setup

### 1. Requirements (requirements.txt)
```
Django>=4.0
```

### 2. Setup Script (setup.py)
```python
import os
import django
import subprocess
import sys

# Install Django
subprocess.check_call([sys.executable, "-m", "pip", "install", "Django"])

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from django.core.management import execute_from_command_line

# Run migrations
execute_from_command_line(['manage.py', 'migrate'])

# Create sample data
from books.models import Author, Book, Member
from django.contrib.auth.models import User
from datetime import date

# Create authors
authors_data = [
    {'name': 'J.K. Rowling', 'email': 'jk@rowling.com'},
    {'name': 'George Orwell', 'email': 'george@orwell.com'},
]

for author_data in authors_data:
    author, created = Author.objects.get_or_create(
        name=author_data['name'],
        defaults={'email': author_data['email']}
    )

# Create books
books_data = [
    {'title': 'Harry Potter and the Sorcerer\'s Stone', 'author': 'J.K. Rowling', 'isbn': '9780439708180', 'date': date(1997, 6, 26)},
    {'title': '1984', 'author': 'George Orwell', 'isbn': '9780451524935', 'date': date(1949, 6, 8)},
]

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

print("Setup completed successfully!")
```

### 3. Admin Creation Script (create_admin.py)
```python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin user created: admin/admin123")
else:
    print("Admin user already exists")
```

## Models (books/models.py)

```python
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    available = models.BooleanField(default=True)
    image_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    def __str__(self):
        return self.user.username

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.member} - {self.book}"
```

## Views (books/views.py)

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from .models import Book, Author, BorrowRecord, Member

def book_list(request):
    books = Book.objects.all()
    user_borrowed_books = []
    
    if request.user.is_authenticated:
        try:
            member = Member.objects.get(user=request.user)
            user_borrowed_books = BorrowRecord.objects.filter(
                member=member, return_date__isnull=True
            )
        except Member.DoesNotExist:
            pass
    
    return render(request, 'books/book_list.html', {
        'books': books,
        'user_borrowed_books': user_borrowed_books
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user_borrowed_this = False
    user_borrow_record = None
    
    if request.user.is_authenticated:
        try:
            member = Member.objects.get(user=request.user)
            user_borrow_record = BorrowRecord.objects.get(
                book=book, member=member, return_date__isnull=True
            )
            user_borrowed_this = True
        except (Member.DoesNotExist, BorrowRecord.DoesNotExist):
            pass
    
    return render(request, 'books/book_detail.html', {
        'book': book,
        'user_borrowed_this': user_borrowed_this,
        'user_borrow_record': user_borrow_record
    })

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.available:
        member, created = Member.objects.get_or_create(
            user=request.user,
            defaults={'phone': '', 'address': ''}
        )
        
        borrow_record = BorrowRecord.objects.create(
            book=book, 
            member=member
        )
        
        book.available = False
        book.save()
        
        messages.success(request, f'Successfully borrowed "{book.title}"! Check "My Books" to manage it.')
    else:
        messages.error(request, 'This book is not available for borrowing.')
    return redirect('book_detail', pk=pk)

@login_required
def return_book(request, pk):
    record = get_object_or_404(BorrowRecord, pk=pk, return_date__isnull=True)
    book_title = record.book.title
    record.return_date = timezone.now()
    record.save()
    record.book.available = True
    record.book.save()
    messages.success(request, f'Successfully returned "{book_title}"!')
    return redirect('my_books')

@login_required
def my_books(request):
    borrowed_books = []
    try:
        member = Member.objects.get(user=request.user)
        borrowed_books = BorrowRecord.objects.filter(member=member, return_date__isnull=True)
    except Member.DoesNotExist:
        pass
    return render(request, 'books/my_books.html', {'borrowed_books': borrowed_books})

@login_required
def cart(request):
    return render(request, 'books/cart.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
```

## URLs (books/urls.py)

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('borrow/<int:pk>/', views.borrow_book, name='borrow_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
    path('my-books/', views.my_books, name='my_books'),
    path('cart/', views.cart, name='cart'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),
    path('register/', views.register, name='register'),
]
```

## Admin Configuration (books/admin.py)

```python
from django.contrib import admin
from .models import Author, Book, Member, BorrowRecord

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'available']
    list_filter = ['available', 'author']
    search_fields = ['title', 'isbn']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user__username']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'borrow_date', 'return_date', 'status']
    list_filter = ['borrow_date', 'return_date']
    search_fields = ['book__title', 'member__user__username']
    
    def status(self, obj):
        return "Returned" if obj.return_date else "Active"
    status.short_description = 'Status'
```

## Templates

### Base Template (templates/base.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Library Management</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    {% load static %}
    <link rel="stylesheet" href="{% static 'books/style.css' %}">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#3b82f6',
                        secondary: '#1e40af'
                    }
                }
            }
        }
    </script>
</head>
<body>
    <!-- Floating book icons -->
    <div class="floating-books">
        <div class="book-icon">📚</div>
        <div class="book-icon">📖</div>
        <div class="book-icon">📕</div>
        <div class="book-icon">📗</div>
        <div class="book-icon">📘</div>
    </div>
    <nav class="bg-white shadow-lg border-b">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center py-4">
                <div class="flex items-center space-x-8">
                    <h1 class="text-2xl font-bold text-primary">📚 Library</h1>
                    <a href="{% url 'book_list' %}" class="text-gray-700 hover:text-primary transition">All Books</a>
                    {% if user.is_authenticated %}
                        <a href="{% url 'my_books' %}" class="text-gray-700 hover:text-primary transition">My Books</a>
                        <a href="{% url 'cart' %}" class="text-gray-700 hover:text-primary transition relative">
                            🛒 Cart
                            <span id="cart-count" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full px-1">0</span>
                        </a>
                    {% endif %}
                </div>
                <div class="flex items-center space-x-4">
                    {% if user.is_authenticated %}
                        <span class="text-gray-600">Welcome, {{ user.username }}!</span>
                        <a href="{% url 'logout' %}" class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition">Logout</a>
                    {% else %}
                        <a href="{% url 'login' %}" class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-secondary transition">Login</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>
    
    <main class="max-w-7xl mx-auto px-4 py-8">
        <div class="content-overlay">
            {% if messages %}
                {% for message in messages %}
                    <div class="mb-4 p-4 rounded-lg {% if message.tags == 'success' %}bg-green-100 text-green-700{% elif message.tags == 'error' %}bg-red-100 text-red-700{% else %}bg-blue-100 text-blue-700{% endif %}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
            
            {% block content %}
            {% endblock %}
        </div>
    </main>
    
    <script>
        // Update cart count
        function updateCartCount() {
            const cart = JSON.parse(localStorage.getItem('cart') || '[]');
            document.getElementById('cart-count').textContent = cart.length;
        }
        
        // Add to cart function
        function addToCart(bookId, title) {
            const cart = JSON.parse(localStorage.getItem('cart') || '[]');
            if (!cart.find(item => item.id === bookId)) {
                cart.push({id: bookId, title: title});
                localStorage.setItem('cart', JSON.stringify(cart));
                updateCartCount();
                alert('Added to cart!');
            } else {
                alert('Book already in cart!');
            }
        }
        
        // Initialize cart count on page load
        document.addEventListener('DOMContentLoaded', updateCartCount);
    </script>
</body>
</html>
```

### Book List Template (templates/books/book_list.html)

```html
{% extends 'base.html' %}

{% block content %}
<div class="mb-8">
    <h1 class="text-4xl font-bold text-gray-800 mb-2">Library Collection</h1>
    <p class="text-gray-600">Discover and borrow from our extensive book collection</p>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {% for book in books %}
    <div class="book-card bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden">
        <div class="h-48 bg-gray-200 flex items-center justify-center overflow-hidden">
            {% if book.image_url %}
                <img src="{{ book.image_url }}" alt="{{ book.title }}" class="w-full h-full object-cover">
            {% else %}
                <span class="text-6xl text-gray-400">📚</span>
            {% endif %}
        </div>
        <div class="p-6">
            <h3 class="text-xl font-bold text-gray-800 mb-2 hover:text-primary transition">
                <a href="{% url 'book_detail' book.pk %}">{{ book.title }}</a>
            </h3>
            <p class="text-gray-600 mb-2">
                <span class="font-medium">Author:</span> {{ book.author.name }}
            </p>
            <p class="text-gray-600 mb-4">
                <span class="font-medium">ISBN:</span> {{ book.isbn }}
            </p>
            <div class="flex items-center justify-between">
                <span class="px-3 py-1 rounded-full text-sm font-medium
                    {% if book.available %}
                        bg-green-100 text-green-800
                    {% else %}
                        bg-red-100 text-red-800
                    {% endif %}">
                    {% if book.available %}
                        ✓ Available
                    {% else %}
                        ✗ Borrowed
                    {% endif %}
                </span>
                {% if user.is_authenticated %}
                    {% if book.available %}
                        <button onclick="addToCart({{ book.pk }}, '{{ book.title|addslashes }}')"
                                class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-secondary transition">
                            🛒 Add to Cart
                        </button>
                    {% else %}
                        {% for record in user_borrowed_books %}
                            {% if record.book.pk == book.pk %}
                                <a href="{% url 'return_book' record.pk %}"
                                   class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition text-sm">
                                    Return Book
                                </a>
                            {% endif %}
                        {% endfor %}
                    {% endif %}
                {% endif %}
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-span-full text-center py-12">
        <div class="text-6xl mb-4">📚</div>
        <h3 class="text-xl font-semibold text-gray-600 mb-2">No books available</h3>
        <p class="text-gray-500">Check back later for new additions to our collection.</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

### Login Template (templates/registration/login.html)

```html
{% extends 'base.html' %}

{% block content %}
<div class="max-w-md mx-auto">
    <div class="bg-white rounded-xl shadow-lg p-8">
        <div class="text-center mb-8">
            <div class="text-6xl mb-4">📚</div>
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Welcome Back</h1>
            <p class="text-gray-600">Sign in to access your library account</p>
        </div>
        
        <form method="post" class="space-y-6">
            {% csrf_token %}
            
            <div>
                <label for="id_username" class="block text-sm font-medium text-gray-700 mb-2">Username</label>
                <input type="text" name="username" id="id_username" required
                       class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition">
            </div>
            
            <div>
                <label for="id_password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                <input type="password" name="password" id="id_password" required
                       class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition">
            </div>
            
            {% if form.errors %}
                <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
                    <p class="font-medium">Login failed:</p>
                    {% for field, errors in form.errors.items %}
                        {% for error in errors %}
                            <p class="text-sm">{{ error }}</p>
                        {% endfor %}
                    {% endfor %}
                </div>
            {% endif %}
            
            <button type="submit" 
                    class="w-full bg-primary text-white py-3 px-4 rounded-lg hover:bg-secondary transition font-medium">
                Sign In
            </button>
        </form>
        
        <div class="mt-6 text-center">
            <p class="text-gray-600">
                Don't have an account? 
                <a href="{% url 'register' %}" class="text-primary hover:text-secondary font-medium">Create Account</a>
            </p>
        </div>
    </div>
</div>
{% endblock %}
```

## CSS Styling (books/static/books/style.css)

```css
/* Custom styles for the library management system */
.book-card {
    transition: transform 0.2s;
}

.book-card:hover {
    transform: translateY(-2px);
}

/* Creative library background */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
    min-height: 100vh;
    position: relative;
}

body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(120, 119, 198, 0.2) 0%, transparent 50%);
    pointer-events: none;
    z-index: -1;
}

/* Floating book icons */
.floating-books {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}

.book-icon {
    position: absolute;
    font-size: 2rem;
    color: rgba(255, 255, 255, 0.1);
    animation: float 6s ease-in-out infinite;
}

.book-icon:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
.book-icon:nth-child(2) { top: 20%; right: 10%; animation-delay: 1s; }
.book-icon:nth-child(3) { top: 60%; left: 5%; animation-delay: 2s; }
.book-icon:nth-child(4) { bottom: 20%; right: 15%; animation-delay: 3s; }
.book-icon:nth-child(5) { bottom: 10%; left: 20%; animation-delay: 4s; }

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(5deg); }
}

/* Content overlay */
.content-overlay {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

## Usage Instructions

### 1. Installation
```bash
# Install Django
pip install -r requirements.txt

# Run setup script
python setup.py

# Create admin user
python create_admin.py

# Add more books (optional)
python add_books.py

# Add book images (optional)
python update_book_images.py

# Start server
cd library_project
python manage.py runserver
```

### 2. Access Points
- **Main Site**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login**: http://127.0.0.1:8000/login/
- **Register**: http://127.0.0.1:8000/register/

### 3. Default Credentials
- **Admin**: admin / admin123

### 4. Key Features
- Browse books with cover images
- User registration and authentication
- Add books to cart
- Borrow and return books
- View borrowed books in "My Books"
- Admin interface for management

## Database Schema

### Tables
1. **auth_user** - Django's built-in user model
2. **books_author** - Author information
3. **books_book** - Book catalog with images
4. **books_member** - Library member profiles
5. **books_borrowrecord** - Borrowing history

### Relationships
- Book → Author (Many-to-One)
- Member → User (One-to-One)
- BorrowRecord → Book (Many-to-One)
- BorrowRecord → Member (Many-to-One)

## Security Features
- CSRF protection on all forms
- User authentication required for borrowing
- Session-based authentication
- SQL injection protection via Django ORM

## Future Enhancements
- Email notifications for due dates
- Book reservations
- Fine calculation system
- Advanced search and filtering
- Book recommendations
- Mobile app integration

---

**Created by**: Library Management System
**Version**: 1.0
**Date**: 2024