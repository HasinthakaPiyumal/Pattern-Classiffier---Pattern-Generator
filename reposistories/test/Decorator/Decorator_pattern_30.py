import time

_cache = {}

def authenticate_request(func):
    def wrapper(request_data):
        print(f"Authenticating request for user '{request_data.get('user')}'...")
        if request_data.get("auth_token") != "VALID_TOKEN_123":
            print("Authentication FAILED: Invalid token.")
            return {"status": "error", "message": "Unauthorized"}
        print("Authentication SUCCESS.")
        return func(request_data)
    return wrapper

def cache_response(func):
    def wrapper(request_data):
        cache_key = f"{request_data.get('endpoint')}-{request_data.get('params')}"
        if cache_key in _cache:
            print(f"Cache HIT for key: {cache_key}. Returning cached response.")
            return _cache[cache_key]
        
        print(f"Cache MISS for key: {cache_key}. Processing request...")
        response = func(request_data)
        _cache[cache_key] = response
        print(f"Response cached for key: {cache_key}.")
        return response
    return wrapper

def rate_limit_request(func):
    _request_counts = {}
    _last_request_time = {}
    LIMIT_PER_MINUTE = 3
    
    def wrapper(request_data):
        user = request_data.get('user', 'anonymous')
        current_time = time.time()

        if user not in _last_request_time or (current_time - _last_request_time[user]) > 60:
            _request_counts[user] = 0
            _last_request_time[user] = current_time

        _request_counts[user] += 1
        
        if _request_counts[user] > LIMIT_PER_MINUTE:
            print(f"Rate limit EXCEEDED for user '{user}'. Please try again later.")
            return {"status": "error", "message": "Rate limit exceeded"}
        
        print(f"Rate limit check passed for user '{user}'. Requests this minute: {_request_counts[user]}/{LIMIT_PER_MINUTE}.")
        return func(request_data)
    return wrapper

@authenticate_request
@cache_response
@rate_limit_request
def process_api_request(request_data):
    print(f"Processing API request for endpoint '{request_data.get('endpoint')}' with params '{request_data.get('params')}'...")
    time.sleep(0.1)
    response = {"status": "success", "data": f"Result for {request_data.get('endpoint')}-{request_data.get('params')}"}
    print("API request processed.")
    return response

if __name__ == "__main__":
    print("--- First request (authenticated, not cached) ---")
    req1 = {"user": "client_a", "auth_token": "VALID_TOKEN_123", "endpoint": "/data", "params": {"id": 1}}
    response1 = process_api_request(req1)
    print(f"Response 1: {response1}\n")

    print("--- Second request (authenticated, cached) ---")
    response2 = process_api_request(req1)
    print(f"Response 2: {response2}\n")

    print("--- Third request (unauthenticated) ---")
    req3 = {"user": "client_b", "auth_token": "INVALID_TOKEN", "endpoint": "/users", "params": {}}
    response3 = process_api_request(req3)
    print(f"Response 3: {response3}\n")

    print("--- Rate limit test (same user, hit limit) ---")
    req4 = {"user": "client_c", "auth_token": "VALID_TOKEN_123", "endpoint": "/status", "params": {}}
    for i in range(5):
        print(f"Request {i+1} for client_c:")
        response_rl = process_api_request(req4)
        print(f"Response: {response_rl}\n")