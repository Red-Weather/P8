import httpx
from config import base_url

# Шаги:
# 1. Проверка успешной аутентификации;
# 2. Ошибка аутентификации (неверный username);
# 3. Ошибка аутентификации (неверный пароль);
# 4. Ошибка аутентификации (пустые поля);
# 5. Верификация токена (позитивный);
# 6. Верификация токена (негативныый);
# 7. Получение информаци о профиле;
# 8. Получение списка профилей;
# 9. Получение информации об администраторе по id (ошибка авторизации).

#res_1, _2, _3 - для удобства

# 1
def test_login():
    res_1 = httpx.post(
        f"{base_url}/api/auth/login", json={
            "username": "user_Podkopaev",
            "password": "Ladiesman34"
        }
    )
    assert res_1.status_code == 200, \
        f"Expected 200, got {res_1.status_code}"
    assert res_1.json()["access_token"] is not None, \
        f"Expected access_token, got {res_1.json()["access_token"]}"

# 2
def test_auth_error_1():
    wlogpas = { #неверное имя пользователя
    "username": "userpodkopaev",
    "password": "Ladiesman34"
    }

    wres = httpx.post(
    f"{base_url}/api/auth/login", json=wlogpas
    )
    assert wres.status_code == 401, \
        f"Expected 401, got {wres.status_code}"

# 3
def test_auth_error_2():
    wlogpas = { #неверый пароль
    "username": "userpodkopaev",
    "password": "ladiesman"
    }

    wres = httpx.post(
    f"{base_url}/api/auth/login", json=wlogpas
    )
    assert wres.status_code == 401, \
        f"Expected 401, got {wres.status_code}"

#4
def test_auth_error_3():
    wlogpas = { #пустые поля
    "username": "",
    "password": ""
    }

    wres = httpx.post(
    f"{base_url}/api/auth/login", json=wlogpas
    )
    assert wres.status_code == 401, \
        f"Expected 401, got {wres.status_code}"

# 5
def test_verify_token_wrong(us_headers):
    wres_token = httpx.post( #без токена
        f"{base_url}/api/auth/verify"
    )
    assert wres_token.status_code == 403, \
        f"Expected 403, got {wres_token.status_code}"

# 6
def test_verify_token_right(us_headers):
    res_token = httpx.post( #c токеном
        f"{base_url}/api/auth/verify", headers=us_headers
    )
    assert res_token.status_code == 200, \
        f"Expected 200, got {res_token.status_code}"

# 7
def test_get_my_profile(us_headers):
    res_2 = httpx.get(
        f"{base_url}/api/profiles/me", headers=us_headers)
    assert res_2.status_code == 200, \
        f"Expected 200, got {res_2.status_code}"
    assert res_2.json()["profile"]["username"] == "user_Podkopaev", \
        f"Expected user_Podkopaev, got {res_2.json()["profile"]["username"]}"

# 8
def test_get_all_profiles(us_headers):
    res_3 = httpx.get(f"{base_url}/api/profiles/", headers=us_headers,
            params={
                "limit": 100,
                "offset": 0
            }
    )
    assert res_3.status_code == 200, f"Expected 200, got {res_3.status_code}"
    assert len(res_3.json()["profiles"]) == 1,\
        f"Expected 1, got {len(res_3.json()["profiles"])}"

# 9
# Админ id=1
def test_get_admin_profile():
    res_4 = httpx.get(
        f"{base_url}/api/profiles/{1}"
    )
    assert res_4.status_code == 403, \
        f"Expected 403, got {res_4.status_code}"