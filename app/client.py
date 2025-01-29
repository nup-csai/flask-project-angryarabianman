import requests

BASE_URL = "http://127.0.0.1:8080"

TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpassword"


def test_signup():
    response = requests.post(f"{BASE_URL}/signup", data={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    assert response.status_code == 200 or response.status_code == 302


def test_login():
    response = requests.post(f"{BASE_URL}/login", data={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    assert response.status_code == 200 or response.status_code == 302

def test_logout():
    session = requests.Session()
    session.post(f"{BASE_URL}/login", data={"email": TEST_EMAIL, "password": TEST_PASSWORD})

    response = session.get(f"{BASE_URL}/logout")
    assert response.status_code == 200 or response.status_code == 302

if __name__ == "__main__":
    test_signup()
    test_login()
    test_logout()

