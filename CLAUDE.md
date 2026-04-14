# Orders Project

## Push to Production

When Steven says "push to production", run these steps in order:

1. `git add -A && git commit` on `stevens-branch`
2. `git push origin stevens-branch`
3. `git checkout main && git merge stevens-branch && git push origin main`
4. `git checkout stevens-branch`
5. SSH to VM: `ssh universal-vm "cd ~/orders_project && git pull origin main"`
6. SSH to VM: restart server only if Python files changed:
   `ssh universal-vm "cd ~/orders_project && source venv/bin/activate && python3 scripts/start_server_scripts/stop_server.py && nohup python3 scripts/start_server_scripts/start_server.py > /dev/null 2>&1 &"`
7. Wait 5 seconds, then verify the server responds:
   `curl --silent --output /dev/null --write-out '%{http_code}' --connect-timeout 5 http://universalrecycling.co.za:8004/`

## Production Server

- Host: universalrecycling.co.za (GCP VM, SSH alias: universal-vm)
- User: steven_cohen714
- Live path: ~/orders_project
- App: FastAPI on port 8004
- Database: ~/orders_project/data/orders.db (SQLite) - NEVER in git
- Backups: daily 3am UTC to gs://urc-orders-backups/ via ~/backup-urc.sh
- venv, data/, logs/, .env are machine-local and excluded from git

## Git Workflow

- Steven works on `stevens-branch`
- `main` is production
- Merge to main = deploy to VM
