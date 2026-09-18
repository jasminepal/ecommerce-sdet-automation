import pytest 
from pathlib import Path
from framework.api_client import APIClient
from framework.data_reader import DataReader

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

