import httpx
import pytest

base_url = "https://secby.ru"

@pytest.fixture
def us_headers():
    res = httpx.post(
        f"{base_url}/api/auth/login", json={
            "username": "user_Podkopaev",
            "password": "Ladiesman34"
        }
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mod_headers():
    res = httpx.post(
        f"{base_url}/api/auth/login", json={
            "username": "moderator",
            "password": "moderator123"
        }
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def ad_headers():
    res = httpx.post(
        f"{base_url}/api/auth/login", json={
            "username": "admin",
            "password": "admin123"
        }
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}