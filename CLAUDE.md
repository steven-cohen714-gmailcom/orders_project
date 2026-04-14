# Orders Project

URC Stores Orders Project — internal ordering system for Universal Recycling.

## Production Server

- **Domain**: universalrecycling.co.za
- **GCP Project**: urc-stores-orders-project (project number 462471577504)
- **VM name**: universal-recycling-google-server
- **VM zone**: africa-south1-a
- **VM IP**: ephemeral (changes on restart) — always use the domain, never hardcode IPs
- **SSH alias**: `universal-vm` (configured in ~/.ssh/config)
- **SSH key**: ~/.ssh/google_compute_engine
- **SSH user**: steven_cohen714
- **Live path on VM**: ~/orders_project
- **App**: FastAPI + Uvicorn on port 8004
- **Python venv on VM**: ~/orders_project/venv
- **Database**: ~/orders_project/data/orders.db (SQLite) — NEVER in git, NEVER delete
- **Uploads**: ~/orders_project/data/uploads/
- **Backups**: daily 3:00 AM UTC via ~/backup-urc.sh → gs://urc-orders-backups/
- **Start server**: `cd ~/orders_project && source venv/bin/activate && python3 scripts/start_server_scripts/start_server.py`
- **Stop server**: `cd ~/orders_project && source venv/bin/activate && python3 scripts/start_server_scripts/stop_server.py`

## SSH Connection

```bash
ssh universal-vm
```

If SSH times out, the VM IP has probably changed. Check the current IP:
- DNS: `dig +short universalrecycling.co.za`
- Or GCP Console → Compute Engine → VM instances

Update ~/.ssh/config HostName if the domain DNS is stale.

## GitHub

- **Repo**: https://github.com/steven-cohen714-gmailcom/orders_project
- **Repo visibility**: public

## Git Workflow

- Steven works on `stevens-branch`
- `main` is production
- Merge to main = deploy to VM

## Push to Production

When Steven says "push to production", run these steps in order:

1. `git add -A && git commit` on `stevens-branch`
2. `git push origin stevens-branch`
3. `git checkout main && git merge stevens-branch && git push origin main`
4. `git checkout stevens-branch`
5. SSH to VM: `ssh universal-vm "cd ~/orders_project && git pull origin main"`
6. If Python files or requirements changed, restart the server:
   ```bash
   ssh universal-vm "cd ~/orders_project && source venv/bin/activate && python3 scripts/start_server_scripts/stop_server.py && nohup python3 scripts/start_server_scripts/start_server.py > /dev/null 2>&1 &"
   ```
7. Wait 5 seconds, then verify the server responds:
   ```bash
   curl --silent --output /dev/null --write-out '%{http_code}' --connect-timeout 5 http://universalrecycling.co.za:8004/
   ```

## What git NEVER touches on the VM

These are in .gitignore and are machine-local:
- `data/` (database, uploads, exports, backups)
- `logs/`
- `venv/`
- `.env`
- `__pycache__/`
