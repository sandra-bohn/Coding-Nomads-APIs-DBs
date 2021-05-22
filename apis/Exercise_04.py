'''
Write a program that makes a PUT request to update your user information to a new first_name, last_name and email.

Again make a GET request to confirm that your information has been updated.

'''
import requests

body = {'id': 357, 'first_name': 'You', 'last_name': 'Yours', 'email': 'your_email@email.com'}

response = requests.put('http://demo.codingnomads.co:8080/tasks_api/users', json=body)

print(response.status_code)

response = requests.get('http://demo.codingnomads.co:8080/tasks_api/users')
data = response.json()

print(response.status_code)
print(data['data'][-1])
