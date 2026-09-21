def assert_product_response(response_data, expected_data):
    assert "id" in response_data
    assert response_data["name"] == expected_data["name"]
    assert response_data["price"] == expected_data["price"]
    assert response_data["stock"] == expected_data["stock"]