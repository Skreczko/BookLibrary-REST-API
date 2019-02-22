from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from datetime import datetime

from datetime import datetime
from datetime import timedelta

DATE_FIELD = ((x,x) for x in range(1900, (datetime.now().year+1)))

class Book(models.Model):
	def upload_path(instance, filename):
		extension = filename.split('.')[-1]
		filename = "{}{}.{}".format(instance.ISBN,instance.title,extension)
		return filename

	ISBN 			= models.SmallIntegerField(unique=True)
	author 			= models.CharField(max_length=128)
	title 			= models.CharField(max_length=124)
	amount			= models.PositiveSmallIntegerField(default=1)
	photo 			= models.ImageField(null=True, blank=True, upload_to=upload_path)
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

	@property
	def return_date(self):
		r_date = datetime.now().date() + timedelta(days=7)
		return r_date





