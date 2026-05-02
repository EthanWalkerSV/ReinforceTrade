#!/usr/bin/env python3
"""
Live Trading Example
This example demonstrates how to use TradingBot for live trading.
"""

import sys
import os
sys.path.insert(0, '..')

from trading_bot import TradingBot
from trading import CCXTExchange
from strategies import RiskManager
from utils import logger
import time


def main():
    """Main example function"""
    logger.info("Live Trading Bot Example")
    
    # Configuration (use environment variables for real API keys)
    api_key = os.getenv('BINANCE_API_KEY', 'your_api_key_here')
    secret = os.getenv('BINANCE_SECRET', 'your_secret_here')
    
    # Initialize exchange (sandbox mode for testing)
    try:
        exchange = CCXTExchange(
            api_key=api_key,
            secret=secret,
            exchange_name='binance',
            sandbox=True
        )
        
        # Initialize trading bot
        symbols = ['BTC/USDT', 'ETH/USDT']
        
        risk_manager = RiskManager(
            max_position_size=0.1,
            max_drawdown=0.15,
            stop_loss_pct=0.05,
            take_profit_pct=0.1
        )
        
        bot = TradingBot(
            exchange=exchange,
            symbols=symbols,
            risk_manager=risk_manager
        )
        
        logger.info(f"Trading Bot: {bot}")
        
        # Start live trading
        logger.info("Starting live trading...")
        bot.run_live(test_mode=True)
        
    except Exception as e:
        logger.error(f"Example failed: {e}")


if __name__ == '__main__':
    main()
