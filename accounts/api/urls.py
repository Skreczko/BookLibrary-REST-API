from django.conf.urls import url, include
from django.urls import path

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token # accounts app

from .views import AuthAPIView, RegisterAPIView, UserListAPIView, UserDetailAPIView, UserDetailScanAPIView

app_name = 'account'

urlpatterns = [
    path('', AuthAPIView.as_view(), name='login'),  # http://127.0.0.1:8000/api/auth/
    path('register/', RegisterAPIView.as_view(), name='register'), # http://127.0.0.1:8000/api/auth/register/
    path('jwt/', obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),

    path('user/', UserListAPIView.as_view(), name='user-list'),
    path('user/<username>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('user/<username>/scan/', UserDetailScanAPIView.as_view(), name='user-detail-scan'),

]