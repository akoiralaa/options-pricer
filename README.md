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

Simply run the interactive calculator:
```bash
python3 launch_pricer.py
```

### How It Works

1. **Enter Parameters** - Input your stock price, strike, expiration, rate, and volatility
2. **Automatic Analysis** - The tool instantly runs all 5 analyses:
   - Black-Scholes pricing
   - Monte Carlo simulation
   - Implied volatility analysis
   - Exotic options pricing
   - Method comparison

3. **View Results** - See all Greeks, confidence intervals, and pricing comparisons
4. **Visualize** - Generate beautiful graphs showing payoff diagrams, sensitivities, and simulations
5. **Iterate** - Input new parameters or exit

### Example Session
```
Enter parameters:
Stock Price: 100
Strike Price: 100
Days to Expiration: 30
Risk-free Rate: 0.05
Volatility: 0.20

[Automatically runs all analyses...]

RESULTS:
1. Black-Scholes Prices & Greeks
2. Monte Carlo Simulation (100,000 paths)
3. Implied Volatility Analysis
4. Exotic Options (Asian, Barrier, Lookback)
5. Comparison of methods

NEXT:
- Visualize Data (Graphs & Charts)
- Input New Parameters
- Exit
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
│   ├── black_scholes.py          # Black-Scholes pricer and Greeks
│   ├── implied_vol.py            # Implied volatility solver
│   ├── monte_carlo.py            # Monte Carlo simulation
│   ├── pricer_interface.py        # User interface
│   └── interactive_visualizer.py  # Visualization engine
├── tests/
│   └── test_black_scholes.py      # Unit tests
├── launch_pricer.py               # Main entry point
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

## Visualizations

The tool generates 4 beautiful graphs:

1. **Option Payoff Diagrams** - Shows profit/loss at expiration
2. **Price Sensitivity** - How option prices change with stock price
3. **The Greeks** - Visual explanation of all Greeks
4. **Monte Carlo Simulation** - Stock paths and payoff distributions

## Performance

- Black-Scholes: < 1ms per option
- Implied Vol (Brent): 2-5ms per option
- Monte Carlo (100K paths): 50-100ms per option

## Use Cases

- **Traders** - Quick option pricing and Greeks for decision making
- **Risk Managers** - Understand exposure and sensitivities
- **Students** - Learn options pricing interactively
- **Quants** - Validate pricing models and compare methods
- **Portfolio Managers** - Analyze exotic option strategies

## References

- Black, F., & Scholes, M. (1973). "The pricing of options and corporate liabilities"
- Hull, J. C. (2012). "Options, Futures, and Other Derivatives"
- Glasserman, P. (2004). "Monte Carlo Methods in Financial Engineering"

## License

MIT

## Author

Built as a quantitative finance portfolio project for systematic option pricing and analysis.
