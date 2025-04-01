'''
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import json, os

router = APIRouter(prefix="/api/access-control", tags=["Access Control"])

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "../database", "users.json")

# Pydantic model for user (for add user)
class User(BaseModel):
    id: int = None
    name: str
    email: str
    role: str

def load_data():
    try:
        with open(DATABASE_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def save_data(data):
    try:
        with open(DATABASE_PATH, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET: Retrieve all users
@router.get("/users")
async def get_users():
    data = load_data()
    return {"users": data.get("users", [])}

# POST: Add a new user
@router.post("/users", status_code=status.HTTP_201_CREATED)
async def add_user(user: User):
    data = load_data()
    if any(existing["email"] == user.email for existing in data.get("users", [])):
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = user.dict()
    new_user["id"] = max([u["id"] for u in data.get("users", [])] or [0]) + 1
    new_user["items"] = []  # Initialize items if needed
    data["users"].append(new_user)
    save_data(data)
    return {"user": new_user}

# PUT: Update a user's role
@router.put("/users/{id}")
async def update_user_role(id: int, role_update: dict):
    data = load_data()
    user = next((u for u in data.get("users", []) if u["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_role = role_update.get("role")
    if not new_role:
        raise HTTPException(status_code=400, detail="Role not provided")
    user["role"] = new_role
    save_data(data)
    return {"role": user["role"]}

# DELETE: Remove a user
@router.delete("/users/{id}")
async def delete_user(id: int):
    data = load_data()
    users = data.get("users", [])
    user = next((u for u in users if u["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data["users"] = [u for u in users if u["id"] != id]
    save_data(data)
    return {"message": "User removed successfully"}'
'''