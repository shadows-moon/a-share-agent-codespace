from fastapi import FastAPI
from pydantic import BaseModel

from src.analysis.scoring import analyze_symbol

app = FastAPI(title="A 股投顾助手")


class AdviceRequest(BaseModel):
    symbol: str
    risk_tolerance: str = "中等"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/advice")
def get_advice(req: AdviceRequest):
    result = analyze_symbol(req.symbol, req.risk_tolerance)
    return result


@app.post("/api/analyze")
def analyze(req: AdviceRequest):
    return analyze_symbol(req.symbol, req.risk_tolerance)
