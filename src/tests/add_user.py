# API Test: Admin Add User

import requests

url = 'http://localhost:5000/admin/user/add'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@flowbite.com",
    "birthday": "1990-05-12",
    "position": "Software Engineer",
    "password": "X4q7Fm9z"
}

response = requests.post(url, data=data, headers=headers)
print(response.text)
print(f"Status code: {response.status_code}")
