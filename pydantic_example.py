from pydantic import BaseModel

class Address(BaseModel):
    city: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    address: Address  # Вложенная модель

user = User(id=1, name="Alice", address=Address(city="New York", zip_code="10001"))
print(user.address.city)  # "New York"

