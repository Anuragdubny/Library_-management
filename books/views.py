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
        # Ensure member exists
        member, created = Member.objects.get_or_create(
            user=request.user,
            defaults={'phone': '', 'address': ''}
        )
        
        # Create borrow record
        borrow_record = BorrowRecord.objects.create(
            book=book, 
            member=member
        )
        
        # Update book availability
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