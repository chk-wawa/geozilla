import asyncio
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from analyzers import llm_access, structured_data, discoverability, content_eeat, brand_authority, llm_queries, recommendations

load_dotenv()

app = FastAPI(title="Geozilla API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    url: str


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    url = req.url.strip()
    if not url.startswith("http"):
        url = f"https://{url}"

    try:
        results = await asyncio.gather(
            brand_authority.analyze(url),
            structured_data.analyze(url),
            content_eeat.analyze(url),
            llm_access.analyze(url),
            discoverability.analyze(url),
            llm_queries.analyze(url),
            return_exceptions=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    sections = ["brand_authority", "structured_data", "content_eeat", "llm_access", "discoverability"]
    section_results = {}
    total_score = 0
    total_max = 0

    for i, key in enumerate(sections):
        r = results[i]
        if isinstance(r, Exception):
            section_results[key] = {"score": 0, "max": [30, 20, 20, 15, 15][i], "error": str(r)}
        else:
            section_results[key] = r
            total_score += r.get("score", 0)
            total_max += r.get("max", 0)

    llm_result = results[5]
    if isinstance(llm_result, Exception):
        llm_result = {"error": str(llm_result), "queries": [], "summary": {}}

    recs = recommendations.generate(section_results)

    return {
        "url": url,
        "total_score": total_score,
        "total_max": total_max,
        "sections": section_results,
        "llm_queries": llm_result,
        "recommendations": recs,
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
