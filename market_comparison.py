import yfinance as yf
from black_scholes import *
from datetime import datetime
import matplotlib.pyplot as plt

ticker = yf.Ticker('SPY') # Gives acces to the SPDR S&P 500 ETF
S = ticker.history(period='1d')['Close'].iloc[-1] # Latest clsing value for SPY

expirations = ticker.options
# Pick an expiration ~30-60 days out
expiration_date = expirations[12] # picking expiration date 10th april on 4th march 2026

chain = ticker.option_chain(expiration_date) # chain contains all options data for 10th april
calls = chain.calls # pandas dataframe containing all call, strike price, bid , and ask for 10th april

# new column created called, mid, has the midpoint value of the bid and ask at that strike price
calls['mid'] = (calls['bid'] + calls['ask']) / 2
calls = calls[calls['bid'] > 0] # filtering out strike pricesf or which no one wants to buy the call
calls = calls[calls['mid'] > 0.5] # filtering out tiny mid prices because the implied volatility solver cannot take them
# strike prices need to be resonable, withing 20 percent of stock price, or the iv calcualtion wont work as expected
calls = calls[calls['strike'] > S * 0.8]
calls = calls[calls['strike'] < S * 1.2]
# Calculating time to expiry
T = (datetime.strptime(expiration_date, '%Y-%m-%d') - datetime.now()).days / 365

# hard coding the risk free rate for now
r = 0.05

# computing the implied volatility for each strike price
strikes = []
ivs = []

for index, row in calls.iterrows():
    # setting strike price from the strike column data in calls
    K = row['strike']
    market_price = row['mid']
    iv = implied_vol(S, K, T, r, market_price, "call")
    # adding calculated iv at strike price K to iv and K to strikes
    strikes.append(K)
    ivs.append(iv)

fig, ax = plt.subplots(figsize=(12, 8))
fig.suptitle('Implied Volatility Smile - SPY')
ax.plot(strikes, ivs)
ax.set_xlabel('Strike Price')
ax.set_ylabel('Implied Volatility')
ax.axvline(x=S, color='red', linestyle='--', label=f'Current Price ({S:.2f})')
ax.legend()
fig.savefig('images/iv_smile.png')
plt.show()

theoretical_prices = []
market_prices = []

for index, row in calls.iterrows():
    K = row['strike']
    market_price = row['mid']
    model_price = C(S, K, T, r, 0.2)
    theoretical_prices.append(model_price)
    market_prices.append(market_price)

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(calls['strike'], theoretical_prices, label='Black-Scholes (σ=0.20)')
ax2.plot(calls['strike'], market_prices, label='Market Mid Price')
ax2.axvline(x=S, color='red', linestyle='--', label=f'Current Price ({S:.2f})')
ax2.set_title('Theoretical vs Market Prices - SPY Calls')
ax2.set_xlabel('Strike Price')
ax2.set_ylabel('Option Price')
ax2.legend()
plt.tight_layout()
fig2.savefig('images/theoretical_vs_market.png')
plt.show()