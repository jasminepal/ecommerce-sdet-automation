import random
from framework.logger import logger
from framework.assertions import assert_product_response


def test_get_products(api_client):
    response = api_client.get("/products")
    # print(f"Response body: {response.json()}")
    logger.info(f"Status code: {response.status_code}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    


def test_create_product(api_client, product_data):
    # product_data = test_data["products"]["valid_product"]

    response = api_client.post("/products", product_data)
    logger.info(f"Status code: {response.status_code}")
    logger.info(f"Product Created")
    response_data = response.json()
    
    assert_product_response(response_data, product_data)
    
    # assert "id" in response_data
    # assert response_data["name"] == product_data["name"]
    # assert response_data["price"] == product_data["price"]
    # assert response_data["stock"] == product_data["stock"]
        


def test_get_product_by_id(api_client, created_product):
    product_id = created_product["id"]
    logger.info(f"Product id fetched")
    # print(f"product id {product_id}")
    
    response = api_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    response_data = response.json()
    # print(f" data {response_data}")
    
    assert response_data["id"] == product_id
    assert response_data["name"] == created_product["name"]
    assert response_data["price"] == created_product["price"]
    assert response_data["stock"] == created_product["stock"]
    
    

def test_update_product_by_id(api_client, product_data):
    created_product_response = api_client.post("/products", product_data)
    logger.info(f"Status code: {created_product_response.status_code}")
    logger.info(f"Product Created")
    assert created_product_response.status_code == 201
    product_id = created_product_response.json()["id"]
    logger.info(f"Product id fetched")
    
    updated_product_data = {
        'name': f"Update {product_data['name']}", 
        'price': product_data['price'] + 1000, 
        'stock': product_data['stock'] + 100
    }
    response = api_client.put(f"/products/{product_id}", updated_product_data)
    response_data = response.json()
    
    assert_product_response(response_data, updated_product_data)
    # print(f"created_product_response.json() is {created_product_response.json()} and response_data is {response_data}")
    assert response_data["id"] == product_id
    assert response_data != created_product_response.json()
    
    

def test_patch_product_by_id(api_client, product_data):
    created_product_response = api_client.post("/products", product_data)
    logger.info(f"Status code: {created_product_response.status_code}")
    logger.info(f"Product Created")
    assert created_product_response.status_code == 201
    product_id = created_product_response.json()["id"]
    logger.info(f"Product id fetched")
    
    random_key = random.choice(list(product_data.keys()))
    random_value = product_data[random_key]
    body = {random_key: random_value}
    if isinstance(body[random_key], (int, float)):
        body[random_key] += 50
    elif isinstance(body[random_key], str):
        body[random_key] += 'Modified'
    # print(f"body is {body} and priduct data was {product_data}")
    
    response = api_client.patch(f"/products/{product_id}", body)
    assert response.status_code == 200
    response_data = response.json()
    
    assert response_data["id"] == product_id
    assert response_data[random_key] == body[random_key]
    
    
    
def test_delete_product_by_id(api_client, product_data):
    created_product_response = api_client.post("/products", product_data)
    logger.info(f"Status code: {created_product_response.status_code}")
    logger.info(f"Product Created")
    assert created_product_response.status_code == 201
    product_id = created_product_response.json()["id"]
    logger.info(f"Product id fetched")
    
    response = api_client.delete(f"/products/{product_id}")
    print(response.url)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200
    response_data = response.json()
    



# negative TCs
def test_create_product_with_invalid_data(api_client, invalid_product_data):
    unwanted_keys = {'test_case', 'expected_status'}
    required_data = {key: value for key, value in invalid_product_data.items() if key not in unwanted_keys}
    logger.info(f"Required body: {required_data}")
    response = api_client.post(f"/products", required_data)
    # response_data = response.json()
    
    assert response.status_code == invalid_product_data["expected_status"]