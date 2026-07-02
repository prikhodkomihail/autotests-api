from faker import Faker
import requests

fake = Faker()

user_data = {
    "name": fake.name(),
    "email": fake.email(),
    "age": fake.random_int(min=18, max=100)
}

response = requests.post("https://api.example.com/users", json=user_data)

assert response.status_code == 201
