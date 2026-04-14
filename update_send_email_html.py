#!/usr/bin/env python3
# Script to update send_email.py to support HTML emails

content = """# File: backend/utils/send_email.py
from __future__ import annotations

import os
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Iterable, List, Union, Optional
from dotenv import load_dotenv
load_dotenv()

# --- Env helpers ------------------------------------------------------------
def _getenv(name: str, default: str = "") -> str:
    v = os.getenv(name)
    return v if v is not None else default

EMAIL_FROM      = _getenv("EMAIL_FROM", "no-reply@example.com")
EMAIL_REPLY_TO  = _getenv("EMAIL_REPLY_TO", EMAIL_FROM)
EMAIL_BCC_DEF   = _getenv("EMAIL_BCC_DEFAULT", "").strip()
EMAIL_TRANSPORT = _getenv("EMAIL_TRANSPORT", "smtp").lower()
EMAIL_DRY_RUN   = _getenv("EMAIL_DRY_RUN", "1").strip().lower()  # "1"/"true"/"yes"/"on" => don't actually send
EMAIL_LOG_FILE  = _getenv("EMAIL_LOG_FILE", "logs/email_dispatch_log.txt")

SMTP_HOST       = _getenv("SMTP_HOST", "smtp.office365.com")
SMTP_PORT       = int(_getenv("SMTP_PORT", "587"))
SMTP_USERNAME   = _getenv("SMTP_USERNAME", "")
SMTP_PASSWORD   = _getenv("SMTP_PASSWORD", "")
SMTP_TIMEOUT    = int(_getenv("SMTP_TIMEOUT", "20"))

# --- Small utils ------------------------------------------------------------
def _truthy(s: str) -> bool:
    return s.lower() in {"1", "true", "yes", "on"}

def _ensure_parent_dir(p: Union[str, Path]) -> Path:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def _coerce_to_list(to: Union[str, Iterable[str]]) -> List[str]:
    if isinstance(to, str):
        return [to]
    # filter empties/None
    return [x for x in to if x]

# --- Dry-run file writer ----------------------------------------------------
def _write_dryrun_log(to: List[str], subject: str, body: str) -> None:
    path = _ensure_parent_dir(EMAIL_LOG_FILE)
    try:
        with path.open("a", encoding="utf-8") as f:
            f.write("\\n" + "-"*80 + "\\n")
            f.write("DRY-RUN EMAIL (not sent)\\n")
            f.write(f"From:     {EMAIL_FROM}\\n")
            f.write(f"To:       {', '.join(to) if to else '(no recipients)'}\\n")
            if EMAIL_BCC_DEF:
                f.write(f"Bcc:      {EMAIL_BCC_DEF}\\n")
            f.write(f"Reply-To: {EMAIL_REPLY_TO}\\n")
            f.write(f"Subject:  {subject}\\n")
            f.write("-"*80 + "\\n")
            f.write((body or "").rstrip() + "\\n")
    except Exception as e:
        # last-resort stderr so we still see failures when logging fails
        print(f"[send_email.py] DRY-RUN log write failed: {e}")

# --- SMTP sender ------------------------------------------------------------
def _send_via_smtp(to: List[str], subject: str, body: str, html_body: Optional[str] = None) -> None:
    if html_body:
        # Send multipart email with both plain text and HTML
        msg = MIMEMultipart('alternative')
        msg["From"] = EMAIL_FROM
        msg["To"] = ", ".join(to)
        if EMAIL_BCC_DEF:
            msg["Bcc"] = EMAIL_BCC_DEF
        msg["Reply-To"] = EMAIL_REPLY_TO
        msg["Subject"] = subject

        # Attach plain text and HTML parts
        part1 = MIMEText(body or "", 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
    else:
        # Send plain text email
        msg = EmailMessage()
        msg["From"] = EMAIL_FROM
        msg["To"] = ", ".join(to)
        if EMAIL_BCC_DEF:
            msg["Bcc"] = EMAIL_BCC_DEF
        msg["Reply-To"] = EMAIL_REPLY_TO
        msg["Subject"] = subject
        msg.set_content(body or "", subtype="plain")

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
        server.ehlo()
        # STARTTLS for 587
        if SMTP_PORT == 587:
            server.starttls(context=context)
            server.ehlo()
        if SMTP_USERNAME and SMTP_PASSWORD:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        # Combine To + Bcc for actual delivery list
        rcpts = list(to)
        if EMAIL_BCC_DEF:
            rcpts.append(EMAIL_BCC_DEF)
        server.send_message(msg, from_addr=EMAIL_FROM, to_addrs=rcpts)

# --- Public API (sync, list-friendly) --------------------------------------
def send_email(to: Union[str, Iterable[str]], subject: str, body: str, html_body: Optional[str] = None) -> None:
    \"\"\"
    Transport used by the email engine.

    - Accepts a single address (str) or list/iterable of addresses.
    - If EMAIL_DRY_RUN is truthy: append the full message to EMAIL_LOG_FILE and return.
    - Else, with EMAIL_TRANSPORT=smtp: send via SMTP settings above.
    - On unknown transport: fall back to dry-run file so we never lose the message.
    - html_body: Optional HTML version of the email (sends multipart with both plain and HTML)
    \"\"\"
    to_list = _coerce_to_list(to)
    if _truthy(EMAIL_DRY_RUN) or EMAIL_TRANSPORT not in {"smtp"}:
        # Always write dry-run (or fallback) for visibility
        if EMAIL_TRANSPORT not in {"smtp"} and not _truthy(EMAIL_DRY_RUN):
            body = f"[UNKNOWN TRANSPORT: {EMAIL_TRANSPORT}]\\n\\n{body or ''}"
        _write_dryrun_log(to_list, subject or "", body or "")
        return

    # Live send via SMTP
    _send_via_smtp(to_list, subject or "", body or "", html_body=html_body)
"""

with open('/home/steven_cohen714/orders_project/backend/utils/send_email.py', 'w') as f:
    f.write(content)

print("✅ send_email.py updated to support HTML emails")
