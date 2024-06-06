import json
import hashlib
from flask import current_app, g, request, jsonify
import logging
from functools import wraps

logging.basicConfig(level=logging.DEBUG)


def get_redis_json_response(response):
    if response.is_json:
        return json.dumps(response.get_json())
    return response.get_data(as_text=True)

def set_redis_json_response(redis_client, key, response, timeout):
    try:
        serialized_response = get_redis_json_response(response)
        result = redis_client.setex(key, timeout, serialized_response)
        # logging.debug(f"Redis SETEX result for key {key}: {result}")
    except Exception as e:
        logging.error(f"Error setting Redis key: {e}")


def get_redis_client():
    if 'redis_client' not in g:
        logging.info("Connecting to Redis")
        g.redis_client = current_app.config['REDIS_CLIENT']
    return g.redis_client

def cache_request(timeout):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            redis_client = get_redis_client()
            key = hashlib.md5(str(request.path + str(request.args)).encode()).hexdigest()
            cached_response = redis_client.get(key)
            # logging.info(f"Cache response for key: {cached_response}")
            if cached_response:
                # logging.info(f"Cache hit for key,,,,,,,,,,,,,,,,,,,,,,,: {key}")
                return jsonify(json.loads(cached_response)), 200
            response = func(*args, **kwargs)
            if response.status_code == 200:
                # logging.info(f"Caching response for key: {key}")
                set_redis_json_response(redis_client, key, response, timeout)
            return response
        return wrapper
    return decorator
