from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from accounts.models import MyUser
from django.contrib.auth import get_user_model

from books.models import Book

User = get_user_model()

class BookSerializer(serializers.ModelSerializer):

	class Meta:
		model = Book
		fields = [
			'id',
			'ISBN',
			'author',
			'title',
			'amount',
			'publisher',
			'publishedDate',
			'description',
			'photo',
		]
class ConfmirmationSerializer(serializers.Serializer):
	confirm_create_by_barcode = serializers.BooleanField(default=False)


