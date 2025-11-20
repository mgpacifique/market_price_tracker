#!/usr/bin/env python3
"""
Local Agricultural Market Price Tracker - Enhanced Version
Main application with authentication and role-based access
"""

import sys
from datetime import date
from src.database import Database
from src.price_manager import PriceManager
from src.auth import AuthManager
from src.user_manager import UserManager
from src.order_manager import OrderManager
from src.analytics import Analytics
from src.export import ReportExporter
from src.ui_enhanced import AuthUI, SuperAdminUI, SellerUI, CustomerUI, AnalyticsUI
from src.permissions import Permissions, PermissionError
from src.utils import validate_price, validate_name, get_date_today


class EnhancedMarketPriceTracker:
    """Enhanced main application with authentication"""
    
    def __init__(self):
        """Initialize the application"""
        self.db = None
        self.auth = None
        self.price_manager = None
        self.user_manager = None
        self.order_manager = None
        self.analytics = None
        self.exporter = None
        self.running = True
    
    def initialize(self):
        """Initialize database and components"""
        try:
            AuthUI.print_info("Connecting to database...")
            self.db = Database()
            
            if not self.db.connect():
                AuthUI.print_error("Failed to connect to database.")
                return False
            
            AuthUI.print_success("Database connected successfully!")
            
            # Initialize managers
            self.auth = AuthManager(self.db)
            self.price_manager = PriceManager(self.db)
            self.user_manager = UserManager(self.db)
            self.order_manager = OrderManager(self.db)
            self.analytics = Analytics(self.db)
            self.exporter = ReportExporter(self.analytics)
            
            # Clean expired sessions
            self.auth.clean_expired_sessions()
            
            return True
            
        except FileNotFoundError as e:
            AuthUI.print_error(str(e))
            return False
        except Exception as e:
            AuthUI.print_error(f"Initialization error: {e}")
            return False
    
    def run(self):
        """Main application loop"""
        try:
            # Initialize application
            if not self.initialize():
                AuthUI.print_error("\nApplication failed to initialize. Exiting...")
                return
            
            # Authentication loop
            while self.running and not self.auth.is_authenticated():
                try:
                    choice = AuthUI.show_auth_menu()
                    
                    if choice == '1':
                        self.login()
                    elif choice == '2':
                        self.register('customer')
                    elif choice == '3':
                        self.register('seller')
                    elif choice == '4':
                        self.exit_application()
                        return
                    else:
                        AuthUI.print_error("Invalid choice.")
                        AuthUI.pause()
                
                except KeyboardInterrupt:
                    print("\n")
                    AuthUI.print_warning("\n⚠️  Interrupted by user")
                    if AuthUI.confirm("Exit application?"):
                        self.exit_application()
                        return
                    else:
                        continue
            
            # Main application loop (authenticated)
            while self.running and self.auth.is_authenticated():
                try:
                    user = self.auth.get_current_user()
                    
                    if user.role == 'super_admin':
                        self.super_admin_menu()
                    elif user.role == 'seller':
                        self.seller_menu()
                    elif user.role == 'customer':
                        self.customer_menu()
                        
                except KeyboardInterrupt:
                    print("\n")
                    AuthUI.print_warning("\n⚠️  Operation interrupted")
                    if AuthUI.confirm("Logout and exit?"):
                        self.logout()
                        self.exit_application()
                        return
                    else:
                        continue
                except PermissionError as e:
                    AuthUI.print_error(str(e))
                    AuthUI.pause()
                except Exception as e:
                    AuthUI.print_error(f"An error occurred: {e}")
                    AuthUI.pause()
        
        except KeyboardInterrupt:
            print("\n")
            AuthUI.print_warning("\n⚠️  Application interrupted by user")
            self.exit_application()
    
    def login(self):
        """Handle user login"""
        username, password = AuthUI.get_login_credentials()
        
        success, message = self.auth.login(username, password)
        
        if success:
            AuthUI.print_success(message)
            AuthUI.pause()
        else:
            AuthUI.print_error(message)
            AuthUI.pause()
    
    def register(self, role):
        """Handle user registration"""
        info = AuthUI.get_registration_info(role)
        
        if not info:
            AuthUI.pause()
            return
        
        success, message = self.auth.register_user(**info)
        
        if success:
            AuthUI.print_success(message)
        else:
            AuthUI.print_error(message)
        
        AuthUI.pause()
    
    def logout(self):
        """Handle user logout"""
        self.auth.logout()
        AuthUI.print_success("Logged out successfully!")
        AuthUI.pause()
    
    # ==================== SUPER ADMIN MENU ====================
    
    def super_admin_menu(self):
        """Super admin main menu"""
        user = self.auth.get_current_user()
        choice = SuperAdminUI.show_main_menu(user)
        
        if choice == '1':
            self.user_management_menu()
        elif choice == '2':
            self.admin_market_management()
        elif choice == '3':
            self.admin_product_management()
        elif choice == '4':
            self.admin_price_management()
        elif choice == '5':
            self.admin_order_management()
        elif choice == '6':
            self.analytics_menu()
        elif choice == '7':
            self.show_system_statistics()
        elif choice == '8':
            self.logout()
        else:
            AuthUI.print_error("Invalid choice.")
            AuthUI.pause()
    
    def user_management_menu(self):
        """User management submenu"""
        while True:
            choice = SuperAdminUI.show_user_management_menu()
            
            if choice == '1':
                users = self.user_manager.get_all_users()
                SuperAdminUI.display_users(users)
                AuthUI.pause()
            elif choice == '2':
                self.approve_sellers()
            elif choice == '3':
                self.search_users()
            elif choice == '4':
                self.suspend_user()
            elif choice == '5':
                self.activate_user()
            elif choice == '6':
                self.delete_user()
            elif choice == '7':
                stats = self.user_manager.get_user_statistics()
                SuperAdminUI.display_user_statistics(stats)
                AuthUI.pause()
            elif choice == '8':
                break
            else:
                AuthUI.print_error("Invalid choice.")
                AuthUI.pause()
    
    def approve_sellers(self):
        """Approve pending seller accounts"""
        pending = self.user_manager.get_pending_sellers()
        
        if not pending:
            AuthUI.print_info("No pending seller registrations.")
            AuthUI.pause()
            return
        
        SuperAdminUI.print_subheader("Pending Seller Approvals")
        SuperAdminUI.display_users(pending)
        
        user_id = AuthUI.get_input("\nEnter User ID to approve (0 to cancel): ", int)
        
        if user_id > 0:
            success, message = self.user_manager.approve_seller(user_id)
            if success:
                AuthUI.print_success(message)
            else:
                AuthUI.print_error(message)
        
        AuthUI.pause()
    
    def search_users(self):
        """Search for users"""
        search_term = AuthUI.get_input("Enter search term (name, username, or email): ")
        users = self.user_manager.search_users(search_term)
        
        if users:
            SuperAdminUI.display_users(users)
        else:
            AuthUI.print_warning("No users found.")
        
        AuthUI.pause()
    
    def suspend_user(self):
        """Suspend a user account"""
        user_id = AuthUI.get_input("Enter User ID to suspend: ", int)
        success, message = self.user_manager.suspend_user(user_id)
        
        if success:
            AuthUI.print_success(message)
        else:
            AuthUI.print_error(message)
        
        AuthUI.pause()
    
    def activate_user(self):
        """Activate a suspended user"""
        user_id = AuthUI.get_input("Enter User ID to activate: ", int)
        success, message = self.user_manager.activate_user(user_id)
        
        if success:
            AuthUI.print_success(message)
        else:
            AuthUI.print_error(message)
        
        AuthUI.pause()
    
    def delete_user(self):
        """Delete a user account"""
        user_id = AuthUI.get_input("Enter User ID to delete: ", int)
        
        if AuthUI.confirm("Are you sure you want to delete this user?"):
            success, message = self.user_manager.delete_user(user_id)
            
            if success:
                AuthUI.print_success(message)
            else:
                AuthUI.print_error(message)
        
        AuthUI.pause()
    
    def admin_market_management(self):
        """Admin market management"""
        markets = self.price_manager.get_all_markets()
        AuthUI.print_subheader("All Markets")
        AuthUI.display_markets(markets, show_numbers=False)
        AuthUI.pause()
    
    def admin_product_management(self):
        """Admin product management"""
        products = self.price_manager.get_all_products()
        AuthUI.print_subheader("All Products")
        AuthUI.display_products(products, show_numbers=False)
        AuthUI.pause()
    
    def admin_price_management(self):
        """Admin price management"""
        prices = self.price_manager.get_current_prices()
        AuthUI.print_subheader("All Current Prices")
        AuthUI.display_prices(prices)
        AuthUI.pause()
    
    def admin_order_management(self):
        """Admin order management - view all orders"""
        AuthUI.clear_screen()
        AuthUI.print_header("ALL ORDERS")
        
        # Get all orders (would need a method in order_manager)
        # For now, show message
        AuthUI.print_info("Order management coming soon...")
        AuthUI.pause()
    
    def show_system_statistics(self):
        """Show system-wide statistics"""
        AuthUI.clear_screen()
        AuthUI.print_header("SYSTEM STATISTICS")
        
        # User statistics
        user_stats = self.user_manager.get_user_statistics()
        SuperAdminUI.display_user_statistics(user_stats)
        
        # Market activity
        AuthUI.print_subheader("\nMarket Activity (Last 30 Days)")
        activity = self.analytics.get_market_activity(days=30)
        if activity:
            from tabulate import tabulate
            print(tabulate(activity, headers="keys", tablefmt="grid"))
        
        AuthUI.pause()
    
    # ==================== SELLER MENU ====================
    
    def seller_menu(self):
        """Seller main menu"""
        user = self.auth.get_current_user()
        choice = SellerUI.show_main_menu(user)
        
        if choice == '1':
            self.seller_market_menu()
        elif choice == '2':
            self.seller_products_menu()
        elif choice == '3':
            self.seller_update_prices()
        elif choice == '4':
            self.seller_orders_menu()
        elif choice == '5':
            self.analytics_menu()
        elif choice == '6':
            self.logout()
        else:
            AuthUI.print_error("Invalid choice.")
            AuthUI.pause()
    
    def seller_market_menu(self):
        """Seller market management"""
        user = self.auth.get_current_user()
        market = self.user_manager.get_seller_market(user.user_id)
        
        while True:
            choice = SellerUI.show_market_menu()
            
            if choice == '1':
                if market:
                    AuthUI.print_subheader("My Market")
                    print(f"Market Name: {market.market_name}")
                    print(f"Location: {market.location}")
                    print(f"Status: {market.status}")
                    if market.description:
                        print(f"Description: {market.description}")
                else:
                    AuthUI.print_warning("You don't have a market yet. Create one first!")
                AuthUI.pause()
            
            elif choice == '2':
                if market:
                    AuthUI.print_warning("You already have a market!")
                else:
                    info = SellerUI.get_market_info()
                    success = self.price_manager.add_market(info['market_name'], info['location'])
                    if success:
                        # Update market with user_id
                        query = "UPDATE markets SET user_id = %s, description = %s WHERE market_name = %s"
                        self.db.execute_query(query, (user.user_id, info.get('description'), info['market_name']))
                        AuthUI.print_success("Market created successfully!")
                        market = self.user_manager.get_seller_market(user.user_id)
                    else:
                        AuthUI.print_error("Failed to create market.")
                AuthUI.pause()
            
            elif choice == '3':
                AuthUI.print_info("Market update feature coming soon...")
                AuthUI.pause()
            
            elif choice == '4':
                if market:
                    report = self.analytics.generate_market_report(market.market_id, days=30)
                    if report:
                        AuthUI.print_subheader("Market Statistics")
                        print(f"Total Products: {report['product_count']}")
                        # Add more statistics
                else:
                    AuthUI.print_warning("Create a market first!")
                AuthUI.pause()
            
            elif choice == '5':
                break
            else:
                AuthUI.print_error("Invalid choice.")
                AuthUI.pause()
    
    def seller_products_menu(self):
        """Seller products management"""
        user = self.auth.get_current_user()
        market = self.user_manager.get_seller_market(user.user_id)
        
        if not market:
            AuthUI.print_warning("You need to create a market first!")
            AuthUI.pause()
            return
        
        while True:
            choice = SellerUI.show_products_menu()
            
            if choice == '1':
                # Show seller's products
                query = "SELECT * FROM products WHERE user_id = %s OR market_id = %s"
                results = self.db.execute_query(query, (user.user_id, market.market_id), fetch=True)
                if results:
                    from src.models import Product
                    products = [Product(**row) for row in results]
                    AuthUI.print_subheader("My Products")
                    AuthUI.display_products(products, show_numbers=False)
                else:
                    AuthUI.print_warning("No products found. Add some products!")
                AuthUI.pause()
            
            elif choice == '2':
                # Add new product
                product_name = AuthUI.get_input("Product name: ")
                category = AuthUI.get_input("Category: ")
                unit = AuthUI.get_input("Unit (kg, piece, liter, etc.): ")
                description = AuthUI.get_input("Description (optional): ", allow_empty=True)
                
                success = self.price_manager.add_product(product_name, category, unit)
                if success:
                    # Update product with user_id and market_id
                    query = "UPDATE products SET user_id = %s, market_id = %s, description = %s WHERE product_name = %s"
                    self.db.execute_query(query, (user.user_id, market.market_id, description, product_name))
                    AuthUI.print_success("Product added successfully!")
                else:
                    AuthUI.print_error("Failed to add product.")
                AuthUI.pause()
            
            elif choice == '3':
                AuthUI.print_info("Edit product feature coming soon...")
                AuthUI.pause()
            
            elif choice == '4':
                AuthUI.print_info("Delete product feature coming soon...")
                AuthUI.pause()
            
            elif choice == '5':
                break
            else:
                AuthUI.print_error("Invalid choice.")
                AuthUI.pause()
    
    def seller_update_prices(self):
        """Seller price updates"""
        user = self.auth.get_current_user()
        market = self.user_manager.get_seller_market(user.user_id)
        
        if not market:
            AuthUI.print_warning("You need to create a market first!")
            AuthUI.pause()
            return
        
        # Get seller's products
        query = "SELECT * FROM products WHERE user_id = %s OR market_id = %s"
        results = self.db.execute_query(query, (user.user_id, market.market_id), fetch=True)
        
        if not results:
            AuthUI.print_warning("You don't have any products. Add products first!")
            AuthUI.pause()
            return
        
        from src.models import Product
        products = [Product(**row) for row in results]
        
        AuthUI.clear_screen()
        AuthUI.print_header("UPDATE PRODUCT PRICES")
        AuthUI.display_products(products)
        
        product_num = AuthUI.get_input("\nSelect product number: ", int)
        if 1 <= product_num <= len(products):
            product = products[product_num - 1]
            price = AuthUI.get_input(f"Enter new price per {product.unit}: ", float)
            
            success = self.price_manager.add_price(
                product.product_id,
                market.market_id,
                price,
                get_date_today(),
                user.full_name
            )
            
            if success:
                AuthUI.print_success("Price updated successfully!")
            else:
                AuthUI.print_error("Failed to update price.")
        
        AuthUI.pause()
    
    def seller_orders_menu(self):
        """Seller order management"""
        user = self.auth.get_current_user()
        market = self.user_manager.get_seller_market(user.user_id)
        
        if not market:
            AuthUI.print_warning("You need to create a market first!")
            AuthUI.pause()
            return
        
        while True:
            choice = SellerUI.show_orders_menu()
            
            if choice == '1':
                orders = self.order_manager.get_market_orders(market.market_id)
                AuthUI.print_subheader("All Orders")
                AnalyticsUI.display_orders(orders)
                AuthUI.pause()
            
            elif choice == '2':
                orders = self.order_manager.get_market_orders(market.market_id, status='pending')
                AuthUI.print_subheader("Pending Orders")
                AnalyticsUI.display_orders(orders)
                AuthUI.pause()
            
            elif choice == '3':
                orders = self.order_manager.get_market_orders(market.market_id, status='confirmed')
                AuthUI.print_subheader("Confirmed Orders")
                AnalyticsUI.display_orders(orders)
                AuthUI.pause()
            
            elif choice == '4':
                order_id = AuthUI.get_input("Enter Order ID: ", int)
                print("\nAvailable statuses:")
                print("  1. pending")
                print("  2. confirmed")
                print("  3. processing")
                print("  4. ready")
                print("  5. completed")
                print("  6. cancelled")
                
                status_choice = AuthUI.get_input("Select status: ", int)
                statuses = ['pending', 'confirmed', 'processing', 'ready', 'completed', 'cancelled']
                
                if 1 <= status_choice <= 6:
                    success, msg = self.order_manager.update_order_status(order_id, statuses[status_choice - 1])
                    if success:
                        AuthUI.print_success(msg)
                    else:
                        AuthUI.print_error(msg)
                
                AuthUI.pause()
            
            elif choice == '5':
                stats = self.order_manager.get_order_statistics(market_id=market.market_id)
                if stats:
                    AuthUI.print_subheader("Order Statistics")
                    from tabulate import tabulate
                    stats_data = [[k, v] for k, v in stats.items()]
                    print(tabulate(stats_data, headers=["Metric", "Value"], tablefmt="grid"))
                AuthUI.pause()
            
            elif choice == '6':
                break
            else:
                AuthUI.print_error("Invalid choice.")
                AuthUI.pause()
    
    # ==================== CUSTOMER MENU ====================
    
    def customer_menu(self):
        """Customer main menu"""
        user = self.auth.get_current_user()
        choice = CustomerUI.show_main_menu(user)
        
        if choice == '1':
            self.browse_products()
        elif choice == '2':
            self.compare_prices_customer()
        elif choice == '3':
            self.place_order()
        elif choice == '4':
            self.customer_orders_menu()
        elif choice == '5':
            self.view_price_trends_customer()
        elif choice == '6':
            self.analytics_menu()
        elif choice == '7':
            self.logout()
        else:
            AuthUI.print_error("Invalid choice.")
            AuthUI.pause()
    
    def browse_products(self):
        """Browse all products and prices"""
        prices = self.price_manager.get_current_prices()
        AuthUI.clear_screen()
        AuthUI.print_header("BROWSE PRODUCTS & PRICES")
        AuthUI.display_prices(prices)
        AuthUI.pause()
    
    def compare_prices_customer(self):
        """Compare prices across markets"""
        products = self.price_manager.get_all_products()
        AuthUI.clear_screen()
        AuthUI.print_header("COMPARE PRICES")
        AuthUI.display_products(products)
        
        product_num = AuthUI.get_input("\nSelect product number: ", int)
        if 1 <= product_num <= len(products):
            product = products[product_num - 1]
            prices = self.price_manager.compare_prices(product.product_id)
            AuthUI.display_price_comparison(prices, product.product_name)
        
        AuthUI.pause()
    
    def place_order(self):
        """Place a new order"""
        user = self.auth.get_current_user()
        
        # Get available products and prices
        products = self.price_manager.get_all_products()
        prices = self.price_manager.get_current_prices()
        
        # Select items
        items = CustomerUI.select_order_items(products, prices)
        
        if not items:
            AuthUI.print_warning("Order cancelled.")
            AuthUI.pause()
            return
        
        # Check if all items from same market
        market_ids = set(item['market_id'] for item in items)
        if len(market_ids) > 1:
            AuthUI.print_error("All items must be from the same market!")
            AuthUI.pause()
            return
        
        market_id = list(market_ids)[0]
        
        # Get delivery info
        order_info = CustomerUI.get_order_info()
        
        # Create order
        success, order_id = self.order_manager.create_order(
            customer_id=user.user_id,
            market_id=market_id,
            items=items,
            delivery_address=order_info['delivery_address'],
            delivery_phone=order_info['delivery_phone'],
            notes=order_info.get('notes')
        )
        
        if success:
            AuthUI.print_success(f"Order placed successfully! Order ID: {order_id}")
        else:
            AuthUI.print_error("Failed to place order.")
        
        AuthUI.pause()
    
    def customer_orders_menu(self):
        """Customer orders menu"""
        user = self.auth.get_current_user()
        
        while True:
            choice = CustomerUI.show_orders_menu()
            
            if choice == '1':
                orders = self.order_manager.get_customer_orders(user.user_id)
                AuthUI.print_subheader("My Orders")
                AnalyticsUI.display_orders(orders)
                AuthUI.pause()
            
            elif choice == '2':
                order_id = AuthUI.get_input("Enter Order ID: ", int)
                order = self.order_manager.get_order_by_id(order_id)
                
                if order and order.customer_id == user.user_id:
                    items = self.order_manager.get_order_items(order_id)
                    AnalyticsUI.display_order_details(order, items)
                else:
                    AuthUI.print_error("Order not found or access denied.")
                
                AuthUI.pause()
            
            elif choice == '3':
                order_id = AuthUI.get_input("Enter Order ID to cancel: ", int)
                success, msg = self.order_manager.cancel_order(order_id, user.user_id, user.role)
                
                if success:
                    AuthUI.print_success(msg)
                else:
                    AuthUI.print_error(msg)
                
                AuthUI.pause()
            
            elif choice == '4':
                break
            else:
                AuthUI.print_error("Invalid choice.")
                AuthUI.pause()
    
    def view_price_trends_customer(self):
        """View price trends"""
        products = self.price_manager.get_all_products()
        markets = self.price_manager.get_all_markets()
        
        AuthUI.clear_screen()
        AuthUI.print_header("VIEW PRICE TRENDS")
        AuthUI.display_products(products)
        
        product_num = AuthUI.get_input("\nSelect product number: ", int)
        if 1 <= product_num <= len(products):
            product = products[product_num - 1]
            
            AuthUI.display_markets(markets)
            market_num = AuthUI.get_input("\nSelect market number: ", int)
            
            if 1 <= market_num <= len(markets):
                market = markets[market_num - 1]
                prices = self.price_manager.get_price_trend(product.product_id, market.market_id)
                trend_info = self.price_manager.analyze_trend(product.product_id, market.market_id)
                AuthUI.display_trend(prices, trend_info)
        
        AuthUI.pause()
    
    # ==================== ANALYTICS MENU (Common) ====================
    
    def analytics_menu(self):
        """Analytics and reporting menu"""
        while True:
            choice = AnalyticsUI.show_analytics_menu()
            
            if choice == '1':
                self.view_analytics_trends()
            elif choice == '2':
                self.view_market_comparison()
            elif choice == '3':
                self.view_product_statistics()
            elif choice == '4':
                self.view_market_activity()
            elif choice == '5':
                self.generate_pdf_report()
            elif choice == '6':
                self.export_excel()
            elif choice == '7':
                self.export_csv()
            elif choice == '8':
                break
            else:
                AuthUI.print_error("Invalid choice.")
                AuthUI.pause()
    
    def view_analytics_trends(self):
        """View price trends analytics"""
        products = self.price_manager.get_all_products()
        AuthUI.display_products(products)
        
        product_num = AuthUI.get_input("\nSelect product number: ", int)
        if 1 <= product_num <= len(products):
            product = products[product_num - 1]
            days = AuthUI.get_input("Number of days (default 30): ", int) or 30
            
            trend_data = self.analytics.get_price_trend_data(product.product_id, days=days)
            if trend_data:
                from tabulate import tabulate
                print(tabulate(trend_data, headers="keys", tablefmt="grid"))
            else:
                AuthUI.print_warning("No data available.")
        
        AuthUI.pause()
    
    def view_market_comparison(self):
        """View market comparison"""
        products = self.price_manager.get_all_products()
        AuthUI.display_products(products)
        
        product_num = AuthUI.get_input("\nSelect product number: ", int)
        if 1 <= product_num <= len(products):
            product = products[product_num - 1]
            comparison = self.analytics.get_market_price_comparison(product.product_id)
            
            if comparison:
                from tabulate import tabulate
                print(tabulate(comparison, headers="keys", tablefmt="grid"))
            else:
                AuthUI.print_warning("No data available.")
        
        AuthUI.pause()
    
    def view_product_statistics(self):
        """View product statistics"""
        products = self.price_manager.get_all_products()
        AuthUI.display_products(products)
        
        product_num = AuthUI.get_input("\nSelect product number: ", int)
        if 1 <= product_num <= len(products):
            product = products[product_num - 1]
            days = AuthUI.get_input("Number of days (default 30): ", int) or 30
            
            stats = self.analytics.get_product_price_statistics(product.product_id, days=days)
            if stats:
                from tabulate import tabulate
                stats_data = [[k, v] for k, v in stats.items()]
                print(tabulate(stats_data, headers=["Metric", "Value"], tablefmt="grid"))
            else:
                AuthUI.print_warning("No data available.")
        
        AuthUI.pause()
    
    def view_market_activity(self):
        """View market activity"""
        days = AuthUI.get_input("Number of days (default 30): ", int) or 30
        activity = self.analytics.get_market_activity(days=days)
        
        if activity:
            from tabulate import tabulate
            print(tabulate(activity, headers="keys", tablefmt="grid"))
        else:
            AuthUI.print_warning("No data available.")
        
        AuthUI.pause()
    
    def generate_pdf_report(self):
        """Generate PDF report"""
        products = self.price_manager.get_all_products()
        AuthUI.display_products(products)
        
        product_num = AuthUI.get_input("\nSelect product number: ", int)
        if 1 <= product_num <= len(products):
            product = products[product_num - 1]
            days = AuthUI.get_input("Number of days (default 30): ", int) or 30
            
            AuthUI.print_info("Generating PDF report...")
            filepath, message = self.exporter.generate_pdf_report(
                product.product_id,
                product.product_name,
                days=days
            )
            
            if filepath:
                AuthUI.print_success(f"Report saved to: {filepath}")
            else:
                AuthUI.print_error(message)
        
        AuthUI.pause()
    
    def export_excel(self):
        """Export data to Excel"""
        products = self.price_manager.get_all_products()
        AuthUI.display_products(products)
        
        product_num = AuthUI.get_input("\nSelect product number: ", int)
        if 1 <= product_num <= len(products):
            product = products[product_num - 1]
            days = AuthUI.get_input("Number of days (default 30): ", int) or 30
            
            trend_data = self.analytics.get_price_trend_data(product.product_id, days=days)
            
            if trend_data:
                filepath, message = self.exporter.export_to_excel(
                    trend_data,
                    f"{product.product_name.lower()}_prices"
                )
                
                if filepath:
                    AuthUI.print_success(f"Data exported to: {filepath}")
                else:
                    AuthUI.print_error(message)
            else:
                AuthUI.print_warning("No data available to export.")
        
        AuthUI.pause()
    
    def export_csv(self):
        """Export data to CSV"""
        products = self.price_manager.get_all_products()
        AuthUI.display_products(products)
        
        product_num = AuthUI.get_input("\nSelect product number: ", int)
        if 1 <= product_num <= len(products):
            product = products[product_num - 1]
            days = AuthUI.get_input("Number of days (default 30): ", int) or 30
            
            trend_data = self.analytics.get_price_trend_data(product.product_id, days=days)
            
            if trend_data:
                filepath, message = self.exporter.export_to_csv(
                    trend_data,
                    f"{product.product_name.lower()}_prices"
                )
                
                if filepath:
                    AuthUI.print_success(f"Data exported to: {filepath}")
                else:
                    AuthUI.print_error(message)
            else:
                AuthUI.print_warning("No data available to export.")
        
        AuthUI.pause()
    
    def exit_application(self):
        """Exit the application"""
        AuthUI.clear_screen()
        AuthUI.print_header("THANK YOU!")
        
        print(f"{AuthUI.COLORS['BOLD']}Thank you for using the Market Price Tracker!{AuthUI.COLORS['END']}\n")
        
        if self.db:
            self.db.disconnect()
            AuthUI.print_info("Database connection closed.")
        
        self.running = False


def main():
    """Main entry point"""
    try:
        app = EnhancedMarketPriceTracker()
        app.run()
    except KeyboardInterrupt:
        print("\n")
        AuthUI.print_warning("\n⚠️  Application terminated by user")
        print(f"\n{AuthUI.COLORS['BOLD']}Thank you for using Market Price Tracker!{AuthUI.COLORS['END']}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{AuthUI.COLORS['RED']}✗ Fatal error: {e}{AuthUI.COLORS['END']}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
