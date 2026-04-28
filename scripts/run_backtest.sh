#!/bin/bash
# Script to run backtest with proper configuration

set -e

# Configuration
STRATEGY=${STRATEGY:-"MultiAgentStrategy"}
SYMBOL=${SYMBOL:-"BTC/USDT"}
TIMEFRAME=${TIMEFRAME:-"1h"}
LIMIT=${LIMIT:-1000}
INITIAL_BALANCE=${INITIAL_BALANCE:-10000}

echo "=========================================="
echo "ReinforceTrade Backtest Runner"
echo "=========================================="
echo "Strategy: $STRATEGY"
echo "Symbol: $SYMBOL"
echo "Timeframe: $TIMEFRAME"
echo "Initial Balance: $INITIAL_BALANCE"
echo "=========================================="

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the backtest
python examples/basic_backtest.py \
    --symbol "$SYMBOL" \
    --timeframe "$TIMEFRAME" \
    --limit "$LIMIT" \
    --initial-balance "$INITIAL_BALANCE"

echo "=========================================="
echo "Backtest completed!"
echo "Check reports/ directory for results"
echo "=========================================="
