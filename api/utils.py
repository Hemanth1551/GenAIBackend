# # backend/api/utils.py
# import hashlib

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def create_user_data(email, username, password):
#     return {
#         "email": email,
#         "username": username,
#         "password": hash_password(password),
#         "role": "user",
#         "created_at": None # You can add a timestamp here
#     }

import hashlib
import uuid
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_data(email, username, password, phone):
    now = datetime.utcnow()
    return {
        # Identity
        "user_id": str(uuid.uuid4()),
        "username": username,
        
        # Auth
        "email": email,
        "password": hash_password(password), # Consistent with your view's check
        "refresh_token": "",
        
        # Profile
        "phone": phone,
        
        # Security
        "role": "user",
        "is_verified": False,
        "is_active": True,
        "membership_name": "basic",

        # Audit
        "created_at": now,
        "updated_at": now,
    }