from rest_framework import generics, mixins
import requests
from rest_framework.reverse import reverse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer, BookListSerializer, ConfmirmationSerializer, ConfmirmationUserAddSerializer
from books.models import Book, BorrowedBook
from accounts.models import MyUser
from books.video_barcode import *
from accounts.api.permissions import IsStaffOrReadOnly

class BookListAPIView(generics.ListCreateAPIView):
	permission_classes 		= []
	serializer_class 		= None
	queryset 				= Book.objects.all()

	def get_serializer_class(self, *args, **kwargs):
		if self.request.method == 'POST':
			return BookSerializer
		if self.request.method == 'GET':
			return BookListSerializer

	def post(self, request, *args, **kwargs):
		if self.request.user.is_staff:
			return super().post(request, *args, **kwargs)
		else:
			return Response({'detail': 'Authentication credentials were not provided.'},
							status=status.HTTP_403_FORBIDDEN)


class BookDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
	permission_classes 		= [IsStaffOrReadOnly]
	serializer_class 		= None
	queryset 				= Book.objects.all()
	lookup_field 			= 'id'

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return ConfmirmationUserAddSerializer
		else:
			return BookSerializer

	def get_serializer_context(self, *args, **kwargs):
		return {"logged_user": self.request.user, 'request': self.request}

	def assign_book_for_user(self, username, *args, **kwargs):
		if username:
			book_id = self.kwargs.get('id')
			book_obj = Book.objects.get(id=book_id)
			user = MyUser.objects.filter(username=username)
			if user.exists():
				user = user.first()
			else:
				return Response(
					{'error_message': '{} does not exists in database'.format(username)},
					status=status.HTTP_400_BAD_REQUEST)
			if Book.objects.get(id=book_id).book_left == 0:
				return Response({'error_message': '{}: {} out of stock.'.format(book_obj.title, book_obj.author)},
								status=status.HTTP_400_BAD_REQUEST)
			elif BorrowedBook.objects.filter(user=user.id, book=book_obj).exists():
				return Response({'error_message': "{}: {} already exists in {}'s loan list".format(book_obj.title,
																								   book_obj.author,
																								   user)},
								status=status.HTTP_400_BAD_REQUEST)
			elif BorrowedBook.objects.filter(user=user.id).count() >= 5:
				return Response({'error_message': '{} reached limit of loan books.'.format(user)},
								status=status.HTTP_400_BAD_REQUEST)
			else:
				BorrowedBook.objects.create(user=user, book=book_obj).save()
				return Response({'message': "{} has been added successfully to {}'s loan list".format(user,
																									  book_obj.title)},
								status=status.HTTP_201_CREATED)

	def post(self, request, *args, **kwargs):
		serializer = ConfmirmationUserAddSerializer(data=request.data)
		if serializer.is_valid():
			if serializer.data.get('confirm_user_add_by_barcode') == True:
				return self.assign_book_for_user(username=capture_user_barcode())

			elif serializer.data.get('users_in_database'):
				return self.assign_book_for_user(username=serializer.data.get('users_in_database'))

			return Response({'message': 'Confirm adding user by barcode or choose user from choice field'},
								status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class BookByBarcode(APIView):
	permission_classes 		= [IsStaffOrReadOnly]
	serializer_class 		= ConfmirmationSerializer
	queryset 				= Book.objects.all()

	def post(self, request, *args, **kwargs):
		serializer = ConfmirmationSerializer(data=request.data)
		if serializer.is_valid():
			if serializer.data.get('confirm_create_by_barcode') == True:
				number = capture_barcode()
				if number:
					headers = {
						"Content-Type": "application/json",
					}
					ENDPOINT = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(number)
					serializer = requests.get(ENDPOINT, headers=headers)
					try:
						ISBN1 = serializer.json()['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier']
						ISBN2 = serializer.json()['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
						if ISBN1[:2] == '97':
							ISBN = ISBN1
						else:
							ISBN = ISBN2
						author = serializer.json()['items'][0]['volumeInfo']['authors'][0] or None
						title = serializer.json()['items'][0]['volumeInfo']['title'] or None
						publisher = serializer.json()['items'][0]['volumeInfo']['publisher'] or None
						publishedDate = serializer.json()['items'][0]['volumeInfo']['publishedDate'] or None
						if len(publishedDate)>4:
							publishedDate = publishedDate[:4]
						if Book.objects.filter(ISBN=ISBN).exists():
							return Response({'detail': [
								{'message': 'This book already exists in database.'},
							]}, status=status.HTTP_400_BAD_REQUEST)
						else:
							current_book=Book.objects.create(
								ISBN=ISBN,
								author=author,
								title=title,
								publisher=publisher,
								publishedDate=publishedDate,
							)
							current_book.save()
							return redirect(reverse('books:book-detail', kwargs={'id': current_book.id}))
					except:
						return Response(
							{'message': 'This book does not exists in google database. Please add book manually.'},
							status=status.HTTP_404_NOT_FOUND)
			else:
				return Response({'message': 'New book will not be added'},
							status=status.HTTP_200_OK)

	def get(self, request, *args, **kwargs):
		number = capture_barcode()
		if number:
			headers = {
			    "Content-Type": "application/json",
			}
			ENDPOINT = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(number)
			serializer = requests.get(ENDPOINT, headers=headers)
			try:
				ISBN1 = serializer.json()['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier']
				ISBN2 = serializer.json()['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
				if ISBN1[:2] == '97':
					ISBN = ISBN1
				else:
					ISBN = ISBN2
				if Book.objects.filter(ISBN=ISBN).exists():
					obj = Book.objects.get(ISBN=ISBN)
					return redirect(reverse('books:book-detail', kwargs={'id':obj.id}))
				else:

					return Response({'message': 'This book does not exists in database. Please confirm creating book.'},
										status=status.HTTP_400_BAD_REQUEST)
			except:
				return Response({'message': 'This book does not exists in google database. Please add book manually.'},
								status=status.HTTP_404_NOT_FOUND)