from typing import Callable, Any
from functools import wraps
import random
import time
from basicrequests import *


class APIError(Exception):
    """Base execption for API errors"""
    pass

class RateLimitError(APIError):
    """Raise when Rate Limit exceeds"""
    pass

class AuthenticationError(APIError):
    """Raise when authentication fails"""
    pass


def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 2.0, max_delay: float = 40.0, jitter: bool = True):
    """A decorator for retrying function with exponential backoff
    max_retries: 
        maximum number of attempt
    backoff_factor:
        multiplier for delay between retries
    max_delay: 
        maximum delay in seconds
    jitter:
        add random jitter to prevent thundering herd"""
    def decorator(fun: Callable) -> Callable:
        @wraps(fun)
        def wrapper(*args, **kwargs) -> Any:
            delay = 1.0
            last_execption = None

            for attempt in range(max_retries +1):
                try:
                    return fun(*args, **kwargs)

                except RateLimitError as e:
                    wait_time = min(delay * backoff_factor ** attempt, max_delay)

                    if jitter:
                        wait_time *= (0.5 + random.random())
                        time.sleep(wait_time)
                        last_execption = e

                except (requests.exceptions.Timeout,
                        requests.exceptions.ConnectionError) as e:
                    if attempt == max_retries:
                        raise

                    wait_time *= (0.5 + random.random())
                    print(f"Network Error: Waiting {wait_time:.2f}.....")
                    time.sleep(wait_time)
                    last_execption = e

                except AuthenticationError:
                    raise

                except Exception as e:
                    print(f"Unexpected Error Occured: {str(e)}")
                    raise

            return last_execption or APIError(f"Failed after {max_retries} retries")

        
        return wrapper
    return decorator