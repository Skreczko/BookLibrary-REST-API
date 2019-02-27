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





data_user = {
	'username': 'TestUser1',
	'password': 'Lol123'
}

r_user = requests.post(AUTH_ENDPOINT, data=json.dumps(data_user), headers=headers)
token_user = r_user.json()['token']


headers = {
	'Content-Type': 'application/json',
	'Authorization': 'JWT ' + token_admin
}


BOOK_ENDPOINT = 'http://127.0.0.1:8000/api/auth/user/TestUser1/30/'
answer = requests.get(BOOK_ENDPOINT, headers=headers)
print(answer.text)