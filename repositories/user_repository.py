from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from models.user_model import User
import hashlib


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db.get_session()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def add_user(self, user_data: dict) -> User:
        # Check for duplicate email or username
        for field in ["email", "username"]:
            result = await self.db.execute(select(User).where(getattr(User, field) == user_data[field]))
            if result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail=f"User with this {field} already exists")

        user_data["password_hash"] = self.hash_password(user_data.pop("password"))
        if "role" not in user_data:
            user_data["role"] = "User"

        user = User(**user_data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user_account(self, username: str, updated_fields: dict) -> User:
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in updated_fields.items():
            if value is not None:
                setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()