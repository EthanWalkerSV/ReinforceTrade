from abc import ABC, abstractmethod
from typing import Dict, Any
from utils.logger import logger

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        logger.info(f"Initialized agent: {name}")

    @abstractmethod
    def analyze(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market data and return insights"""
        pass

    @abstractmethod
    def generate_signal(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trading signal based on analysis"""
        pass
