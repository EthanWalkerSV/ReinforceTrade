"""
Unit tests for OrderManager and Order classes.
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '..')

from trading.order_manager import OrderManager, Order, OrderStatus, OrderType, OrderSide


class TestOrder(unittest.TestCase):
    """Test cases for Order class"""
    
    def test_order_creation(self):
        """Test order creation"""
        order = Order(
            id='test_1',
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0,
            price=50000.0
        )
        
        self.assertEqual(order.id, 'test_1')
        self.assertEqual(order.symbol, 'BTC/USDT')
        self.assertEqual(order.side, OrderSide.BUY)
        self.assertEqual(order.order_type, OrderType.MARKET)
        self.assertEqual(order.amount, 1.0)
        self.assertEqual(order.price, 50000.0)
        self.assertEqual(order.status, OrderStatus.PENDING)
        self.assertEqual(order.remaining, 1.0)
        
    def test_order_is_active_pending(self):
        """Test is_active for pending order"""
        order = Order(
            id='test_1',
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        self.assertTrue(order.is_active)
        
    def test_order_is_active_filled(self):
        """Test is_active for filled order"""
        order = Order(
            id='test_1',
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0,
            status=OrderStatus.FILLED
        )
        
        self.assertFalse(order.is_active)
        self.assertTrue(order.is_filled)
        
    def test_order_is_cancelled(self):
        """Test is_cancelled"""
        order = Order(
            id='test_1',
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0,
            status=OrderStatus.CANCELLED
        )
        
        self.assertTrue(order.is_cancelled)
        self.assertFalse(order.is_active)
        
    def test_fill_percentage(self):
        """Test fill percentage calculation"""
        order = Order(
            id='test_1',
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0,
            filled=0.5
        )
        
        self.assertEqual(order.fill_percentage, 50.0)
        
    def test_fill_percentage_zero(self):
        """Test fill percentage with zero amount"""
        order = Order(
            id='test_1',
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=0.0,
            filled=0.0
        )
        
        self.assertEqual(order.fill_percentage, 0.0)
        
    def test_update_from_exchange(self):
        """Test order update from exchange data"""
        order = Order(
            id='test_1',
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        exchange_data = {
            'id': 'exchange_123',
            'status': 'filled',
            'filled': 1.0,
            'remaining': 0.0,
            'price': 50000.0,
            'fee': {'cost': 10.0}
        }
        
        order.update_from_exchange(exchange_data)
        
        self.assertEqual(order.exchange_id, 'exchange_123')
        self.assertEqual(order.status, OrderStatus.FILLED)
        self.assertEqual(order.filled, 1.0)
        self.assertEqual(order.remaining, 0.0)
        self.assertEqual(order.price, 50000.0)
        self.assertEqual(order.fee, 10.0)
        self.assertIsNotNone(order.filled_at)
        self.assertIsNotNone(order.updated_at)
        
    def test_parse_status(self):
        """Test status parsing from exchange strings"""
        order = Order(
            id='test_1',
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        # Test various status strings
        self.assertEqual(order._parse_status('pending'), OrderStatus.PENDING)
        self.assertEqual(order._parse_status('open'), OrderStatus.OPEN)
        self.assertEqual(order._parse_status('filled'), OrderStatus.FILLED)
        self.assertEqual(order._parse_status('closed'), OrderStatus.FILLED)
        self.assertEqual(order._parse_status('cancelled'), OrderStatus.CANCELLED)
        self.assertEqual(order._parse_status('canceled'), OrderStatus.CANCELLED)
        self.assertEqual(order._parse_status('rejected'), OrderStatus.REJECTED)
        self.assertEqual(order._parse_status('expired'), OrderStatus.EXPIRED)
        self.assertEqual(order._parse_status('unknown'), OrderStatus.PENDING)
        
    def test_to_dict(self):
        """Test order serialization"""
        order = Order(
            id='test_1',
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0,
            price=50000.0,
            filled=0.5
        )
        
        data = order.to_dict()
        
        self.assertEqual(data['id'], 'test_1')
        self.assertEqual(data['symbol'], 'BTC/USDT')
        self.assertEqual(data['side'], 'buy')
        self.assertEqual(data['type'], 'market')
        self.assertEqual(data['amount'], 1.0)
        self.assertEqual(data['price'], 50000.0)
        self.assertEqual(data['status'], 'pending')
        self.assertEqual(data['filled'], 0.5)
        self.assertEqual(data['fill_percentage'], 50.0)


class TestOrderManager(unittest.TestCase):
    """Test cases for OrderManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.order_manager = OrderManager(max_pending_orders=5)
        
    def test_init(self):
        """Test OrderManager initialization"""
        self.assertIsNone(self.order_manager.exchange)
        self.assertEqual(self.order_manager.max_pending_orders, 5)
        self.assertEqual(len(self.order_manager._orders), 0)
        
        stats = self.order_manager.get_order_statistics()
        self.assertEqual(stats['total_orders'], 0)
        self.assertEqual(stats['active_orders'], 0)
        
    def test_create_order_success(self):
        """Test successful order creation"""
        order = self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        self.assertIsNotNone(order)
        self.assertEqual(order.symbol, 'BTC/USDT')
        self.assertEqual(order.side, OrderSide.BUY)
        self.assertEqual(order.order_type, OrderType.MARKET)
        self.assertEqual(order.amount, 1.0)
        self.assertEqual(order.status, OrderStatus.PENDING)
        
        # Check statistics
        stats = self.order_manager.get_order_statistics()
        self.assertEqual(stats['total_orders'], 1)
        self.assertEqual(stats['pending_orders'], 1)
        
    def test_create_order_limit_requires_price(self):
        """Test that limit orders require price"""
        order = self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            amount=1.0,
            price=None
        )
        
        self.assertIsNone(order)
        
    def test_create_order_invalid_amount(self):
        """Test order creation with invalid amount"""
        order = self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=-1.0
        )
        
        self.assertIsNone(order)
        
    def test_create_order_max_pending(self):
        """Test max pending orders limit"""
        # Create max pending orders
        for i in range(5):
            self.order_manager.create_order(
                symbol='BTC/USDT',
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                amount=1.0
            )
        
        # Try to create one more
        order = self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        self.assertIsNone(order)
        
    def test_get_order(self):
        """Test getting order by ID"""
        order = self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        retrieved = self.order_manager.get_order(order.id)
        
        self.assertEqual(retrieved.id, order.id)
        
    def test_get_order_not_found(self):
        """Test getting non-existent order"""
        order = self.order_manager.get_order('nonexistent')
        
        self.assertIsNone(order)
        
    def test_get_orders_by_symbol(self):
        """Test getting orders by symbol"""
        self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        self.order_manager.create_order(
            symbol='ETH/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        btc_orders = self.order_manager.get_orders_by_symbol('BTC/USDT')
        
        self.assertEqual(len(btc_orders), 1)
        self.assertEqual(btc_orders[0].symbol, 'BTC/USDT')
        
    def test_get_active_orders(self):
        """Test getting active orders"""
        self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        active = self.order_manager.get_active_orders()
        
        self.assertEqual(len(active), 1)
        
    def test_cancel_order(self):
        """Test order cancellation"""
        order = self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        result = self.order_manager.cancel_order(order.id)
        
        self.assertTrue(result)
        self.assertEqual(order.status, OrderStatus.CANCELLED)
        
        # Check statistics
        stats = self.order_manager.get_order_statistics()
        self.assertEqual(stats['total_cancelled'], 1)
        
    def test_cancel_order_not_found(self):
        """Test cancelling non-existent order"""
        result = self.order_manager.cancel_order('nonexistent')
        
        self.assertFalse(result)
        
    def test_cancel_order_not_active(self):
        """Test cancelling non-active order"""
        order = self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        # Cancel once
        self.order_manager.cancel_order(order.id)
        
        # Try to cancel again
        result = self.order_manager.cancel_order(order.id)
        
        self.assertFalse(result)
        
    def test_cancel_all_orders(self):
        """Test cancelling all orders"""
        for i in range(3):
            self.order_manager.create_order(
                symbol='BTC/USDT',
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                amount=1.0
            )
        
        cancelled = self.order_manager.cancel_all_orders()
        
        self.assertEqual(cancelled, 3)
        
    def test_cancel_all_orders_by_symbol(self):
        """Test cancelling orders by symbol"""
        self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        self.order_manager.create_order(
            symbol='ETH/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        cancelled = self.order_manager.cancel_all_orders(symbol='BTC/USDT')
        
        self.assertEqual(cancelled, 1)
        
    def test_cleanup_old_orders(self):
        """Test cleaning up old orders"""
        # Create an order and manually set old cancellation time
        order = self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        # Cancel order and set old time
        self.order_manager.cancel_order(order.id)
        order.cancelled_at = datetime.now() - timedelta(days=10)
        self.order_manager._cancelled_orders[order.id] = order
        
        # Clean up orders older than 7 days
        removed = self.order_manager.cleanup_old_orders(days=7)
        
        self.assertEqual(removed, 1)
        
    def test_cleanup_recent_orders(self):
        """Test that recent orders are not cleaned up"""
        order = self.order_manager.create_order(
            symbol='BTC/USDT',
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=1.0
        )
        
        self.order_manager.cancel_order(order.id)
        
        # Clean up orders older than 7 days
        removed = self.order_manager.cleanup_old_orders(days=7)
        
        self.assertEqual(removed, 0)
        
    def test_repr(self):
        """Test string representation"""
        repr_str = repr(self.order_manager)
        
        self.assertIn('OrderManager', repr_str)
        self.assertIn('active=0', repr_str)
        self.assertIn('filled=0', repr_str)


if __name__ == '__main__':
    unittest.main()
