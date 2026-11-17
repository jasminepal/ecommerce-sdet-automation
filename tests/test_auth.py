import pytest
import allure

from framework.logger import logger


@pytest.mark.positive
@allure.feature("Authentication")
@allure.story("JWT Authentication")
@allure.title("Verify authenticated user can access their profile")
def test_get_my_profile(api_client, created_user, auth_token):

    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    response = api_client.get("/users/me", headers=headers)

    assert response.status_code == 200, response.text
    assert response.json()["id"] == created_user["id"]
    assert response.json()["email"] == created_user["email"]

    logger.info("Authenticated user accessed their profile successfully")


@pytest.mark.negative
@allure.feature("Authentication")
@allure.story("JWT Authentication")
@allure.title("Verify profile access is rejected without a token")
def test_get_my_profile_without_token(api_client):

    response = api_client.get("/users/me")

    assert response.status_code == 401, response.text


@pytest.mark.negative
@allure.feature("Authentication")
@allure.story("JWT Authentication")
@allure.title("Verify profile access is rejected with an invalid token")
def test_get_my_profile_with_invalid_token(api_client):

    headers = {
        "Authorization": "Bearer invalid.token.value"
    }

    response = api_client.get("/users/me", headers=headers)

    assert response.status_code == 401, response.text


@pytest.mark.negative
@allure.feature("Authentication")
@allure.story("JWT Authorization")
@allure.title("Verify inactive user cannot access their profile")
def test_inactive_user_cannot_access_profile(
    api_client, created_user, auth_token
):
    # Deactivate the user
    response = api_client.patch(
        f"/users/{created_user['id']}",
        {"is_active": False}
    )

    assert response.status_code == 200, response.text

    # Try accessing the profile using the previously generated token
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    response = api_client.get("/users/me", headers=headers)

    assert response.status_code == 401, response.text