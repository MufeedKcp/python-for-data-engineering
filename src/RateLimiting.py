import time
from threading import Lock


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

    