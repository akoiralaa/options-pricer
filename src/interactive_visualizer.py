import numpy as np
import matplotlib.pyplot as plt
from black_scholes import BlackScholesModel
from monte_carlo import MonteCarloSimulation


class InteractiveVisualizer:
    """Create beginner-friendly visualizations"""
    
    def __init__(self, S, K, T, r, sigma):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
    
    def plot_option_payoff(self):
        """Show what profit/loss looks like at expiration"""
        stock_at_expiry = np.linspace(self.K * 0.5, self.K * 1.5, 100)
        
        call_payoff = np.maximum(stock_at_expiry - self.K, 0)
        put_payoff = np.maximum(self.K - stock_at_expiry, 0)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Call payoff
        ax1.fill_between(stock_at_expiry, 0, call_payoff, alpha=0.3, color='green', label='Profit')
        ax1.plot(stock_at_expiry, call_payoff, 'g-', linewidth=3, label='Call Payoff')
        ax1.axvline(self.K, color='red', linestyle='--', linewidth=2, label=f'Strike (${self.K})')
        ax1.axvline(self.S, color='blue', linestyle='--', linewidth=2, label=f'Current Price (${self.S})')
        ax1.set_xlabel('Stock Price at Expiration ($)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Profit/Loss ($)', fontsize=12, fontweight='bold')
        ax1.set_title('CALL OPTION - What happens at expiration?', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=10)
        ax1.set_ylim(bottom=-5)
        
        # Put payoff
        ax2.fill_between(stock_at_expiry, 0, put_payoff, alpha=0.3, color='red', label='Profit')
        ax2.plot(stock_at_expiry, put_payoff, 'r-', linewidth=3, label='Put Payoff')
        ax2.axvline(self.K, color='red', linestyle='--', linewidth=2, label=f'Strike (${self.K})')
        ax2.axvline(self.S, color='blue', linestyle='--', linewidth=2, label=f'Current Price (${self.S})')
        ax2.set_xlabel('Stock Price at Expiration ($)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Profit/Loss ($)', fontsize=12, fontweight='bold')
        ax2.set_title('PUT OPTION - What happens at expiration?', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10)
        ax2.set_ylim(bottom=-5)
        
        plt.tight_layout()
        return fig
    
    def plot_price_sensitivity(self):
        """Show how option price changes with stock price"""
        stock_prices = np.linspace(self.K * 0.7, self.K * 1.3, 100)
        call_prices = []
        put_prices = []
        
        for s in stock_prices:
            bs = BlackScholesModel(s, self.K, self.T, self.r, self.sigma)
            call_prices.append(bs.call_price())
            put_prices.append(bs.put_price())
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Call price sensitivity
        ax1.plot(stock_prices, call_prices, 'g-', linewidth=3, label='Call Price')
        ax1.axvline(self.S, color='blue', linestyle='--', linewidth=2, label=f'Current Price (${self.S})')
        ax1.axvline(self.K, color='red', linestyle='--', linewidth=2, label=f'Strike (${self.K})')
        ax1.scatter([self.S], [BlackScholesModel(self.S, self.K, self.T, self.r, self.sigma).call_price()], 
                   color='blue', s=200, zorder=5, label='You are here')
        ax1.set_xlabel('Stock Price ($)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Call Option Price ($)', fontsize=12, fontweight='bold')
        ax1.set_title('How Call Price Changes with Stock Price', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=10)
        ax1.fill_between(stock_prices, 0, call_prices, alpha=0.2, color='green')
        
        # Put price sensitivity
        ax2.plot(stock_prices, put_prices, 'r-', linewidth=3, label='Put Price')
        ax2.axvline(self.S, color='blue', linestyle='--', linewidth=2, label=f'Current Price (${self.S})')
        ax2.axvline(self.K, color='red', linestyle='--', linewidth=2, label=f'Strike (${self.K})')
        ax2.scatter([self.S], [BlackScholesModel(self.S, self.K, self.T, self.r, self.sigma).put_price()], 
                   color='blue', s=200, zorder=5, label='You are here')
        ax2.set_xlabel('Stock Price ($)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Put Option Price ($)', fontsize=12, fontweight='bold')
        ax2.set_title('How Put Price Changes with Stock Price', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10)
        ax2.fill_between(stock_prices, 0, put_prices, alpha=0.2, color='red')
        
        plt.tight_layout()
        return fig
    
    def plot_greeks_explanation(self):
        """Show Greeks with intuitive explanations"""
        stock_prices = np.linspace(self.K * 0.7, self.K * 1.3, 100)
        deltas = []
        gammas = []
        vegas = []
        thetas = []
        
        for s in stock_prices:
            bs = BlackScholesModel(s, self.K, self.T, self.r, self.sigma)
            deltas.append(bs.call_delta())
            gammas.append(bs.gamma())
            vegas.append(bs.call_vega())
            thetas.append(bs.call_theta())
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)
        
        # Delta
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(stock_prices, deltas, 'b-', linewidth=3)
        ax1.axvline(self.S, color='red', linestyle='--', linewidth=2)
        ax1.set_ylabel('Delta', fontsize=11, fontweight='bold')
        ax1.set_title('DELTA: Price move when stock moves $1', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Gamma
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(stock_prices, gammas, 'g-', linewidth=3)
        ax2.axvline(self.S, color='red', linestyle='--', linewidth=2)
        ax2.set_ylabel('Gamma', fontsize=11, fontweight='bold')
        ax2.set_title('GAMMA: How fast delta changes', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Vega
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.plot(stock_prices, vegas, 'purple', linewidth=3)
        ax3.axvline(self.S, color='red', linestyle='--', linewidth=2)
        ax3.set_ylabel('Vega', fontsize=11, fontweight='bold')
        ax3.set_xlabel('Stock Price', fontsize=11, fontweight='bold')
        ax3.set_title('VEGA: Price move if volatility up 1 percent', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Theta
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.plot(stock_prices, thetas, 'orange', linewidth=3)
        ax4.axvline(self.S, color='red', linestyle='--', linewidth=2)
        ax4.axhline(0, color='black', linestyle='-', linewidth=0.5)
        ax4.set_ylabel('Theta', fontsize=11, fontweight='bold')
        ax4.set_xlabel('Stock Price', fontsize=11, fontweight='bold')
        ax4.set_title('THETA: Daily time decay loss', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('THE GREEKS: Understanding Option Sensitivities', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def plot_monte_carlo_simulation(self):
        """Show Monte Carlo stock price paths"""
        mc = MonteCarloSimulation(self.S, self.K, self.T, self.r, self.sigma, 
                                num_simulations=1000, num_steps=252)
        paths = mc.generate_paths()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        
        # Plot 1: All paths
        ax = axes[0, 0]
        for i in range(min(500, len(paths))):
            ax.plot(paths[i], alpha=0.01, color='blue')
        ax.axhline(self.S, color='red', linestyle='--', linewidth=2, label='Current Price')
        ax.axhline(self.K, color='green', linestyle='--', linewidth=2, label='Strike')
        ax.set_ylabel('Stock Price ($)', fontsize=12, fontweight='bold')
        ax.set_title('Monte Carlo: 500 Simulated Price Paths', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 2: Final price distribution
        ax = axes[0, 1]
        final_prices = paths[:, -1]
        ax.hist(final_prices, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        ax.axvline(np.mean(final_prices), color='red', linestyle='--', linewidth=2, label=f'Mean: ${np.mean(final_prices):.2f}')
        ax.axvline(self.S, color='green', linestyle='--', linewidth=2, label=f'Current: ${self.S}')
        ax.set_xlabel('Stock Price at Expiration ($)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Final Stock Prices (1000 simulations)', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Call payoff distribution
        ax = axes[1, 0]
        call_payoffs = np.maximum(final_prices - self.K, 0)
        ax.hist(call_payoffs, bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
        ax.axvline(np.mean(call_payoffs), color='red', linestyle='--', linewidth=2, label=f'Expected: ${np.mean(call_payoffs):.2f}')
        ax.set_xlabel('Call Payoff at Expiration ($)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Call Option Payoffs', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Put payoff distribution
        ax = axes[1, 1]
        put_payoffs = np.maximum(self.K - final_prices, 0)
        ax.hist(put_payoffs, bins=50, color='lightcoral', edgecolor='black', alpha=0.7)
        ax.axvline(np.mean(put_payoffs), color='red', linestyle='--', linewidth=2, label=f'Expected: ${np.mean(put_payoffs):.2f}')
        ax.set_xlabel('Put Payoff at Expiration ($)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Put Option Payoffs', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def show_all_visualizations(self):
        """Display all visualizations"""
        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS...")
        print("="*60)
        
        fig1 = self.plot_option_payoff()
        fig1.savefig('option_payoff.png', dpi=150, bbox_inches='tight')
        print("Saved: option_payoff.png")
        
        fig2 = self.plot_price_sensitivity()
        fig2.savefig('price_sensitivity.png', dpi=150, bbox_inches='tight')
        print("Saved: price_sensitivity.png")
        
        fig3 = self.plot_greeks_explanation()
        fig3.savefig('greeks_explained.png', dpi=150, bbox_inches='tight')
        print("Saved: greeks_explained.png")
        
        fig4 = self.plot_monte_carlo_simulation()
        fig4.savefig('monte_carlo_simulation.png', dpi=150, bbox_inches='tight')
        print("Saved: monte_carlo_simulation.png")
        
        print("\n" + "="*60)
        print("All visualizations saved!")
        print("="*60)
        
        plt.show()
