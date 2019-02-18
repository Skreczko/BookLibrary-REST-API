from django.urls import path
from .views import BookListAPIView, BookAddByBarcode

app_name = 'books'

urlpatterns = [
	path('', BookListAPIView.as_view(), name='book-list'),
	path('scan/', BookAddByBarcode.as_view(), name='book-add-barcode'),

]