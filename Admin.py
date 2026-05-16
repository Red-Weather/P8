import httpx
import pytest
#import json

# Тесты:
# 0. headers
# 1. Проверка аутентификации;
# 2. Верификация токена;
# 3. Получение информации о профиле
# 4. Получение списка всех профилей
# 5. Получение информации о профиле по id


base_url = "https://secby.ru"

# 0
@pytest.fixture
def headers():
    res = httpx.post(
        f"{base_url}/api/auth/login", json={
            "username": "admin",
            "password": "admin123"
        }
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# 1
def test_login():
    res_1 = httpx.post(
        f"{base_url}/api/auth/login", json={
            "username": "admin",
            "password": "admin123"
        }
    )
    assert res_1.status_code == 200
    assert res_1.json()["access_token"] is not None

# 2
def test_verify_token(headers):

    wres_token = httpx.post( #без токена
        f"{base_url}/api/auth/verify"
    )
    assert wres_token.status_code == 403

    res_token = httpx.post( #c токеном
        f"{base_url}/api/auth/verify", headers=headers
    )
    assert res_token.status_code == 200

# 3
def test_get_my_profile(headers):
    res_2 = httpx.get(
        f"{base_url}/api/profiles/me", headers=headers)
    assert res_2.status_code == 200
    assert res_2.json()["profile"]["username"] == "admin"

# 4
def test_get_all_profiles(headers):
    res_3 = httpx.get(
        f"{base_url}/api/profiles/", headers=headers
    )
    assert res_3.status_code != 403
    """
    print (json.dumps(
        res_3.json(),
        indent=3
    ))
    """

# 5
def test_get_admin_profile(headers):
    res_4 = httpx.get(
        f"{base_url}/api/profiles/{1}", headers=headers
    )
    assert res_4.status_code == 200
    assert res_4.json()["profile"]["email"] == "admin@example.com"
    #print(json.dumps(res_4.json(), indent=3), flush=True)