from django.urls import path
from .views import BookAddByBarcode

app_name = 'books'

urlpatterns = [
	path('scan/', BookAddByBarcode.as_view(), name='book-list'),

]