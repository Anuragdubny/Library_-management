from django.contrib import admin
from .models import Author, Book, Member, BorrowRecord

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'available']
    list_filter = ['available', 'author']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'borrow_date', 'return_date', 'is_returned']
    list_filter = ['borrow_date', 'return_date', 'book__author']
    search_fields = ['book__title', 'member__user__username']
    readonly_fields = ['borrow_date']
    
    def is_returned(self, obj):
        return obj.return_date is not None
    is_returned.boolean = True
    is_returned.short_description = 'Returned'