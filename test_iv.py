import sys
sys.path.insert(0, 'src')

from black_scholes import BlackScholesModel
from implied_vol import calculate_iv

# First, generate a market price using a known volatility
S = 100
K = 100
T = 30/365
r = 0.05
true_vol = 0.25  # 25% actual volatility

bs = BlackScholesModel(S, K, T, r, true_vol)
market_price_call = bs.call_price()
market_price_put = bs.put_price()

print("\n=== Implied Volatility Test ===")
print(f"True Volatility: {true_vol*100}%")
print(f"Market Call Price: ${market_price_call:.4f}")
print(f"Market Put Price: ${market_price_put:.4f}\n")

# Now reverse-engineer the volatility from the price
implied_vol_call = calculate_iv(S, K, T, r, market_price_call, 'call')
implied_vol_put = calculate_iv(S, K, T, r, market_price_put, 'put')

print(f"Implied Vol (Call): {implied_vol_call*100:.4f}%")
print(f"Implied Vol (Put): {implied_vol_put*100:.4f}%")
print(f"Difference: {abs(implied_vol_call - true_vol)*100:.6f}%\n")

# Verify by pricing with recovered volatility
bs_recovered = BlackScholesModel(S, K, T, r, implied_vol_call)
recovered_price = bs_recovered.call_price()
print(f"Recovered Call Price: ${recovered_price:.4f}")
print(f"Price Match: ${abs(recovered_price - market_price_call):.10f}")
