# app.py

from flask import Flask # type: ignore
import redis # type: ignore
from config import BaseConfig

import os

from src.routes import main

# Instantiate the config 
config = BaseConfig()

print("CACHE_REDIS_HOST:", config.CACHE_REDIS_HOST)

def create_app():
  app = Flask(__name__)

# Configure Redis client and store it in app context
  app.config['REDIS_CLIENT'] = redis.Redis(
      host=config.CACHE_REDIS_HOST, 
      port=config.CACHE_REDIS_PORT, 
      db=config.CACHE_REDIS_DB
  )

  # Blueprints
  app.register_blueprint(main)

  return app

app = create_app()

if __name__ == "__main__":
   app.run(debug=(os.getenv('FLASK_ENV') == 'development'))


