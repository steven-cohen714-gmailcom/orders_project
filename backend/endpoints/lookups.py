from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database import get_db_connection
import sqlite3
import logging

# Logging setup
logging.basicConfig(
    filename="logs/lookups_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

router = APIRouter(prefix="/lookups", tags=["lookups"])

@router.get("/users")
def get_users():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, rights FROM users")
        users = [dict(row) for row in cursor.fetchall()]
    return {"users": users}

class UserCreate(BaseModel):
    username: str
    password: str
    rights: str

@router.post("/users")
def create_user(user: UserCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, rights) VALUES (?, ?, ?)",
                (user.username, user.password, user.rights)
            )
            conn.commit()
        return {"status": "User created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET username = ?, rights = ? WHERE id = ?",
                (user.username, user.rights, user_id)
            )
            conn.commit()
        return {"status": "User updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/requesters")
def get_requesters():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM requesters")
        requesters = [dict(row) for row in cursor.fetchall()]
    return {"requesters": requesters}

class RequesterCreate(BaseModel):
    name: str

@router.post("/requesters")
def create_requester(requester: RequesterCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO requesters (name) VALUES (?)", (requester.name,))
            conn.commit()
        return {"status": "Requester created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create requester: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/requesters/{requester_id}")
def update_requester(requester_id: int, requester: RequesterCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE requesters SET name = ? WHERE id = ?", (requester.name, requester_id))
            conn.commit()
        return {"status": "Requester updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update requester: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/suppliers")
def get_suppliers():
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM suppliers")
            suppliers = [dict(row) for row in cursor.fetchall()]
        return {"suppliers": suppliers}
    except sqlite3.Error as e:
        logging.error(f"Failed to fetch suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class SupplierCreate(BaseModel):
    name: str

@router.post("/suppliers")
def create_supplier(supplier: SupplierCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO suppliers (name) VALUES (?)", (supplier.name,))
            conn.commit()
        return {"status": "Supplier created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create supplier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/suppliers/{supplier_id}")
def update_supplier(supplier_id: int, supplier: SupplierCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE suppliers SET name = ? WHERE id = ?", (supplier.name, supplier_id))
            conn.commit()
        return {"status": "Supplier updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update supplier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/items")
def get_items():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_code, item_description FROM items")
        items = [dict(row) for row in cursor.fetchall()]
    return {"items": items}

class ItemCreate(BaseModel):
    item_code: str
    item_description: str

@router.post("/items")
def create_item(item: ItemCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (item_code, item_description) VALUES (?, ?)",
                (item.item_code, item.item_description)
            )
            conn.commit()
        return {"status": "Item created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE items SET item_code = ?, item_description = ? WHERE id = ?",
                (item.item_code, item.item_description, item_id)
            )
            conn.commit()
        return {"status": "Item updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/projects")
def get_projects():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, project_code, project_name FROM projects")
        projects = [dict(row) for row in cursor.fetchall()]
    return {"projects": projects}

class ProjectCreate(BaseModel):
    project_code: str
    project_name: str

@router.post("/projects")
def create_project(project: ProjectCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO projects (project_code, project_name) VALUES (?, ?)",
                (project.project_code, project.project_name)
            )
            conn.commit()
        return {"status": "Project created"}
    except sqlite3.Error as e:
        logging.error(f"Failed to create project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/projects/{project_id}")
def update_project(project_id: int, project: ProjectCreate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE projects SET project_code = ?, project_name = ? WHERE id = ?",
                (project.project_code, project.project_name, project_id)
            )
            conn.commit()
        return {"status": "Project updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/settings")
def get_settings():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        settings = dict(cursor.fetchall())
    return settings

class SettingUpdate(BaseModel):
    key: str
    value: str

@router.put("/settings")
def update_setting(setting: SettingUpdate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (setting.key, setting.value))
            conn.commit()
        return {"status": "Setting updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update setting: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/business_details")
def get_business_details():
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                FROM business_details WHERE id = 1
            """)
            row = cursor.fetchone()
            if not row:
                return {
                    "company_name": "",
                    "address_line1": "",
                    "address_line2": "",
                    "city": "",
                    "province": "",
                    "postal_code": "",
                    "telephone": "",
                    "vat_number": ""
                }
            return dict(row)
    except sqlite3.Error as e:
        logging.error(f"Failed to fetch business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class BusinessDetailsUpdate(BaseModel):
    company_name: str
    address_line1: str
    address_line2: str
    city: str
    province: str
    postal_code: str
    telephone: str
    vat_number: str

@router.put("/business_details")
def update_business_details(details: BusinessDetailsUpdate):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO business_details (
                    id, company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                details.company_name,
                details.address_line1,
                details.address_line2,
                details.city,
                details.province,
                details.postal_code,
                details.telephone,
                details.vat_number
            ))
            conn.commit()
        return {"status": "Business details updated"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update business details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")