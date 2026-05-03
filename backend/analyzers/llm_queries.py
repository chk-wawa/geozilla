import os
import asyncio
from urllib.parse import urlparse


COMPETITORS = {
    "empik.com": ["taniaksiazka.pl", "bonito.pl", "gandalf.com.pl", "merlin.pl", "matras.pl"],
}

QUERY_TEMPLATES = [
    "best online bookstore in Poland",
    "where to buy books online in Poland",
    "top Polish book retailers",
    "buy Polish books online",
    "best place to buy audiobooks in Poland",
    "online shop for school books Poland",
    "best ebook store Poland",
    "Polish book subscription service",
    "buy bestseller books Poland",
    "top rated bookshop Poland",
]


def _extract_mentions(text: str, domain: str, competitors: list[str]) -> dict:
    text_lower = text.lower()
    brand = domain.replace("www.", "").split(".")[0].lower()
    result = {
        "target_mentioned": brand in text_lower or domain in text_lower,
        "competitors_mentioned": [c.split(".")[0] for c in competitors if c.split(".")[0] in text_lower],
        "response_snippet": text[:400],
    }
    return result


async def _query_openai(query: str) -> str:
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": query}],
            max_tokens=300,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        return f"[error: {e}]"


async def _query_claude(query: str) -> str:
    try:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        resp = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": query}],
        )
        return resp.content[0].text
    except Exception as e:
        return f"[error: {e}]"


async def _query_gemini(query: str) -> str:
    try:
        from google import genai
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        resp = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.0-flash",
            contents=query,
        )
        return resp.text
    except Exception as e:
        return f"[error: {e}]"


async def analyze(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    competitors = COMPETITORS.get(domain, [])

    has_openai = bool(os.environ.get("OPENAI_API_KEY"))
    has_claude = bool(os.environ.get("ANTHROPIC_API_KEY"))
    has_gemini = bool(os.environ.get("GEMINI_API_KEY"))

    results = []
    for i, query in enumerate(QUERY_TEMPLATES):
        # Run OpenAI + Claude in parallel; Gemini sequentially with delay to respect free-tier rate limits
        parallel_tasks = {}
        if has_openai:
            parallel_tasks["openai"] = _query_openai(query)
        if has_claude:
            parallel_tasks["claude"] = _query_claude(query)

        parallel_responses = await asyncio.gather(*parallel_tasks.values(), return_exceptions=True)

        llm_results: dict = {}
        for llm, resp in zip(parallel_tasks.keys(), parallel_responses):
            text = str(resp) if not isinstance(resp, str) else resp
            llm_results[llm] = _extract_mentions(text, domain, competitors) if text and not text.startswith("[error") else None

        if has_gemini:
            if i > 0:
                await asyncio.sleep(4)  # stay within free-tier RPM
            gemini_resp = await _query_gemini(query)
            llm_results["gemini"] = (
                _extract_mentions(gemini_resp, domain, competitors)
                if gemini_resp and not gemini_resp.startswith("[error")
                else None
            )

        results.append({"query": query, "llms": llm_results})

    # Summary stats
    total_queries = len(results)
    llm_names = ["openai", "claude", "gemini"]
    mention_counts = {llm: sum(1 for r in results if r["llms"].get(llm) and r["llms"][llm]["target_mentioned"]) for llm in llm_names}

    return {
        "queries": results,
        "summary": {
            "total_queries": total_queries,
            "mention_counts": mention_counts,
            "competitors": competitors,
        },
    }
