#!/usr/bin/env python3
"""
OrderManager Usage Example
Demonstrates order lifecycle management.
"""

import sys
sys.path.insert(0, '..')

from trading import OrderManager, OrderSide, OrderType
from trading import CCXTExchange
from utils.logger import logger
import os


def main():
    """Main example function"""
    logger.info("OrderManager Example")
    
    # Initialize exchange
    api_key = os.getenv('BINANCE_API_KEY', 'test_key')
    secret = os.getenv('BINANCE_SECRET', 'test_secret')
    
    try:
        exchange = CCXTExchange(api_key, secret, 'binance', sandbox=True)
        
        # Initialize OrderManager
        order_manager = OrderManager(exchange=exchange, max_pending_orders=5)
        
        logger.info(f"OrderManager: {order_manager}")
        
        # Create a market order
        order = order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=0.001,
            metadata={'strategy': 'test'}
        )
        
        if order:
            logger.info(f"Order created: {order.id}")
            logger.info(f"Order status: {order.status.value}")
            logger.info(f"Order is active: {order.is_active}")
            
            # Get order statistics
            stats = order_manager.get_order_statistics()
            logger.info(f"Statistics: {stats}")
            
            # Get order by ID
            retrieved_order = order_manager.get_order(order.id)
            logger.info(f"Retrieved order: {retrieved_order}")
            
        # Create a limit order
        limit_order = order_manager.create_order(
            symbol='ETH/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            amount=0.01,
            price=3000.0
        )
        
        if limit_order:
            logger.info(f"Limit order created: {limit_order.id}")
            logger.info(f"Order price: ${limit_order.price}")
            
        # Get all active orders
        active_orders = order_manager.get_active_orders()
        logger.info(f"Active orders: {len(active_orders)}")
        
        for order in active_orders:
            logger.info(f"  - {order.id}: {order.side.value} {order.amount} {order.symbol}")
        
        # Cancel all orders
        cancelled = order_manager.cancel_all_orders()
        logger.info(f"Cancelled {cancelled} orders")
        
        # Final statistics
        final_stats = order_manager.get_order_statistics()
        logger.info(f"Final statistics: {final_stats}")
        
    except Exception as e:
        logger.error(f"Example failed: {e}")


def test_order_lifecycle():
    """Test order lifecycle without exchange"""
    logger.info("Testing order lifecycle...")
    
    order_manager = OrderManager(max_pending_orders=10)
    
    # Create orders
    for i in range(3):
        order = order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=0.001
        )
        
        if order:
            logger.info(f"Created order {i+1}: {order.id}")
    
    # Check statistics
    stats = order_manager.get_order_statistics()
    logger.info(f"Created {stats['total_orders']} orders")
    
    # Get orders by symbol
    btc_orders = order_manager.get_orders_by_symbol('BTC/USDT')
    logger.info(f"BTC/USDT orders: {len(btc_orders)}")
    
    # Get pending orders (they're pending because no exchange)
    active = order_manager.get_active_orders()
    logger.info(f"Active orders: {len(active)}")


if __name__ == '__main__':
    test_order_lifecycle()
    print()
    main()
