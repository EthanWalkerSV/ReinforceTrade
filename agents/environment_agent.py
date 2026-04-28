from .base_agent import BaseAgent
import pandas as pd
from typing import Dict, Any

class EnvironmentAgent(BaseAgent):
    def __init__(self):
        super().__init__("EnvironmentAgent")

    def analyze(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        # Calculate volatility
        prices = market_data.get('prices', [])
        if not prices:
            return {"volatility": 0, "trend": "neutral"}
        df = pd.DataFrame(prices)
        volatility = df['close'].pct_change().std()
        # Simple trend: recent price vs previous
        recent_avg = df['close'].tail(10).mean()
        prev_avg = df['close'].head(len(df)-10).mean() if len(df) > 10 else recent_avg
        trend = "bullish" if recent_avg > prev_avg else "bearish" if recent_avg < prev_avg else "neutral"
        return {"volatility": volatility, "trend": trend}

    def generate_signal(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        # Based on analysis, generate environment signal
        volatility = analysis.get('volatility', 0)
        trend = analysis.get('trend', 'neutral')
        signal_strength = 1 if volatility < 0.05 else 0.5
        return {"signal": trend, "strength": signal_strength}
