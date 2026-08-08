from typing import Optional, Dict, List
from datetime import timedelta, time, datetime
from pathlib import Path
from basicrequests import *

class IncrementalCollector:

    def __init__(self, api_client: APIClient, state_file: str = 'collect_state.json'):
        self.api_client = api_client
        self.state_file = Path(state_file)
        self.state = self.load_state()

    def load_state(self) -> Dict:
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
            
        return {}

    def save_load(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)

    def collect_incremental(self, endpoint: str, date_field: str = 'updated_at', loolback_hour: int = 1) -> List[Dict]:

        last_run = self.state.get(endpoint, {}).get('last_run')

        if last_run:
            last_run_dt = datetime.isoformat(last_run)
            since_dt = last_run_dt - timedelta(hours=loolback_hour)
        else: 
            since_dt = datetime.now() - timedelta(days=7)

        params = {
            f"{date_field}_since": since_dt.isoformat(),
            'sort': date_field,
            'order': 'asc'        
        }
        data = self.api_client.get(endpoint, params=params)
        print(f"Fetched {endpoint} with {len(data)} items")

        self.state[endpoint] = {
            'last_run': datetime.now().isoformat(),
            'record_fetched': len(data),
            'since': since_dt.isoformat()
        }
        self.save_load()

        return data