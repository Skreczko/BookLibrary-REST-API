from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth import get_user_model

from books.models import Book, BorrowedBook

User = get_user_model()

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
		return BorrowedBookSerializer(qs, many=True).data


class ConfmirmationSerializer(serializers.Serializer):
	confirm_create_by_barcode = serializers.BooleanField(default=False)

class ConfmirmationUserAddSerializer(serializers.Serializer):
	confirm_user_add_by_barcode = serializers.BooleanField(default=False)


class BorrowedBookSerializer(serializers.ModelSerializer):
	username = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)
	# uri_user = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = BorrowedBook
		fields = [
			# 'uri_user',
			'user',
			'username',
			'book',
			'borrow_date',
			'return_date',
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

	# def get_uri_user(self,obj):
	# 	request = self.context.get('request')
	# 	return reverse('')

class BookListSerializer(serializers.ModelSerializer):
	uri = serializers.SerializerMethodField(read_only=True)
	borrowed_by = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Book
		fields = [
			'id',
			'uri',
			'ISBN',
			'author',
			'title',
			'borrowed_by',
			'amount',
			'book_left',
		]

	def get_uri(self, obj):
		request = self.context.get('request')
		return reverse('api-books:book-detail', kwargs={'id': obj.id}, request=request)

	def get_borrowed_by(self, obj):
		qs = obj.borrowedbook_book.all()
		return BorrowedBookSerializer(qs, many=True).data




