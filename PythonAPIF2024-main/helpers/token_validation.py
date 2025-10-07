from flask import request
import jwt
import app_config as config

def validate_jwt():
    token = None
    user_information = None
    
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    
    if not token:
        return 400
    
    try:
        user_information = jwt.decode(token, key = config.TOKEN_SECRET, algorithms = ["HS256"])
    except:
        return 401

    return user_information