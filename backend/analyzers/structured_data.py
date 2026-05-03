import httpx
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse


VALUABLE_SCHEMAS = [
    "Organization", "WebSite", "Product", "BreadcrumbList",
    "FAQPage", "Article", "Review", "AggregateRating",
    "ItemList", "LocalBusiness", "Brand",
]


async def analyze(url: str) -> dict:
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        try:
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; Geozilla/1.0)"})
            html = r.text
        except Exception as e:
            return {"score": 0, "max": 20, "details": {"error": str(e)}}

    soup = BeautifulSoup(html, "lxml")
    found_types = []
    has_json_ld = False

    for tag in soup.find_all("script", type="application/ld+json"):
        has_json_ld = True
        try:
            data = json.loads(tag.string or "")
            items = data if isinstance(data, list) else [data]
            for item in items:
                t = item.get("@type", "")
                if isinstance(t, list):
                    found_types.extend(t)
                elif t:
                    found_types.append(t)
        except Exception:
            pass

    # Microdata fallback
    for tag in soup.find_all(attrs={"itemtype": True}):
        t = tag["itemtype"].split("/")[-1]
        if t:
            found_types.append(t)

    found_types = list(set(found_types))
    matched = [s for s in VALUABLE_SCHEMAS if s in found_types]

    # Scoring: 20 pts
    score = 0
    if has_json_ld:
        score += 4
    score += min(len(matched) * 2, 16)

    return {
        "score": score,
        "max": 20,
        "details": {
            "has_json_ld": has_json_ld,
            "schema_types_found": found_types,
            "valuable_schemas_matched": matched,
        },
    }
