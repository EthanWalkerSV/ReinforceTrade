import unittest
import numpy as np
from agents import BaseAgent, EnvironmentAgent, ShortTermAgent, TrendAgent, DecisionTower

class TestEnvironmentAgent(unittest.TestCase):
    def setUp(self):
        self.agent = EnvironmentAgent()
    
    def test_analyze_empty_data(self):
        """Test analysis with empty data"""
        result = self.agent.analyze({'prices': []})
        self.assertEqual(result['volatility'], 0)
        self.assertEqual(result['trend'], 'neutral')
    
    def test_analyze_bullish_trend(self):
        """Test bullish trend detection"""
        # Create synthetic data with upward trend
        prices = [{'close': 100 + i*2, 'volume': 1000} for i in range(20)]
        result = self.agent.analyze({'prices': prices})
        
        self.assertEqual(result['trend'], 'bullish')
        self.assertGreater(result['volatility'], 0)
    
    def test_analyze_bearish_trend(self):
        """Test bearish trend detection"""
        # Create synthetic data with downward trend
        prices = [{'close': 100 - i*2, 'volume': 1000} for i in range(20)]
        result = self.agent.analyze({'prices': prices})
        
        self.assertEqual(result['trend'], 'bearish')
    
    def test_generate_signal(self):
        """Test signal generation"""
        analysis = {'volatility': 0.03, 'trend': 'bullish'}
        signal = self.agent.generate_signal(analysis)
        
        self.assertEqual(signal['signal'], 'bullish')
        self.assertGreater(signal['strength'], 0)

class TestShortTermAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ShortTermAgent()
    
    def test_analyze_momentum(self):
        """Test momentum analysis"""
        # Create data with positive momentum
        prices = [{'close': 100 + i*1.5, 'volume': 1000} for i in range(10)]
        result = self.agent.analyze({'prices': prices})
        
        self.assertIn('momentum', result)
    
    def test_generate_buy_signal(self):
        """Test buy signal generation"""
        analysis = {'momentum': 0.025}
        signal = self.agent.generate_signal(analysis)
        
        self.assertEqual(signal['signal'], 'buy')
        self.assertGreater(signal['strength'], 0)
    
    def test_generate_sell_signal(self):
        """Test sell signal generation"""
        analysis = {'momentum': -0.025}
        signal = self.agent.generate_signal(analysis)
        
        self.assertEqual(signal['signal'], 'sell')
        self.assertGreater(signal['strength'], 0)
    
    def test_generate_hold_signal(self):
        """Test hold signal generation for neutral momentum"""
        analysis = {'momentum': 0.01}
        signal = self.agent.generate_signal(analysis)
        
        self.assertEqual(signal['signal'], 'hold')

class TestTrendAgent(unittest.TestCase):
    def setUp(self):
        self.agent = TrendAgent()
    
    def test_analyze_trend_strength(self):
        """Test trend strength calculation"""
        # Create data with clear trend
        prices = [{'close': 100 + i*2, 'volume': 1000} for i in range(60)]
        result = self.agent.analyze({'prices': prices})
        
        self.assertIn('trend_strength', result)
    
    def test_generate_long_signal(self):
        """Test long signal for strong uptrend"""
        analysis = {'trend_strength': 0.08}
        signal = self.agent.generate_signal(analysis)
        
        self.assertEqual(signal['signal'], 'long')
        self.assertGreater(signal['strength'], 0)
    
    def test_generate_short_signal(self):
        """Test short signal for strong downtrend"""
        analysis = {'trend_strength': -0.08}
        signal = self.agent.generate_signal(analysis)
        
        self.assertEqual(signal['signal'], 'short')
        self.assertGreater(signal['strength'], 0)

class TestDecisionTower(unittest.TestCase):
    def setUp(self):
        self.agents = [
            EnvironmentAgent(),
            ShortTermAgent(),
            TrendAgent()
        ]
        self.tower = DecisionTower(self.agents)
    
    def test_aggregate_signals_buy(self):
        """Test signal aggregation when agents recommend buy"""
        signals = {
            'EnvironmentAgent': {'signal': 'buy', 'strength': 0.8},
            'ShortTermAgent': {'signal': 'buy', 'strength': 0.9},
            'TrendAgent': {'signal': 'long', 'strength': 0.7}
        }
        
        result = self.tower.aggregate_signals(signals)
        
        self.assertEqual(result['action'], 'buy')
        self.assertGreater(result['confidence'], 0)
    
    def test_aggregate_signals_sell(self):
        """Test signal aggregation when agents recommend sell"""
        signals = {
            'EnvironmentAgent': {'signal': 'sell', 'strength': 0.8},
            'ShortTermAgent': {'signal': 'sell', 'strength': 0.9},
            'TrendAgent': {'signal': 'short', 'strength': 0.7}
        }
        
        result = self.tower.aggregate_signals(signals)
        
        self.assertEqual(result['action'], 'sell')
    
    def test_aggregate_signals_hold(self):
        """Test signal aggregation when agents disagree"""
        signals = {
            'EnvironmentAgent': {'signal': 'buy', 'strength': 0.4},
            'ShortTermAgent': {'signal': 'sell', 'strength': 0.4},
            'TrendAgent': {'signal': 'neutral', 'strength': 0.5}
        }
        
        result = self.tower.aggregate_signals(signals)
        
        self.assertEqual(result['action'], 'hold')

if __name__ == '__main__':
    unittest.main()
