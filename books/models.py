from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta

DATE_FIELD = ((x,x) for x in range(1900, (datetime.now().year+1)))

class Book(models.Model):
	ISBN 			= models.SmallIntegerField(unique=True)
	author 			= models.CharField(max_length=128)
	title 			= models.CharField(max_length=124)
	amount			= models.PositiveSmallIntegerField(default=1)
	publisher 		= models.CharField(max_length=128, null=True, blank=True)
	publishedDate 	= models.PositiveSmallIntegerField(null=True, blank=True, choices=DATE_FIELD)
	description 	= models.CharField(max_length=1024, null=True, blank=True)

	def __str__(self):
		return str("{}: {}\tISBN:{}".format(self.author, self.title, self.ISBN))

	@property
	def book_left(self):
		count = BorrowedBook.objects.filter(book=self).count()
		return self.amount - count


class BorrowedBook(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrowedbook_user')
	book			= models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowedbook_book')
	borrow_date		= models.DateField(auto_now_add=True)
	return_date		= models.DateField(default=(datetime.now().date() + timedelta(days=7)) ,help_text='If none: default for 7 days')


class BorrowedBookHistory(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrowedbook_user_history')
	book			= models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowedbook_book_history')
	borrow_date		= models.DateField()
	return_date		= models.DateField()
