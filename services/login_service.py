import hashlib
import jwt
import datetime
import os
from repositories.user_repository import UserRepository
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

class LoginService:
    # Function to verify a jwt token
    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            # Decode token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
        
    # Function to verify login from users.json
    @staticmethod
    def get_login_token(username: str, password: str) -> str:
        try:
            # Fetch user from database
            user = UserRepository.get_user_by_username(username)
            if not user:
                raise Exception("User not found")

            # Hash input password using SHA256
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Verify password match
            if user.password_hash != hashed_password:
                raise Exception("Invalid credentials")
            
            user_payload = {
                "username": user.username,
                "name": user.name
            }

            # Generate JWT token
            expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
            token_payload = {
                "sub": user.username,  # Subject (user)
                "exp": expiration_time,  # Expiry time
                "user": user_payload  # Include role or other user attributes if needed
            }
            token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

            return token
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")