from fastapi import status


def test_register_and_login(client):
    response = client.post("/api/auth/register", json={"email": "user@example.com", "password": "pass1234"})
    assert response.status_code == status.HTTP_200_OK

    login_response = client.post("/api/auth/login", json={"email": "user@example.com", "password": "pass1234"})
    assert login_response.status_code == status.HTTP_200_OK
    data = login_response.json()
    assert "access_token" in data
