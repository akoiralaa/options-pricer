import numpy as np
from scipy.optimize import brentq
from black_scholes import BlackScholesModel


class ImpliedVolatility:
    """
    Find the volatility that matches a market price.
    
    This is the reverse of pricing - we know the price,
    need to find what volatility it implies.
    """
    
    def __init__(self, S, K, T, r, market_price, option_type='call'):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.market_price = market_price
        self.option_type = option_type.lower()
        
        if self.option_type not in ['call', 'put']:
            raise ValueError("option_type must be 'call' or 'put'")
    
    def _price_diff(self, sigma):
        """How far off are we from the market price with this volatility?"""
        bs = BlackScholesModel(self.S, self.K, self.T, self.r, sigma)
        
        if self.option_type == 'call':
            theo_price = bs.call_price()
        else:
            theo_price = bs.put_price()
        
        return theo_price - self.market_price
    
    def solve(self, initial_guess=0.3, bounds=(0.001, 5.0)):
        """
        Find the implied volatility.
        Uses Brent's method (reliable numerical solver).
        """
        try:
            iv = brentq(self._price_diff, bounds[0], bounds[1])
            return iv
        except ValueError:
            # If Brent fails, fall back to Newton-Raphson
            return self._newton_raphson(initial_guess)
    
    def _newton_raphson(self, sigma_guess, max_iter=100, tol=1e-6):
        """
        Newton-Raphson method as backup.
        Uses vega as the derivative (how price changes with vol).
        """
        sigma = sigma_guess
        
        for i in range(max_iter):
            bs = BlackScholesModel(self.S, self.K, self.T, self.r, sigma)
            
            if self.option_type == 'call':
                price_diff = bs.call_price() - self.market_price
                vega = bs.call_vega()
            else:
                price_diff = bs.put_price() - self.market_price
                vega = bs.put_vega()
            
            # If we're close enough, stop
            if abs(price_diff) < tol:
                return sigma
            
            # Newton-Raphson: sigma_new = sigma - f(sigma) / f'(sigma)
            # Vega is per 1%, so multiply by 100
            if vega > 1e-6:
                sigma = sigma - price_diff / (vega * 100)
            else:
                break
        
        return sigma


def calculate_iv(S, K, T, r, market_price, option_type='call'):
    """Quick function to find implied vol"""
    solver = ImpliedVolatility(S, K, T, r, market_price, option_type)
    return solver.solve()