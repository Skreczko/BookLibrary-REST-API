import json
import requests

"""	CREATING USERS	"""

CREATING_ENDPOINT = 'http://127.0.0.1:8000/api/auth/register/'

headers = {
	'Content-Type': 'application/json'
}

data_user1 = {
	'username': 'TestUser1',
	'email': 'TestUser1@gmail.com',
	'password': 'TestUser1',
	'confirm_password': 'TestUser1',
}

data_user2 = {
	'username': 'TestUser2',
	'email': 'TestUser2@gmail.com',
	'password': 'TestUser2',
	'confirm_password': 'TestUser2',
}

data_user3 = {
	'username': 'TestUser3',
	'email': 'TestUser3@gmail.com',
	'password': 'TestUser3',
	'confirm_password': 'TestUser3',
}

r_user1 = requests.post(CREATING_ENDPOINT, data=json.dumps(data_user1), headers=headers)
r_user2 = requests.post(CREATING_ENDPOINT, data=json.dumps(data_user2), headers=headers)
r_user3 = requests.post(CREATING_ENDPOINT, data=json.dumps(data_user3), headers=headers)


"""	LOGIN AS ADMIN	"""

AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/'

headers = {
	"Content-Type": "application/json",
}

data = {
	'username': 'Admin1',
	'password': 'Admin1',
}

r_admin = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token_admin = r_admin.json()['token']


"""	LOGIN AS NON STAFF USERS	"""

AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/'

headers = {
	"Content-Type": "application/json",
}

data_user1 = {
	'username': 'TestUser1',
	'password': 'TestUser1',
}

data_user2 = {
	'username': 'TestUser2',
	'password': 'TestUser2',
}

data_user3 = {
	'username': 'TestUser3',
	'password': 'TestUser3',
}


r_user1_login = requests.post(AUTH_ENDPOINT, data=json.dumps(data_user1), headers=headers)
r_user2_login = requests.post(AUTH_ENDPOINT, data=json.dumps(data_user2), headers=headers)
r_user3_login = requests.post(AUTH_ENDPOINT, data=json.dumps(data_user3), headers=headers)
token_user1 = r_user1_login.json()['token']
token_user2 = r_user2_login.json()['token']
token_user3 = r_user3_login.json()['token']



""" CREATING BOOKS """

BOOK_ENDPOINT = 'http://127.0.0.1:8000/api/books/'

headers = {
	'Content-Type': 'application/json',
	'Authorization': 'JWT ' + token_admin
}

data_book_1 = {
    "ISBN": 9788365743558,
    "author": "Dmitry Glukhovsky",
    "title": "Tekst",
    "publisher": "Insignis",
    "publishedDate": 2017,
    "description": "",
    "amount": 20
}

data_book_2 = {
    "ISBN": 9780871161956,
    "author": "Philip Martin",
    "title": "The Writer's Guide to Fantasy Literature",
    "publisher": "Writer",
    "publishedDate": 2002,
    "description": "In this helpful resource, over 30 fantasy authors reveal their insider secrets for success. Features detailed overviews on such topics as generating ideas, overcoming writer's block, mastering the genre, marketing your work, and more.",
    "amount": 5
}

data_book_3 = {
    "ISBN": 9780441005901,
    "author": "Frank Herbert",
    "title": "Dune",
    "publisher": "Ace Hardcover",
    "publishedDate": 1999,
    "description": "The new hardcover release of a sci-fi classic follows the adventures of Paul Atreides, the son of a betrayed duke given up for dead on a treacherous desert planet and adopted by its fierce, nomadic people, who help him unravel his most unexpected destiny. Reissue.",
    "amount": 10
}

data_book_4 = {
    "ISBN": 9780316438988,
    "author": "Andrzej Sapkowski",
    "title": "Blood of Elves",
    "publisher": "Orbit",
    "publishedDate": 2018,
    "description": "The New York Times bestselling series that inspired the international hit video game: The Witcher. *Look out for Season of Storms in April 2018*",
    "amount": 8
}

data_book_5 = {
    "ISBN": 9780547928227,
    "author": "J. R. R. Tolkien",
    "title": "The Hobbit, Or, There and Back Again",
    "publisher": "Mariner Books",
    "publishedDate": 2012,
    "description": "Celebrating 75 years of one of the world's most treasured classics with an all new trade paperback edition. Repackaged with new cover art. 500,000 first printing.",
    "amount": 3
}


r_data_book_1 = requests.post(BOOK_ENDPOINT, data=json.dumps(data_book_1), headers=headers)
r_data_book_2 = requests.post(BOOK_ENDPOINT, data=json.dumps(data_book_2), headers=headers)
r_data_book_3 = requests.post(BOOK_ENDPOINT, data=json.dumps(data_book_3), headers=headers)
r_data_book_4 = requests.post(BOOK_ENDPOINT, data=json.dumps(data_book_4), headers=headers)
r_data_book_5 = requests.post(BOOK_ENDPOINT, data=json.dumps(data_book_5), headers=headers)
