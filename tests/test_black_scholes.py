import sys
sys.path.insert(0, '../src')

from black_scholes import BlackScholesModel

S = 100
K = 100
T = 30/365
r = 0.05
sigma = 0.20

bs = BlackScholesModel(S, K, T, r, sigma)

print("\n=== Black-Scholes Option Pricing ===")
print(f"Stock Price: ${S}")
print(f"Strike Price: ${K}")
print(f"Days to Expiration: 30")
print(f"Risk-free Rate: {r*100}%")
print(f"Volatility: {sigma*100}%\n")

print("CALL OPTION:")
print(f"  Price: ${bs.call_price():.4f}")
print(f"  Delta: {bs.call_delta():.4f}")
print(f"  Gamma: {bs.gamma():.6f}")
print(f"  Vega: ${bs.call_vega():.4f}")
print(f"  Theta: ${bs.call_theta():.4f}")
print(f"  Rho: ${bs.call_rho():.4f}\n")

print("PUT OPTION:")
print(f"  Price: ${bs.put_price():.4f}")
print(f"  Delta: {bs.put_delta():.4f}")
print(f"  Gamma: {bs.gamma():.6f}")
print(f"  Vega: ${bs.put_vega():.4f}")
print(f"  Theta: ${bs.put_theta():.4f}")
print(f"  Rho: ${bs.put_rho():.4f}\n")
