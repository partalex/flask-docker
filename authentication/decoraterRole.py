from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify


def roleCheck(roles):
    def innerRole(function):
        @wraps(function)
        def decorator(*arguments, **keyargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "roles" in claims:
                rolesParsed = roles.split(',')
                for role in rolesParsed:
                    if role in claims["roles"]:
                        return function(*arguments, **keyargs)
            else:
                return jsonify(message="Missing Authorization Header"), 401

        return decorator

    return innerRole
