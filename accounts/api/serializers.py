import datetime
from rest_framework.reverse import reverse
from rest_framework import serializers
from accounts.models import MyUser
from books.api.serializers import BOOK_EXCEED_PAYMENT, BorrowedBookSerializer

from rest_framework_jwt.settings import api_settings

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = MyUser
		fields = [
			'id',
			'username',
			'email'
		]


class UserListSerializer(serializers.ModelSerializer):
	uri = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = MyUser
		fields = [
			'id',
			'uri',
			'username',
			'email'
		]

	def get_uri(self,obj):
		request = self.context.get('request')
		return reverse('account:user-detail', kwargs={'username': obj.username}, request=request)


class UserDetailSerializer(serializers.ModelSerializer):
	books = serializers.SerializerMethodField(read_only=True)
	total_exceeded_payment = serializers.SerializerMethodField(read_only=True)
	borrowing_history = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = MyUser
		fields = [
			'id',
			'username',
			'email',
			'books',
			'total_exceeded_payment',
			'borrowing_history',
		]

	def get_books(self, obj):
		request = self.context.get('request')
		qs = obj.borrowedbook_user.all()
		return BorrowedBookSerializer(qs, many=True, context={'request': request}).data

	def get_total_exceeded_payment(self, obj):
		qs = obj.borrowedbook_user.all()
		total_payment = 0
		for item in qs:
			if item.return_date < datetime.datetime.now().date():
				total_payment += float('{0:.2f}'.format((datetime.datetime.now().date() - item.return_date).days * BOOK_EXCEED_PAYMENT))
		return float('{0:.2f}'.format(total_payment))

	def get_borrowing_history(self, obj):
		request = self.context.get('request')
		return reverse('account:user-list-history', kwargs={'username':obj.username}, request=request)


class ConfmirmationSerializer(serializers.Serializer):
	confirm_adding_book_by_barcode = serializers.BooleanField(default=False)


class UserBookExtensionBookSerializer(serializers.Serializer):
	book_id= serializers.IntegerField()


class UserLoginSerializer(serializers.ModelSerializer):
	password 	= serializers.CharField(style={'input_type': 'password'}, write_only=True)
	class Meta:
		model = MyUser
		fields = [
			'username',
			'password',
		]


class UserRegisterSerializer(serializers.ModelSerializer):
	password 	= serializers.CharField(style={'input_type': 'password'}, write_only=True)
	confirm_password 	= serializers.CharField(style={'input_type': 'password'}, write_only=True)
	response = serializers.SerializerMethodField(read_only=True)
	message = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = MyUser
		fields = [
			'username',
			'email',
			'response',
			'password',
			'confirm_password',
			'message'
		]
		extra_kwargs = ({
			'username': {'write_only': True},
			 'email': {'write_only': True},

		})

	def get_response(self, obj):
		user = obj
		payload = jwt_payload_handler(user)
		token = jwt_encode_handler(payload)
		response = jwt_response_payload_handler(token, user=obj, request=None)
		return response

	def get_message(self,obj):
		return 'Now you can log in.'

	def validate_username(self, value):
		if MyUser.objects.filter(username__iexact=value).exists():
			raise serializers.ValidationError('User with this index number exists.')
		return value

	def validate_email(self, value):
		if MyUser.objects.filter(email__iexact=value).exists():
			raise serializers.ValidationError('User with this email exists.')
		return value

	def validate(self, data):
		password = data.get('password')
		confirm_password = data.pop('confirm_password')
		if password != confirm_password:
			raise serializers.ValidationError('Passwords must match.')
		return data

	def create(self, validated_data):
		username = validated_data.get('username')
		email = validated_data.get('email')
		password = validated_data.get('password')
		user = MyUser.objects.create(
			username = username,
			email = email,
		)
		user.set_password(password)
		user.is_staff = False
		user.save()
		return user