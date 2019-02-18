from rest_framework import generics, mixins, permissions
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer
from books.models import Book
from books.video_barcode import *

class rwrw(generics.ListCreateAPIView):
	permission_classes 		= []
	authentication_classes 	= []
	serializer_class 		= BookSerializer
	queryset 				= Book.objects.all()




class BookAddByBarcode(APIView):
	permission_classes 		= []
	authentication_classes 	= []
	serializer_class 		= BookSerializer
	queryset 				= Book.objects.all()


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

			author = serializer.json()['items'][0]['volumeInfo']['authors'][0] or None
			title = serializer.json()['items'][0]['volumeInfo']['title'] or None
			publisher = serializer.json()['items'][0]['volumeInfo']['publisher'] or None
			publishedDate = serializer.json()['items'][0]['volumeInfo']['publishedDate'] or None
			if len(publishedDate)>4:
				publishedDate = publishedDate[:4]

			if Book.objects.filter(ISBN=ISBN).exists():
				return Response({'detail': [
					{'message': 'This book already exists in database.'},
				]}, status=400)
			else:
				Book.objects.create(
					ISBN=ISBN,
					author=author,
					title=title,
					publisher=publisher,
					publishedDate=publishedDate,
				).save()

				return Response({'detail':[
					{'ISBN':'{}'.format(ISBN)},
					{'Author': '{}'.format(author)},
					{'title': '{}'.format(title)},
					{'publisher': '{}'.format(publisher)},
					{'publishedDate': '{}'.format(publishedDate)},
					{'message': 'Please update the quantity on the stock of this book'},
								 ]}, status=201)



