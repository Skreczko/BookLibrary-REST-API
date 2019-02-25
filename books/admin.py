from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Book, BorrowedBook
# Register your models here.

class BookAdmin(admin.ModelAdmin):

	list_display = ['id','ISBN','title', 'author', 'publisher', 'is_photo',  'amount', 'book_left']
	search_fields = ['ISBN']
	readonly_fields = ['show_photo']
	list_per_page = 50

	class Meta:
		model = Book

	def is_photo(self, obj):
		if obj.photo:
			return True
		else:
			return False
	is_photo.boolean = True

	def show_photo(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url=obj.photo.url,
			width=120,
			height=240,))


class BorrowedBookAdmin(admin.ModelAdmin):
	list_display = ['user', 'book', 'borrow_date', 'return_date',]
	list_per_page = 50
	readonly_fields = ['borrow_date',]

	class Meta:
		model = BorrowedBook


admin.site.register(Book, BookAdmin)
admin.site.register(BorrowedBook, BorrowedBookAdmin)
