import requests

session = requests.Session()

# initial GET request
response0 = session.get('http://localhost:8000')

username = 'serge'
password = '123'

post_data = {'username': username, 'password' : password}

# sign in POST request
response1 = session.post('http://localhost:8000/signin', data=post_data)
print(response1.content)

data = '56'

post_data = {'data' : data}

# sensor POST request
response2 = session.post('http://localhost:8000/sensor', data=post_data)

print()
print(response2.content)
