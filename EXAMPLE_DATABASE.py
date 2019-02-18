import json
import requests

"""	LOGIN AS ADMIN	"""

AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/'

headers = {
	"Content-Type": "application/json",
}

data = {
	'username': 'Skreczko',
	'password': 'Lol123',
}

r_admin = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token_admin = r_admin.json()['token']

""" CREATING BOOKS """

BOOK_ENDPOINT = 'http://127.0.0.1:8000/api/books/'