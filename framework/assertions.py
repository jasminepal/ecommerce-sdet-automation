def assert_product_response(response_data, expected_data):
    assert "id" in response_data
    assert response_data["name"] == expected_data["name"]
    assert response_data["price"] == expected_data["price"]
    assert response_data["stock"] == expected_data["stock"]
    
def get_mutable_product_fields(product_data):
    return {
        key: value
        for key, value in product_data.items()
        if key != "category_id"
    }