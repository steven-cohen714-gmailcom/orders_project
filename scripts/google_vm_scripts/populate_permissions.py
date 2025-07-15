import sqlite3
from pathlib import Path

# Define the path to your database
DB_PATH = Path("data/orders.db")

def get_db_connection():
    """Establishes and returns a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def populate_screen_permissions(user_id: int):
    """
    Populates the screen_permissions table for a given user_id with all available screens.
    """
    all_screens = [
        "new_requisition",
        "pending_requisitions",
        "new_order",
        "pending_orders",
        "received_orders",
        "partially_delivered_orders",
        "audit_trail",
        "my_authorisations",
        "cod_orders",
        "maintenance"
    ]

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # First, delete any existing permissions for the user
            cursor.execute("DELETE FROM screen_permissions WHERE user_id = ?", (user_id,))
            print(f"Deleted existing screen permissions for user ID: {user_id}")

            # Insert new permissions for all screens
            for screen_code in all_screens:
                cursor.execute(
                    "INSERT INTO screen_permissions (user_id, screen_code) VALUES (?, ?)",
                    (user_id, screen_code)
                )
                print(f"Granted '{screen_code}' permission to user ID: {user_id}")

            conn.commit()
            print(f"Successfully populated all screen permissions for user ID: {user_id}.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    user_id_to_populate = 14
    populate_screen_permissions(user_id_to_populate)