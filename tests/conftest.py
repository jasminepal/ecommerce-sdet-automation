import pytest 
from framework.api_client import APIClient
from framework.data_reader import DataReader

# Responsible for dealing with the APi URL/requests
@pytest.fixture
def api_client():
    return APIClient()

# Responsible for CRUD with test data file
@pytest.fixture
def test_data():
    reader = DataReader("test_data/test_data.yaml")
    return reader.read_date()
