import pytest 
from pathlib import Path
from framework.api_client import APIClient
from framework.data_reader import DataReader
from framework.logger import logger

# Responsible for dealing with the APi URL/requests
@pytest.fixture
def api_client():
    return APIClient()


# read test_data.yaml file path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_DATA_FILE = PROJECT_ROOT / "test_data" / "test_data.yaml"

# Responsible for CRUD with test data file
reader = DataReader(TEST_DATA_FILE)
test_data = reader.read_date()
# Get the list of products
products = test_data["products"]
invalid_products = test_data["invalid_products"]

# Gives entire yaml
@pytest.fixture
def test_data():
    return test_data

@pytest.fixture(
    params=products, 
    ids = [product["name"] for product in products]
)
def product_data(request):
    return request.param

@pytest.fixture(
    params=invalid_products,
    ids=[invalid_product["test_case"] for invalid_product in invalid_products]
)
def invalid_product_data(request):
    return request.param

@pytest.fixture
def created_product(api_client, product_data):
    response = api_client.post("/products", product_data)
    logger.info(f"Product Created")
    assert response.status_code == 201
    created_product_data = response.json()
    
    yield created_product_data
    
    product_id = created_product_data["id"]
    delete_product_id_response = api_client.delete(f"/products/{product_id}")
    assert delete_product_id_response.status_code == 200
    
    
