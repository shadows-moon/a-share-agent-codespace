from fastapi import FastAPI
from pydantic import BaseModel

from src.analysis.scoring import analyze_symbol

app = FastAPI(title="A Share Investment Assistant")


class AdviceRequest(BaseModel):
    symbol: str
    risk_tolerance: str = "medium"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/advice")
def get_advice(req: AdviceRequest):
    """返回简化的股票分析结果。"""
    result = analyze_symbol(req.symbol)
    return result


@app.post("/api/analyze")
def analyze(req: AdviceRequest):
    """接口别名，适合前端调用。"""
    return analyze_symbol(req.symbol)
