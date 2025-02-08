from fastapi import Depends, HTTPException, Request
import jwt
import requests
from jwcrypto import jwk
from keys.keys import jwks_json, jwks_issuer

# Fetch JWKS keys
jwks_data = requests.get(jwks_json).json()
jwks_keys = {key["kid"]: key for key in jwks_data["keys"]}

def decode_jwt(token: str):
    headers = jwt.get_unverified_header(token)
    key = jwks_keys.get(headers["kid"])
    if not key:
        raise HTTPException(status_code=401, detail="Invalid token")

    key = jwk.JWK(**key)
    return jwt.decode(token, key.export_to_pem(), algorithms=["RS256"], issuer=jwks_issuer)

async def get_current_user(request: Request):
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split("Bearer ")[1]
    try:
        return decode_jwt(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
