import sys
sys.path.insert(0, '.')

from black_scholes import BlackScholesModel, get_all_greeks
from implied_vol import ImpliedVolatility, calculate_iv
from monte_carlo import MonteCarloSimulation


class OptionsPricerInterface:
    """
    User-friendly interface for options pricing.
    Allows users to input custom parameters and compare pricing methods.
    """
    
    def __init__(self):
        self.S = None
        self.K = None
        self.T = None
        self.r = None
        self.sigma = None
        self.market_price = None
    
    def get_user_input(self):
        """Get option parameters from user"""
        print("\n" + "="*60)
        print("OPTIONS PRICER - INPUT YOUR PARAMETERS")
        print("="*60 + "\n")
        
        try:
            self.S = float(input("Stock Price (S) [e.g., 100]: "))
            self.K = float(input("Strike Price (K) [e.g., 100]: "))
            days = float(input("Days to Expiration [e.g., 30]: "))
            self.T = days / 365
            self.r = float(input("Risk-free Rate [e.g., 0.05 for 5%]: "))
            self.sigma = float(input("Volatility [e.g., 0.20 for 20%]: "))
            
            print("\n" + "-"*60)
            print("Parameters accepted. Ready to price.")
            print("-"*60)
            
        except ValueError:
            print("ERROR: Invalid input. Please enter numbers only.")
            return False
        
        return True
    
    def price_black_scholes(self):
        """Calculate Black-Scholes prices and Greeks"""
        print("\n" + "="*60)
        print("BLACK-SCHOLES PRICING")
        print("="*60)
        
        bs = BlackScholesModel(self.S, self.K, self.T, self.r, self.sigma)
        
        print(f"\nCALL OPTION:")
        print(f"  Price: ${bs.call_price():.4f}")
        print(f"  Delta: {bs.call_delta():.4f}")
        print(f"  Gamma: {bs.gamma():.6f}")
        print(f"  Vega: ${bs.call_vega():.4f} (per 1% vol change)")
        print(f"  Theta: ${bs.call_theta():.4f} (per day)")
        print(f"  Rho: ${bs.call_rho():.4f} (per 1% rate change)")
        
        print(f"\nPUT OPTION:")
        print(f"  Price: ${bs.put_price():.4f}")
        print(f"  Delta: {bs.put_delta():.4f}")
        print(f"  Gamma: {bs.gamma():.6f}")
        print(f"  Vega: ${bs.put_vega():.4f} (per 1% vol change)")
        print(f"  Theta: ${bs.put_theta():.4f} (per day)")
        print(f"  Rho: ${bs.put_rho():.4f} (per 1% rate change)")
        
        return {
            'call_price': bs.call_price(),
            'put_price': bs.put_price(),
            'call_delta': bs.call_delta(),
            'put_delta': bs.put_delta()
        }
    
    def price_monte_carlo(self, num_sims=50000):
        """Price using Monte Carlo"""
        print("\n" + "="*60)
        print(f"MONTE CARLO PRICING ({num_sims:,} simulations)")
        print("="*60)
        
        mc = MonteCarloSimulation(self.S, self.K, self.T, self.r, self.sigma, 
                                 num_simulations=num_sims)
        
        call = mc.european_call()
        put = mc.european_put()
        
        print(f"\nCALL OPTION:")
        print(f"  Price: ${call['price']:.4f}")
        print(f"  Std Error: ${call['std_error']:.4f}")
        print(f"  95% CI: (${call['confidence_95'][0]:.4f}, ${call['confidence_95'][1]:.4f})")
        
        print(f"\nPUT OPTION:")
        print(f"  Price: ${put['price']:.4f}")
        print(f"  Std Error: ${put['std_error']:.4f}")
        print(f"  95% CI: (${put['confidence_95'][0]:.4f}, ${put['confidence_95'][1]:.4f})")
        
        return {
            'call_price': call['price'],
            'put_price': put['price'],
            'call_std_error': call['std_error'],
            'put_std_error': put['std_error']
        }
    
    def calculate_implied_vol(self):
        """Calculate implied volatility from market price"""
        print("\n" + "="*60)
        print("IMPLIED VOLATILITY CALCULATOR")
        print("="*60)
        
        try:
            option_type = input("\nOption type (call/put): ").lower()
            market_price = float(input("Market price of option: $"))
            
            if option_type not in ['call', 'put']:
                print("ERROR: Option type must be 'call' or 'put'")
                return None
            
            iv = calculate_iv(self.S, self.K, self.T, self.r, market_price, option_type)
            
            print(f"\nIMPLIED VOLATILITY: {iv*100:.4f}%")
            print(f"Input Volatility: {self.sigma*100:.4f}%")
            print(f"Difference: {abs(iv - self.sigma)*100:.4f}%")
            
            return iv
            
        except ValueError:
            print("ERROR: Invalid input.")
            return None
    
    def price_exotic_options(self):
        """Price exotic options"""
        print("\n" + "="*60)
        print("EXOTIC OPTIONS (Monte Carlo)")
        print("="*60)
        
        mc = MonteCarloSimulation(self.S, self.K, self.T, self.r, self.sigma)
        
        print("\nAsian Call (average price):")
        asian = mc.asian_call()
        print(f"  Price: ${asian['price']:.4f} ± ${asian['std_error']:.4f}")
        
        print("\nBarrier Call (knock-out @ 110% of spot):")
        barrier = mc.barrier_call(barrier_level=self.S * 1.1, barrier_type='knock_out')
        print(f"  Price: ${barrier['price']:.4f} ± ${barrier['std_error']:.4f}")
        
        print("\nLookback Call (max price observed):")
        lookback = mc.lookback_call()
        print(f"  Price: ${lookback['price']:.4f} ± ${lookback['std_error']:.4f}")
    
    def compare_methods(self):
        """Compare Black-Scholes vs Monte Carlo"""
        print("\n" + "="*60)
        print("COMPARISON: BLACK-SCHOLES vs MONTE CARLO")
        print("="*60)
        
        bs_results = self.price_black_scholes()
        mc_results = self.price_monte_carlo(num_sims=100000)
        
        print("\n" + "-"*60)
        print("SUMMARY")
        print("-"*60)
        
        call_diff = abs(bs_results['call_price'] - mc_results['call_price'])
        call_diff_pct = (call_diff / bs_results['call_price']) * 100
        
        put_diff = abs(bs_results['put_price'] - mc_results['put_price'])
        put_diff_pct = (put_diff / bs_results['put_price']) * 100
        
        print(f"\nCALL OPTION:")
        print(f"  Black-Scholes: ${bs_results['call_price']:.4f}")
        print(f"  Monte Carlo:   ${mc_results['call_price']:.4f}")
        print(f"  Difference:    ${call_diff:.4f} ({call_diff_pct:.2f}%)")
        print(f"  Within 95% CI: {'✓' if call_diff < mc_results['call_std_error'] * 1.96 else '✗'}")
        
        print(f"\nPUT OPTION:")
        print(f"  Black-Scholes: ${bs_results['put_price']:.4f}")
        print(f"  Monte Carlo:   ${mc_results['put_price']:.4f}")
        print(f"  Difference:    ${put_diff:.4f} ({put_diff_pct:.2f}%)")
        print(f"  Within 95% CI: {'✓' if put_diff < mc_results['put_std_error'] * 1.96 else '✗'}")
    
    def visualize_data(self):
        """Show all visualizations"""
        from interactive_visualizer import InteractiveVisualizer
        
        print("\nGenerating visualizations... This may take a moment.")
        visualizer = InteractiveVisualizer(self.S, self.K, self.T, self.r, self.sigma)
        visualizer.show_all_visualizations()
    
    def interactive_menu(self):
        """Main interactive menu"""
        while True:
            print("\n" + "="*60)
            print("OPTIONS PRICER - MAIN MENU")
            print("="*60)
            print("1. Price with Black-Scholes")
            print("2. Price with Monte Carlo")
            print("3. Calculate Implied Volatility")
            print("4. Price Exotic Options")
            print("5. Compare Black-Scholes vs Monte Carlo")
            print("6. 📊 VISUALIZE DATA (Graphs & Charts)")
            print("7. Input new parameters")
            print("8. Exit")
            print("="*60)
            
            choice = input("\nSelect option (1-8): ")
            
            if choice == '1':
                self.price_black_scholes()
            elif choice == '2':
                self.price_monte_carlo()
            elif choice == '3':
                self.calculate_implied_vol()
            elif choice == '4':
                self.price_exotic_options()
            elif choice == '5':
                self.compare_methods()
            elif choice == '6':
                self.visualize_data()
            elif choice == '7':
                if self.get_user_input():
                    continue
                else:
                    continue
            elif choice == '8':
                print("\nExiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def run(self):
        """Run the interface"""
        print("\n" + "█"*60)
        print("█" + " "*58 + "█")
        print("█" + "  PROFESSIONAL OPTIONS PRICING CALCULATOR".center(58) + "█")
        print("█" + "  Black-Scholes | Monte Carlo | Implied Vol".center(58) + "█")
        print("█" + " "*58 + "█")
        print("█"*60)
        
        if self.get_user_input():
            self.interactive_menu()
        else:
            print("Exiting...")