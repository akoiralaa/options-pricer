import sys
sys.path.insert(0, 'src')

from black_scholes import BlackScholesModel
from monte_carlo import MonteCarloSimulation

S = 100
K = 100
T = 30/365
r = 0.05
sigma = 0.20

# Compare Black-Scholes vs Monte Carlo
print("\n=== Black-Scholes vs Monte Carlo ===\n")

# Black-Scholes
bs = BlackScholesModel(S, K, T, r, sigma)
bs_call = bs.call_price()
bs_put = bs.put_price()

print(f"Black-Scholes Prices:")
print(f"  Call: ${bs_call:.4f}")
print(f"  Put: ${bs_put:.4f}\n")

# Monte Carlo
mc = MonteCarloSimulation(S, K, T, r, sigma, num_simulations=100000)

print(f"Monte Carlo (100,000 simulations):")
mc_call = mc.european_call()
mc_put = mc.european_put()

print(f"  Call: ${mc_call['price']:.4f} ± ${mc_call['std_error']:.4f}")
print(f"    95% CI: (${mc_call['confidence_95'][0]:.4f}, ${mc_call['confidence_95'][1]:.4f})")
print(f"  Put: ${mc_put['price']:.4f} ± ${mc_put['std_error']:.4f}")
print(f"    95% CI: (${mc_put['confidence_95'][0]:.4f}, ${mc_put['confidence_95'][1]:.4f})\n")

# Exotic options
print(f"Exotic Options (Monte Carlo):")
asian = mc.asian_call()
print(f"  Asian Call: ${asian['price']:.4f} ± ${asian['std_error']:.4f}")

barrier = mc.barrier_call(barrier_level=110, barrier_type='knock_out')
print(f"  Barrier Call (KO @ 110): ${barrier['price']:.4f} ± ${barrier['std_error']:.4f}")

lookback = mc.lookback_call()
print(f"  Lookback Call: ${lookback['price']:.4f} ± ${lookback['std_error']:.4f}\n")
