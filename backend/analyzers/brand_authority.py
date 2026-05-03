import httpx
from urllib.parse import urlparse, quote


async def _check_url(client: httpx.AsyncClient, url: str) -> bool:
    try:
        r = await client.get(url, timeout=8, follow_redirects=True)
        return r.status_code == 200
    except Exception:
        return False


async def analyze(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    brand = domain.split(".")[0]
    details = {}

    async with httpx.AsyncClient(
        timeout=10,
        follow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0 (compatible; Geozilla/1.0)"},
    ) as client:
        # Wikipedia
        wiki_url = f"https://en.wikipedia.org/wiki/{quote(brand.capitalize())}"
        wiki_pl_url = f"https://pl.wikipedia.org/wiki/{quote(brand.capitalize())}"
        details["wikipedia_en"] = await _check_url(client, wiki_url)
        details["wikipedia_pl"] = await _check_url(client, wiki_pl_url)

        # Trustpilot
        details["trustpilot"] = await _check_url(client, f"https://www.trustpilot.com/review/{domain}")

        # YouTube channel
        details["youtube"] = await _check_url(client, f"https://www.youtube.com/@{brand}")

        # Google Business / Maps presence (proxy: check if brand appears in knowledge panel via search API — skipping, needs API key)
        # LinkedIn
        details["linkedin"] = await _check_url(client, f"https://www.linkedin.com/company/{brand}")

        # Crunchbase
        details["crunchbase"] = await _check_url(client, f"https://www.crunchbase.com/organization/{brand}")

    # Scoring: 30 pts
    score = 0
    weights = {
        "wikipedia_en": 8,
        "wikipedia_pl": 5,
        "trustpilot": 7,
        "youtube": 5,
        "linkedin": 3,
        "crunchbase": 2,
    }
    for key, pts in weights.items():
        if details.get(key):
            score += pts

    return {"score": min(score, 30), "max": 30, "details": details}
