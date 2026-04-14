# File: backend/endpoints/lookups/projects.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.database import get_db_connection
import logging, sqlite3, csv

router = APIRouter(tags=["projects"])

# ──────────────────────────── logging ────────────────────────────
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# ──────────────────────────── helpers ────────────────────────────
def _validate_payload(payload: dict, require_both: bool = True) -> tuple[str, str]:
    """
    Extract and validate project_code & project_name from `payload`.
    If `require_both` is False (used in PUT), empty strings are allowed.
    """
    code = (payload.get("project_code") or "").strip()
    name = (payload.get("project_name") or "").strip()

    if require_both and (not code or not name):
        raise HTTPException(status_code=400,
                            detail="Project code and name are required.")

    return code, name


def _duplicate_check(conn: sqlite3.Connection, code: str, exclude_id: int | None = None):
    """
    Throw if `code` already exists (optionally excluding `exclude_id` row).
    """
    cur = conn.cursor()
    if exclude_id:
        cur.execute(
            "SELECT 1 FROM projects WHERE project_code = ? AND id != ?",
            (code, exclude_id),
        )
    else:
        cur.execute("SELECT 1 FROM projects WHERE project_code = ?", (code,))
    if cur.fetchone():
        raise HTTPException(status_code=400,
                            detail=f"Project code '{code}' already exists.")


# ───────────────────────────── routes ─────────────────────────────
@router.get("/projects")
async def list_projects():
    """Return projects newest-first."""
    try:
        with get_db_connection() as conn:
            rows = conn.execute("""
                SELECT id, project_code, project_name
                FROM projects
                ORDER BY id DESC
            """).fetchall()
            return {"projects": [dict(row) for row in rows]}
    except sqlite3.Error as e:
        logging.error("DB error list_projects: %s", e)
        raise HTTPException(500, "Database error while listing projects")


@router.post("/projects")
async def add_project(payload: dict):
    code, name = _validate_payload(payload)

    try:
        with get_db_connection() as conn:
            _duplicate_check(conn, code)
            cur = conn.execute(
                "INSERT INTO projects (project_code, project_name) VALUES (?, ?)",
                (code, name),
            )
            conn.commit()
            logging.info("Project added id=%s code=%s", cur.lastrowid, code)
            return {"message": "Project added", "id": cur.lastrowid}
    except sqlite3.Error as e:
        logging.error("DB error add_project: %s", e)
        raise HTTPException(500, "Database error while adding project")


@router.put("/projects/{project_id}")
async def update_project(project_id: int, payload: dict):
    code, name = _validate_payload(payload, require_both=True)

    try:
        with get_db_connection() as conn:
            _duplicate_check(conn, code, exclude_id=project_id)
            cur = conn.execute("""
                UPDATE projects
                   SET project_code = ?, project_name = ?
                 WHERE id = ?
            """, (code, name, project_id))
            if cur.rowcount == 0:
                raise HTTPException(404, "Project not found")
            conn.commit()
            logging.info("Project updated id=%s", project_id)
            return {"message": "Project updated"}
    except sqlite3.Error as e:
        logging.error("DB error update_project: %s", e)
        raise HTTPException(500, "Database error while updating project")


@router.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    """Hard-delete a project."""
    try:
        with get_db_connection() as conn:
            cur = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            if cur.rowcount == 0:
                raise HTTPException(404, "Project not found")
            conn.commit()
            logging.info("Project deleted id=%s", project_id)
            return {"message": "Project deleted"}
    except sqlite3.Error as e:
        logging.error("DB error delete_project: %s", e)
        raise HTTPException(500, "Database error while deleting project")


# ─────────────────────────── CSV import ───────────────────────────
@router.post("/projects/import_csv")
async def import_projects_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Only CSV files are supported")

    try:
        raw_text = (await file.read()).decode("utf-8")
        reader = csv.DictReader(raw_text.splitlines())

        rows: list[tuple[str, str]] = []
        for row in reader:
            code = (row.get("code") or "").strip()
            name = (row.get("name") or row.get("description") or "").strip()
            if code and name:
                rows.append((code, name))

        if not rows:
            raise HTTPException(400, "CSV appears empty or invalid")

        with get_db_connection() as conn:
            conn.execute("DELETE FROM projects;")
            conn.executemany(
                "INSERT INTO projects (project_code, project_name) VALUES (?, ?)",
                rows,
            )
            conn.commit()
            logging.info("Imported %s projects via CSV", len(rows))
            return {"message": f"Imported {len(rows)} projects"}
    except Exception as e:
        logging.error("Import projects CSV failed: %s", e)
        raise HTTPException(500, f"Import failed: {e}")
