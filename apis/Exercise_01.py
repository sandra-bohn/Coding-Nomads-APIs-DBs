'''
Using the requests package, make a GET request to the api behind this endpoint:

    http://demo.codingnomads.co:8080/tasks_api/users

Print out:

    - the status code
    - the encoding of the response
    - the text of the response body



'''

import requests

response = requests.get('http://demo.codingnomads.co:8080/tasks_api/users')

print('Status code: ', response.status_code)
print('Encoding: ', response.encoding)
print('Body: ', response.text)
