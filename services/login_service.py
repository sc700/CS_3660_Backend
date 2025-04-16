import hashlib
import jwt
import datetime
import os
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
ALGORITHM = "HS256"

class LoginService:
    def __init__(self, user_repository_factory):
        self.user_repository_factory = user_repository_factory

    async def get_login_token(self, db: AsyncSession, username: str, password: str) -> str:
        user_repository = self.user_repository_factory(db)
        user = await user_repository.get_user_by_username(username)

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def get_login_token(self, db: AsyncSession, username: str, password: str) -> str:
        user_repository = self.user_repository_factory(db)
        user = await user_repository.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != hashed_password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        payload = {
            "sub": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            "user": {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)