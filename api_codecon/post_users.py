import requests
import json

def post_users():
    request_file = open('usuarios.json').read()
    request = json.loads(request_file)

    response = requests.post('http://localhost:8000/users', json=request)
    print(response.text)

post_users()