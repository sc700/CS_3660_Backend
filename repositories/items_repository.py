import json
import os
from fastapi import HTTPException

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../database', 'users.json')

def load_data():
    try:
        with open(DATABASE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Database file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON")

def save_data(data):
    try:
        with open(DATABASE_PATH, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_user_items(username: str):
    data = load_data()
    user = next((user for user in data.get("users", []) if user.get("username") == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.get("items", [])

def add_user_item(username: str, item: dict):
    data = load_data()
    user = next((user for user in data.get("users", []) if user.get("username") == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not item.get("id"):
        current_ids = [existing_item.get("id", 0) for existing_item in user.get("items", [])]
        item["id"] = max(current_ids, default=0) + 1
    else:
        if any(existing_item.get("id") == item["id"] for existing_item in user.get("items", [])):
            raise HTTPException(status_code=400, detail="Item ID already exists")
    
    user.setdefault("items", []).append(item)
    save_data(data)
    return item

def get_location_history(username: str):
    data = load_data()
    user = next((u for u in data.get("users", []) if u.get("username") == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    history = [item for item in user.get("items", []) if "history" in item]
    return history

def delete_user_item(username: str, item_id: int):
    """
    Delete an item for a specific user by its ID.
    """
    data = load_data()
    user = next((user for user in data.get("users", []) if user.get("username") == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    items = user.get("items", [])
    if not any(item.get("id") == item_id for item in items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    user["items"] = [item for item in items if item.get("id") != item_id]
    save_data(data)
    return True

def update_user_item(username: str, item_id: int, updated_item: dict):
    data = load_data()
    user = next((u for u in data.get("users", []) if u.get("username") == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    items = user.get("items", [])
    for idx, item in enumerate(items):
        if item.get("id") == item_id:
            for key, value in updated_item.items():
                if value is not None:
                    items[idx][key] = value
            save_data(data)
            return items[idx]
    
    raise HTTPException(status_code=404, detail="Item not found")