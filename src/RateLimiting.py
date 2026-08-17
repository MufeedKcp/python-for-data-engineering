from datetime import timedelta, datetime
import time
from threading import Lock
from collections import deque
from basicrequests import *

class RateLimiting:
    """Token Bucket Rate Limiter for API requests"""
    def __init__(self, rate: int, per: float = 1.0):
        """Initializing the rate limit
        args:
        rate: Number of request allowed
        per: time period in seconds"""
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.updated_at = time.time()
        self.lock = Lock()

    def acquire(self, tokens: int) -> float:
        """Acquiring token, block if neccesary
        args:
        tokens: Number of token to acquire"""
        with self.lock:
            while tokens > self.tokens:
                now = time.time()
                elapsed = now - self.updated_at

                self.tokens += elapsed * (self.rate / self.per)
                self.tokens = min(self.tokens, self.rate)
                self.updated_at = now

                if tokens > self.tokens:
                    deficit = tokens - self.tokens
                    wait_time = deficit * (self.rate / self.per)
                    time.sleep(wait_time)

            self.tokens -= tokens

        return 0

class SlidinWindowRateLimiter:
    """Sliding window rate limiter for more precise control"""
    def __init__(self, max_requests: int, window_size: int):
        """Initializing the rate limiter
        args:
        max_requests: Maximum requests allowed in a window
        window_size: Window size in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests = deque()
        self.lock = Lock()

    def is_allowed(self) -> bool:
        """Check if requests is allowed"""
        with self.lock:
            now = datetime.now()
            window_start = now - timedelta(seconds=self.window_size)

            # Remove old requests outside window
            while self.requests and self.requests[0] < window_start:
                self.requests.popleft()

            # Checking if we can make requests
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False

        def wait_if_needed(self) -> float:
            """Wait if rate limit exceeds"""
            total_wait_time = 0
            while not self.is_allowed:
                wait_time = 1.0
                total_wait_time +=wait_time
                time.sleep(wait_time)
                
            return total_wait_time

        
class ThrottledAPIClient(APIClient):
    """API Client with build-in Rate limiter"""

    def __init__(self, base_url, timeout = 30, requests_per_sec: float = 10):
        """Initializing the Throttled API-Client"""
        super().__init__(base_url, timeout)
        self.rate_limiter = RateLimiting(rate=int(requests_per_sec), per=2.0)

    def get(self, endpoints: str, **kwargs) -> Dict:
        """Rate-Limiter for GET request"""
        self.rate_limiter.acquire()
        return super().get(endpoints, **kwargs)


throttled_client = ThrottledAPIClient('https://api.example.com', requests_per_sec=3)

for i in range(20):
    start = time.time()
    response = throttled_client.get(f'/users/{i}')
    elapsed = time.time() - start
    print(f"Requests {i} completed in {elapsed:.2f}s")
    