import numpy as np
from scipy.optimize import brentq
from black_scholes import BlackScholesModel


class ImpliedVolatility:
    """
    Calculate implied volatility from option market prices.
    
    Uses numerical methods to solve for the volatility that matches
    the observed market price.
    """
    
    def __init__(self, S, K, T, r, market_price, option_type='call'):
        """
        Parameters:
        -----------
        S : float
            Current stock price
        K : float
            Strike price
        T : float
            Time to expiration (in years)
        r : float
            Risk-free rate
        market_price : float
            Observed market price of the option
        option_type : str
            'call' or 'put'
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.market_price = market_price
        self.option_type = option_type.lower()
        
        if self.option_type not in ['call', 'put']:
            raise ValueError("option_type must be 'call' or 'put'")
    
    def _price_difference(self, sigma):
        """
        Calculate difference between theoretical and market price.
        This is what we're trying to minimize.
        """
        bs = BlackScholesModel(self.S, self.K, self.T, self.r, sigma)
        
        if self.option_type == 'call':
            theoretical_price = bs.call_price()
        else:
            theoretical_price = bs.put_price()
        
        return theoretical_price - self.market_price
    
    def solve(self, initial_guess=0.3, bounds=(0.001, 5.0)):
        """
        Solve for implied volatility using Brent's method.
        
        Parameters:
        -----------
        initial_guess : float
            Starting volatility guess (default 30%)
        bounds : tuple
            Min and max bounds for volatility search
        
        Returns:
        --------
        float : Implied volatility (as decimal, e.g., 0.25 = 25%)
        """
        try:
            # Use Brent's method for root finding
            # We're looking for sigma where price_diff = 0
            iv = brentq(self._price_difference, bounds[0], bounds[1])
            return iv
        except ValueError:
            # If Brent's method fails, use Newton-Raphson with vega as derivative
            return self._newton_raphson(initial_guess)
    
    def _newton_raphson(self, sigma_guess, max_iterations=100, tolerance=1e-6):
        """
        Newton-Raphson method for solving implied vol.
        Uses vega as the derivative.
        """
        sigma = sigma_guess
        
        for i in range(max_iterations):
            bs = BlackScholesModel(self.S, self.K, self.T, self.r, sigma)
            
            if self.option_type == 'call':
                price_diff = bs.call_price() - self.market_price
                vega = bs.call_vega()
            else:
                price_diff = bs.put_price() - self.market_price
                vega = bs.put_vega()
            
            # Check convergence
            if abs(price_diff) < tolerance:
                return sigma
            
            # Newton-Raphson update: sigma_new = sigma - f(sigma) / f'(sigma)
            # Vega is in terms of 1% change, so multiply by 100
            if vega > 1e-6:
                sigma = sigma - price_diff / (vega * 100)
            else:
                break
        
        return sigma


def calculate_iv(S, K, T, r, market_price, option_type='call'):
    """
    Convenience function to calculate implied volatility.
    
    Parameters:
    -----------
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to expiration (in years)
    r : float
        Risk-free rate
    market_price : float
        Observed market price
    option_type : str
        'call' or 'put'
    
    Returns:
    --------
    float : Implied volatility
    """
    iv_solver = ImpliedVolatility(S, K, T, r, market_price, option_type)
    return iv_solver.solve()