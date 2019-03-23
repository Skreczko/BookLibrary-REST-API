from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()

class UserAPITestCase(APITestCase):
	def setUp(self):
		user = User.objects.create(
			username='MEA542142',
			email='MEA542142@gmail.com'
		)
		user.set_password('MEA542142')
		user.save()

	def test_create_user(self):
		qs = User.objects.all().count()
		self.assertEqual(qs,1)

	def test_register_user_success_api(self):
		url = reverse('account:register')
		data = {
			'username'			: 'AUT542142',
			'email'				: 'AUT542142@gmail.com',
			'password'			: 'AUT542142',
			'confirm_password'	: 'AUT542142',
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertGreater(len(response.data['response']['token']), 0)
		registered_user = User.objects.get(username=response.data['response']['user']['username'])
		self.assertEqual(registered_user.is_admin, False)
		self.assertEqual(registered_user.is_staff, False)


	def test_register_user_failed_password_api(self):
		url = reverse('account:register')
		data = {
			'username'			: 'WAU542142',
			'email'				: 'WAU542142@gmail.com',
			'password'			: 'MPR542142',
			'confirm_password'	: 'MPR542142MPR542142MPR542142', #no matching passwords
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_register_user_failed_password2_api(self):
		url = reverse('account:register')
		data = {
			'username'			: 'WWU542142',
			'email'				: 'WWU542142@gmail.com',
			'password'			: 'WWU542142', #without confirming password

		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_register_user_failed_by_authenticated_user_api(self):
		url = reverse('account:register')
		data = {
			'username'			: 'MEA542142',
			'password'			: 'incorect_password',
		}
		user = User.objects.get(username='MEA542142')
		self.client.force_authenticate(user=user)
		response_for_authenticated_user = self.client.post(url, data, format='json')
		self.assertEqual(response_for_authenticated_user.status_code, status.HTTP_403_FORBIDDEN)

	def test_login_user_by_username_success_api(self):
		url = reverse('account:login')
		data = {
			'username'			: 'MEA542142',
			'password'			: 'MEA542142',
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_login_user_by_email_success_api(self):
		url = reverse('account:login')
		data = {
			'username'			: 'MEA542142@gmail.com',
			'password'			: 'MEA542142',
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_login_user_failed_api(self):
		url = reverse('account:login')
		data = {
			'username'			: 'NonExistingUser',
			'password'			: 'NonExistingUser',
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)







