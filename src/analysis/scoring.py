from __future__ import annotations

import numpy as np
import pandas as pd


def _symbol_seed(symbol: str) -> int:
    return sum(ord(ch) for ch in str(symbol).strip())


def _make_mock_history(symbol: str, days: int = 120) -> pd.DataFrame:
    """为代码提供离线模拟行情。"""
    seed = _symbol_seed(symbol)
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days, freq="B")

    base = 20 + (seed % 50)
    drift = 0.001 + ((seed % 12) / 1000.0)
    shocks = rng.normal(loc=drift, scale=0.025, size=len(dates))

    prices = [base]
    for change in shocks[1:]:
        next_price = max(prices[-1] * (1 + change), 5.0)
        prices.append(float(next_price))

    df = pd.DataFrame({"date": dates, "close": prices})
    df["pct_change"] = df["close"].pct_change().fillna(0.0)
    return df


def analyze_symbol(symbol: str, risk_tolerance: str = "中等") -> dict:
    """根据模拟数据给出投顾风格分析结果。"""
    symbol = str(symbol).strip() or "600519"
    try:
        df = _make_mock_history(symbol)
    except Exception as exc:
        return {"error": f"无法生成分析：{exc}"}

    closes = df["close"].astype(float)
    returns = df["pct_change"].astype(float)

    current_price = float(closes.iloc[-1])
    recent_20 = returns.iloc[-20:].mean() * 100
    recent_60 = returns.iloc[-60:].mean() * 100
    volatility = float(returns.std() * 100)
    drawdown = float(((closes / closes.max()) - 1).min() * 100)

    trend_score = float(np.clip(50 + recent_60 * 18 + recent_20 * 12, 0, 100))
    risk_score = float(np.clip(35 + volatility * 12 + abs(drawdown) * 4, 0, 100))
    valuation_score = float(np.clip(55 + recent_20 * 20 - volatility * 3, 0, 100))
    combined = float(np.clip((trend_score * 0.55) + (valuation_score * 0.30) + ((100 - risk_score) * 0.15), 0, 100))

    if combined >= 75:
        advice = "适合关注 / 可考虑布局"
        thesis = "短期趋势相对稳健，风险相对可控，适合在合理区间内关注。"
    elif combined >= 60:
        advice = "中性观察"
        thesis = "市场仍有结构性机会，但需要等待更明确确认。"
    else:
        advice = "谨慎观察 / 暂缓加仓"
        thesis = "当前波动和回撤风险偏高，建议等待趋势确认后再部署。"

    reasons = [
        f"近20日收益约 {recent_20:.2f}% ，短线动能 {('偏强' if recent_20 > 0 else '偏弱')}。",
        f"近60日收益约 {recent_60:.2f}% ，说明中期趋势{('较为稳健' if abs(recent_60) < 2 else '较清晰')}。",
        f"波动率约 {volatility:.2f}% ，在 {risk_tolerance} 的偏好下应保持风险控制。",
        f"最大回撤约 {abs(drawdown):.2f}% ，提醒注意仓位和止损。",
    ]

    risk_notes = [
        "不要在高估值区间追涨，避免追高。",
        "建议控制单一标的仓位，不要过度集中。",
        "关键是看趋势是否延续，并结合基本面确认。",
    ]

    metrics = {
        "近20日收益": f"{recent_20:.2f}%",
        "近60日收益": f"{recent_60:.2f}%",
        "波动率": f"{volatility:.2f}%",
        "最大回撤": f"{abs(drawdown):.2f}%",
    }

    return {
        "symbol": symbol,
        "price": round(current_price, 2),
        "score": int(round(combined)),
        "trend_score": int(round(trend_score)),
        "risk_score": int(round(risk_score)),
        "valuation_score": int(round(valuation_score)),
        "advice": advice,
        "summary": f"{symbol} 当前模拟评分为 {int(round(combined))}/100，{thesis}",
        "investment_thesis": thesis,
        "reasons": reasons,
        "risk_notes": risk_notes,
        "metrics": metrics,
    }


if __name__ == "__main__":
    print(analyze_symbol("600519"))
