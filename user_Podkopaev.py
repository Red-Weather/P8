import httpx
#import json
import pytest

# Тесты:
# 0. headers;
# 1. Проверка аутентификации;
# 2. Ошибка аутентификации;
# 3. Верификация токена;
# 4. Получение информаци о профиле;
# 5. Получение списка всех профилей;
# 6. Получение информации об администраторе по id (ошибка авторизации).

base_url = "https://secby.ru"

# 0
@pytest.fixture
def headers():
    logpas = {  # верное имя пользователя
        "username": "user_Podkopaev",
        "password": "Ladiesman34"
    }
    res = httpx.post(
        f"{base_url}/api/auth/login", json=logpas
    )
    print(res.json())
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# 1
def test_login():
    res_1 = httpx.post(
        f"{base_url}/api/auth/login", json={
            "username": "user_Podkopaev",
            "password": "Ladiesman34"
        }
    )
    assert res_1.status_code == 200
    assert res_1.json()["access_token"] is not None

# 2
def test_auth_error(headers):
    wlogpas = { #неверное имя пользователя
    "username": "userpodkopaev",
    "password": "Ladiesman34"
    }

    wres = httpx.post(
    f"{base_url}/api/auth/login", json=wlogpas
    )
    assert wres.status_code == 401

# 3
def test_verify_token(headers):
    wres_token = httpx.post( #без токена
        f"{base_url}/api/auth/verify"
    )
    assert wres_token.status_code == 403

    res_token = httpx.post( #c токеном
        f"{base_url}/api/auth/verify", headers=headers
    )
    assert res_token.status_code == 200

# 4
def test_get_my_profile(headers):
    res_2 = httpx.get(
        f"{base_url}/api/profiles/me", headers=headers)
    assert res_2.status_code == 200
    """
    print(
        json.dumps(
            res_2.json(),
            indent=3
        )
    )
    """
    assert res_2.json()["profile"]["username"] == "user_Podkopaev"

# 5
def test_get_all_profiles(headers): #доступно модератору и администратору
    res_3 = httpx.get(f"{base_url}/api/profiles/",
            params={
                "limit": 100,
                "offset": 0
            }
    )
    assert res_3.status_code == 403

# 6
def test_get_admin_profile(headers):
    res_4 = httpx.get(
        f"{base_url}/api/profiles/{1}", headers=headers
    )
    assert res_4.status_code == 403

