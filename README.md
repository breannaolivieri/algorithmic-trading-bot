# Algorithmic Trading Bot

An automated trading system that executes trades based on technical analysis strategies. Features multiple trading algorithms with backtesting capabilities and performance visualization.

## Features
- **Automated Trading**: Executes buy/sell orders based on moving average crossover signals
- **Paper Trading**: Simulates trades with virtual capital (zero financial risk)
- **Multiple Strategies**: Compare different trading algorithms (MA 20/50, MA 10/30, Buy & Hold)
- **Performance Tracking**: Real-time portfolio value monitoring and trade history
- **Backtesting**: Test strategies on historical data to evaluate performance
- **Visual Analytics**: Charts showing price movements, signals, and portfolio performance
- **Strategy Comparison Tool**: Compare multiple strategies side-by-side

## Technologies Used
- **Python 3.13**
- **yfinance**: Real-time and historical market data
- **pandas**: Time series data manipulation
- **NumPy**: Mathematical operations and signal processing
- **matplotlib**: Performance visualization and charting

## Installation

1. Clone this repository
2. Install required packages:
"```bash"
pip3 install yfinance pandas numpy matplotlib

## Usage
Main Trading Bot
- python3 trading_bot.py

Enter a stock ticker and starting capital. The bot will:

1. Download historical data
2. Generate buy/sell signals using moving average crossover
3. Execute simulated trades
4. Display performance metrics and compare to buy & hold

## Strategy Comparison Tool
- python3 strategy_comparison.py
    - Tests multiple strategies on the same stock and shows which performs best.

Moving Average Crossover:

- Buy Signal: When short-term moving average crosses above long-term moving average
- Sell Signal: When short-term moving average crosses below long-term moving average

This strategy identifies momentum shifts and trend changes in stock prices.

## How It Works

1. **Data Collection:** Downloads 2 years of historical stock data
2. **Signal Generation:** Calculates moving averages and identifies crossover points
3. **Trade Execution:** Simulates buying/selling at signal points
4. **Performance Tracking:** Monitors portfolio value throughout the period
5. **Analysis:** Compares bot performance to simple buy & hold strategy

## Sample Output

- Total trades executed (buy and sell orders)
- Final portfolio value and total return percentage
- Comparison to buy & hold strategy
- Recent trade history with dates, prices, and shares
- Visual charts showing:

    - Price movements with buy/sell signals
    - Portfolio value over time
    - Strategy performance comparison



## Skills Demonstrated

1. Algorithmic trading system design
2. Technical analysis and trading strategies
3. Financial API integration
4. Time series data processing
5. Backtesting and performance evaluation
6. Risk management (paper trading)
7. Quantitative analysis