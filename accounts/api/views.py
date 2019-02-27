from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.reverse import reverse
from rest_framework import status

from .serializers import UserLoginSerializer, UserRegisterSerializer,\
	UserListSerializer, UserDetailSerializer, ConfmirmationSerializer
from accounts.models import MyUser
from books.video_barcode import *
from books.models import BorrowedBook, Book, BorrowedBookHistory
from books.api.serializers import BorrowedBookSerializer, BorrowedBookHistorySerializer


from .permissions import IsAnonymous, IsStaffUser, IsStaffOrOwner, IsStaffObjectPermission,\
	IsStaffCRUDPermission
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
				return Response({'detail': 'Invalid credential'}, status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response({'detail': 'Invalid credential'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterAPIView(generics.CreateAPIView):
	permission_classes 		= [IsAnonymous]
	serializer_class 		= UserRegisterSerializer
	queryset 				= User.objects.all()


class UserListAPIView(generics.ListAPIView):
	# permission_classes 		= [IsStaffUser]
	# authentication_classes 	= []
	serializer_class 		= UserListSerializer
	queryset 				= MyUser.objects.all()

	def get_queryset(self, *args, **kwargs):
		if self.request.user.is_staff:
			return MyUser.objects.all()
		return MyUser.objects.filter(username=self.request.user)


class UserDetailAPIView(APIView):
	permission_classes 		= [IsStaffCRUDPermission]
	# authentication_classes 	= []
	serializer_class 		= ConfmirmationSerializer
	queryset 				= MyUser.objects.all()

	def get_queryset(self, *args, **kwargs):
		user_from_token = MyUser.objects.filter(username=self.request.user)
		user_from_url = MyUser.objects.filter(username=self.kwargs.get('username'))
		if user_from_token.first() == user_from_url.first():
			return user_from_url
		elif user_from_token.first().is_staff:
			return user_from_url
		else:
			return MyUser.objects.none()

	def post(self, request, format=None, **kwargs):
		serializer = ConfmirmationSerializer(data=request.data)
		if serializer.is_valid():
			if serializer.data.get('confirm_adding_book_by_barcode') == True:
				number = capture_barcode()
				if number:
					user = MyUser.objects.get(username=self.kwargs.get('username'))
					if Book.objects.filter(ISBN=int(number)).exists():
						book = Book.objects.get(ISBN=int(number))
					else:
						return Response({'error_message': "{} does not exists in database".format(number)},
										status=status.HTTP_400_BAD_REQUEST)
					if BorrowedBook.objects.filter(user=user, book=book).exists():
						return Response({'error_message': "{}: {} already exists in {}'s loan list".format(book.title, book.author, user)},
										status=status.HTTP_400_BAD_REQUEST)
					elif book.book_left == 0:
						return Response(
							{'error_message': '{}: {} out of stock.'.format(book.title, book.author)},
							status=status.HTTP_400_BAD_REQUEST)
					else:
						BorrowedBook.objects.create(user=user,book=book,).save()
						return redirect(reverse('account:user-detail', kwargs={'username': self.kwargs.get('username')}))
			return Response({'message': 'New book will not be added'}, status=status.HTTP_200_OK)


	def get(self, request, *args, **kwargs):
		if self.get_queryset():
			serializer = UserDetailSerializer(self.get_queryset(), many=True, context={'request': request})
			return Response(serializer.data)
		return Response({'detail': 'Invalid Authorization header. No credentials provided.'},
						status=status.HTTP_401_UNAUTHORIZED)



class UserBorrowedBookAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin,generics.RetrieveAPIView):
	permission_classes 		= [IsStaffObjectPermission]
	# authentication_classes 	= []
	queryset 				= BorrowedBook.objects.all()
	serializer_class		= BorrowedBookSerializer
	lookup_field 			= 'id'

	def get_queryset(self, *args, **kwargs):
		user_from_token = MyUser.objects.filter(username=self.request.user).first()
		user_from_url = MyUser.objects.filter(username=self.kwargs.get('username')).first()
		if user_from_token == user_from_url or user_from_token.is_staff:
			return BorrowedBook.objects.filter(user=user_from_url)
		return BorrowedBook.objects.none()

	def get(self, request, *args, **kwargs):
		if self.get_queryset():
			return super().get(request, *args, **kwargs)
		return Response({'detail': 'Invalid Authorization header. No credentials provided.'},
						status=status.HTTP_401_UNAUTHORIZED)

	def put(self, request, *args, **kwargs):
		if self.get_queryset():
			return super().update(request, *args, **kwargs)
		return Response({'detail': 'Invalid Authorization header. No credentials provided.'},
						status=status.HTTP_401_UNAUTHORIZED)

	def delete(self, request, *args, **kwargs):
		instance = self.get_object()
		BorrowedBookHistory.objects.create(
			user=instance.user,
			book=instance.book,
			borrow_date=instance.borrow_date,
			return_date=instance.return_date
		).save()
		return self.destroy(request, *args, **kwargs)


class UserBorrowedBookHistoryAPIView(generics.ListAPIView):
	permission_classes 		= [IsStaffObjectPermission]
	# authentication_classes 	= []
	queryset 				= BorrowedBookHistory.objects.all()
	serializer_class		= BorrowedBookHistorySerializer
	lookup_field 			= 'id'

	def get_queryset(self):
		user_from_token = MyUser.objects.filter(username=self.request.user).first()
		user_from_url = MyUser.objects.filter(username=self.kwargs.get('username')).first()
		if user_from_token == user_from_url or user_from_token.is_staff:
			return BorrowedBookHistory.objects.filter(user=user_from_url)
		return BorrowedBookHistory.objects.none()

	def get(self, request, *args, **kwargs):
		if self.get_queryset():
			return super().get(request, *args, **kwargs)
		return Response({'detail': 'Invalid Authorization header. No credentials provided.'},
						status=status.HTTP_401_UNAUTHORIZED)