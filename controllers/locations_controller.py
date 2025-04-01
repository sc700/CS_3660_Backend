from fastapi import APIRouter
import json
import os
from schemas.message_schema import MessageResponse

router = APIRouter()

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../database', 'users.json')

def load_data():
    try:
        with open(DATABASE_PATH, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"error": "Database file not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON"}

@router.get("/users/{username}/items")
async def get_items(username: str):
    data = load_data()
    user = next((user for user in data["users"] if user["username"] == username), None)
    return {"items": user["items"]}