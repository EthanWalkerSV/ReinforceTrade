from agents import DecisionTower, EnvironmentAgent, ShortTermAgent, TrendAgent
from trading import Exchange
from strategies import BaseStrategy
from backtesting import Backtester
from config import settings
from utils import logger

class TradingBot:
    def __init__(self):
        self.agents = [EnvironmentAgent(), ShortTermAgent(), TrendAgent()]
        self.decision_tower = DecisionTower(self.agents)
        # self.exchange = some implementation of Exchange
        # self.strategy = some strategy
        logger.info("TradingBot initialized")

    def run_backtest(self, data):
        # use backtester
        pass

    def run_live(self):
        # live trading
        pass
