import jwt, os, uuid
from datetime import datetime, timedelta
SECRET = os.getenv("JWT_SECRET", "sovereign-super-secret-key-change-in-prod")

def create_token(user_id):
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(days=30)}
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None

def gen_api_key():
    return "sk_" + uuid.uuid4().hex[:24]
