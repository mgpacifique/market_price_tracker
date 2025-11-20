"""
User Interface module
Handles all user interactions and display formatting
"""

import os
from datetime import date
from tabulate import tabulate


class UI:
    """Manages user interface and interactions"""
    
    # ANSI Color codes for terminal
    COLORS = {
        'HEADER': '\033[95m',
        'BLUE': '\033[94m',
        'CYAN': '\033[96m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'RED': '\033[91m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'END': '\033[0m'
    }
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    @staticmethod
    def print_header(text):
        """Print a formatted header"""
        print("\n" + "="*70)
        print(f"{UI.COLORS['BOLD']}{UI.COLORS['CYAN']}{text.center(70)}{UI.COLORS['END']}")
        print("="*70 + "\n")
    
    @staticmethod
    def print_subheader(text):
        """Print a formatted subheader"""
        print(f"\n{UI.COLORS['BOLD']}{UI.COLORS['BLUE']}{text}{UI.COLORS['END']}")
        print("-" * len(text))
    
    @staticmethod
    def print_success(text):
        """Print success message"""
        print(f"{UI.COLORS['GREEN']}✓ {text}{UI.COLORS['END']}")
    
    @staticmethod
    def print_error(text):
        """Print error message"""
        print(f"{UI.COLORS['RED']}✗ {text}{UI.COLORS['END']}")
    
    @staticmethod
    def print_warning(text):
        """Print warning message"""
        print(f"{UI.COLORS['YELLOW']}! {text}{UI.COLORS['END']}")
    
    @staticmethod
    def print_info(text):
        """Print info message"""
        print(f"{UI.COLORS['CYAN']}ℹ {text}{UI.COLORS['END']}")
    
    @staticmethod
    def show_welcome():
        """Display welcome screen"""
        UI.clear_screen()
        UI.print_header("LOCAL AGRICULTURAL MARKET PRICE TRACKER")
        
        print(f"{UI.COLORS['BOLD']}Welcome to the Market Price Tracker!{UI.COLORS['END']}\n")
        print("This application helps farmers and market participants:")
        print("  • View current market prices for agricultural products")
        print("  • Compare prices across different markets")
        print("  • Track price trends over time")
        print("  • Make informed selling and buying decisions")
        print("\nPress Enter to continue...")
        input()
    
    @staticmethod
    def show_main_menu():
        """Display main menu and get user choice"""
        UI.clear_screen()
        UI.print_header("MAIN MENU")
        
        print(f"{UI.COLORS['BOLD']}Please select an option:{UI.COLORS['END']}\n")
        print("  1. View Current Market Prices")
        print("  2. Enter New Price Data")
        print("  3. Compare Prices Across Markets")
        print("  4. View Price Trends")
        print("  5. Manage Products and Markets")
        print("  6. Exit Application")
        
        choice = input(f"\n{UI.COLORS['YELLOW']}Enter your choice (1-6): {UI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def display_products(products, show_numbers=True):
        """Display list of products in a formatted table"""
        if not products:
            UI.print_warning("No products found.")
            return
        
        table_data = []
        for i, product in enumerate(products, 1):
            row = [
                i if show_numbers else product.product_id,
                product.product_name,
                product.category,
                product.unit
            ]
            table_data.append(row)
        
        headers = ["#" if show_numbers else "ID", "Product Name", "Category", "Unit"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def display_markets(markets, show_numbers=True):
        """Display list of markets in a formatted table"""
        if not markets:
            UI.print_warning("No markets found.")
            return
        
        table_data = []
        for i, market in enumerate(markets, 1):
            row = [
                i if show_numbers else market.market_id,
                market.market_name,
                market.location
            ]
            table_data.append(row)
        
        headers = ["#" if show_numbers else "ID", "Market Name", "Location"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def display_prices(prices, show_trend=False):
        """Display price information in a formatted table"""
        if not prices:
            UI.print_warning("No price data found.")
            return
        
        table_data = []
        for price in prices:
            row = [
                price.product_name,
                f"{float(price.price):.2f}",
                price.unit,
                price.market_name,
                str(price.date)
            ]
            table_data.append(row)
        
        headers = ["Product", "Price", "Unit", "Market", "Date"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def display_price_comparison(prices, product_name):
        """Display price comparison across markets"""
        if not prices:
            UI.print_warning(f"No price data found for {product_name}.")
            return
        
        UI.print_subheader(f"Price Comparison for: {product_name}")
        
        table_data = []
        prices_list = [float(p.price) for p in prices]
        min_price = min(prices_list)
        max_price = max(prices_list)
        
        for price in prices:
            price_val = float(price.price)
            marker = ""
            if price_val == min_price:
                marker = f"{UI.COLORS['GREEN']}[LOWEST]{UI.COLORS['END']}"
            elif price_val == max_price:
                marker = f"{UI.COLORS['RED']}[HIGHEST]{UI.COLORS['END']}"
            
            row = [
                price.market_name,
                f"{price_val:.2f}",
                price.unit,
                str(price.date),
                marker
            ]
            table_data.append(row)
        
        headers = ["Market", "Price", "Unit", "Date", ""]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        avg_price = sum(prices_list) / len(prices_list)
        print(f"\n{UI.COLORS['BOLD']}Average Price: {avg_price:.2f}{UI.COLORS['END']}")
        print(f"Price Range: {min_price:.2f} - {max_price:.2f}")
    
    @staticmethod
    def display_trend(prices, trend_info):
        """Display price trend information"""
        if not prices:
            UI.print_warning("Insufficient data for trend analysis.")
            return
        
        UI.print_subheader(f"Price History: {prices[0].product_name} at {prices[0].market_name}")
        
        table_data = []
        for price in prices:
            row = [
                str(price.date),
                f"{float(price.price):.2f}",
                price.unit
            ]
            table_data.append(row)
        
        headers = ["Date", "Price", "Unit"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Display trend analysis
        trend, change, change_percent = trend_info
        
        if trend != "insufficient_data":
            print(f"\n{UI.COLORS['BOLD']}Trend Analysis:{UI.COLORS['END']}")
            
            if trend == "increased":
                color = UI.COLORS['RED']
                arrow = "↑"
            elif trend == "decreased":
                color = UI.COLORS['GREEN']
                arrow = "↓"
            else:
                color = UI.COLORS['YELLOW']
                arrow = "→"
            
            print(f"Status: {color}{arrow} Price has {trend}{UI.COLORS['END']}")
            print(f"Change: {change:+.2f} ({change_percent:+.2f}%)")
    
    @staticmethod
    def get_input(prompt, input_type=str, allow_empty=False):
        """Get validated input from user"""
        while True:
            try:
                value = input(f"{UI.COLORS['YELLOW']}{prompt}{UI.COLORS['END']}")
                
                if not value and not allow_empty:
                    UI.print_error("Input cannot be empty. Please try again.")
                    continue
                
                if not value and allow_empty:
                    return None
                
                if input_type == int:
                    return int(value)
                elif input_type == float:
                    return float(value)
                else:
                    return value
            except ValueError:
                UI.print_error(f"Invalid input. Please enter a valid {input_type.__name__}.")
            except KeyboardInterrupt:
                print("\n")
                UI.print_warning("Input cancelled")
                raise  # Re-raise to be handled by caller
    
    @staticmethod
    def confirm(prompt):
        """Ask for yes/no confirmation"""
        try:
            response = input(f"{UI.COLORS['YELLOW']}{prompt} (y/n): {UI.COLORS['END']}").lower()
            return response in ['y', 'yes']
        except KeyboardInterrupt:
            print("\n")
            UI.print_warning("Confirmation cancelled")
            return False  # Default to "no" on interrupt
    
    @staticmethod
    def pause():
        """Pause and wait for user to press Enter"""
        try:
            input(f"\n{UI.COLORS['CYAN']}Press Enter to continue...{UI.COLORS['END']}")
        except KeyboardInterrupt:
            print("\n")
            pass  # Just continue on interrupt
