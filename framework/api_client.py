import requests
from framework.config import BASE_URL, REQUEST_TIMEOUT

class APIClient:
    
    def _request(self, method, endpoint, data = None):
        return requests.request(method, f"{BASE_URL}{endpoint}", json=data, timeout=REQUEST_TIMEOUT)
        
    def get(self, endpoint):
        return self._request("GET", endpoint)
    
    def post(self, endpoint, request_body):
        return self._request("POST", endpoint, request_body)
    
    def put(self, endpoint, request_body):
        return self._request("PUT", endpoint, request_body)
    
    def patch(self, endpoint, request_body):
        return self._request("PATCH", endpoint, request_body)
        
    def delete(self, endpoint):
        return self._request("DELETE", endpoint)
    