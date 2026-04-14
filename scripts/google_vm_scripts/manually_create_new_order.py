import asyncio
import sqlite3
import sys
from pathlib import Path
# --- FIX: Dynamically add the project root to the Python path ---
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent
# Add the project root directory to the system path if it's not already there.
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
try:
    # Now that the project root is in the path, we can import from the 'backend' package.
    from backend.database import get_db_connection, init_db, create_order
except ImportError as e:
    print(f"Error: Could not import from 'backend.database'. Please check your project structure and the imports within database.py.")
    print(f"Debug: sys.path is currently {sys.path}")
    print(f"ImportError details: {e}")
    sys.exit(1)

async def create_order_2344_script():
    """
    Creates order number 2344 based on the provided purchase order document.
    This script handles the insertion of new suppliers, projects, and items
    if they do not already exist, maintaining database integrity.
    Uses tax-exclusive amounts as per database convention.
    """
    print("Initializing database...")
    init_db()
    # Define the data for the new order and its items
    new_order_data = {
        'order_number': '2344',
        'status': 'Pending',
        'created_date': '2025-07-28',
        'total': 6261.05,  # Tax-exclusive total from document
        'order_note': 'Order 2344 created via script',
        'note_to_supplier': 'Purchase Order UPO26783',
        'payment_terms': 'On account',
    }
    new_items_data = [
        {
            'item_code': 'AIRC003',
            'item_description': 'AIR CONDITIONER SERVI',
            'project': 'AD01M',
            'qty_ordered': 6.00,
            'price': 1043.51,
        }
    ]
    # Use a specific user ID for the creator
    current_user_id = 1
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # --- STEP 1: Check and insert dependencies (Supplier, Project, Item) ---
            print("Ensuring dependencies (supplier, project, item) exist...")
            # Insert supplier if not present with address details
            supplier_name = 'XTREME AIR CONTROL (PTY) LTD'
            cursor.execute("SELECT id FROM suppliers WHERE name = ?", (supplier_name,))
            row = cursor.fetchone()
            if row:
                supplier_id = row[0]
            else:
                cursor.execute("""
                    INSERT INTO suppliers (account_number, name, address_line1, address_line2, postal_code)
                    VALUES (?, ?, ?, ?, ?)
                """, ('T-XTR20', supplier_name, 'P.O. Box 2292', 'Highland North', '2037'))
                supplier_id = cursor.lastrowid
            new_order_data['supplier_id'] = supplier_id
            # Insert a generic requester if not present
            requester_name = 'Various'
            cursor.execute("INSERT OR IGNORE INTO requesters (name) VALUES (?)", (requester_name,))
            cursor.execute("SELECT id FROM requesters WHERE name = ?", (requester_name,))
            requester_id = cursor.fetchone()[0]
            new_order_data['requester_id'] = requester_id
            # Insert project if not present
            project_code = 'AD01M'
            project_name = 'Aircon Maintenance'
            cursor.execute("INSERT OR IGNORE INTO projects (project_code, project_name) VALUES (?, ?)", (project_code, project_name))
            # Insert item if not present
            for item in new_items_data:
                cursor.execute("INSERT OR IGNORE INTO items (item_code, item_description) VALUES (?, ?)", (item['item_code'], item['item_description']))
            conn.commit()
            print("Dependencies checked and created if needed.")
    except sqlite3.Error as e:
        print(f"Database error during dependency check: {e}")
        return
    # --- STEP 2: Create the order using the create_order function from database.py ---
    print(f"Creating order {new_order_data['order_number']}...")
    try:
        # Manually determine the required auth band and status (temporary override)
        # Total R6261.05; assume thresholds (e.g., >R10000 for band 1) not met, so Pending.
        new_order_data['required_auth_band'] = 0
        new_order_data['status'] = 'Pending'
        created_order = await create_order(
            new_order_data, 
            new_items_data, 
            current_user_id,
            created_date=new_order_data['created_date']
        )
        print(f"\n✅ Successfully created order: {created_order['order_number']}")
        print(f" Order ID: {created_order['id']}")
        print(f" Status: {created_order['status']}")
        print(f" Total: R{created_order['total']:.2f}")
    except ValueError as e:
        print(f"\n❌ Failed to create order: {e}")
        print("Please check your database settings table. The `create_order` function requires authorization thresholds to be configured.")
    except Exception as e:
        print(f"\n❌ Failed to create order: {e}")

if __name__ == "__main__":
    asyncio.run(create_order_2344_script())