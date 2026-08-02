import requests
import json
from typing import Dict, Optional, List

class APIClient:
    """A robust API client with comprehensive error handling"""

    def _init_(self, base_url: str, timeout: int = 30):
        """Initialize the APIClient class"""
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _build_url(self, endpoint: str) -> str:
        """Construct full URL from base URL and endpoint"""
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """Make GET request to API endpoint

            Args:
                endpoint: API endpoint path
                params: Query parameters
                headers: Additional headers

            Returns:
                Response data as dictionary"""

        url = self._build_url(endpoint)

        try:
            """Make GET request with comprehensive error handling"""
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            response. raise_for_status() # Raise exception for bad status codes
            return response. json()

        except requests.exceptions. Timeout:
            print(f"Request timed out for {url}")
            raise
        except requests.exceptions.ConnectionError:
            print(f"Connection error for {url}")
            raise
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error {e.reponse.status_code}: {e.response.text}")
            raise
        except requests.JSONDecodeError:
            print(f"JSON Decode Error for {url}")
            print(f"Response content: {response.text}")
            raise

client = APIClient('https://api.example.com')

# GET requests
params = {'limit': 10, 'offset': 0} 
"""Query parameters for the API request"""

headers = {'Authorization': 'Bearer <token>'}
"""Additional headers for the API request"""

data = client.get('Endpoint', params=params, headers=headers)
"""Returns the response data as a dictionary or raises an exception"""

print(f"Retreived {len(data)} items")
# Example: {'items': [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}]}
