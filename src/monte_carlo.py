import numpy as np
from black_scholes import BlackScholesModel


class MonteCarloSimulation:
    """
    Monte Carlo for option pricing.
    
    Simulates many random stock price paths and calculates
    average payoff. Works for any option type.
    """
    
    def __init__(self, S, K, T, r, sigma, num_simulations=10000, num_steps=252):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.num_simulations = num_simulations
        self.num_steps = num_steps
        self.dt = T / num_steps
        
        # Pre-calculate drift and volatility components for efficiency
        self.drift = (r - 0.5 * sigma ** 2) * self.dt
        self.vol_shock = sigma * np.sqrt(self.dt)
    
    def generate_paths(self, random_seed=None):
        """
        Generate random stock price paths using GBM.
        
        Each path is one possible future scenario.
        With 1000+ paths, we get a good distribution of outcomes.
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Initialize all paths starting at current price
        paths = np.zeros((self.num_simulations, self.num_steps + 1))
        paths[:, 0] = self.S
        
        # Generate random normal shocks
        shocks = np.random.standard_normal((self.num_simulations, self.num_steps))
        
        # Simulate each step forward in time
        for t in range(self.num_steps):
            paths[:, t + 1] = paths[:, t] * np.exp(
                self.drift + self.vol_shock * shocks[:, t]
            )
        
        return paths
    
    def european_call(self):
        """Price a European call - simple payoff at expiration"""
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
        """Price a European put"""
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
        """Asian call - payoff based on average price, not final price"""
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
        Barrier option - has a knock-in or knock-out level.
        
        knock_out: if price ever touches barrier, option becomes worthless
        knock_in: option only pays off if price touches barrier
        """
        paths = self.generate_paths()
        final_prices = paths[:, -1]
        
        if barrier_type == 'knock_out':
            # Did the price ever touch the barrier?
            knocked_out = np.any(paths >= barrier_level, axis=1)
            payoffs = np.where(knocked_out, 0, np.maximum(final_prices - self.K, 0))
        elif barrier_type == 'knock_in':
            # Did the price ever touch the barrier?
            knocked_in = np.any(paths >= barrier_level, axis=1)
            payoffs = np.where(knocked_in, np.maximum(final_prices - self.K, 0), 0)
        else:
            raise ValueError("barrier_type must be 'knock_out' or 'knock_in'")
        
        price = np.exp(-self.r * self.T) * np.mean(payoffs)
        std_error = np.std(payoffs) / np.sqrt(self.num_simulations)
        
        return {
            'price': price,
            'std_error': std_error,
            'confidence_95': (price - 1.96 * std_error, price + 1.96 * std_error)
        }
    
    def lookback_call(self):
        """Lookback call - payoff based on the highest price reached"""
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