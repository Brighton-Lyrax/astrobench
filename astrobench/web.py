"""
AstroBench web app — FastAPI powering the public benchmark dashboard and API.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from astrobench.submit import run_benchmark
from astrobench.problems import load_problems, iter_categories, PROBLEMS_DIR

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI(title="AstroBench", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    cats = sorted(iter_categories())
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "AstroBench — Can your model think like an astrophysicist?",
            "categories": cats,
            "problem_count": len(load_problems()),
        },
    )


@app.get("/problems", response_class=HTMLResponse)
async def problems_page(request: Request, category: str | None = None, difficulty: str | None = None) -> HTMLResponse:
    ps = load_problems(categories=[category] if category else None, difficulty=difficulty)
    return templates.TemplateResponse(
        "problems.html",
        {"request": request, "problems": ps, "filter_category": category},
    )


@app.get("/api/problems")
async def api_problems(category: str | None = None, difficulty: str | None = None) -> JSONResponse:
    ps = load_problems(categories=[category] if category else None, difficulty=difficulty)
    return JSONResponse({"count": len(ps), "problems": ps})


@app.post("/api/run")
async def api_run(body: dict[str, Any]) -> JSONResponse:
    provider = body.get("provider", "local")
    model = body.get("model", "ollama/llama3")
    categories = body.get("categories")
    difficulty = body.get("difficulty")
    summary = run_benchmark(
        categories=categories,
        difficulty=difficulty,
        provider=provider,
        model=model,
    )
    return JSONResponse(summary)


@app.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard(request: Request) -> HTMLResponse:
    cached = BASE_DIR / "leaderboard.json"
    data: dict[str, Any] | None = None
    if cached.exists():
        data = json.loads(cached.read_text())
    return templates.TemplateResponse("leaderboard.html", {
        "request": request,
        "title": "AstroBench Leaderboard",
        "leaderboard": data,
    })


@app.get("/model/{model_id}", response_class=HTMLResponse)
async def model_page(request: Request, model_id: str) -> HTMLResponse:
    return templates.TemplateResponse("model.html", {
        "request": request,
        "model_id": model_id,
    })
