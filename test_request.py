import requests

session = requests.Session()

# initial GET request
response0 = session.get('http://localhost:8000')

csrf_token = response0.cookies['csrftoken']

username = 'serge'
password = '123'

post_data = {'csrfmiddlewaretoken' : csrf_token, 'username': username, 'password' : password}

# sign in POST request
response1 = session.post('http://localhost:8000/signin', data=post_data)
print(response1.content)


response0 = session.get('http://localhost:8000')

csrf_token = response0.cookies['csrftoken']

data = '69'

post_data = {'csrfmiddlewaretoken' : csrf_token, 'data' : data}

# sensor POST request
response2 = session.post('http://localhost:8000/sensor', data=post_data)

print()
print(response2.content)
