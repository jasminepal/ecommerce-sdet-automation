
def test_get_products(api_client):
    response = api_client.get("/products")
    # print(f"Response body: {response.json()}")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    


def test_create_product(api_client, product_data):
    print(f"dfyguhbnbn{product_data}")
    # product_data = test_data["products"]["valid_product"]

    response = api_client.post("/products", product_data)
    response_data = response.json()
    
    assert "id" in response_data
    assert response_data["name"] == product_data["name"]
    assert response_data["price"] == product_data["price"]
    assert response_data["stock"] == product_data["stock"]
        