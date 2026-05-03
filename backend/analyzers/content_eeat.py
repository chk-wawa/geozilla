import httpx
import re
from bs4 import BeautifulSoup


async def analyze(url: str) -> dict:
    details = {}

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        try:
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; Geozilla/1.0)"})
            html = r.text
        except Exception as e:
            return {"score": 0, "max": 20, "details": {"error": str(e)}}

    soup = BeautifulSoup(html, "lxml")

    # Heading hierarchy
    h1s = soup.find_all("h1")
    h2s = soup.find_all("h2")
    h3s = soup.find_all("h3")
    details["h1_count"] = len(h1s)
    details["h2_count"] = len(h2s)
    details["h3_count"] = len(h3s)
    details["good_heading_structure"] = len(h1s) == 1 and len(h2s) >= 2

    # FAQ detection
    text = soup.get_text(" ", strip=True).lower()
    faq_signals = ["faq", "frequently asked", "pytania", "odpowiedzi"]
    details["faq_detected"] = any(s in text for s in faq_signals)

    # About/contact pages linked
    links = [a.get("href", "").lower() for a in soup.find_all("a", href=True)]
    details["about_page_linked"] = any("about" in l or "o-nas" in l or "o nas" in l for l in links)
    details["contact_page_linked"] = any("contact" in l or "kontakt" in l for l in links)

    # Author bylines
    author_tags = soup.find_all(attrs={"rel": "author"}) + soup.find_all(attrs={"class": re.compile(r"author|byline", re.I)})
    details["author_signals"] = len(author_tags) > 0

    # Review/rating presence
    review_signals = soup.find_all(attrs={"itemprop": re.compile(r"rating|review", re.I)})
    details["reviews_present"] = len(review_signals) > 0

    # Word count (rough content depth)
    word_count = len(text.split())
    details["word_count"] = word_count
    details["content_rich"] = word_count > 500

    # Scoring: 20 pts
    score = 0
    if details["good_heading_structure"]:
        score += 4
    if details["faq_detected"]:
        score += 4
    if details["about_page_linked"]:
        score += 2
    if details["contact_page_linked"]:
        score += 2
    if details["author_signals"]:
        score += 3
    if details["reviews_present"]:
        score += 3
    if details["content_rich"]:
        score += 2

    return {"score": min(score, 20), "max": 20, "details": details}
