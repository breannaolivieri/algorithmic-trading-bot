import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

print("="*70)
print("STRATEGY COMPARISON TOOL - BACKTEST MULTIPLE STRATEGIES")
print("="*70)

ticker = input("\nEnter stock ticker (e.g., AAPL): ").upper().strip()
initial_capital = 100000

# Download 3 years of data
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=3*365)

print(f"\nDownloading {ticker} data for strategy comparison...")
data = yf.download(ticker, start=start_date, end=end_date)

if data.empty:
    print(f"Error: Could not find data for {ticker}")
    exit()

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

print(f"Testing strategies on {len(data)} trading days...\n")

# Strategy 1: Buy and Hold
buy_hold_shares = initial_capital / data['Close'].iloc[0]
buy_hold_final = buy_hold_shares * data['Close'].iloc[-1]
buy_hold_return = ((buy_hold_final - initial_capital) / initial_capital) * 100

# Strategy 2: Moving Average Crossover (20/50)
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()
data['Signal_20_50'] = np.where(data['MA20'] > data['MA50'], 1, 0)
data['Position_20_50'] = data['Signal_20_50'].diff()

capital_20_50 = initial_capital
shares_20_50 = 0
for index, row in data.iterrows():
    if row['Position_20_50'] == 1 and capital_20_50 > 0:
        shares_20_50 = capital_20_50 / row['Close']
        capital_20_50 = 0
    elif row['Position_20_50'] == -1 and shares_20_50 > 0:
        capital_20_50 = shares_20_50 * row['Close']
        shares_20_50 = 0

ma_20_50_final = capital_20_50 + (shares_20_50 * data['Close'].iloc[-1])
ma_20_50_return = ((ma_20_50_final - initial_capital) / initial_capital) * 100

# Strategy 3: Moving Average Crossover (10/30) - faster
data['MA10'] = data['Close'].rolling(window=10).mean()
data['MA30'] = data['Close'].rolling(window=30).mean()
data['Signal_10_30'] = np.where(data['MA10'] > data['MA30'], 1, 0)
data['Position_10_30'] = data['Signal_10_30'].diff()

capital_10_30 = initial_capital
shares_10_30 = 0
for index, row in data.iterrows():
    if row['Position_10_30'] == 1 and capital_10_30 > 0:
        shares_10_30 = capital_10_30 / row['Close']
        capital_10_30 = 0
    elif row['Position_10_30'] == -1 and shares_10_30 > 0:
        capital_10_30 = shares_10_30 * row['Close']
        shares_10_30 = 0

ma_10_30_final = capital_10_30 + (shares_10_30 * data['Close'].iloc[-1])
ma_10_30_return = ((ma_10_30_final - initial_capital) / initial_capital) * 100

# Display results
print("="*70)
print("STRATEGY COMPARISON RESULTS")
print("="*70)
print(f"Initial Capital: ${initial_capital:,.2f}")
print()
print(f"1. BUY & HOLD")
print(f"   Final Value: ${buy_hold_final:,.2f}")
print(f"   Return:      {buy_hold_return:+.2f}%")
print()
print(f"2. MOVING AVERAGE CROSSOVER (20/50 day)")
print(f"   Final Value: ${ma_20_50_final:,.2f}")
print(f"   Return:      {ma_20_50_return:+.2f}%")
print()
print(f"3. MOVING AVERAGE CROSSOVER (10/30 day - Faster)")
print(f"   Final Value: ${ma_10_30_final:,.2f}")
print(f"   Return:      {ma_10_30_return:+.2f}%")
print("="*70)

# Find best strategy
strategies = {
    'Buy & Hold': buy_hold_return,
    'MA 20/50': ma_20_50_return,
    'MA 10/30': ma_10_30_return
}
best_strategy = max(strategies, key=strategies.get)
print(f"\n BEST STRATEGY: {best_strategy} with {strategies[best_strategy]:+.2f}% return")

# Visualize comparison
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Strategy returns comparison
strategy_names = list(strategies.keys())
returns = list(strategies.values())
colors = ['green' if r > 0 else 'red' for r in returns]

ax1.bar(strategy_names, returns, color=colors, alpha=0.7, edgecolor='black')
ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax1.set_title(f'{ticker} - Strategy Performance Comparison', fontsize=14, fontweight='bold')
ax1.set_ylabel('Return (%)', fontsize=12)
ax1.grid(axis='y', alpha=0.3)

for i, (name, ret) in enumerate(zip(strategy_names, returns)):
    ax1.text(i, ret + (2 if ret > 0 else -2), f'{ret:.2f}%', 
            ha='center', fontweight='bold', fontsize=11)

# Price chart with signals
ax2.plot(data.index, data['Close'], label='Stock Price', color='black', alpha=0.5, linewidth=1)
ax2.plot(data.index, data['MA20'], label='20-Day MA', color='blue', linewidth=1)
ax2.plot(data.index, data['MA50'], label='50-Day MA', color='red', linewidth=1)

buy_20_50 = data[data['Position_20_50'] == 1]
sell_20_50 = data[data['Position_20_50'] == -1]

ax2.scatter(buy_20_50.index, buy_20_50['Close'], 
           color='green', marker='^', s=80, label='Buy (20/50)', zorder=5, alpha=0.7)
ax2.scatter(sell_20_50.index, sell_20_50['Close'], 
           color='red', marker='v', s=80, label='Sell (20/50)', zorder=5, alpha=0.7)

ax2.set_title('Price Chart with Trading Signals (20/50 Strategy)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('Price ($)', fontsize=12)
ax2.legend(loc='best')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('strategy_comparison.png', dpi=300)
print("\n Comparison chart saved as 'strategy_comparison.png'!")
plt.show()
