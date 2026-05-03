import httpx
from urllib.parse import urlparse


async def analyze(url: str) -> dict:
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    results = {}

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        # robots.txt — check AI crawler rules
        ai_bots = ["GPTBot", "ClaudeBot", "Google-Extended", "PerplexityBot", "anthropic-ai"]
        try:
            r = await client.get(f"{base}/robots.txt")
            robots_text = r.text if r.status_code == 200 else ""
        except Exception:
            robots_text = ""

        results["robots_txt_found"] = bool(robots_text)
        blocked_bots = [bot for bot in ai_bots if f"User-agent: {bot}" in robots_text and "Disallow: /" in robots_text]
        allowed_bots = [bot for bot in ai_bots if bot.lower() in robots_text.lower() and bot not in blocked_bots]
        results["ai_bots_blocked"] = blocked_bots
        results["ai_bots_mentioned"] = allowed_bots

        # llms.txt
        for path, key in [("/llms.txt", "llms_txt"), ("/llms-full.txt", "llms_full_txt")]:
            try:
                r = await client.get(f"{base}{path}")
                results[key] = r.status_code == 200
            except Exception:
                results[key] = False

    # Scoring: 15 pts total
    score = 0
    if results["robots_txt_found"]:
        score += 3
    if not results["ai_bots_blocked"]:
        score += 5
    if results["llms_txt"]:
        score += 4
    if results["llms_full_txt"]:
        score += 3

    return {"score": score, "max": 15, "details": results}
