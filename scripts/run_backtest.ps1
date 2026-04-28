# PowerShell script to run backtest
param(
    [string]$Strategy = "MultiAgentStrategy",
    [string]$Symbol = "BTC/USDT",
    [string]$Timeframe = "1h",
    [int]$Limit = 1000,
    [decimal]$InitialBalance = 10000
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "ReinforceTrade Backtest Runner" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Strategy: $Strategy"
Write-Host "Symbol: $Symbol"
Write-Host "Timeframe: $Timeframe"
Write-Host "Initial Balance: $InitialBalance"
Write-Host "==========================================" -ForegroundColor Cyan

# Check if virtual environment exists and activate
if (Test-Path "venv\Scripts\Activate.ps1") {
    & venv\Scripts\Activate.ps1
}

# Run the backtest
python examples\basic_backtest.py

Write-Host "==========================================" -ForegroundColor Green
Write-Host "Backtest completed!" -ForegroundColor Green
Write-Host "Check reports\ directory for results" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
