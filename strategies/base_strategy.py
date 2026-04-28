from abc import ABC, abstractmethod
from typing import Dict, Any
from utils.logger import logger

class BaseStrategy(ABC):
    def __init__(self, name: str):
        self.name = name
        logger.info(f"Strategy {name} initialized")

    @abstractmethod
    def should_enter(self, market_data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def should_exit(self, market_data: Dict[str, Any], position: Dict[str, Any]) -> bool:
        pass

    def calculate_stop_loss(self, entry_price: float, position_side: str) -> float:
        # Default 5% stop loss
        return entry_price * 0.95 if position_side == 'long' else entry_price * 1.05

    def calculate_take_profit(self, entry_price: float, position_side: str) -> float:
        # Default 10% take profit
        return entry_price * 1.1 if position_side == 'long' else entry_price * 0.9
