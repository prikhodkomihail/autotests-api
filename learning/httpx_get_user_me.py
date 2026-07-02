import httpx

login_payload = {
    "email": "user@example.com",
    "password": "password"
}

login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

print("Login response:", login_response_data)
print("Status Code:", login_response.status_code)

get_me_header = {"Authorization": f'Bearer {login_response_data["token"]["accessToken"]}'}

get_me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=get_me_header)
get_me_response_data = get_me_response.json()

print("Get me response:", get_me_response_data)
print("Status Code:", get_me_response.status_code)
