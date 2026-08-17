import time
from typing import Generator, List, Dict, Optional
from basicrequests import APIClient

class PaginatedAPIClient(APIClient):

    """Extended API client with pagination support"""

    def fetch_all_pages(self, endpoint: str, page_size: int = 100, max_pages: Optional[int] = None) -> List[Dict]:
        """
        Fetch all pages from a paginated endpoint

        Args:
        endpoint: API endpoint
        page_size: Number of items per page
        max_pages: Maximum number of pages to fetch (None for all)

        Returns:
        List of all items from all pages
        """
        all_items = []
        page = 1

        while True:
            """Check if we've reached max pages"""
            if max_pages and page > max_pages:
                break

            """Fetch current page"""
            params = {'page': page, 'per_page': page_size}
            response = self.get(endpoint, params=params)

            """Check if response is empty or we've reached the end"""
            if not response or len(response) == 0:
                break

            all_items.extend(response)
            print(f"Fetched page {page} with {len(response)} items")

            """Check if we got less than page_size (last page)"""
            if len(response) < page_size:
                break

            page += 1
            time.sleep(0.1)

        return all_items
                                       


    def fetch_with_cursor(self, endpoint: str, cursor: Optional[str] = None, limit: int = 100) -> Generator[Dict, None, None]:
        """
        Fetch data using cursor-based pagination

        Args:
        endpoint: API endpoint
        cursor: Starting cursor (None for beginning)
        limit: Items per request

        Yields:
        Items from each page
        """
        next_cursor = cursor

        while True:
            params = {'limit': limit}
            if next_cursor:
                params ['cursor'] = next_cursor

            response = self.get(endpoint, params=params)

            # Yield items from current page
            items = response.get('data', [])

            for item in items:
                yield item

            next_cursor = response.get('cursor')
            if not next_cursor:
                break

paginated_client = PaginatedAPIClient('https://api.example.com/')

all_users = paginated_client.fetch_all_pages('/users', page_size=20)
print(f"Total user Fetched {len(all_users)}")

for item in paginated_client.fetch_with_cursor('/users', limit=20):
    print(f"Processed Item: {item}")