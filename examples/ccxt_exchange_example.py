#!/usr/bin/env python3
"""
CCXTExchange Usage Example
This example demonstrates how to use the CCXTExchange class for cryptocurrency trading.
"""

import sys
import os
sys.path.insert(0, '..')

from trading import CCXTExchange
from utils import logger
import time

def main():
    """Main example function"""
    logger.info("CCXTExchange Example")
    
    # Configuration (use environment variables for real API keys)
    api_key = os.getenv('BINANCE_API_KEY', 'your_api_key_here')
    secret = os.getenv('BINANCE_SECRET', 'your_secret_here')
    
    # Initialize exchange (sandbox mode for testing)
    try:
        exchange = CCXTExchange(
            api_key=api_key,
            secret=secret,
            exchange_name='binance',
            sandbox=True  # Use testnet
        )
        logger.info(f"Connected to {exchange}")
        
        # Check connection health
        if not exchange.check_connection():
            logger.error("Exchange connection check failed")
            return
        
        # Get account balance
        logger.info("Getting account balance...")
        balance = exchange.get_balance()
        logger.info(f"Balance: {balance}")
        
        # Get ticker information
        logger.info("Getting BTC/USDT ticker...")
        ticker = exchange.get_ticker('BTC/USDT')
        if ticker:
            logger.info(f"BTC/USDT Price: ${ticker['price']:.2f}")
            logger.info(f"24h Change: {ticker['change_percent']:.2f}%")
        
        # Get market data
        logger.info("Getting market data...")
        market_data = exchange.get_market_data('BTC/USDT', '1h', limit=5)
        if market_data:
            logger.info(f"Latest candle: {market_data[-1]}")
        
        # Get trading fees
        logger.info("Getting trading fees...")
        fees = exchange.get_trading_fees()
        if fees:
            logger.info(f"Maker fee: {fees['trading']['maker']:.4f}")
            logger.info(f"Taker fee: {fees['trading']['taker']:.4f}")
        
        # Example: Place a small test order (commented out for safety)
        # Uncomment only if you want to test with real orders
        """
        if balance.get('USDT', 0) > 10:  # Need at least 10 USDT
            logger.info("Placing test market buy order...")
            order = exchange.place_order(
                symbol='BTC/USDT',
                side='buy',
                amount=0.001,  # Small amount for testing
                order_type='market'
            )
            
            if order:
                logger.info(f"Order placed: {order['id']}")
                
                # Wait a bit for order to process
                time.sleep(2)
                
                # Check order status
                status = exchange.get_order_status(order['id'])
                logger.info(f"Order status: {status['status']}")
                
                # Cancel order if still open (for market orders, it's usually filled immediately)
                if status['status'] == 'open':
                    logger.info("Canceling order...")
                    if exchange.cancel_order(order['id']):
                        logger.info("Order cancelled successfully")
        else:
            logger.warning("Insufficient USDT balance for test order")
        """
        
        # Get supported symbols
        logger.info("Getting supported symbols...")
        symbols = exchange.get_supported_symbols()
        logger.info(f"Supported symbols: {len(symbols)}")
        
        # Show some popular symbols
        popular_symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT']
        available_symbols = [s for s in popular_symbols if s in symbols]
        logger.info(f"Available popular symbols: {available_symbols}")
        
    except Exception as e:
        logger.error(f"Example failed: {e}")
        logger.info("Make sure to set BINANCE_API_KEY and BINANCE_SECRET environment variables")
        logger.info("For testing, you can get testnet keys from Binance")

def test_error_handling():
    """Test error handling scenarios"""
    logger.info("Testing error handling...")
    
    # Test with invalid credentials
    try:
        exchange = CCXTExchange(
            api_key='invalid_key',
            secret='invalid_secret',
            exchange_name='binance',
            sandbox=True
        )
        # This should work for initialization but fail on API calls
        balance = exchange.get_balance()
        logger.info(f"Balance with invalid creds: {balance}")
    except Exception as e:
        logger.error(f"Expected error with invalid credentials: {e}")
    
    # Test with invalid exchange
    try:
        exchange = CCXTExchange(
            api_key='test',
            secret='test',
            exchange_name='invalid_exchange',
            sandbox=True
        )
    except Exception as e:
        logger.error(f"Expected error with invalid exchange: {e}")

if __name__ == '__main__':
    main()
    test_error_handling()
    logger.info("Example completed!")
