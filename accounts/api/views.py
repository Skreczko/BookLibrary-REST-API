from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserRegisterSerializer,\
	UserSerializer, UserListSerializer, UserDetailSerializer, ConfmirmationSerializer
from accounts.models import MyUser


from .permissions import IsAnonymous, IsStaffUser
# from .serializers import UserRegisterSerializer
from rest_framework_jwt.settings import api_settings

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()

class AuthAPIView(APIView):
	permission_classes 		= [IsAnonymous]
	authentication_classes 	= []
	serializer_class 		= UserLoginSerializer

	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return Response({'detail': 'You are already logged'}, status=400)
		data = request.data
		username = data.get('username')
		password = data.get('password')
		qs = User.objects.filter(
			Q(username__iexact=username) |
			Q(email__iexact=username)
		).distinct()
		if qs.count() == 1:
			user = qs.first()
			if user.check_password(password):
				payload = jwt_payload_handler(user)
				token = jwt_encode_handler(payload)
				my_payload = jwt_response_payload_handler(token, user, request=request)
				print(payload,"\n\n\n\n",token,"\n\n\n\n",my_payload)
				return Response(my_payload)
			else:
				return Response({'detail': 'Invalid credential'}, status=401)
		else:
			return Response({'detail': 'Invalid credential'}, status=401)



class RegisterAPIView(generics.CreateAPIView):
	permission_classes 		= [IsAnonymous]
	serializer_class 		= UserRegisterSerializer
	queryset 				= User.objects.all()


class UserListAPIView(generics.ListAPIView):
	permission_classes 		= []
	authentication_classes 	= []
	serializer_class 		= UserListSerializer
	queryset 				= MyUser.objects.all()



class UserDetailAPIView(APIView):
	permission_classes 		= []
	authentication_classes 	= []

	def get_serializer_class(self):
		if self.request.method == 'GET':
			return UserDetailSerializer
		else:
			return ConfmirmationSerializer

	def post(self, request, format=None):
		serializer = self.get_serializer_class()(data=request.data)
		print(serializer.data)
		if serializer.is_valid():
			return Response({'detail': [
								{'message': 'This book already exists in database.'},
							]})
	def get_queryset(self):
		return MyUser.objects.filter(username=self.kwargs.get('username'))


	def get(self, request, *args, **kwargs):
		serializer = self.get_serializer_class()(self.get_queryset(), many=True)
		return Response(serializer.data)








from books.models import BorrowedBook
from books.api.serializers import aaaSerializer

class UserDetailScanAPIView(generics.ListAPIView):
	permission_classes 		= []
	authentication_classes 	= []
	serializer_class 		= aaaSerializer
	queryset 				= BorrowedBook.objects.all()








