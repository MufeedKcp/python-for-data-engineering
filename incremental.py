from typing import Optional, Dict, List, Generator
from datetime import timedelta, time, datetime
from pathlib import Path
from basicrequests import *

class IncrementalCollector:
    """Collect only new or updated data since last run"""

    def __init__(self, api_client: APIClient, state_file: str = 'collect_state.json'):
        self.api_client = api_client
        self.state_file = Path(state_file)
        self.state = self.load_state()

    def load_state(self) -> Dict:
        """Load the collector state from file"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
            
        return {}

    def save_load(self):
        """Save the collector state file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)

    def collect_incremental(self, endpoint: str, date_field: str = 'updated_at', loolback_hour: int = 1) -> List[Dict]:
        """Collect data updated since last collection
            
            endpoint: 
                API endpoint
            date_field: 
                Field containing update timestamp
            lookback_hours: 
                Hours to look back for safety margin

            Returns:
                List of new/updated records"""

        
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

    
    def collect_with_checkpoint(self, endpoints: str, batch_size: int = 100) -> Generator[Dict, None, None]:
        """Colect data from last collected offset
        
        endpoint: 
            API endpoint
        batch_size: 
            sixe of each batch
         
        Yields:
            Batch of records"""

        checkpoint = self.state.get(f"{endpoints}_checkpoint", {})
        starter_offset = checkpoint.get('offset', 0)

        offset = starter_offset
        total_fetch = 0

        try:
            while True:
                params = {
                    'offset': starter_offset,
                    'limit': batch_size
                }
                data = self.api_client.get(endpoints, params=params)

                if not data:
                    self.state[f"{endpoints}_checkpoint"] = {'offset': 0}
                    self.save_load()
                    break

                yield data

                total_fetch += len(data)
                offset += batch_size

                self.state[f"{endpoints}_checkpoint"] = {
                    'offset': offset,
                    'last_batch_size': len(data),
                    'total_fetched': total_fetch,
                    'updated_at': datetime.now().isoformat()
                }
                self.save_load()

                if len(data) < batch_size:
                    self.state[f"{endpoints}_checkpoint"] = {'offset': 0}
                    self.save_load()
                    break

        except Exception as e:
            print(f"Error at offset {offset}: {str(e)}")
            print(f"Checkpoint Saved: You can resume from offset {offset}")
            raise

