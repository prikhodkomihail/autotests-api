import httpx
from tools.fakers import get_random_email

payload = {
    "email": get_random_email(),
    "password": "password",
    "lastName": "Meow",
    "firstName": "Very Meow",
    "middleName": "Not Meow"
}

response = httpx.post("http://localhost:8000/api/v1/users", json=payload)

print(response.status_code)
print(response.json())