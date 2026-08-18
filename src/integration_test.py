import datetime
import vcr
import pytest
from basicrequests import *
from ErrorHandling import *
from pagination import *


class APIIntegrationTests:
    """Integration test for API-Integration"""
    @vcr.use_cassette('tests/cassette/github_user.yaml')
    def test_github_api_integration(self):
        """test the github api integration"""
        client = APIClient('https://api.github.com')
        user = client.get('/users/octocat')

        assert 'login' in user
        assert 'id' in user
        assert user['login'] == 'octocat'
        assert user['type'] == 'User'

    def test_rate_limit_behaviour(self):
        """Test rate limit behaviour"""
        client = RobustAPIClient('https://api.github.com')

        for i in range(20):
            try:
                response = client.fetch_data(f'/users/user{1}')
                print(f"Request for user{i} succesfully completed")
            except RateLimitError:
                print(f"Rate limited at request {i}")
                break

        assert len(response) == 10

    @pytest.mark.slow
    def test_large_dataset_collection(self):
        """Test collecting large datasets"""
        client = PaginatedAPIClient('https://jsonplaceholder.typicode.com')

        start_time = datetime.now()

        # Collect all posts
        all_posts = client.fetch_all_pages('/posts', page_size=10)
        duration = (datetime.now() - start_time).total_seconds()

        assert len(all_posts) > 0
        assert duration < 30 # Should complete within 30 seconds
        
        print(f"Collected {len(all_posts)} posts in {duration :.2f}s")