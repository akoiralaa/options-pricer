import numpy as np
import matplotlib.pyplot as plt
from black_scholes import BlackScholesModel


class OptionVisualizer:
    """Create visualizations for option Greeks and pricing."""
    
    def __init__(self, S, K, T, r):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
    
    def plot_price_vs_stock(self, sigma, option_type='call'):
        """Plot option price vs stock price"""
        stock_prices = np.linspace(self.K * 0.7, self.K * 1.3, 100)
        prices = []
        
        for s in stock_prices:
            bs = BlackScholesModel(s, self.K, self.T, self.r, sigma)
            if option_type == 'call':
                prices.append(bs.call_price())
            else:
                prices.append(bs.put_price())
        
        plt.figure(figsize=(10, 6))
        plt.plot(stock_prices, prices, 'b-', linewidth=2)
        plt.axvline(self.S, color='r', linestyle='--', label='Current Price')
        plt.axvline(self.K, color='g', linestyle='--', label='Strike')
        plt.xlabel('Stock Price ($)')
        plt.ylabel('Option Price ($)')
        plt.title(f'{option_type.upper()} Option Price vs Stock Price (σ={sigma*100}%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt
    
    def plot_greeks_vs_stock(self, sigma, option_type='call'):
        """Plot all Greeks vs stock price"""
        stock_prices = np.linspace(self.K * 0.7, self.K * 1.3, 100)
        deltas, gammas, vegas, thetas = [], [], [], []
        
        for s in stock_prices:
            bs = BlackScholesModel(s, self.K, self.T, self.r, sigma)
            deltas.append(bs.call_delta() if option_type == 'call' else bs.put_delta())
            gammas.append(bs.gamma())
            vegas.append(bs.call_vega())
            thetas.append(bs.call_theta() if option_type == 'call' else bs.put_theta())
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        axes[0, 0].plot(stock_prices, deltas, 'b-', linewidth=2)
        axes[0, 0].set_ylabel('Delta')
        axes[0, 0].set_title('Delta vs Stock Price')
        axes[0, 0].grid(True, alpha=0.3)
        
        axes[0, 1].plot(stock_prices, gammas, 'g-', linewidth=2)
        axes[0, 1].set_ylabel('Gamma')
        axes[0, 1].set_title('Gamma vs Stock Price')
        axes[0, 1].grid(True, alpha=0.3)
        
        axes[1, 0].plot(stock_prices, vegas, 'r-', linewidth=2)
        axes[1, 0].set_ylabel('Vega')
        axes[1, 0].set_xlabel('Stock Price ($)')
        axes[1, 0].set_title('Vega vs Stock Price')
        axes[1, 0].grid(True, alpha=0.3)
        
        axes[1, 1].plot(stock_prices, thetas, 'orange', linewidth=2)
        axes[1, 1].set_ylabel('Theta (daily)')
        axes[1, 1].set_xlabel('Stock Price ($)')
        axes[1, 1].set_title('Theta vs Stock Price')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return plt
    
    def plot_volatility_smile(self, sigma_range=None):
        """Plot implied volatility smile"""
        if sigma_range is None:
            sigma_range = np.linspace(0.1, 0.4, 50)
        
        strikes = np.linspace(self.K * 0.8, self.K * 1.2, 10)
        
        plt.figure(figsize=(10, 6))
        for strike in strikes:
            ivs = []
            for sigma in sigma_range:
                bs = BlackScholesModel(self.S, strike, self.T, self.r, sigma)
                ivs.append(sigma)
            plt.plot(strikes / self.K, ivs, 'o-', label=f'Strike=${strike:.0f}')
        
        plt.xlabel('Strike / Spot')
        plt.ylabel('Implied Volatility')
        plt.title('Volatility Smile')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt
