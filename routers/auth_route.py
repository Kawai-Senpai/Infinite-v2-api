from fastapi import HTTPException, Request
from functools import wraps
import jwt
import requests
from jwcrypto import jwk
from keys.keys import jwks_json, jwks_issuer

# Fetch JWKS keys
jwks_data = requests.get(jwks_json).json()
jwks_keys = {key["kid"]: key for key in jwks_data["keys"]}

def decode_jwt(token):
    headers = jwt.get_unverified_header(token)
    key = jwks_keys.get(headers["kid"])
    if not key:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    key = jwk.JWK(**key)
    payload = jwt.decode(token, key.export_to_pem(), algorithms=["RS256"], issuer=jwks_issuer)
    return payload

def clerk_auth():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Find request in kwargs or *args
            request = kwargs.pop("request", None)
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise HTTPException(status_code=400, detail="Bad Request: Missing request object.")
            
            authorization = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Unauthorized")
            
            token = authorization.split("Bearer ")[1]
            try:
                user_data = decode_jwt(token)
                # Avoid duplicates by removing keys
                kwargs.pop("user", None)
                # Re-inject user and request as keyword arguments
                kwargs["user"] = user_data
                kwargs["request"] = request
                return await func(*args, **kwargs)
            except Exception as e:
                raise HTTPException(status_code=401, detail=str(e))
        return wrapper
    return decorator