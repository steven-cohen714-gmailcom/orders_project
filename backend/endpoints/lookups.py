from fastapi import APIRouter, HTTPException
from typing import Optional
import sqlite3

router = APIRouter(prefix="/lookups", tags=["lookups"])

@router.get("/suppliers")
def get_suppliers():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM suppliers ORDER BY name")
            suppliers = [dict(row) for row in cursor.fetchall()]
        return {"suppliers": suppliers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch suppliers: {e}")

@router.get("/requesters")
def get_requesters():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM requesters ORDER BY name")
            requesters = [dict(row) for row in cursor.fetchall()]
        return {"requesters": requesters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch requesters: {e}")

@router.post("/requesters")
def add_requester(name: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO requesters (name) VALUES (?)", (name,))
            conn.commit()
        return {"status": "Requester added"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Requester name already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add requester: {e}")

@router.put("/requesters/{id}")
def update_requester(id: int, name: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE requesters SET name = ? WHERE id = ?", (name, id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Requester not found")
        return {"status": "Requester updated"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Requester name already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update requester: {e}")

@router.get("/items")
def get_items():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items ORDER BY item_code")
            items = [dict(row) for row in cursor.fetchall()]
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {e}")

@router.post("/items")
def add_item(item_code: str, item_description: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (item_code, item_description) VALUES (?, ?)", (item_code, item_description))
            conn.commit()
        return {"status": "Item added"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Item code already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add item: {e}")

@router.put("/items/{id}")
def update_item(id: int, item_code: str, item_description: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE items SET item_code = ?, item_description = ? WHERE id = ?", (item_code, item_description, id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Item not found")
        return {"status": "Item updated"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Item code already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update item: {e}")

@router.get("/projects")
def get_projects():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects ORDER BY project_code")
            projects = [dict(row) for row in cursor.fetchall()]
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {e}")

@router.post("/projects")
def add_project(project_code: str, project_name: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO projects (project_code, project_name) VALUES (?, ?)", (project_code, project_name))
            conn.commit()
        return {"status": "Project added"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Project code already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add project: {e}")

@router.put("/projects/{id}")
def update_project(id: int, project_code: str, project_name: str):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE projects SET project_code = ?, project_name = ? WHERE id = ?", (project_code, project_name, id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Project not found")
        return {"status": "Project updated"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Project code already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update project: {e}")

@router.get("/users")
def get_users():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, rights FROM users ORDER BY username")
            users = [dict(row) for row in cursor.fetchall()]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {e}")

@router.post("/users")
def add_user(user: dict):
    username = user.get("username")
    password = user.get("password")
    rights = user.get("rights")
    if not username or not password or not rights:
        raise HTTPException(status_code=400, detail="Missing required fields: username, password, rights")
    if rights not in ["edit", "view", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid rights value")
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash, rights) VALUES (?, ?, ?)", (username, password, rights))
            conn.commit()
        return {"status": "User added"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add user: {e}")

@router.put("/users/{id}")
def update_user(id: int, user: dict):
    username = user.get("username")
    rights = user.get("rights")
    if not username or not rights:
        raise HTTPException(status_code=400, detail="Missing required fields: username, rights")
    if rights not in ["edit", "view", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid rights value")
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username = ?, rights = ? WHERE id = ?", (username, rights, id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        return {"status": "User updated"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {e}")

@router.get("/settings")
def get_settings():
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM settings WHERE key IN ('order_number_start', 'auth_threshold')")
            settings = {row["key"]: row["value"] for row in cursor.fetchall()}
            # Provide defaults if settings are not found
            if "order_number_start" not in settings:
                settings["order_number_start"] = "URC0001"
            if "auth_threshold" not in settings:
                settings["auth_threshold"] = "10000"
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch settings: {e}")

@router.put("/settings")
def update_setting(setting: dict):
    key = setting.get("key")
    value = setting.get("value")
    if not key or not value:
        raise HTTPException(status_code=400, detail="Missing required fields: key, value")
    try:
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
            conn.commit()
        return {"status": "Setting updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update setting: {e}")