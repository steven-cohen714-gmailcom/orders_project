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
- **Start server**: `cd ~/orders_project && source venv/bin/activate && python3 scripts/start_server_scripts/start_server.py`
- **Stop server**: `cd ~/orders_project && source venv/bin/activate && python3 scripts/start_server_scripts/stop_server.py`

## VM Storage

The VM uses a GCP persistent disk (network-attached storage, not RAM). On VM restart:
- Disk survives — all files, database, uploads stay intact
- RAM is cleared — any in-memory state is lost
- External IP changes (ephemeral) — always use the domain name, never hardcode IPs

Data would only be lost if the VM is deleted (with its disk) or disk failure (rare on GCP).

## Backups

- **Cron**: daily 3:00 AM UTC via `~/backup-urc.sh`
- **Destination**: `gs://urc-orders-backups/` (Google Cloud Storage)
- **Retention**: 7 days — the script auto-deletes older backups after each run
- **What's backed up**:
  - `data/orders.db` — SQLite database (safe online copy via `sqlite3 .backup`)
  - `data/uploads/` — invoices, delivery notes, quotes (1,600+ PDFs)
  - `data/pdfs/` — generated order PDFs
- **What's NOT backed up**: `data/printouts/`, `data/exports/`, `logs/`

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

## Email System

- **Provider**: Mimecast SMTP (`za-smtp-outbound-1.mimecast.co.za`, port 587, STARTTLS)
- **From address**: aaron@urc.co.za
- **BCC**: aaron@urc.co.za (copy of every outgoing email)
- **Config**: all email settings are in `.env` on the VM (SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_DRY_RUN, etc.)
- **Dry run mode**: set `EMAIL_DRY_RUN=1` in `.env` to log emails to file instead of sending. Production has it set to `0` (live).
- **Code**:
  - `backend/utils/send_email.py` — low-level SMTP sender, supports plain text and HTML (multipart)
  - `backend/utils/email_and_alerts_engine.py` — email logic, templates, and triggers (calls send_email)
  - `backend/endpoints/email.py` — email-related API endpoints

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
