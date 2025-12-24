import numpy as np
from black_scholes import BlackScholesModel


class MonteCarloSimulation:
    """
    Monte Carlo simulation for option pricing.
    
    Useful for:
    - Exotic options (Asian, Barrier, Lookback)
    - American options (early exercise)
    - Path-dependent payoffs
    """
    
    def __init__(self, S, K, T, r, sigma, num_simulations=10000, num_steps=252):
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
        sigma : float
            Volatility
        num_simulations : int
            Number of Monte Carlo paths
        num_steps : int
            Number of time steps per path
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.num_simulations = num_simulations
        self.num_steps = num_steps
        self.dt = T / num_steps
        
        # Pre-compute for efficiency
        self.drift = (r - 0.5 * sigma ** 2) * self.dt
        self.volatility_shock = sigma * np.sqrt(self.dt)
    
    def generate_paths(self, random_seed=None):
        """
        Generate stock price paths using geometric Brownian motion.
        
        dS = mu * S * dt + sigma * S * dW
        
        Returns:
        --------
        np.array : Shape (num_simulations, num_steps + 1)
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Initialize paths
        paths = np.zeros((self.num_simulations, self.num_steps + 1))
        paths[:, 0] = self.S
        
        # Generate random shocks
        shocks = np.random.standard_normal((self.num_simulations, self.num_steps))
        
        # Simulate paths
        for t in range(self.num_steps):
            paths[:, t + 1] = paths[:, t] * np.exp(
                self.drift + self.volatility_shock * shocks[:, t]
            )
        
        return paths
    
    def european_call(self):
        """Price European call option"""
        paths = self.generate_paths()
        final_prices = paths[:, -1]
        payoffs = np.maximum(final_prices - self.K, 0)
        price = np.exp(-self.r * self.T) * np.mean(payoffs)
        std_error = np.std(payoffs) / np.sqrt(self.num_simulations)
        
        return {
            'price': price,
            'std_error': std_error,
            'confidence_95': (price - 1.96 * std_error, price + 1.96 * std_error)
        }
    
    def european_put(self):
        """Price European put option"""
        paths = self.generate_paths()
        final_prices = paths[:, -1]
        payoffs = np.maximum(self.K - final_prices, 0)
        price = np.exp(-self.r * self.T) * np.mean(payoffs)
        std_error = np.std(payoffs) / np.sqrt(self.num_simulations)
        
        return {
            'price': price,
            'std_error': std_error,
            'confidence_95': (price - 1.96 * std_error, price + 1.96 * std_error)
        }
    
    def asian_call(self):
        """Price Asian call (average price)"""
        paths = self.generate_paths()
        average_prices = np.mean(paths, axis=1)
        payoffs = np.maximum(average_prices - self.K, 0)
        price = np.exp(-self.r * self.T) * np.mean(payoffs)
        std_error = np.std(payoffs) / np.sqrt(self.num_simulations)
        
        return {
            'price': price,
            'std_error': std_error,
            'confidence_95': (price - 1.96 * std_error, price + 1.96 * std_error)
        }
    
    def barrier_call(self, barrier_level, barrier_type='knock_out'):
        """
        Price barrier option.
        
        barrier_type: 'knock_out' or 'knock_in'
        """
        paths = self.generate_paths()
        final_prices = paths[:, -1]
        
        if barrier_type == 'knock_out':
            # Knock out if price ever touches barrier
            knocked_out = np.any(paths >= barrier_level, axis=1)
            payoffs = np.where(knocked_out, 0, np.maximum(final_prices - self.K, 0))
        elif barrier_type == 'knock_in':
            # Only pays if price touches barrier
            knocked_in = np.any(paths >= barrier_level, axis=1)
            payoffs = np.where(knocked_in, np.maximum(final_prices - self.K, 0), 0)
        
        price = np.exp(-self.r * self.T) * np.mean(payoffs)
        std_error = np.std(payoffs) / np.sqrt(self.num_simulations)
        
        return {
            'price': price,
            'std_error': std_error,
            'confidence_95': (price - 1.96 * std_error, price + 1.96 * std_error)
        }
    
    def lookback_call(self):
        """Price lookback call (max price observed)"""
        paths = self.generate_paths()
        max_prices = np.max(paths, axis=1)
        payoffs = np.maximum(max_prices - self.K, 0)
        price = np.exp(-self.r * self.T) * np.mean(payoffs)
        std_error = np.std(payoffs) / np.sqrt(self.num_simulations)
        
        return {
            'price': price,
            'std_error': std_error,
            'confidence_95': (price - 1.96 * std_error, price + 1.96 * std_error)
        }
