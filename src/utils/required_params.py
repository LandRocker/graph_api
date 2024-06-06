from functools import wraps
from flask import request, jsonify

def require_params(*required_args):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            missing = [arg for arg in required_args if request.args.get(arg) is None]
            if missing:
                response = {"error": "Missing required parameters", "missing_parameters": missing}
                return jsonify(response), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator