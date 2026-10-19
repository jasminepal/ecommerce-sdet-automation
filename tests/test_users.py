
import pytest
import allure
import uuid
from framework.logger import logger



@pytest.mark.positive
@allure.feature("User API")
@allure.story("Create User")
@allure.title("Verify a user can be created successfully")
def test_create_user(api_client, user_data):
    user_payload = user_data.copy()

    # Generate a unique email for every test run.
    user_payload["email"] = (
        f"{user_payload['email'].split('@')[0]}+"
        f"{uuid.uuid4().hex[:8]}@"
        f"{user_payload['email'].split('@')[1]}"
    )

    created_user_id = None

    try:
        with allure.step("Send POST request to create a user"):
            logger.info("Creating user with email: %s", user_payload["email"])
            response = api_client.post("/users", user_payload)

            logger.info(
                "Create user response status: %s",
                response.status_code
            )

        with allure.step("Verify the response status is 201"):
            assert response.status_code == 201, (
                f"Expected 201 Created, got {response.status_code}. "
                f"Response: {response.text}"
            )

        with allure.step("Validate the created user response"):
            response_data = response.json()

            assert "id" in response_data
            created_user_id = response_data["id"]

            assert response_data["name"] == user_payload["name"]
            assert response_data["email"] == user_payload["email"]
            assert "password" not in response_data

            logger.info(
                "User created successfully: ID %s",
                created_user_id
            )

    finally:
        if created_user_id is not None:
            with allure.step("Clean up the created user"):
                delete_response = api_client.delete(
                    f"/users/{created_user_id}"
                )

                assert delete_response.status_code == 200, (
                    f"Failed to delete test user {created_user_id}. "
                    f"Status: {delete_response.status_code}. "
                    f"Response: {delete_response.text}"
                )

                logger.info("Cleaned up test user ID: %s", created_user_id)



@pytest.mark.positive
@allure.feature("User API")
@allure.story("Get All Users")
@allure.title("Verify all users can be retrieved")
def test_get_all_users(api_client, created_user):
    with allure.step("Send GET request to retrieve all users"):
        logger.info("Fetching all users")

        response = api_client.get("/users")

        logger.info(
            "Get all users response status: %s",
            response.status_code
        )

    with allure.step("Verify the response status is 200"):
        assert response.status_code == 200, (
            f"Expected 200 OK, got {response.status_code}. "
            f"Response: {response.text}"
        )

    with allure.step("Verify the created user is present in the response"):
        response_data = response.json()

        assert isinstance(response_data, list), (
            "Expected the API to return a list of users"
        )

        assert any(
            user["id"] == created_user["id"]
            for user in response_data
        ), f"Created user ID {created_user['id']} was not found"

        logger.info(
            "Verified user ID %s exists in the users list",
            created_user["id"]
        )


@pytest.mark.positive
@allure.feature("User API")
@allure.story("Get User By ID")
@allure.title("Verify a user can be retrieved by ID")
def test_get_user_by_id(api_client, created_user):
    user_id = created_user["id"]

    with allure.step(f"Send GET request for user ID {user_id}"):
        logger.info("Fetching user ID: %s", user_id)

        response = api_client.get(f"/users/{user_id}")

        logger.info(
            "Get user by ID response status: %s",
            response.status_code
        )

    with allure.step("Verify the response status is 200"):
        assert response.status_code == 200, (
            f"Expected 200 OK, got {response.status_code}. "
            f"Response: {response.text}"
        )

    with allure.step("Validate the returned user details"):
        response_data = response.json()

        assert response_data["id"] == user_id
        assert response_data["name"] == created_user["name"]
        assert response_data["email"] == created_user["email"]

        assert "password" not in response_data, (
            "API response must not expose the password"
        )

        logger.info("Successfully retrieved user ID: %s", user_id)
