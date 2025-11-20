#!/usr/bin/env python3
"""
Local Agricultural Market Price Tracker
Main application entry point
"""

import sys
from datetime import date
from src.database import Database
from src.price_manager import PriceManager
from src.ui import UI
from src.utils import validate_price, validate_name, get_date_today


class MarketPriceTracker:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.db = None
        self.price_manager = None
        self.running = True
    
    def initialize(self):
        """Initialize database and components"""
        try:
            UI.print_info("Connecting to database...")
            self.db = Database()
            
            if not self.db.connect():
                UI.print_error("Failed to connect to database. Please check your configuration.")
                return False
            
            UI.print_success("Database connected successfully!")
            
            # Initialize database tables
            UI.print_info("Initializing database tables...")
            if not self.db.initialize_database():
                UI.print_error("Failed to initialize database tables.")
                return False
            
            # Check if we need to insert sample data
            self.price_manager = PriceManager(self.db)
            products = self.price_manager.get_all_products()
            
            if len(products) == 0:
                UI.print_info("No data found. Inserting sample data...")
                self.db.insert_sample_data()
                UI.print_success("Sample data inserted successfully!")
            
            return True
            
        except FileNotFoundError as e:
            UI.print_error(str(e))
            return False
        except Exception as e:
            UI.print_error(f"Initialization error: {e}")
            return False
    
    def run(self):
        """Main application loop"""
        # Show welcome screen
        UI.show_welcome()
        
        # Initialize application
        if not self.initialize():
            UI.print_error("\nApplication failed to initialize. Exiting...")
            return
        
        # Main loop
        while self.running:
            try:
                choice = UI.show_main_menu()
                
                if choice == '1':
                    self.view_current_prices()
                elif choice == '2':
                    self.enter_new_price()
                elif choice == '3':
                    self.compare_prices()
                elif choice == '4':
                    self.view_price_trends()
                elif choice == '5':
                    self.manage_data()
                elif choice == '6':
                    self.exit_application()
                else:
                    UI.print_error("Invalid choice. Please select 1-6.")
                    UI.pause()
                    
            except KeyboardInterrupt:
                print("\n")
                if UI.confirm("Do you want to exit?"):
                    self.exit_application()
            except Exception as e:
                UI.print_error(f"An error occurred: {e}")
                UI.pause()
    
    def view_current_prices(self):
        """Display current market prices"""
        UI.clear_screen()
        UI.print_header("VIEW CURRENT MARKET PRICES")
        
        print("Filter by:")
        print("  1. All products")
        print("  2. Specific product")
        print("  3. Specific market")
        print("  4. Product category")
        
        choice = UI.get_input("\nEnter choice (1-4): ")
        
        if choice == '1':
            prices = self.price_manager.get_current_prices()
            UI.print_subheader("All Current Prices")
            UI.display_prices(prices)
        
        elif choice == '2':
            products = self.price_manager.get_all_products()
            UI.print_subheader("Select Product")
            UI.display_products(products)
            
            try:
                product_num = UI.get_input("\nEnter product number: ", int)
                if 1 <= product_num <= len(products):
                    product = products[product_num - 1]
                    prices = self.price_manager.get_current_prices(product_id=product.product_id)
                    UI.print_subheader(f"Current Prices for: {product.product_name}")
                    UI.display_prices(prices)
                else:
                    UI.print_error("Invalid product number.")
            except ValueError:
                UI.print_error("Invalid input.")
        
        elif choice == '3':
            markets = self.price_manager.get_all_markets()
            UI.print_subheader("Select Market")
            UI.display_markets(markets)
            
            try:
                market_num = UI.get_input("\nEnter market number: ", int)
                if 1 <= market_num <= len(markets):
                    market = markets[market_num - 1]
                    prices = self.price_manager.get_current_prices(market_id=market.market_id)
                    UI.print_subheader(f"Current Prices at: {market.market_name}")
                    UI.display_prices(prices)
                else:
                    UI.print_error("Invalid market number.")
            except ValueError:
                UI.print_error("Invalid input.")
        
        elif choice == '4':
            categories = self.price_manager.get_all_categories()
            UI.print_subheader("Product Categories")
            for i, cat in enumerate(categories, 1):
                print(f"  {i}. {cat}")
            
            try:
                cat_num = UI.get_input("\nEnter category number: ", int)
                if 1 <= cat_num <= len(categories):
                    category = categories[cat_num - 1]
                    products = self.price_manager.get_products_by_category(category)
                    
                    all_prices = []
                    for product in products:
                        prices = self.price_manager.get_current_prices(product_id=product.product_id)
                        all_prices.extend(prices)
                    
                    UI.print_subheader(f"Current Prices - Category: {category}")
                    UI.display_prices(all_prices)
                else:
                    UI.print_error("Invalid category number.")
            except ValueError:
                UI.print_error("Invalid input.")
        
        UI.pause()
    
    def enter_new_price(self):
        """Enter new price data"""
        UI.clear_screen()
        UI.print_header("ENTER NEW PRICE DATA")
        
        # Select product
        products = self.price_manager.get_all_products()
        UI.print_subheader("Select Product")
        UI.display_products(products)
        
        try:
            product_num = UI.get_input("\nEnter product number: ", int)
            if not (1 <= product_num <= len(products)):
                UI.print_error("Invalid product number.")
                UI.pause()
                return
            
            product = products[product_num - 1]
            
            # Select market
            markets = self.price_manager.get_all_markets()
            UI.print_subheader("Select Market")
            UI.display_markets(markets)
            
            market_num = UI.get_input("\nEnter market number: ", int)
            if not (1 <= market_num <= len(markets)):
                UI.print_error("Invalid market number.")
                UI.pause()
                return
            
            market = markets[market_num - 1]
            
            # Enter price
            price_str = UI.get_input(f"\nEnter price per {product.unit}: ")
            valid, result = validate_price(price_str)
            
            if not valid:
                UI.print_error(result)
                UI.pause()
                return
            
            price = result
            
            # Enter date (optional)
            use_today = UI.confirm("Use today's date?")
            date_str = get_date_today() if use_today else UI.get_input("Enter date (YYYY-MM-DD): ")
            
            # Enter recorder name
            recorded_by = UI.get_input("Enter your name (optional): ", allow_empty=True) or "User"
            
            # Confirm and save
            print(f"\n{UI.COLORS['BOLD']}Confirm Entry:{UI.COLORS['END']}")
            print(f"Product: {product.product_name}")
            print(f"Market: {market.market_name}")
            print(f"Price: {price} per {product.unit}")
            print(f"Date: {date_str}")
            print(f"Recorded by: {recorded_by}")
            
            if UI.confirm("\nSave this price data?"):
                if self.price_manager.add_price(product.product_id, market.market_id, 
                                                price, date_str, recorded_by):
                    UI.print_success("Price data saved successfully!")
                else:
                    UI.print_error("Failed to save price data.")
            else:
                UI.print_warning("Price data not saved.")
                
        except ValueError:
            UI.print_error("Invalid input.")
        except Exception as e:
            UI.print_error(f"Error: {e}")
        
        UI.pause()
    
    def compare_prices(self):
        """Compare prices across markets"""
        UI.clear_screen()
        UI.print_header("COMPARE PRICES ACROSS MARKETS")
        
        # Select product
        products = self.price_manager.get_all_products()
        UI.print_subheader("Select Product to Compare")
        UI.display_products(products)
        
        try:
            product_num = UI.get_input("\nEnter product number: ", int)
            if not (1 <= product_num <= len(products)):
                UI.print_error("Invalid product number.")
                UI.pause()
                return
            
            product = products[product_num - 1]
            prices = self.price_manager.compare_prices(product.product_id)
            
            if prices:
                UI.display_price_comparison(prices, product.product_name)
            else:
                UI.print_warning(f"No price data found for {product.product_name}")
                
        except ValueError:
            UI.print_error("Invalid input.")
        except Exception as e:
            UI.print_error(f"Error: {e}")
        
        UI.pause()
    
    def view_price_trends(self):
        """View price trends over time"""
        UI.clear_screen()
        UI.print_header("VIEW PRICE TRENDS")
        
        # Select product
        products = self.price_manager.get_all_products()
        UI.print_subheader("Select Product")
        UI.display_products(products)
        
        try:
            product_num = UI.get_input("\nEnter product number: ", int)
            if not (1 <= product_num <= len(products)):
                UI.print_error("Invalid product number.")
                UI.pause()
                return
            
            product = products[product_num - 1]
            
            # Select market
            markets = self.price_manager.get_all_markets()
            UI.print_subheader("Select Market")
            UI.display_markets(markets)
            
            market_num = UI.get_input("\nEnter market number: ", int)
            if not (1 <= market_num <= len(markets)):
                UI.print_error("Invalid market number.")
                UI.pause()
                return
            
            market = markets[market_num - 1]
            
            # Get price history and trend
            prices = self.price_manager.get_price_trend(product.product_id, market.market_id)
            trend_info = self.price_manager.analyze_trend(product.product_id, market.market_id)
            
            if prices:
                UI.display_trend(prices, trend_info)
            else:
                UI.print_warning("No price history found for this product and market.")
                
        except ValueError:
            UI.print_error("Invalid input.")
        except Exception as e:
            UI.print_error(f"Error: {e}")
        
        UI.pause()
    
    def manage_data(self):
        """Manage products and markets"""
        UI.clear_screen()
        UI.print_header("MANAGE PRODUCTS AND MARKETS")
        
        print("Options:")
        print("  1. Add new product")
        print("  2. Add new market")
        print("  3. View all products")
        print("  4. View all markets")
        print("  5. Back to main menu")
        
        choice = UI.get_input("\nEnter choice (1-5): ")
        
        if choice == '1':
            self.add_product()
        elif choice == '2':
            self.add_market()
        elif choice == '3':
            products = self.price_manager.get_all_products()
            UI.print_subheader("All Products")
            UI.display_products(products, show_numbers=False)
            UI.pause()
        elif choice == '4':
            markets = self.price_manager.get_all_markets()
            UI.print_subheader("All Markets")
            UI.display_markets(markets, show_numbers=False)
            UI.pause()
        elif choice == '5':
            return
        else:
            UI.print_error("Invalid choice.")
            UI.pause()
    
    def add_product(self):
        """Add a new product"""
        UI.print_subheader("Add New Product")
        
        product_name = UI.get_input("Enter product name: ")
        valid, validated_name = validate_name(product_name)
        
        if not valid:
            UI.print_error(validated_name)
            UI.pause()
            return
        
        categories = self.price_manager.get_all_categories()
        print("\nExisting categories:")
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        print(f"  {len(categories) + 1}. Create new category")
        
        cat_choice = UI.get_input("\nSelect category: ", int)
        
        if 1 <= cat_choice <= len(categories):
            category = categories[cat_choice - 1]
        elif cat_choice == len(categories) + 1:
            category = UI.get_input("Enter new category name: ")
        else:
            UI.print_error("Invalid choice.")
            UI.pause()
            return
        
        unit = UI.get_input("Enter unit (e.g., kg, each, liter): ")
        
        if self.price_manager.add_product(validated_name, category, unit):
            UI.print_success(f"Product '{validated_name}' added successfully!")
        else:
            UI.print_error("Failed to add product. It may already exist.")
        
        UI.pause()
    
    def add_market(self):
        """Add a new market"""
        UI.print_subheader("Add New Market")
        
        market_name = UI.get_input("Enter market name: ")
        valid, validated_name = validate_name(market_name)
        
        if not valid:
            UI.print_error(validated_name)
            UI.pause()
            return
        
        location = UI.get_input("Enter market location: ")
        
        if self.price_manager.add_market(validated_name, location):
            UI.print_success(f"Market '{validated_name}' added successfully!")
        else:
            UI.print_error("Failed to add market. It may already exist.")
        
        UI.pause()
    
    def exit_application(self):
        """Exit the application"""
        UI.clear_screen()
        UI.print_header("THANK YOU!")
        
        print(f"{UI.COLORS['BOLD']}Thank you for using the Local Market Price Tracker!{UI.COLORS['END']}")
        print("\nThis application helps promote fair pricing and informed")
        print("decision-making in agricultural markets.\n")
        print("Stay informed. Farm better. Prosper together.\n")
        
        if self.db:
            self.db.disconnect()
            UI.print_info("Database connection closed.")
        
        self.running = False


def main():
    """Main entry point"""
    try:
        app = MarketPriceTracker()
        app.run()
    except Exception as e:
        print(f"\n{UI.COLORS['RED']}Fatal error: {e}{UI.COLORS['END']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
