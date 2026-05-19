import httpx
from config import base_url

# Шаги:
# 1. Проверка аутентификации;
# 2. Верификация токена (позитивный);
# 3. Верификация токена (негативныый);
# 4. Получение информации о профиле
# 5. Получение списка всех профилей
# 6. Получение информации о профиле по id

# 1
def test_login():
    res_1 = httpx.post(
        f"{base_url}/api/auth/login", json={
            "username": "moderator",
            "password": "moderator123"
        }
    )
    assert res_1.status_code == 200, \
        f"Expected 200, got {res_1.status_code}"
    assert res_1.json()["access_token"] is not None, \
        f"Expected access_token, got {res_1.json()["access_token"]}"

# 2
def test_verify_token_wrong(mod_headers):

    wres_token = httpx.post( #без токена
        f"{base_url}/api/auth/verify"
    )
    assert wres_token.status_code == 403, \
        f"Expected 403, ot {wres_token.status_code}"

# 3
def test_verify_token_right(mod_headers):
    res_token = httpx.post( #c токеном
        f"{base_url}/api/auth/verify", headers=mod_headers
    )
    assert res_token.status_code == 200, \
        f"Expected 200, got {res_token.status_code}"

# 4
def test_get_my_profile(mod_headers):
    res_2 = httpx.get(
        f"{base_url}/api/profiles/me", headers=mod_headers)
    assert res_2.status_code == 200, \
        f"Expected 200, got {res_2.status_code}"
    assert res_2.json()["profile"]["username"] == "moderator", \
        f"Expected moderator, got {res_2.json()["profile"]["username"]}"

# 5
def test_get_all_profiles(mod_headers):
    res_3 = httpx.get(
        f"{base_url}/api/profiles/", headers=mod_headers
    )
    assert res_3.status_code == 200, \
        f"Expected 200, got {res_3.status_code}"
    assert len(res_3.json()["profiles"]) > 1, \
        f"Expected more than 1 profile, got {len(res_3.json()["profiles"])}"

# 6
def test_get_admin_profile(mod_headers):
    res_4 = httpx.get(
        f"{base_url}/api/profiles/{1}", headers=mod_headers
    )
    assert res_4.status_code == 200, \
        f"Expected 200, got {res_4.status_code}"
    assert res_4.json()["profile"]["username"] == "admin", \
        f"Expected admin, got {res_4.json()["profile"]["username"]}"
