import random
import pytest
import allure
from framework.logger import logger
from framework.assertions import assert_product_response


@pytest.mark.positive
def test_get_products(api_client):
    with allure.step("Get All Products"):
        response = api_client.get("/products")
    
    # print(f"Response body: {response.json()}")
    logger.info(f"Status code: {response.status_code}")
    
    with allure.step("Validate Products Response"):
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    


@pytest.mark.positive
def test_create_product(api_client, product_data):
    # product_data = test_data["products"]["valid_product"]
    
    with allure.step("Create Product"):
        response = api_client.post("/products", product_data)
        
    logger.info(f"Status code: {response.status_code}")
    logger.info(f"Product Created")
    
    with allure.step("Validate Product Response"):
        assert response.status_code == 201
        response_data = response.json()
        
        assert_product_response(response_data, product_data)
    
    # assert "id" in response_data
    # assert response_data["name"] == product_data["name"]
    # assert response_data["price"] == product_data["price"]
    # assert response_data["stock"] == product_data["stock"]
        


@pytest.mark.positive
def test_get_product_by_id(api_client, created_product):
    with allure.step("Get Product ID"):
        product_id = created_product["id"]
        logger.info(f"Product id fetched")
    
    # print(f"product id {product_id}")
    
    with allure.step("Get Product By ID"):
        response = api_client.get(f"/products/{product_id}")
    
    with allure.step("Validate Product Response"):
        assert response.status_code == 200
        response_data = response.json()
        # print(f" data {response_data}")
        
        assert response_data["id"] == product_id
        assert_product_response(response_data, created_product)
    
    

@pytest.mark.positive
def test_update_product_by_id(api_client, product_data):
    with allure.step("Create Product"):
        created_product_response = api_client.post("/products", product_data)
    
    logger.info(f"Status code: {created_product_response.status_code}")
    logger.info(f"Product Created")
    
    with allure.step("Get Created Product ID"):
        assert created_product_response.status_code == 201
        product_id = created_product_response.json()["id"]
        logger.info(f"Product id fetched")
    
    with allure.step("Prepare Updated Product Data"):
        updated_product_data = {
            'name': f"Update {product_data['name']}", 
            'price': product_data['price'] + 1000, 
            'stock': product_data['stock'] + 100
        }
    
    with allure.step("Update Product"):
        response = api_client.put(f"/products/{product_id}", updated_product_data)
        response_data = response.json()
    
    with allure.step("Validate Updated Product Response"):
        assert response.status_code == 200
        assert_product_response(response_data, updated_product_data)
        # print(f"created_product_response.json() is {created_product_response.json()} and response_data is {response_data}")
        assert response_data["id"] == product_id
        assert response_data != created_product_response.json()
    
    

@pytest.mark.positive
def test_patch_product_by_id(api_client, product_data):
    with allure.step("Create Product"):
        created_product_response = api_client.post("/products", product_data)
    
    logger.info(f"Status code: {created_product_response.status_code}")
    logger.info(f"Product Created")
    
    with allure.step("Get Created Product ID"):
        assert created_product_response.status_code == 201
        product_id = created_product_response.json()["id"]
        logger.info(f"Product id fetched")
    
    with allure.step("Prepare Patch Data"):
        random_key = random.choice(list(product_data.keys()))
        random_value = product_data[random_key]
        body = {random_key: random_value}
        if isinstance(body[random_key], (int, float)):
            body[random_key] += 50
        elif isinstance(body[random_key], str):
            body[random_key] += 'Modified'
    
    # print(f"body is {body} and priduct data was {product_data}")
    
    with allure.step("Patch Product"):
        response = api_client.patch(f"/products/{product_id}", body)
    
    with allure.step("Validate Patched Product Response"):
        assert response.status_code == 200
        response_data = response.json()
        
        assert response_data["id"] == product_id
        assert response_data[random_key] == body[random_key]
    
    

@pytest.mark.positive
def test_delete_product_by_id(api_client, product_data):
    with allure.step("Create Product"):
        created_product_response = api_client.post("/products", product_data)
    
    logger.info(f"Status code: {created_product_response.status_code}")
    logger.info(f"Product Created")
    
    with allure.step("Get Created Product ID"):
        assert created_product_response.status_code == 201
        product_id = created_product_response.json()["id"]
        logger.info(f"Product id fetched")
    
    with allure.step("Delete Product"):
        response = api_client.delete(f"/products/{product_id}")
    
    with allure.step("Validate Delete Response"):
        print(response.url)
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Product deleted successfully"
        
    



# negative TCs
@pytest.mark.negative
def test_create_product_with_invalid_data(api_client, invalid_product_data):
    with allure.step("Prepare Invalid Product Data"):
        unwanted_keys = {'test_case', 'expected_status'}
        required_data = {key: value for key, value in invalid_product_data.items() if key not in unwanted_keys}
        logger.info(f"Required body: {required_data}")
    
    with allure.step("Create Product With Invalid Data"):
        response = api_client.post(f"/products", required_data)
    
    # response_data = response.json()
    
    with allure.step("Validate Error Response"):
        assert response.status_code == invalid_product_data["expected_status"]