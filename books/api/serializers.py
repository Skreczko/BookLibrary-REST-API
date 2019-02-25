from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth import get_user_model

from books.models import Book, BorrowedBook
import datetime
from django.utils.timesince import timesince

User = get_user_model()

BOOK_EXCEED_PAYMENT = 0.20		#in zloty

class BookSerializer(serializers.ModelSerializer):
	borrowed_by = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Book
		fields = [
			'id',
			'ISBN',
			'author',
			'title',
			'publisher',
			'publishedDate',
			'description',
			'photo',
			'borrowed_by',
			'amount',
			'book_left',
		]

	def get_borrowed_by(self, obj):
		qs = obj.borrowedbook_book.all()
		return BorrowedBook2Serializer(qs, many=True, context=self.context).data


class ConfmirmationSerializer(serializers.Serializer):
	confirm_create_by_barcode = serializers.BooleanField(default=False)

class ConfmirmationUserAddSerializer(serializers.Serializer):
	confirm_user_add_by_barcode = serializers.BooleanField(default=False)




	# def get_uri_user(self,obj):
	# 	request = self.context.get('request')
	# 	return reverse('')

class BookListSerializer(serializers.ModelSerializer):
	uri = serializers.SerializerMethodField(read_only=True)
	# borrowed_by = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Book
		fields = [
			'id',
			'uri',
			'ISBN',
			'author',
			'title',
			# 'borrowed_by',
			'amount',
			'book_left',
		]

	def get_uri(self, obj):
		request = self.context.get('request')
		return reverse('api-books:book-detail', kwargs={'id': obj.id}, request=request)
	#
	# def get_borrowed_by(self, obj):
	# 	qs = obj.borrowedbook_book.all()
	# 	return BorrowedBookSerializer(qs, many=True).data


class UserBookSerializer(serializers.ModelSerializer):
	uri = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Book
		fields = [
			'id',
			'uri',
			'ISBN',
			'author',
			'title',
		]

	def get_uri(self, obj):
		request = self.context.get('request')
		return reverse('api-books:book-detail', kwargs={'id': obj.id}, request=request)

class BorrowedBook2Serializer(serializers.ModelSerializer):
	username = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)
	exceed_payment_in_zloty = serializers.SerializerMethodField(read_only=True)
	exceed_days = serializers.SerializerMethodField(read_only=True)
	uri_user = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = BorrowedBook
		fields = [
			'user',
			'uri_user',
			'username',
			'borrow_date',
			'return_date',
			'exceed_days',
			'exceed_payment_in_zloty',
		]

	def validate(self, data):
		book = data.get('book')
		user = data.get('user')
		if book.book_left == 0:
			return serializers.ValidationError('{}: {} out of stock.'.format(book.title,book.author))
		elif BorrowedBook.objects.filter(user=user, book=book).exists():
			return serializers.ValidationError("{}: {} already exists in {}'s loan list".format(book.title, book.author, user))
		elif BorrowedBook.objects.filter(user=user).count() >= 5:
			return serializers.ValidationError('{} reached limit of loan books.'.format(user))
		return data

	def get_uri_user(self,obj):
		request = self.context.get('request')
		return reverse('account:user-detail', kwargs={'username':obj.user}, request=request)

	def get_exceed_days(self, obj):
		if obj.return_date > datetime.datetime.now().date():
			return 0
		else:
			return (datetime.datetime.now().date() - obj.return_date).days

	def get_exceed_payment_in_zloty(self, obj):
		if obj.return_date > datetime.datetime.now().date():
			return int(0)
		else:
			return float('{0:.2f}'.format((datetime.datetime.now().date() - obj.return_date).days * BOOK_EXCEED_PAYMENT))


class BorrowedBookSerializer(serializers.ModelSerializer):
	book = BookListSerializer(Book, many=False, read_only=True)
	exceed_payment_in_zloty = serializers.SerializerMethodField(read_only=True)
	exceed_days = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = BorrowedBook
		fields = [
			'book',
			'borrow_date',
			'return_date',
			'exceed_days',
			'exceed_payment_in_zloty',
		]

	def validate(self, data):
		book = data.get('book')
		user = data.get('user')
		if book.book_left == 0:
			return serializers.ValidationError('{}: {} out of stock.'.format(book.title,book.author))
		elif BorrowedBook.objects.filter(user=user, book=book).exists():
			return serializers.ValidationError("{}: {} already exists in {}'s loan list".format(book.title, book.author, user))
		elif BorrowedBook.objects.filter(user=user).count() >= 5:
			return serializers.ValidationError('{} reached limit of loan books.'.format(user))
		return data

	def get_exceed_days(self, obj):
		if obj.return_date > datetime.datetime.now().date():
			return 0
		else:
			return (datetime.datetime.now().date() - obj.return_date).days


	def get_exceed_payment_in_zloty(self, obj):
		if obj.return_date > datetime.datetime.now().date():
			return int(0)
		else:
			return float('{0:.2f}'.format((datetime.datetime.now().date() - obj.return_date).days * BOOK_EXCEED_PAYMENT))



class aaaSerializer(serializers.ModelSerializer):
	book = BookListSerializer(Book, many=False, read_only=True)

	class Meta:
		model = BorrowedBook
		fields = [
			'user',
			'book',
			'borrow_date',
			'return_date',

		]