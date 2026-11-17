import requests
import allure
import json
from framework.config import BASE_URL, REQUEST_TIMEOUT

class APIClient:
    
    def _request(self, method, endpoint, data = None, headers=None):
        
        url = f"{BASE_URL}{endpoint}"
        # allure request
        if data:
            safe_data = data.copy()
            if "password" in safe_data:
                safe_data["password"] = "[REDACTED]"
                
            allure.attach(
                json.dumps(safe_data, indent=4),
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
            headers=headers,
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
        
    def get(self, endpoint, headers=None):
        return self._request("GET", endpoint, headers=headers)
    
    def post(self, endpoint, request_body, headers=None):
        return self._request("POST", endpoint, request_body, headers=headers)
    
    def put(self, endpoint, request_body, headers=None):
        return self._request("PUT", endpoint, request_body, headers=headers)
    
    def patch(self, endpoint, request_body, headers=None):
        return self._request("PATCH", endpoint, request_body, headers=headers)
        
    def delete(self, endpoint, headers=None):
        return self._request("DELETE", endpoint, headers=headers)
    