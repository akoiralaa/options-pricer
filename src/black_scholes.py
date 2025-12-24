import numpy as np
from scipy.stats import norm
from scipy.optimize import fminbound


class BlackScholesModel:
    """
    Black-Scholes options pricing model.
    
    Prices European-style options and calculates Greeks.
    
    Parameters:
    -----------
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to expiration (in years)
    r : float
        Risk-free interest rate (annual)
    sigma : float
        Volatility (annual, as decimal)
    """
    
    def __init__(self, S, K, T, r, sigma):
        self.S = S  # Current stock price
        self.K = K  # Strike price
        self.T = T  # Time to expiration
        self.r = r  # Risk-free rate
        self.sigma = sigma  # Volatility
        
        # Pre-calculate d1 and d2 (used in most Greeks)
        self.d1 = self._calculate_d1()
        self.d2 = self.d1 - self.sigma * np.sqrt(self.T)
    
    def _calculate_d1(self):
        """Calculate d1 from Black-Scholes formula"""
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (
            self.sigma * np.sqrt(self.T)
        )
    
    def call_price(self):
        """Calculate European call option price"""
        call = (self.S * norm.cdf(self.d1)) - (
            self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        )
        return call
    
    def put_price(self):
        """Calculate European put option price"""
        put = (self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)) - (
            self.S * norm.cdf(-self.d1)
        )
        return put
    
    def call_delta(self):
        """Delta: rate of change of call price w.r.t. stock price"""
        return norm.cdf(self.d1)
    
    def put_delta(self):
        """Delta: rate of change of put price w.r.t. stock price"""
        return norm.cdf(self.d1) - 1
    
    def gamma(self):
        """Gamma: rate of change of delta w.r.t. stock price"""
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))
    
    def call_vega(self):
        """Vega: rate of change of call price w.r.t. volatility"""
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) / 100  # Divided by 100 for 1% change
    
    def put_vega(self):
        """Vega: rate of change of put price w.r.t. volatility (same as call)"""
        return self.call_vega()
    
    def call_theta(self):
        """Theta: rate of change of call price w.r.t. time (per day)"""
        term1 = -(self.S * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T))
        term2 = -self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        return (term1 + term2) / 365  # Convert to daily theta
    
    def put_theta(self):
        """Theta: rate of change of put price w.r.t. time (per day)"""
        term1 = -(self.S * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T))
        term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
        return (term1 + term2) / 365  # Convert to daily theta
    
    def call_rho(self):
        """Rho: rate of change of call price w.r.t. interest rate"""
        return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) / 100  # Per 1% change
    
    def put_rho(self):
        """Rho: rate of change of put price w.r.t. interest rate"""
        return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2) / 100  # Per 1% change


def get_all_greeks(S, K, T, r, sigma, option_type='call'):
    """
    Convenience function to get all Greeks at once.
    
    Parameters:
    -----------
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to expiration (in years)
    r : float
        Risk-free interest rate
    sigma : float
        Volatility
    option_type : str
        'call' or 'put'
    
    Returns:
    --------
    dict : Dictionary with price and all Greeks
    """
    bs = BlackScholesModel(S, K, T, r, sigma)
    
    if option_type.lower() == 'call':
        return {
            'price': bs.call_price(),
            'delta': bs.call_delta(),
            'gamma': bs.gamma(),
            'vega': bs.call_vega(),
            'theta': bs.call_theta(),
            'rho': bs.call_rho()
        }
    elif option_type.lower() == 'put':
        return {
            'price': bs.put_price(),
            'delta': bs.put_delta(),
            'gamma': bs.gamma(),
            'vega': bs.put_vega(),
            'theta': bs.put_theta(),
            'rho': bs.put_rho()
        }
    else:
        raise ValueError("option_type must be 'call' or 'put'")