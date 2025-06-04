# File: backend/endpoints/lookups/projects.py

from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.database import get_db_connection
import logging
import sqlite3
import csv

router = APIRouter()

# Configure logging
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@router.get("/projects")
async def get_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, project_code, project_name FROM projects ORDER BY id DESC")
        projects = cursor.fetchall()
        result = [{"id": p[0], "project_code": p[1], "project_name": p[2]} for p in projects]

        logging.info(f"Projects fetched: {len(result)} items")
        return { "projects": result }
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
        cursor.execute(
            "INSERT INTO projects (project_code, project_name) VALUES (?, ?)",
            (project_code, project_name)
        )
        conn.commit()
        new_id = cursor.lastrowid
        logging.info(f"New project added: {project_code} - {project_name}")
        return {
            "id": new_id,
            "project_code": project_code,
            "project_name": project_name
        }
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
        cursor.execute(
            "UPDATE projects SET project_code = ?, project_name = ? WHERE id = ?",
            (new_code, new_name, project_id)
        )
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

@router.post("/import_projects_csv")
async def import_projects_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        contents = await file.read()
        lines = contents.decode("utf-8").splitlines()
        reader = csv.DictReader(lines)

        projects = []
        for row in reader:
            code = row.get("code", "").strip()
            description = row.get("description", "").strip()
            if code and description:
                projects.append((code, description))

        if not projects:
            raise HTTPException(status_code=400, detail="CSV is empty or invalid.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects;")
        cursor.executemany(
            "INSERT INTO projects (project_code, project_name) VALUES (?, ?);",
            projects
        )
        conn.commit()
        conn.close()

        logging.info(f"✅ Imported {len(projects)} projects from CSV.")
        return {"inserted": len(projects)}

    except Exception as e:
        logging.error(f"❌ Error importing projects CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
