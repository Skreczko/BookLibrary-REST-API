from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from books.models import Book, BorrowedBook

from django.contrib.auth import get_user_model

User = get_user_model()

class BookAPITestCase(APITestCase):

	def setUp(self):
		"""CREATING USERS"""
		staff_user = User.objects.create(
			username = 'Admin1',
			email = 'Admin1@gmail.com',
			is_staff = True
			)
		staff_user.set_password('Admin1')
		staff_user.save()

		test_user1 = User.objects.create(
			username='test_user1',
			email='test_user1@gmail.com',
			)
		test_user1.set_password('test_user1')
		test_user1.save()

		test_user2 = User.objects.create(
			username='test_user2',
			email='test_user2@gmail.com',
			)
		test_user2.set_password('test_user2')
		test_user2.save()

		"""CREATING BOOK"""
		Book.objects.create(
			ISBN = 9780316438988,
			author = "Andrzej Sapkowski",
			title = "Blood of Elves",
			publisher = "Orbit",
			publishedDate = 2018,
			description = "The New York Times bestselling series that inspired the international hit video "
						   "game: The Witcher. *Look out for Season of Storms in April 2018*",
			amount = 20,
		).save()

	def login_user(self, type_of_user=None):
		if type_of_user == 'Admin':
			data_login = {
				'username' : 'Admin1',
				'password' : 'Admin1'
			}
		elif type_of_user == 'User1':
			data_login = {
				'username' : 'test_user1',
				'password' : 'test_user1',
				}
		elif type_of_user == 'User2':
			data_login = {
				'username' : 'test_user2',
				'password' : 'test_user2',
				}
		url_login = reverse('account:login')
		response = self.client.post(url_login, data_login, format='json')
		token = response.data.get('token')
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

	"""..................BOOK SECTION.................."""

	def test_create_book(self):
		self.login_user(type_of_user='Admin')
		data_book = {
			"ISBN": 9780316438988,
			"author": "Andrzej Sapkowski",
			"title": "Blood of Elves",
			"publisher": "Orbit",
			"publishedDate": 2018,
			"description": "The New York Times bestselling series that inspired the international hit video "
						   "game: The Witcher. *Look out for Season of Storms in April 2018*",
			"amount": 20,
			}


		url_adding_book = reverse('books:book-list')
		response = self.client.put(url_adding_book, data_book, format='json')
		self.assertEqual(Book.objects.all().count(), 1)
		self.assertEqual(Book.objects.filter(ISBN=9780316438988).exists(), True)

	def test_create_book_by_annonymous_user(self):
		data_book = {
			"ISBN": 9780441005901,
			"author": "Frank Herbert",
			"title": "Dune",
			"publisher": "Ace Hardcover",
			"publishedDate": 1999,
			"description": "The new hardcover release of a sci-fi classic follows the adventures of Paul Atreides,"
						   " the son of a betrayed duke given up for dead on a treacherous desert planet and adopted "
						   "by its fierce, nomadic people, who help him unravel his most unexpected destiny. Reissue.",
			"amount": 5,
		}
		url_adding_book = reverse('books:book-list')
		response = self.client.put(url_adding_book, data_book, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_create_book_by_non_staff_user(self):
		self.login_user('User1')
		data_book = {
			"ISBN": 9780441005901,
			"author": "Frank Herbert",
			"title": "Dune",
			"publisher": "Ace Hardcover",
			"publishedDate": 1999,
			"description": "The new hardcover release of a sci-fi classic follows the adventures of Paul Atreides,"
						   " the son of a betrayed duke given up for dead on a treacherous desert planet and adopted "
						   "by its fierce, nomadic people, who help him unravel his most unexpected destiny. Reissue.",
			"amount": 5,
		}
		url_adding_book = reverse('books:book-list')
		response = self.client.put(url_adding_book, data_book, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_get_book_list_by_annonymous_user(self):
		response = self.client.get(reverse('books:book-list'), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('results')[0]['ISBN'], 9780316438988)

	def borrow_book(self, user=None):
		self.login_user('Admin')
		book = Book.objects.all().first()
		data = {
			"users_in_database": "{}".format(user)
		}
		book_url = reverse('books:book-detail', kwargs={'id': book.id})
		self.client.post(book_url, data, format='json')

	def test_borrowing_book_by_staff_user_from_book_section(self):
		self.login_user('Admin')
		book = Book.objects.all().first()
		data = {
			"users_in_database": "test_user1"
		}
		book_url = reverse('books:book-detail', kwargs={'id': book.id})

		response = self.client.post(book_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data.get('message'), "test_user1 has been added successfully to Blood of Elves's loan list")

		response2 = self.client.post(book_url, data, format='json')
		self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response2.data.get('error_message'),
						 "Blood of Elves: Andrzej Sapkowski already exists in test_user1's loan list")


	def test_get_book_detail_by_annonymous_user(self):
		book = Book.objects.all().first()
		response = self.client.get(reverse('books:book-detail', kwargs={'id':book.id}), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('ISBN'), 9780316438988)
		self.assertEqual(response.data.get('borrowed_by')['detail'], 'Authentication credentials were not provided.')

	def test_get_book_detail_by_staff_user(self):
		self.login_user('Admin')
		self.borrow_book('test_user1')
		book = Book.objects.all().first()
		response = self.client.get(reverse('books:book-detail', kwargs={'id':book.id}), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('ISBN'), 9780316438988)
		self.assertEqual(response.data.get('borrowed_by')[0]['username'], 'test_user1')
		self.assertEqual(response.data.get('book_left'), 19)

	def test_get_book_detail_by_test_user1(self):
		self.borrow_book('test_user1')
		self.client.credentials()
		self.login_user('User1')
		book = Book.objects.all().first()
		response = self.client.get(reverse('books:book-detail', kwargs={'id':book.id}), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('ISBN'), 9780316438988)
		self.assertEqual(response.data.get('borrowed_by')[0]['username'], 'test_user1') #user borrowed this book

	def test_get_book_detail_by_test_user2(self):
		self.borrow_book('test_user1')
		self.client.credentials()
		self.login_user('User2')
		book = Book.objects.all().first()
		response = self.client.get(reverse('books:book-detail', kwargs={'id':book.id}), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('ISBN'), 9780316438988)
		self.assertEqual(response.data.get('borrowed_by'), []) #returns empty list of users

	def test_change_book_detail_as_staff(self):
		self.login_user('Admin')
		data = {
			"ISBN": 9780316438988,
			"author": "ANNONYMOUS AUTHOR",
			"title": "Blood of Elves",
			"publisher": "Orbit",
			"publishedDate": 2018,
		}
		book = Book.objects.all().first()
		response = self.client.put(reverse('books:book-detail', kwargs={'id': book.id}), data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('author'), 'ANNONYMOUS AUTHOR')

	def test_change_book_detail_as_user(self):
		self.login_user('User1')
		data = {
			"ISBN": 9780316438988,
			"author": "ANNONYMOUS AUTHOR",
			"title": "Blood of Elves",
			"publisher": "Orbit",
			"publishedDate": 2018,
		}
		book = Book.objects.all().first()
		response = self.client.put(reverse('books:book-detail', kwargs={'id': book.id}), data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	"""..................USER SECTION.................."""


	def test_get_user_list_as_staff(self):
		self.login_user('Admin')
		response = self.client.get(reverse('account:user-list'), format='json')
		self.assertEqual(len(response.data.get('results')), 3)
		self.assertEqual(response.data.get('results')[0]['username'], 'Admin1')
		self.assertEqual(response.data.get('results')[1]['username'], 'test_user1')
		self.assertEqual(response.data.get('results')[2]['username'], 'test_user2')

	def test_get_user_list_as_non_staff(self):
		self.login_user('User1')
		response = self.client.get(reverse('account:user-list'), format='json')
		self.assertEqual(len(response.data.get('results')), 1)
		self.assertEqual(response.data.get('results')[0]['username'], 'test_user1')

	def test_get_user_list_as_annonymous(self):
		response = self.client.get(reverse('account:user-list'), format='json')
		self.assertEqual(len(response.data.get('results')), 0)

	def test_get_user_detail_as_admin(self):
		self.borrow_book('test_user1')
		self.client.credentials()
		self.login_user("Admin")
		response = self.client.get(reverse('account:user-detail', kwargs={
			'username': 'test_user1'
		}), format='json')
		self.assertEqual((response.data)[0].get('username'), 'test_user1')

	def test_get_user_detail_as_anonymous(self):
		self.borrow_book('test_user1')
		self.client.credentials()
		response = self.client.get(reverse('account:user-detail', kwargs={
			'username': 'test_user1'
		}), format='json')
		self.assertEqual(response.data.get('results'), None)

	def test_get_user_detail_as_other_user(self):
		self.borrow_book('test_user2')
		self.client.credentials()
		response = self.client.get(reverse('account:user-detail', kwargs={
			'username': 'test_user1'
		}), format='json')
		self.assertEqual(response.data.get('results'), None)

	def test_user_detail_adding_book_as_admin(self):
		data_book = {
			"confirm_adding_book_by_barcode": False,
			"ISBN_number": 9780316438988,
		}
		self.login_user('Admin')
		url_add_book = reverse('account:user-detail', kwargs={
			'username': 'test_user1'})
		response_post = self.client.post(url_add_book, data_book, format='json')
		response_get = self.client.get(url_add_book, format='json')
		self.assertEqual(response_get.data[0]['books'][0]['book']['ISBN'], 9780316438988)

	def test_user_detail_adding_book_as_user(self):
		data_book = {
			"confirm_adding_book_by_barcode": False,
			"ISBN_number": 9780316438988,
		}
		self.login_user('User1')
		url_add_book = reverse('account:user-detail', kwargs={
			'username': 'test_user1'})
		response_post = self.client.post(url_add_book, data_book, format='json')
		self.assertEqual(response_post.status_code, status.HTTP_403_FORBIDDEN)



