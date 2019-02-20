from rest_framework import generics, mixins, permissions
import requests
from rest_framework.reverse import reverse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer, ConfmirmationSerializer
from books.models import Book
from books.video_barcode import *

class BookListAPIView(generics.ListAPIView):
	permission_classes 		= []
	authentication_classes 	= []
	serializer_class 		= BookSerializer
	queryset 				= Book.objects.all()

class BookDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
	permission_classes 		= []
	authentication_classes 	= []
	serializer_class 		= BookSerializer
	queryset 				= Book.objects.all()
	lookup_field = 'id'

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class BookByBarcode(APIView):
	permission_classes 		= []
	authentication_classes 	= []
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






