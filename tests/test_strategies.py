import unittest
from strategies import BaseStrategy, MultiAgentStrategy, RiskManager

class TestRiskManager(unittest.TestCase):
    def setUp(self):
        self.risk_manager = RiskManager(
            max_risk_per_trade=0.01,
            max_portfolio_risk=0.05
        )
    
    def test_calculate_position_size(self):
        """Test position size calculation"""
        balance = 10000
        entry_price = 50000
        stop_loss = 47500  # 5% stop
        confidence = 0.8
        
        size = self.risk_manager.calculate_position_size(
            balance, entry_price, stop_loss, confidence
        )
        
        # Should be less than max position (10% of balance)
        self.assertLessEqual(size, balance * 0.1)
        self.assertGreater(size, 0)
    
    def test_check_exposure_allowed(self):
        """Test exposure check for allowed trade"""
        result = self.risk_manager.check_exposure(
            'BTC', 500, 10000  # 5% of portfolio
        )
        self.assertTrue(result)
    
    def test_check_exposure_rejected(self):
        """Test exposure check for oversized trade"""
        result = self.risk_manager.check_exposure(
            'BTC', 3000, 10000  # 30% of portfolio - should fail
        )
        self.assertFalse(result)
    
    def test_record_trade(self):
        """Test trade recording"""
        trade = {
            'entry_price': 50000,
            'exit_price': 51000,
            'pnl': 1000,
            'side': 'long'
        }
        self.risk_manager.record_trade(trade)
        
        metrics = self.risk_manager.get_risk_metrics()
        self.assertEqual(metrics['total_trades'], 1)
    
    def test_get_risk_metrics(self):
        """Test risk metrics calculation"""
        # Add some trades
        for i in range(5):
            self.risk_manager.record_trade({
                'entry_price': 50000,
                'exit_price': 51000 if i < 3 else 49000,  # 3 wins, 2 losses
                'pnl': 1000 if i < 3 else -1000,
                'side': 'long'
            })
        
        metrics = self.risk_manager.get_risk_metrics()
        
        self.assertEqual(metrics['total_trades'], 5)
        self.assertEqual(metrics['win_rate'], 0.6)
    
    def test_should_reduce_exposure(self):
        """Test consecutive loss detection"""
        # Add 3 losing trades
        for _ in range(3):
            self.risk_manager.record_trade({
                'entry_price': 50000,
                'exit_price': 49000,
                'pnl': -1000,
                'side': 'long'
            })
        
        result = self.risk_manager.should_reduce_exposure(consecutive_losses=3)
        self.assertTrue(result)
    
    def test_should_not_reduce_exposure(self):
        """Test when no consecutive losses"""
        # Add mixed trades
        self.risk_manager.record_trade({'pnl': -1000, 'side': 'long'})
        self.risk_manager.record_trade({'pnl': 1000, 'side': 'long'})
        self.risk_manager.record_trade({'pnl': -1000, 'side': 'long'})
        
        result = self.risk_manager.should_reduce_exposure(consecutive_losses=3)
        self.assertFalse(result)

class TestMultiAgentStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = MultiAgentStrategy(
            use_rl=False,  # Skip RL for unit tests
            confidence_threshold=0.6
        )
    
    def test_strategy_initialization(self):
        """Test strategy initialization"""
        self.assertEqual(self.strategy.name, "MultiAgentStrategy")
        self.assertEqual(self.strategy.confidence_threshold, 0.6)
        self.assertEqual(len(self.strategy.agents), 3)  # Without RL
    
    def test_calculate_position_size(self):
        """Test position size calculation"""
        balance = 10000
        confidence = 0.8
        
        size = self.strategy.calculate_position_size(balance, confidence)
        
        self.assertGreater(size, 0)
        self.assertLessEqual(size, balance * self.strategy.max_position_size)
    
    def test_stop_loss_calculation(self):
        """Test stop loss price calculation"""
        entry_price = 50000
        position_side = 'long'
        
        stop_price = self.strategy.get_stop_loss_price(entry_price, position_side)
        
        self.assertLess(stop_price, entry_price)
        # Should be around 5% below entry
        expected_stop = entry_price * 0.95
        self.assertAlmostEqual(stop_price, expected_stop, places=2)
    
    def test_take_profit_calculation(self):
        """Test take profit price calculation"""
        entry_price = 50000
        position_side = 'long'
        
        tp_price = self.strategy.get_take_profit_price(entry_price, position_side)
        
        self.assertGreater(tp_price, entry_price)
        # Should be around 10% above entry
        expected_tp = entry_price * 1.1
        self.assertAlmostEqual(tp_price, expected_tp, places=2)

if __name__ == '__main__':
    unittest.main()
