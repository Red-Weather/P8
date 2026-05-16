import httpx
#import json
import pytest

# Шаги:
# 0. headers;
# 1. Проверка успешной аутентификации;
# 2. Ошибка аутентификации (неверный username);
# 3. Ошибка аутентификации (неверный пароль);
# 4. Ошибка аутентификации (пустые поля);
# 5. Верификация токена;
# 6. Получение информаци о профиле;
# 7. Получение списка профилей;
# 8. Получение информации об администраторе по id (ошибка авторизации).

#res_1, _2, _3 - для удобства

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
def test_auth_error_1():
    wlogpas = { #неверное имя пользователя
    "username": "userpodkopaev",
    "password": "Ladiesman34"
    }

    wres = httpx.post(
    f"{base_url}/api/auth/login", json=wlogpas
    )
    assert wres.status_code == 401

# 3
def test_auth_error_2():
    wlogpas = { #неверый пароль
    "username": "userpodkopaev",
    "password": "ladiesman"
    }

    wres = httpx.post(
    f"{base_url}/api/auth/login", json=wlogpas
    )
    assert wres.status_code == 401

#4
def test_auth_error_3():
    wlogpas = { #пустые поля
    "username": "",
    "password": ""
    }

    wres = httpx.post(
    f"{base_url}/api/auth/login", json=wlogpas
    )
    assert wres.status_code == 401

# 5
def test_verify_token(headers):
    wres_token = httpx.post( #без токена
        f"{base_url}/api/auth/verify"
    )
    assert wres_token.status_code == 403

    res_token = httpx.post( #c токеном
        f"{base_url}/api/auth/verify", headers=headers
    )
    assert res_token.status_code == 200

# 6
def test_get_my_profile(headers):
    res_2 = httpx.get(
        f"{base_url}/api/profiles/me", headers=headers)
    assert res_2.status_code == 200
    assert res_2.json()["profile"]["username"] == "user_Podkopaev"

# 7
def test_get_all_profiles(headers):
    res_3 = httpx.get(f"{base_url}/api/profiles/", headers=headers,
            params={
                "limit": 100,
                "offset": 0
            }
    )
    #print(json.dumps(res_3.json(), indent=3), flush=True)
    #Выводит только свой профиль
    assert res_3.status_code == 200
    assert len(res_3.json()["profiles"]) == 1 #проверка количества пользователей

# 8
# Админ id=1
def test_get_admin_profile():
    res_4 = httpx.get(
        f"{base_url}/api/profiles/{1}"
    )
    assert res_4.status_code == 403