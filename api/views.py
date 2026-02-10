# # backend/api/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .db_connection import db
# from .utils import create_user_data
# from rest_framework_simplejwt.tokens import RefreshToken
# from .utils import hash_password

# class RegisterUserView(APIView):
#     def post(self, request):
#         data = request.data
#         email = data.get('email')
#         username = data.get('username')
#         password = data.get('password')

#         # Check if user already exists in your custom collection
#         if db.custom_users.find_one({"email": email}):
#             return Response({"error": "User already exists"}, status=400)

#         # Create user object
#         new_user = create_user_data(email, username, password)
        
#         # Insert into MongoDB
#         db.custom_users.insert_one(new_user)
        
#         return Response({"message": "User registered successfully in MongoDB Atlas!"})
    

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
        
#         # 1. Find user in your custom MongoDB collection
#         user = db.custom_users.find_one({"email": email})
        
#         if user and user['password'] == hash_password(password):
#             # 2. Generate Tokens manually for this user
#             # Note: SimpleJWT usually needs a Django User object. 
#             # We pass the user ID as a custom claim.
#             refresh = RefreshToken()
#             refresh['user_id'] = str(user['_id'])
#             refresh['email'] = user['email']

#             return Response({
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "username": user['username']
#             })
        
#         return Response({"error": "Invalid Credentials"}, status=401)



from rest_framework.views import APIView
from rest_framework.response import Response
from .db_connection import db
from .utils import create_user_data, hash_password
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

class RegisterUserView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')

        if not email or not username or not password or not phone:
            return Response({"error": "Missing required fields"}, status=400)

        # Check existing user
        if db.custom_users.find_one({"email": email}):
            return Response({"error": "Email already registered"}, status=400)
        
        if db.custom_users.find_one({"phone": phone}):
            return Response({"error": "Phone number is already taken"}, status=400)

        # Create user with the full schema from utils
        new_user = create_user_data(email, username, password, phone)
        db.custom_users.insert_one(new_user)
        
        return Response({"message": "User registered successfully!"}, status=201)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = db.custom_users.find_one({"email": email})
        
        if user and user['password'] == hash_password(password):
            # Update last_login in MongoDB (Audit Requirement)
            db.custom_users.update_one(
                {"_id": user['_id']},
                {"$set": {"last_login": datetime.utcnow()}}
            )

            # Generate Tokens manually
            refresh = RefreshToken()
            refresh['user_id'] = user['user_id'] # Use the UUID string from schema
            refresh['role'] = user['role']

            user['_id'] = str(user['_id'])  # Convert MongoDB ObjectId to a serializable string
            
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user['username'],
                "user_id": user['user_id'],
                "role": user['role'],
                "user": user
            })
        
        
        return Response({"error": "Invalid email or password"}, status=401)