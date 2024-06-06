# config.py


import os
from dotenv import load_dotenv

# # Load environment variables from .env file
load_dotenv()



print("CACHE_REDIS_HOST:", os.getenv('CACHE_REDIS_HOST'))
print("CACHE_REDIS_PORT:", os.getenv('CACHE_REDIS_PORT'))
print("CACHE_REDIS_DB:", os.getenv('CACHE_REDIS_DB'))

class BaseConfig(object):
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'redis')  # Default to 'redis' if not set
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST', 'rediscmc')
    CACHE_REDIS_PORT = os.getenv('CACHE_REDIS_PORT', 6379)
    CACHE_REDIS_DB = os.getenv('CACHE_REDIS_DB', 0)
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://rediscmc:6379/0')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
    SUBGRAPH_URL = os.getenv('SUBGRAPH_URL')

