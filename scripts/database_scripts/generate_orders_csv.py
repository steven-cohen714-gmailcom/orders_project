import sqlite3
import csv
from pathlib import Path
from datetime import datetime
import os

def generate_orders_csv():
    # Get the directory of the current script
    script_dir = Path(__file__).parent.resolve()
    # Go up to the project root (assuming script is in scripts/database_scripts)
    project_root = script_dir.parent.parent # .parent from 'database_scripts' to 'scripts', then .parent to 'orders_project'
    
    # Define the database path relative to the project root
    db_path = project_root / "data" / "orders.db"
    
    # Define the output CSV file path to the Desktop
    desktop_path = Path.home() / "Desktop"
    output_csv_filename = f"universal_recycling_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output_csv_path = desktop_path / output_csv_filename

    # Debugging print statements (you can remove these once it works)
    print(f"DEBUG: Script directory: {script_dir}")
    print(f"DEBUG: Project root: {project_root}")
    print(f"DEBUG: Attempting to open database at: {db_path}")
    print(f"DEBUG: Output CSV will be saved to: {output_csv_path}")


    conn = None
    try:
        # Check if database file exists before trying to connect
        if not db_path.exists():
            raise FileNotFoundError(f"Database file not found at: {db_path}")
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row # Allows accessing columns by name
        cursor = conn.cursor()

        # Query to get main order details
        cursor.execute("""
            SELECT
                o.id AS order_id,
                o.order_number,
                o.created_date,
                s.name AS supplier_name
            FROM orders o
            LEFT JOIN suppliers s ON o.supplier_id = s.id
            ORDER BY o.created_date DESC, o.order_number DESC
        """)
        orders = cursor.fetchall()

        if not orders:
            print("No orders found in the database to generate a report.")
            return

        # Prepare data for CSV
        csv_data = []
        # CSV Header
        csv_data.append([
            "Order ID",
            "Order Number",
            "Order Date",
            "Supplier Name",
            "Items Ordered" # This column will contain all line items concatenated
        ])

        for order in orders:
            order_id = order["order_id"]
            order_number = order["order_number"]
            order_date = order["created_date"]
            supplier_name = order["supplier_name"]

            # Fetch all items for the current order
            cursor.execute("""
                SELECT
                    item_code,
                    item_description,
                    project,
                    qty_ordered,
                    price
                FROM order_items
                WHERE order_id = ?
                ORDER BY id ASC
            """, (order_id,))
            items = cursor.fetchall()

            items_ordered_str = ""
            if items:
                # Format each item into a string and join them
                item_strings = []
                for item in items:
                    # Example format: "ITEM001 - Description (ProjectX): 5 x R10.00"
                    item_desc_part = item['item_description'] if item['item_description'] else "N/A"
                    project_part = f" (Prj: {item['project']})" if item['project'] else ""
                    
                    item_strings.append(
                        f"{item['item_code']} - {item_desc_part}{project_part}: "
                        f"{item['qty_ordered']} x R{item['price']:.2f}"
                    )
                items_ordered_str = "; ".join(item_strings)
            else:
                items_ordered_str = "No items"

            csv_data.append([
                order_id,
                order_number,
                order_date,
                supplier_name,
                items_ordered_str
            ])
        
        # Write to CSV file
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(csv_data)

        print(f"✅ CSV report generated successfully to: {output_csv_path}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure 'orders.db' exists in the 'data' directory relative to your project root.")
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        print("Please ensure the database file is not locked or corrupted.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    generate_orders_csv()