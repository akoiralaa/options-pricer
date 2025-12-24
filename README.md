# Options Pricer

A professional-grade options pricing library implementing Black-Scholes model, Greeks calculations, implied volatility solving, and Monte Carlo simulations for exotic derivatives.

## Features

### Core Pricing
- **Black-Scholes Model** - European call/put option pricing
- **Greeks Calculation** - Delta, Gamma, Vega, Theta, Rho
- **Implied Volatility** - Reverse-engineer volatility from market prices using Brent's method
- **Monte Carlo Simulation** - Price exotic options and validate analytical results

### Supported Options
- European Calls/Puts
- Asian Options (average price)
- Barrier Options (knock-out, knock-in)
- Lookback Options (max price observed)

## Installation
```bash
pip install numpy scipy pandas matplotlib plotly jupyter
```

## Quick Start

### Price a European Option
```python
from src.black_scholes import BlackScholesModel

# Parameters
S = 100      # Stock price
K = 100      # Strike price
T = 30/365   # 30 days to expiration
r = 0.05     # 5% risk-free rate
sigma = 0.20 # 20% volatility

# Create pricer
bs = BlackScholesModel(S, K, T, r, sigma)

# Get price and Greeks
print(f"Call Price: ${bs.call_price():.4f}")
print(f"Delta: {bs.call_delta():.4f}")
print(f"Gamma: {bs.gamma():.6f}")
print(f"Vega: ${bs.call_vega():.4f}")
print(f"Theta: ${bs.call_theta():.4f}")
print(f"Rho: ${bs.call_rho():.4f}")
```

### Calculate Implied Volatility
```python
from src.implied_vol import calculate_iv

# Market observed price
market_price = 2.50

# Solve for implied volatility
iv = calculate_iv(S=100, K=100, T=30/365, r=0.05, 
                  market_price=market_price, option_type='call')
print(f"Implied Volatility: {iv*100:.2f}%")
```

### Price Exotic Options with Monte Carlo
```python
from src.monte_carlo import MonteCarloSimulation

# Create simulator
mc = MonteCarloSimulation(S=100, K=100, T=30/365, r=0.05, 
                         sigma=0.20, num_simulations=100000)

# Price exotic options
asian = mc.asian_call()
barrier = mc.barrier_call(barrier_level=110, barrier_type='knock_out')
lookback = mc.lookback_call()

print(f"Asian Call: ${asian['price']:.4f}")
print(f"Barrier Call: ${barrier['price']:.4f}")
print(f"Lookback Call: ${lookback['price']:.4f}")
```

## Mathematical Background

### Black-Scholes Formula

For a European call option:
```
C = S₀·N(d₁) - K·e^(-rT)·N(d₂)
```

Where:
```
d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)
d₂ = d₁ - σ√T
```

### Greeks

- **Delta (Δ)** - Rate of change of option price w.r.t. stock price
- **Gamma (Γ)** - Rate of change of delta w.r.t. stock price  
- **Vega (ν)** - Rate of change of option price w.r.t. volatility (per 1%)
- **Theta (Θ)** - Rate of change of option price w.r.t. time (per day)
- **Rho (ρ)** - Rate of change of option price w.r.t. interest rate (per 1%)

### Implied Volatility

Uses Brent's method to solve for σ such that:
```
BlackScholesPrice(σ) = MarketPrice
```

Falls back to Newton-Raphson if needed.

### Monte Carlo Method

Simulates stock price paths using geometric Brownian motion:
```
dS = μS dt + σS dW
```

Then computes expected payoff under risk-neutral measure.

## Project Structure
```
options-pricer/
├── src/
│   ├── __init__.py
│   ├── black_scholes.py      # Black-Scholes pricer and Greeks
│   ├── implied_vol.py        # Implied volatility solver
│   └── monte_carlo.py        # Monte Carlo simulation
├── tests/
│   └── test_pricer.py        # Unit tests
├── run_simple.py             # Quick start script
├── test_iv.py                # Implied vol test
├── test_monte_carlo.py       # Monte Carlo test
└── README.md
```

## Results

### Black-Scholes vs Monte Carlo (100K simulations)

| Option Type | B-S Price | MC Price | Error |
|---|---|---|---|
| Call | $2.4934 | $2.4957 ± $0.0114 | 0.09% |
| Put | $2.0833 | $2.0769 ± $0.0098 | -0.31% |

### Implied Volatility Accuracy

| Input Vol | Recovered Vol | Error |
|---|---|---|
| 25.00% | 25.0000% | 0.000% |

## Performance

- Black-Scholes: < 1ms per option
- Implied Vol (Brent): 2-5ms per option
- Monte Carlo (100K paths): 50-100ms per option

## Future Enhancements

- [ ] American option pricing (binomial tree)
- [ ] Volatility surface visualization
- [ ] Real market data integration
- [ ] Greeks surface plots
- [ ] Vectorized batch pricing

## References

- Black, F., & Scholes, M. (1973). "The pricing of options and corporate liabilities"
- Hull, J. C. (2012). "Options, Futures, and Other Derivatives"
- Glasserman, P. (2004). "Monte Carlo Methods in Financial Engineering"

## License

MIT

## Author

Built as a quantitative finance portfolio project for systematic option pricing and analysis.
