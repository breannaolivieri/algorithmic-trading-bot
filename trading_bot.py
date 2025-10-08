import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

print("="*70)
print("ALGORITHMIC TRADING BOT - MOVING AVERAGE CROSSOVER STRATEGY")
print("="*70)

# Get user input
ticker = input("\nEnter stock ticker to trade (e.g., AAPL): ").upper().strip()
initial_capital = float(input("Enter starting capital ($): "))

print(f"\nSetting up bot for {ticker} with ${initial_capital:,.2f} initial capital...")

# Download 2 years of data
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=2*365)

print("Downloading historical data...")
data = yf.download(ticker, start=start_date, end=end_date)

if data.empty:
    print(f"Error: Could not find data for {ticker}")
    exit()

# Handle multi-index columns
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

print(f"Analyzing {len(data)} trading days...")

# Calculate moving averages
short_window = 20  # 20-day moving average
long_window = 50   # 50-day moving average

data['MA_Short'] = data['Close'].rolling(window=short_window).mean()
data['MA_Long'] = data['Close'].rolling(window=long_window).mean()

# Generate signals
data['Signal'] = 0
data['Signal'][short_window:] = np.where(
    data['MA_Short'][short_window:] > data['MA_Long'][short_window:], 1, 0
)
data['Position'] = data['Signal'].diff()

# Drop NaN values
data = data.dropna()

print("\nTrading Strategy:")
print(f"  Short MA: {short_window} days")
print(f"  Long MA:  {long_window} days")
print("  BUY when short MA crosses above long MA")
print("  SELL when short MA crosses below long MA")

# Simulate trading
capital = initial_capital
shares = 0
trades = []

for index, row in data.iterrows():
    if row['Position'] == 1:  # Buy signal
        if capital > 0:
            shares_bought = capital // row['Close']
            cost = shares_bought * row['Close']
            shares += shares_bought
            capital -= cost
            trades.append({
                'Date': index,
                'Action': 'BUY',
                'Price': row['Close'],
                'Shares': shares_bought,
                'Total_Shares': shares,
                'Capital': capital
            })
    
    elif row['Position'] == -1:  # Sell signal
        if shares > 0:
            revenue = shares * row['Close']
            capital += revenue
            trades.append({
                'Date': index,
                'Action': 'SELL',
                'Price': row['Close'],
                'Shares': shares,
                'Total_Shares': 0,
                'Capital': capital
            })
            shares = 0

# Final portfolio value
final_value = capital + (shares * data['Close'].iloc[-1])
total_return = final_value - initial_capital
return_pct = (total_return / initial_capital) * 100

# Buy and hold comparison
buy_hold_shares = initial_capital / data['Close'].iloc[0]
buy_hold_value = buy_hold_shares * data['Close'].iloc[-1]
buy_hold_return = buy_hold_value - initial_capital
buy_hold_pct = (buy_hold_return / initial_capital) * 100

# Display results
print("\n" + "="*70)
print("TRADING BOT PERFORMANCE")
print("="*70)
print(f"Total Trades Executed: {len(trades)}")
print(f"  Buy Orders:  {sum(1 for t in trades if t['Action'] == 'BUY')}")
print(f"  Sell Orders: {sum(1 for t in trades if t['Action'] == 'SELL')}")
print()
print(f"Initial Capital:       ${initial_capital:,.2f}")
print(f"Final Portfolio Value: ${final_value:,.2f}")
print(f"Total Return:          ${total_return:,.2f} ({return_pct:+.2f}%)")
print()
print("="*70)
print("COMPARISON: BOT vs BUY & HOLD")
print("="*70)
print(f"Bot Strategy Return:      ${total_return:,.2f} ({return_pct:+.2f}%)")
print(f"Buy & Hold Return:        ${buy_hold_return:,.2f} ({buy_hold_pct:+.2f}%)")
print(f"Difference:               ${total_return - buy_hold_return:,.2f}")
print("="*70)

if return_pct > buy_hold_pct:
    print("Bot OUTPERFORMED buy & hold strategy!")
else:
    print("Buy & hold performed better this time.")

# Show recent trades
if trades:
    print("\nRecent Trades (last 5):")
    trades_df = pd.DataFrame(trades)
    print(trades_df.tail(5).to_string(index=False))

# Visualize
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Price and moving averages
ax1.plot(data.index, data['Close'], label='Stock Price', color='black', alpha=0.6, linewidth=1.5)
ax1.plot(data.index, data['MA_Short'], label=f'{short_window}-Day MA', color='blue', linewidth=1.5)
ax1.plot(data.index, data['MA_Long'], label=f'{long_window}-Day MA', color='red', linewidth=1.5)

# Mark buy/sell signals
buy_signals = data[data['Position'] == 1]
sell_signals = data[data['Position'] == -1]

ax1.scatter(buy_signals.index, buy_signals['Close'], 
           color='green', marker='^', s=100, label='Buy Signal', zorder=5)
ax1.scatter(sell_signals.index, sell_signals['Close'], 
           color='red', marker='v', s=100, label='Sell Signal', zorder=5)

ax1.set_title(f'{ticker} - Algorithmic Trading Bot Signals', fontsize=14, fontweight='bold')
ax1.set_ylabel('Price ($)', fontsize=12)
ax1.legend(loc='best')
ax1.grid(alpha=0.3)

# Portfolio value over time
portfolio_values = []
current_capital = initial_capital
current_shares = 0

for index, row in data.iterrows():
    if row['Position'] == 1 and current_capital > 0:
        shares_bought = current_capital // row['Close']
        current_shares += shares_bought
        current_capital -= shares_bought * row['Close']
    elif row['Position'] == -1 and current_shares > 0:
        current_capital += current_shares * row['Close']
        current_shares = 0
    
    portfolio_value = current_capital + (current_shares * row['Close'])
    portfolio_values.append(portfolio_value)

ax2.plot(data.index, portfolio_values, label='Bot Portfolio Value', color='green', linewidth=2)
ax2.axhline(y=initial_capital, color='gray', linestyle='--', label='Initial Capital', linewidth=1)
ax2.fill_between(data.index, initial_capital, portfolio_values, 
                 where=np.array(portfolio_values) >= initial_capital, 
                 color='green', alpha=0.2, label='Profit')
ax2.fill_between(data.index, initial_capital, portfolio_values, 
                 where=np.array(portfolio_values) < initial_capital, 
                 color='red', alpha=0.2, label='Loss')

ax2.set_title('Portfolio Value Over Time', fontsize=14, fontweight='bold')
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('Portfolio Value ($)', fontsize=12)
ax2.legend(loc='best')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('trading_bot_performance.png', dpi=300)
print("\n Performance chart saved as 'trading_bot_performance.png'!")
plt.show()
