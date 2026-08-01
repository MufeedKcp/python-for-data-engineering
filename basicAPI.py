import requests

# GET - Retrieve data
response = requests.get('https://api.example.com/users')

# POST - Create new resource
new_user = {'name': 'John Doe', 'email': 'john@example.com'}
response = requests.post('https://api.example. com/users', json=new_user)

# PUT - Update entire resource
updated_user = {'id': 1, 'name': 'Jane Doe', 'email': 'jane@example.com'}
response = requests.put('https://api.example.com/users/1', json=updated_user)

# PATCH - Partial update
partial_update = {'email': 'newemail@example.com'}
response = requests.patch('https://api.example.com/users/1', json=partial_update)

# DELETE - Remove resource
response = requests.delete('https://api.example.com/users/1')