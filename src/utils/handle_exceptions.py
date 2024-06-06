from flask import jsonify, request
from functools import wraps
import logging
import traceback
from werkzeug.exceptions import HTTPException

def log_error(e):
    """Log error with traceback and request info for debugging."""
    trace = traceback.format_exc()
    logging.error(f"Error: {e} at {request.path}: {trace}")
    # Optionally log request data if it's not sensitive:
    # logging.error(f"Request data: {request.json}")

def handle_exceptions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Catch this if specific values are incorrect (e.g., conversion failures)
            logging.info(f"ValueError: {e}")
            return jsonify({"error": "Invalid data format", "details": str(e)}), 400
        except KeyError as e:
            # Catch this if required keys are missing in the data accesses
            logging.info(f"KeyError: {e}")
            return jsonify({"error": "Missing data", "details": str(e)}), 404
        except HTTPException as e:
            # Specific handler for HTTP exceptions raised by Flask or by you
            logging.warning(f"HTTPException: {e}")
            return jsonify({"error": e.name, "description": e.description}), e.code
        except Exception as e:
            # Generic handler for any other exceptions
            log_error(e)  # Use a detailed logging function
            return jsonify({"error": "Unexpected error", "details": "Please contact support"}), 500
    return decorated_function
