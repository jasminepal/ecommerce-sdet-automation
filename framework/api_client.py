import requests
from framework.config import BASE_URL

class APIClient:
    def get(self, endpoint):
        return requests.get(f"{BASE_URL}{endpoint}")
    
    def post(self, endpoint, request_body):
        return requests.post(f"{BASE_URL}{endpoint}", json = request_body)
    
    def put(self, endpoint, request_body):
        return requests.put(f"{BASE_URL}{endpoint}", json = request_body)
    
    def patch(self, endpoint, request_body):
            return requests.patch(f"{BASE_URL}{endpoint}", json = request_body)