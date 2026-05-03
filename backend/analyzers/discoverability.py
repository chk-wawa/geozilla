import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse


async def analyze(url: str) -> dict:
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    details = {}

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        # Sitemap
        sitemap_found = False
        for path in ["/sitemap.xml", "/sitemap_index.xml", "/sitemap/"]:
            try:
                r = await client.get(f"{base}{path}")
                if r.status_code == 200 and ("xml" in r.headers.get("content-type", "") or "<sitemap" in r.text or "<urlset" in r.text):
                    sitemap_found = True
                    break
            except Exception:
                pass
        details["sitemap_found"] = sitemap_found

        # Page-level signals
        try:
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; Geozilla/1.0)"})
            html = r.text
            details["https"] = url.startswith("https")
        except Exception as e:
            return {"score": 0, "max": 15, "details": {"error": str(e)}}

    soup = BeautifulSoup(html, "lxml")

    meta_desc = soup.find("meta", attrs={"name": "description"})
    details["meta_description"] = bool(meta_desc and meta_desc.get("content"))

    canonical = soup.find("link", rel="canonical")
    details["canonical_tag"] = bool(canonical)

    hreflang = soup.find("link", rel="alternate", hreflang=True)
    details["hreflang"] = bool(hreflang)

    title = soup.find("title")
    details["title_tag"] = bool(title and title.text.strip())

    og_tags = soup.find_all("meta", property=lambda v: v and v.startswith("og:"))
    details["open_graph"] = len(og_tags) >= 3

    # Scoring: 15 pts
    score = 0
    if details.get("sitemap_found"):
        score += 4
    if details.get("meta_description"):
        score += 2
    if details.get("canonical_tag"):
        score += 2
    if details.get("title_tag"):
        score += 2
    if details.get("https"):
        score += 3
    if details.get("open_graph"):
        score += 2

    return {"score": min(score, 15), "max": 15, "details": details}
