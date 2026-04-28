from .base_agent import BaseAgent
import pandas as pd
from typing import Dict, Any

class TrendAgent(BaseAgent):
    def __init__(self):
        super().__init__("TrendAgent")

    def analyze(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        prices = market_data.get('prices', [])
        if not prices:
            return {"trend_strength": 0}
        df = pd.DataFrame(prices)
        # Simple trend strength using moving averages
        short_ma = df['close'].rolling(20).mean().iloc[-1]
        long_ma = df['close'].rolling(50).mean().iloc[-1]
        if pd.isna(short_ma) or pd.isna(long_ma):
            return {"trend_strength": 0}
        trend_strength = (short_ma - long_ma) / long_ma
        return {"trend_strength": trend_strength}

    def generate_signal(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        trend_strength = analysis.get('trend_strength', 0)
        if trend_strength > 0.05:
            return {"signal": "long", "strength": min(trend_strength * 20, 1)}
        elif trend_strength < -0.05:
            return {"signal": "short", "strength": min(abs(trend_strength) * 20, 1)}
        else:
            return {"signal": "neutral", "strength": 0}
