from fastapi import APIRouter, HTTPException, Query
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

router = APIRouter(prefix="/supplier_lookup", tags=["supplier_lookup"])

# Log file path
LOG_FILE = Path(__file__).resolve().parent.parent.parent / "logs" / "supplier_lookup_debug.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_debug(entry: dict):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"\n[{timestamp}]\n")
        for k, v in entry.items():
            if isinstance(v, str) and len(v) > 1000:
                v = v[:1000] + "... (truncated)"
            f.write(f"{k}: {v}\n")

@router.get("")
def lookup_alternatives(query: str = Query(..., min_length=2)):
    log_debug({"💥 ROUTE HIT": f"query = {query}"})

    try:
        search_url = f"https://www.builders.co.za/search/?text={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}

        resp = requests.get(search_url, headers=headers)
        log_debug({
            "Fetched URL": search_url,
            "HTTP Status": resp.status_code,
            "First 1000 characters of response": resp.text
        })

        if resp.status_code != 200:
            raise Exception(f"Builders returned status {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []

        for product in soup.select(".product-grid .product-tile")[:5]:
            title_el = product.select_one(".product-title")
            price_el = product.select_one(".price")
            link_el = product.select_one("a")

            if not (title_el and price_el and link_el):
                continue

            results.append({
                "title": title_el.text.strip(),
                "price": price_el.text.strip(),
                "link": "https://www.builders.co.za" + link_el.get("href")
            })

        if not results:
            raise Exception("No products matched or structure changed")

        return {"results": results}

    except Exception as e:
        log_debug({"Exception": str(e)})
        raise HTTPException(status_code=500, detail=f"Lookup failed: {str(e)}")
