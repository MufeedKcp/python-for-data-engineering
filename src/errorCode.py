import requests 

def interpret_status_code(response) :

    """Interprets HTTP status codes and returns appropriate response"""

    status = response.status_code

    if 200 <= status < 300:
        print(f"Success! Status: {status}")
        return "success"
    elif status == 400:
        print("Bad Request - Check your parameters")
        return "client_error"
    elif status == 401:
        print("Unauthorized - Check authentication")
        return "auth_error"
    elif status == 404:
        print("Not Found - Resource doesn't exist")
        return "not_found"
    elif status == 429:
        print("Too Many Requests - Rate limited")
        return "rate_limit"
    elif 500 <= status < 600:
        print(f"Server Error: {status}")
        return "server_error"
    else:
        print(f"Unexpected status: {status}")
        return "unknown"

# Example usage
response = requests.get('https://api.github.com/users')

status_result = interpret_status_code(response)