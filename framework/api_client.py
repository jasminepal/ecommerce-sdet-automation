import requests
import allure
import json
from framework.config import BASE_URL, REQUEST_TIMEOUT

class APIClient:
    
    def _request(self, method, endpoint, data = None):
        
        url = f"{BASE_URL}{endpoint}"
        # allure request
        if data:
            allure.attach(
                json.dumps(data, indent=4),
                name=f"{method} Request",
                attachment_type=allure.attachment_type.JSON
            )
        else:
            allure.attach(
                "No request body",
                name=f"{method} Request",
                attachment_type=allure.attachment_type.TEXT
            )

        # actual request call
        response = requests.request(
            method,
            url,
            json=data,
            timeout=REQUEST_TIMEOUT
        )

        # allure response
        try:
            response_body = json.dumps(response.json(), indent=4)
            allure.attach(
                response_body,
                name=f"{method} Response - {response.status_code}",
                attachment_type=allure.attachment_type.JSON
            )
        except ValueError:
            allure.attach(
                response.text,
                name=f"{method} Response - {response.status_code}",
                attachment_type=allure.attachment_type.TEXT
            )

        return response
        
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
    