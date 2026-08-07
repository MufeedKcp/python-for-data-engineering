import pandas as pd
import concurrent.futures
from typing import List, Dict, Optional, Generator, Callable
from basicrequests import *

class batchCollector:

    def __init__(self, api_client, max_workers: int = 5):
        self.api_client = api_client
        self.max_workers = max_workers

    def collect_data_parellal(self, endpoints: List[Dict]):

        results = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_endpoint = {
                executor.submit(self.api_client.get, endpoint): endpoint
                for endpoint in endpoints
            }
            for future in concurrent.futures.as_completed(future_to_endpoint):
                endpoint = future_to_endpoint[future]

                try:
                    data = future.result()
                    results[endpoint] = data
                    print(f"Successfully Fetched {endpoint}")
                except Exception as e:
                    print(f"Failed to Fetch {endpoint}")
                    results[endpoint] = None
        
        return results

    def collect_and_transform(self, endpoints: List[str], transformation_fun: Callable) -> pd.DataFrame:

        raw_data = self.collect_data_parellal(endpoints)

        transformed_data = []
        for endpoint, data in raw_data.items():
            if data:
                transformed = transformation_fun(data, endpoint)
                transformed_data.extend(transformed)
        
        return pd.DataFrame(transformed_data)




def transform_users(data: List[dict], source: str) -> List[Dict]:
    if isinstance(data, list):
        return [
            {
                'id': user.get('id'),
                'name': user.get('name'),
                'email': user.get('email'),
                'address': user.get('address', {}).get('street') + ' ' + user.get('address', {}).get('suite') + ' ' + user.get('address', {}).get('city'),
                'phone': user.get('phone'),
                'company': user.get('company', {}).get('name'),
                "source": source,
                'collected_at': pd.Timestamp.now()
            }
            for user in data
        ]
    return []


client = APIClient('https://jsonplaceholder.typicode.com')
collector = batchCollector(client, max_workers=1)


user_endpoint = ['/users']
transfom_user_endpoint = collector.collect_and_transform(user_endpoint, transform_users)

print(transfom_user_endpoint)