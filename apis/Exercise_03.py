'''
Write the necessary code to make a POST request to:

    http://demo.codingnomads.co:8080/tasks_api/users

and create a user with your information.

Make a GET request to confirm that your user information has been saved.

'''

import requests

body = {'first_name': 'Me', 'last_name': 'Mine', 'email': 'myemail@email.com'}

response = requests.post('http://demo.codingnomads.co:8080/tasks_api/users', json=body)

print(response.status_code)

response = requests.get('http://demo.codingnomads.co:8080/tasks_api/users')
data = response.json()

print(response.status_code)
print(data['data'][-1])
