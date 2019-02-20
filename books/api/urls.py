from django.urls import path
from .views import BookListAPIView, BookByBarcode,BookDetailAPIView

app_name = 'books'

urlpatterns = [
	path('', BookListAPIView.as_view(), name='book-list'),
	path('detail/<id>/', BookDetailAPIView.as_view(), name='book-detail'),
	path('scan/', BookByBarcode.as_view(), name='book-add-barcode'),

]