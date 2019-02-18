
from django.conf import settings
from django.utils import timezone

from rest_framework import serializers
from accounts.models import MyUser

expire_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']

class UserSerializer(serializers.ModelSerializer):
	"""
	This class here is needed here (I did not import from account/api/serializers.py,
	because I would like to get jwt_response_payload_handler as token in account/api/serializers.py
	in class UserRegisterSerializer. If I do so, I would import
	from account/api/serializers.py
	to account/api/serializers.py
	to get token - getting error.
	"""
	class Meta:
		model = MyUser
		fields = [
			'id',
			'username',
			'email'
		]

def jwt_response_payload_handler(token, user=None, request=None):
	return {
		'user': UserSerializer(user).data,
		'token': token,
		'expires': timezone.now() + expire_delta
	}