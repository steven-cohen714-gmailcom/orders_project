#!/usr/bin/env bash
set -euo pipefail

# 1) Kill any Uvicorn on port 8004
if lsof -i:8004 | grep -q LISTEN; then
  echo "⏳ Stopping old server…"
  lsof -ti:8004 | xargs kill -9
  sleep 1
else
  echo "⚠ no process on port 8004"
fi

# 2) Delete the old DB
echo "🗑 Removing old database…"
rm -f data/orders.db

# 3) Recreate all tables
echo "📦 Initializing schema…"
python3 - << 'EOF'
from backend.database import init_db
init_db()
EOF

# 4) Seed lookups (requesters, suppliers, plus you can add projects/users/items here)
echo "🌱 Seeding lookup tables…"
sqlite3 data/orders.db << 'EOF'
-- requesters
INSERT OR IGNORE INTO requesters(name) VALUES
  ('Aaron'),('Leon'),('Gert'),('Omar'),('Raymond'),('Yolandi');
-- suppliers
INSERT OR IGNORE INTO suppliers(account_number,name) VALUES
  ('SUPP001','Test Supplier');
-- projects (optional stub)
CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_code TEXT UNIQUE
);
INSERT OR IGNORE INTO projects(project_code) VALUES ('TEST');
-- users (optional stub)
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  password_hash TEXT NOT NULL,
  rights TEXT NOT NULL
);
INSERT OR IGNORE INTO users(username,password_hash,rights) VALUES ('aaron','<hash>','Edit');
-- items (optional stub)
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_code TEXT UNIQUE,
  item_description TEXT
);
INSERT OR IGNORE INTO items(item_code,item_description) VALUES ('TEST123','Integration Widget');
EOF

# 5) Start the server in the background
echo "🚀 Starting server…"
nohup python3 scripts/start_server.py &>/dev/null &

# 6) Wait for it to spin up
sleep 3

# 7) Fire off a test order (should land as ID=1)
echo "📝 Creating a test order…"
curl -s -X POST http://localhost:8004/orders \
  -H "Content-Type: application/json" \
  -d '{
    "requester_id": 1,
    "supplier_id": 1,
    "order_note": "Shell test order",
    "supplier_note": "Test supplier",
    "items": [{
      "item_code": "TEST123",
      "item_description": "Integration Widget",
      "project": "TEST",
      "qty_ordered": 3,
      "price": 9.99
    }]
  }' | jq .

# 8) Run your validation script
echo "🔍 Running validation…"
python3 scripts/validate_repaired_routes.py

echo "✅ All done!"

