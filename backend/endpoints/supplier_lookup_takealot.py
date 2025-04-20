from fastapi import APIRouter, HTTPException, Query
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

router = APIRouter(prefix="/supplier_lookup_takealot", tags=["supplier_lookup"])

LOG_FILE = Path(__file__).resolve().parent.parent.parent / "logs" / "takealot_lookup.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

SCRAPER_API_KEY = "f272c508f0e84b88ac0fa928d4acdda"

def log_debug(entry: dict):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"\n[{timestamp}]\n")
        for k, v in entry.items():
            if isinstance(v, str) and len(v) > 1000:
                v = v[:1000] + "... (truncated)"
            f.write(f"{k}: {v}\n")

@router.get("")
def lookup_takealot(query: str = Query(..., min_length=2)):
    try:
        target_url = f"https://www.takealot.com/all?q={query.replace(' ', '+')}"
        scraper_url = (
            f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}"
            f"&url={target_url}"
        )

        resp = requests.get(scraper_url)
        log_debug({
            "Target URL": target_url,
            "Scraper URL": scraper_url,
            "HTTP Status": resp.status_code,
            "HTML Preview": resp.text
        })

        if resp.status_code != 200:
            raise Exception(f"ScraperAPI returned {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        product_cards = soup.select("div[data-product-id]")

        results = []
        for card in product_cards[:5]:
            title_el = card.select_one("div[data-testid='product-title']")
            price_el = card.select_one("span.currency")
            link_el = card.select_one("a[href]")

            if not (title_el and link_el):
                continue

            results.append({
                "title": title_el.text.strip(),
                "price": price_el.text.strip() if price_el else "N/A",
                "link": "https://www.takealot.com" + link_el["href"]
            })

        if not results:
            raise Exception("No products matched or structure changed")

        return {"results": results}

    except Exception as e:
        log_debug({"Exception": str(e)})
        raise HTTPException(status_code=500, detail=f"Lookup failed: {str(e)}")
