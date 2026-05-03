#!/usr/bin/env python3
"""
WebSocket Client Usage Example
Demonstrates real-time market data streaming using WebSocket.
"""

import sys
import asyncio
sys.path.insert(0, '..')

from trading import BinanceWebSocket, WebSocketConfig
from utils.logger import logger


async def handle_ticker(data):
    """Handle ticker updates"""
    symbol = data.get('symbol')
    price = data.get('price')
    change = data.get('change_percent')
    print(f"[{symbol}] Price: ${price:,.2f} | Change: {change:+.2f}%")


async def handle_orderbook(data):
    """Handle orderbook updates"""
    symbol = data.get('symbol')
    print(f"Orderbook update for {symbol}")


async def handle_trade(data):
    """Handle trade updates"""
    symbol = data.get('symbol')
    print(f"Trade update for {symbol}")


async def main():
    """Main example function"""
    logger.info("WebSocket Client Example")
    
    # Configuration
    symbols = ['BTC/USDT', 'ETH/USDT']
    config = WebSocketConfig(
        reconnect_attempts=5,
        reconnect_delay=1.0,
        heartbeat_interval=30
    )
    
    # Initialize WebSocket client
    ws_client = BinanceWebSocket(symbols=symbols, config=config)
    
    # Register callbacks
    ws_client.on_ticker(handle_ticker)
    ws_client.on_orderbook(handle_orderbook)
    ws_client.on_trade(handle_trade)
    
    logger.info(f"WebSocket Client: {ws_client}")
    logger.info(f"Symbols: {symbols}")
    
    # Connect and run
    try:
        connected = await ws_client.connect()
        if not connected:
            logger.error("Failed to connect to WebSocket")
            return
        
        logger.info("Connected to Binance WebSocket")
        logger.info("Receiving real-time data... Press Ctrl+C to stop")
        
        # Run for 60 seconds as example
        await asyncio.sleep(60)
        
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Example error: {e}")
    finally:
        await ws_client.disconnect()
        logger.info("Example completed")


def test_price_cache():
    """Test price cache functionality"""
    logger.info("Testing price cache...")
    
    config = WebSocketConfig()
    ws_client = BinanceWebSocket(symbols=['BTC/USDT'], config=config)
    
    # Simulate price update
    ws_client._price_cache['BTC/USDT'] = 50000.0
    ws_client._last_update['BTC/USDT'] = datetime.now()
    
    price = ws_client.get_price('BTC/USDT')
    last_update = ws_client.get_last_update('BTC/USDT')
    
    print(f"Cached price: ${price:,.2f}")
    print(f"Last update: {last_update}")
    print(f"Is connected: {ws_client.is_connected()}")


if __name__ == '__main__':
    from datetime import datetime
    
    # Test price cache
    test_price_cache()
    print()
    
    # Run main example
    asyncio.run(main())
