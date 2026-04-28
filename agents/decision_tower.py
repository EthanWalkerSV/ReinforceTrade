from .base_agent import BaseAgent
from typing import Dict, Any, List
from utils.logger import logger

class DecisionTower:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        logger.info("DecisionTower initialized with agents: " + ", ".join([a.name for a in agents]))

    def process_market_data(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        analyses = {}
        signals = {}
        for agent in self.agents:
            analysis = agent.analyze(market_data)
            signal = agent.generate_signal(analysis)
            analyses[agent.name] = analysis
            signals[agent.name] = signal
        # Aggregate signals
        decision = self.aggregate_signals(signals)
        return {"analyses": analyses, "signals": signals, "decision": decision}

    def aggregate_signals(self, signals: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        # Simple aggregation: majority vote or weighted
        buy_strength = 0
        sell_strength = 0
        hold_strength = 0
        for agent_signals in signals.values():
            signal = agent_signals.get('signal', 'hold')
            strength = agent_signals.get('strength', 0)
            if signal == 'buy' or signal == 'long':
                buy_strength += strength
            elif signal == 'sell' or signal == 'short':
                sell_strength += strength
            else:
                hold_strength += strength
        if buy_strength > sell_strength and buy_strength > hold_strength:
            action = "buy"
            confidence = buy_strength / (buy_strength + sell_strength + hold_strength + 1e-6)
        elif sell_strength > buy_strength and sell_strength > hold_strength:
            action = "sell"
            confidence = sell_strength / (buy_strength + sell_strength + hold_strength + 1e-6)
        else:
            action = "hold"
            confidence = hold_strength / (buy_strength + sell_strength + hold_strength + 1e-6)
        return {"action": action, "confidence": confidence}
