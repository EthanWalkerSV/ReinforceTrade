from .base_agent import BaseAgent
import pandas as pd
from typing import Dict, Any

class ShortTermAgent(BaseAgent):
    def __init__(self):
        super().__init__("ShortTermAgent")

    def analyze(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        prices = market_data.get('prices', [])
        if not prices:
            return {"momentum": 0}
        df = pd.DataFrame(prices)
        # Simple momentum: recent returns
        momentum = df['close'].pct_change(5).iloc[-1] if len(df) > 5 else 0
        return {"momentum": momentum}

    def generate_signal(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        momentum = analysis.get('momentum', 0)
        if momentum > 0.02:
            return {"signal": "buy", "strength": min(momentum * 100, 1)}
        elif momentum < -0.02:
            return {"signal": "sell", "strength": min(abs(momentum) * 100, 1)}
        else:
            return {"signal": "hold", "strength": 0}
