import jwt
from fastapi import HTTPException

SECRET_KEY = "your-secret-key"  # In a real-world scenario, this should be stored securely

def verify_token(token: str) -> bool:
    if not token:
        return False
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.PyJWTError:
        return False
