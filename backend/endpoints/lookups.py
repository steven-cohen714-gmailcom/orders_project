from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging
import sqlite3

router = APIRouter()

# Configure logging
logging.basicConfig(filename="logs/server.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

@router.get("/suppliers")
async def get_suppliers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM suppliers")
        suppliers = cursor.fetchall()
        result = [{"id": s[0], "name": s[1]} for s in suppliers]
        logging.info(f"Suppliers fetched: {len(result)} items")
        return {"suppliers": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching suppliers: {str(e)}")
    finally:
        conn.close()

@router.get("/users")
async def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, rights FROM users")
        users = cursor.fetchall()
        result = [{"id": u[0], "username": u[1], "rights": u[2]} for u in users]
        logging.info(f"Users fetched: {len(result)} items")
        return {"users": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
    finally:
        conn.close()

@router.post("/users")
async def add_user(payload: dict):
    username = payload.get("username")
    password = payload.get("password")
    rights = payload.get("rights")
    if not username or not password or not rights:
        logging.error("Missing username, password or rights in add_user request")
        raise HTTPException(status_code=400, detail="Missing username, password, or rights")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Store new user (password stored as provided; implement hashing in the future)
        cursor.execute("INSERT INTO users (username, password_hash, rights) VALUES (?, ?, ?)",
                       (username, password, rights))
        conn.commit()
        logging.info(f"New user added: {username} with rights {rights}")
        return {"message": "User added successfully"}
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error adding user: {str(e)}")
        raise HTTPException(status_code=400, detail="User could not be added (possibly duplicate username).")
    except sqlite3.Error as e:
        logging.error(f"Database error adding user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error adding user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")
    finally:
        conn.close()

@router.put("/users/{user_id}")
async def update_user(user_id: int, payload: dict):
    new_username = payload.get("username")
    new_rights = payload.get("rights")
    if not new_username or not new_rights:
        logging.error("Missing username or rights in update_user request")
        raise HTTPException(status_code=400, detail="Missing username or rights")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username = ?, rights = ? WHERE id = ?", 
                       (new_username, new_rights, user_id))
        if cursor.rowcount == 0:
            logging.warning(f"No user found with id {user_id} to update")
            raise HTTPException(status_code=404, detail="User not found")
        conn.commit()
        logging.info(f"User {user_id} updated: username -> {new_username}, rights -> {new_rights}")
        return {"message": "User updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")
    finally:
        conn.close()

@router.get("/requesters")
async def get_requesters():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM requesters")
        requesters = cursor.fetchall()
        result = [{"id": r[0], "name": r[1]} for r in requesters]
        logging.info(f"Requesters fetched: {len(result)} items")
        return {"requesters": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching requesters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching requesters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching requesters: {str(e)}")
    finally:
        conn.close()

@router.post("/requesters")
async def add_requester(payload: dict):
    name = payload.get("name")
    if not name:
        logging.error("Missing name in add_requester request")
        raise HTTPException(status_code=400, detail="Missing requester name")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requesters (name) VALUES (?)", (name,))
        conn.commit()
        logging.info(f"New requester added: {name}")
        return {"message": "Requester added successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error adding requester: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error adding requester: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding requester: {str(e)}")
    finally:
        conn.close()

@router.put("/requesters/{requester_id}")
async def update_requester(requester_id: int, payload: dict):
    new_name = payload.get("name")
    if not new_name:
        logging.error("Missing name in update_requester request")
        raise HTTPException(status_code=400, detail="Missing requester name")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE requesters SET name = ? WHERE id = ?", (new_name, requester_id))
        if cursor.rowcount == 0:
            logging.warning(f"No requester found with id {requester_id}")
            raise HTTPException(status_code=404, detail="Requester not found")
        conn.commit()
        logging.info(f"Requester {requester_id} updated to: {new_name}")
        return {"message": "Requester updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating requester {requester_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating requester {requester_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating requester: {str(e)}")
    finally:
        conn.close()

@router.get("/items")
async def get_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_code, item_description FROM items")
        items = cursor.fetchall()
        result = [{"id": i[0], "item_code": i[1], "item_description": i[2]} for i in items]
        logging.info(f"Items fetched: {len(result)} items")
        return {"items": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching items: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching items: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")
    finally:
        conn.close()

@router.post("/items")
async def add_item(payload: dict):
    item_code = payload.get("item_code")
    item_description = payload.get("item_description")
    if not item_code or not item_description:
        logging.error("Missing item_code or item_description in add_item request")
        raise HTTPException(status_code=400, detail="Missing item code or description")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (item_code, item_description) VALUES (?, ?)",
                       (item_code, item_description))
        conn.commit()
        logging.info(f"New item added: {item_code} - {item_description}")
        return {"message": "Item added successfully"}
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error adding item: {str(e)}")
        raise HTTPException(status_code=400, detail="Item code might already exist.")
    except sqlite3.Error as e:
        logging.error(f"Database error adding item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error adding item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding item: {str(e)}")
    finally:
        conn.close()

@router.put("/items/{item_id}")
async def update_item(item_id: int, payload: dict):
    new_code = payload.get("item_code")
    new_description = payload.get("item_description")
    if not new_code or not new_description:
        logging.error("Missing item_code or item_description in update_item request")
        raise HTTPException(status_code=400, detail="Missing item code or description")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET item_code = ?, item_description = ? WHERE id = ?",
                       (new_code, new_description, item_id))
        if cursor.rowcount == 0:
            logging.warning(f"No item found with id {item_id}")
            raise HTTPException(status_code=404, detail="Item not found")
        conn.commit()
        logging.info(f"Item {item_id} updated: code -> {new_code}, description -> {new_description}")
        return {"message": "Item updated successfully"}
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error updating item {item_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Item code might conflict with an existing item.")
    except sqlite3.Error as e:
        logging.error(f"Database error updating item {item_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating item {item_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating item: {str(e)}")
    finally:
        conn.close()

@router.get("/projects")
async def get_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, project_code, project_name FROM projects")
        projects = cursor.fetchall()
        result = [{"id": p[0], "project_code": p[1], "project_name": p[2]} for p in projects]
        logging.info(f"Projects fetched: {len(result)} items")
        return {"projects": result}
    except sqlite3.Error as e:
        logging.error(f"Database error fetching projects: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")
    finally:
        conn.close()

@router.post("/projects")
async def add_project(payload: dict):
    project_code = payload.get("project_code")
    project_name = payload.get("project_name")
    if not project_code or not project_name:
        logging.error("Missing project_code or project_name in add_project request")
        raise HTTPException(status_code=400, detail="Missing project code or name")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (project_code, project_name) VALUES (?, ?)",
                       (project_code, project_name))
        conn.commit()
        logging.info(f"New project added: {project_code} - {project_name}")
        return {"message": "Project added successfully"}
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error adding project: {str(e)}")
        raise HTTPException(status_code=400, detail="Project code might already exist.")
    except sqlite3.Error as e:
        logging.error(f"Database error adding project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error adding project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding project: {str(e)}")
    finally:
        conn.close()

@router.put("/projects/{project_id}")
async def update_project(project_id: int, payload: dict):
    new_code = payload.get("project_code")
    new_name = payload.get("project_name")
    if not new_code or not new_name:
        logging.error("Missing project_code or project_name in update_project request")
        raise HTTPException(status_code=400, detail="Missing project code or name")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE projects SET project_code = ?, project_name = ? WHERE id = ?",
                       (new_code, new_name, project_id))
        if cursor.rowcount == 0:
            logging.warning(f"No project found with id {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        conn.commit()
        logging.info(f"Project {project_id} updated: code -> {new_code}, name -> {new_name}")
        return {"message": "Project updated successfully"}
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error updating project {project_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Project code might conflict with an existing project.")
    except sqlite3.Error as e:
        logging.error(f"Database error updating project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating project: {str(e)}")
    finally:
        conn.close()

@router.get("/settings")
async def get_settings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        rows = cursor.fetchall()
        settings = {row[0]: row[1] for row in rows} if rows else {}
        # Provide a default start order number if not set
        if "order_number_start" not in settings:
            settings["order_number_start"] = "URC1000"
        logging.info(f"Settings fetched: {settings}")
        return settings
    except sqlite3.Error as e:
        logging.error(f"Database error fetching settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching settings: {str(e)}")
    finally:
        conn.close()

@router.put("/settings")
async def update_settings(request: dict):
    key = request.get("key")
    value = request.get("value")
    if not key or value is None:
        logging.error("Missing key or value in update settings request")
        raise HTTPException(status_code=400, detail="Missing key or value")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        logging.info(f"Settings updated: {key} = {value}")
        return {"message": "Settings updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating settings: {str(e)}")
    finally:
        conn.close()

@router.get("/business_details")
async def get_business_details():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number FROM business_details LIMIT 1")
        details = cursor.fetchone()
        if not details:
            logging.warning("No business details found in database")
            raise HTTPException(status_code=404, detail="Business details not found")
        result = {
            "company_name": details[0],
            "address_line1": details[1],
            "address_line2": details[2],
            "city": details[3],
            "province": details[4],
            "postal_code": details[5],
            "telephone": details[6],
            "vat_number": details[7]
        }
        logging.info(f"Business details fetched: {result}")
        return result
    except sqlite3.Error as e:
        logging.error(f"Database error fetching business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error fetching business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching business details: {str(e)}")
    finally:
        conn.close()

@router.put("/business_details")
async def update_business_details(payload: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Update or insert the single business details record (assumes ID 1)
        cursor.execute("""
            INSERT OR REPLACE INTO business_details 
            (id, company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number) 
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            payload.get("company_name", ""), 
            payload.get("address_line1", ""), 
            payload.get("address_line2", ""), 
            payload.get("city", ""), 
            payload.get("province", ""), 
            payload.get("postal_code", ""), 
            payload.get("telephone", ""), 
            payload.get("vat_number", "")
        ))
        conn.commit()
        logging.info("Business details updated successfully")
        return {"message": "Business details updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Database error updating business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating business details: {str(e)}")
    finally:
        conn.close()
