import hashlib
import jwt
import datetime
from models.user_model import User
from repositories.user_repository import UserRepository
from config import settings


class LoginService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    def get_user(self, username: str) -> User:
        try:
            return self.user_repository.get_user_by_username(username)
        except Exception as e:
            raise Exception(f"Failed to fetch user roles: {str(e)}")

    def get_login_token(self, username: str, password: str) -> str:
        try:
            user = self.user_repository.get_user_by_username(username)
            if not user:
                raise Exception("User not found")

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if user.password_hash != hashed_password:
                raise Exception("Invalid credentials")

            user_payload = {
                "username": user.username,
                "name": user.name,
            }

            expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

            token_payload = {
                "sub": user.username,
                "exp": expiration_time,
                "user": user_payload,
            }

            token = jwt.encode(token_payload, settings.secret_key, algorithm=settings.algorithm)
            return token
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")