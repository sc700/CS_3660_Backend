import json, os
from typing import Optional
from schemas.user_schema import User
from fastapi import HTTPException
import hashlib


DATABASE_PATH = os.path.join(os.path.dirname(__file__), "../database", "users.json")

class UserRepository:
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        try:
            with open("database/users.json", "r") as file:
                data = json.load(file)
                for user in data["users"]:
                    if user["username"] == username:
                        user.setdefault("items", [])
                        return User(**user)
        except FileNotFoundError:
            raise Exception("User file not found")

        return None
    

def load_data():
    try:
        with open(DATABASE_PATH, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def save_data(data):
    try:
        with open(DATABASE_PATH, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_user_by_username(username: str):
    data = load_data()
    return next((user for user in data.get("users", []) if user.get("username") == username), None)

def update_user_account(username: str, updated_fields: dict):
    data = load_data()
    user = next((user for user in data.get("users", []) if user.get("username") == username), None)
    if not user:
        return None
    for key, value in updated_fields.items():
        if value is not None:
            user[key] = value
    save_data(data)
    return user

def hash_password(password: str) -> str:
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(new_user_data: dict):
    """
    Expects new_user_data to include:
      - name (str)
      - email (str)
      - password (str)
      - username (str)
    """
    data = load_data()
    users = data.get("users", [])

    if any(u.get("email") == new_user_data.get("email") for u in users):
        raise HTTPException(status_code=400, detail="User with this email already exists")
    if any(u.get("username") == new_user_data.get("username") for u in users):
        raise HTTPException(status_code=400, detail="User with this username already exists")

    plain_password = new_user_data.pop("password")
    new_user_data["password_hash"] = hash_password(plain_password)

    new_id = max([u.get("id", 0) for u in users] or [0]) + 1
    new_user_data["id"] = new_id

    new_user_data.setdefault("role", "User")
    new_user_data.setdefault("items", [])

    users.append(new_user_data)
    data["users"] = users
    save_data(data)
    return new_user_data