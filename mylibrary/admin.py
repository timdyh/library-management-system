from django.contrib import admin
from mylibrary.models import User, Book, Borrow, Log


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'password']


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'publisher', 'is_available']


class BorrowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'borrow_time', 'return_ddl']


class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'time', 'user', 'book', 'action']


admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(Log, LogAdmin)
