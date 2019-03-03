from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Book, BorrowedBook, BorrowedBookHistory
# Register your models here.

class BookAdmin(admin.ModelAdmin):

	list_display = ['id','ISBN','title', 'author', 'publisher', 'amount', 'book_left']
	search_fields = ['ISBN']
	list_per_page = 50

	class Meta:
		model = Book


class BorrowedBookAdmin(admin.ModelAdmin):
	list_display = ['user', 'book', 'borrow_date', 'return_date',]
	list_per_page = 50
	search_fields = ['user__username', 'book__title', 'book__ISBN',]
	readonly_fields = ['borrow_date',]

	class Meta:
		model = BorrowedBook

class BorrowedBookHistoryAdmin(admin.ModelAdmin):
	list_display = ['user', 'book', 'borrow_date', 'return_date',]
	list_per_page = 50
	search_fields = ['user__username', 'book__title', 'book__ISBN', ]
	readonly_fields = ['user', 'book', 'borrow_date', 'return_date',]

	class Meta:
		model = BorrowedBookHistory


admin.site.register(Book, BookAdmin)
admin.site.register(BorrowedBook, BorrowedBookAdmin)
admin.site.register(BorrowedBookHistory, BorrowedBookHistoryAdmin)
