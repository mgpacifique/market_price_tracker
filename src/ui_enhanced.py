"""
Enhanced User Interface module with role-based menus
Handles all user interactions for different user roles
"""

import os
from datetime import date
from tabulate import tabulate
from src.ui import UI as BaseUI


class AuthUI(BaseUI):
    """Enhanced UI with authentication and role-based menus"""
    
    @staticmethod
    def show_auth_menu():
        """Display authentication menu"""
        BaseUI.clear_screen()
        BaseUI.print_header("WELCOME TO MARKET PRICE TRACKER")
        
        print(f"{BaseUI.COLORS['BOLD']}Please select an option:{BaseUI.COLORS['END']}\n")
        print("  1. Login")
        print("  2. Register as Customer")
        print("  3. Register as Seller")
        print("  4. Exit")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-4): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def get_login_credentials():
        """Get login credentials from user"""
        BaseUI.clear_screen()
        BaseUI.print_header("LOGIN")
        
        username = BaseUI.get_input("Username or Email: ")
        password = BaseUI.get_input("Password: ")
        
        return username, password
    
    @staticmethod
    def get_registration_info(role='customer'):
        """Get registration information from user"""
        BaseUI.clear_screen()
        role_title = "CUSTOMER" if role == 'customer' else "SELLER"
        BaseUI.print_header(f"{role_title} REGISTRATION")
        
        print(f"{BaseUI.COLORS['BOLD']}Please provide your information:{BaseUI.COLORS['END']}\n")
        
        username = BaseUI.get_input("Username: ")
        email = BaseUI.get_input("Email: ")
        password = BaseUI.get_input("Password: ")
        confirm_password = BaseUI.get_input("Confirm Password: ")
        
        if password != confirm_password:
            BaseUI.print_error("Passwords do not match!")
            return None
        
        full_name = BaseUI.get_input("Full Name: ")
        phone_number = BaseUI.get_input("Phone Number (optional): ", allow_empty=True)
        
        return {
            'username': username,
            'email': email,
            'password': password,
            'full_name': full_name,
            'phone_number': phone_number,
            'role': role
        }
    
    @staticmethod
    def show_user_info(user):
        """Display current user information"""
        print(f"\n{BaseUI.COLORS['CYAN']}Logged in as: {BaseUI.COLORS['BOLD']}{user.full_name}{BaseUI.COLORS['END']}")
        role_display = user.role.replace('_', ' ').title()
        print(f"Role: {BaseUI.COLORS['BOLD']}{role_display}{BaseUI.COLORS['END']}\n")


class SuperAdminUI(BaseUI):
    """UI for Super Admin users"""
    
    @staticmethod
    def show_main_menu(user):
        """Display super admin main menu"""
        BaseUI.clear_screen()
        BaseUI.print_header("SUPER ADMIN DASHBOARD")
        AuthUI.show_user_info(user)
        
        print(f"{BaseUI.COLORS['BOLD']}Main Menu:{BaseUI.COLORS['END']}\n")
        print("  1. User Management")
        print("  2. Market Management")
        print("  3. Product Management")
        print("  4. Price Management")
        print("  5. Order Management")
        print("  6. Analytics & Reports")
        print("  7. System Statistics")
        print("  8. Logout")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-8): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def show_user_management_menu():
        """Display user management submenu"""
        BaseUI.clear_screen()
        BaseUI.print_header("USER MANAGEMENT")
        
        print(f"{BaseUI.COLORS['BOLD']}Select an option:{BaseUI.COLORS['END']}\n")
        print("  1. View All Users")
        print("  2. Approve Pending Sellers")
        print("  3. Search Users")
        print("  4. Suspend User")
        print("  5. Activate User")
        print("  6. Delete User")
        print("  7. User Statistics")
        print("  8. Back to Main Menu")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-8): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def display_users(users):
        """Display list of users"""
        if not users:
            BaseUI.print_warning("No users found.")
            return
        
        table_data = []
        for user in users:
            status_color = BaseUI.COLORS['GREEN'] if user.status == 'active' else BaseUI.COLORS['YELLOW']
            row = [
                user.user_id,
                user.username,
                user.full_name,
                user.email,
                user.role.replace('_', ' ').title(),
                f"{status_color}{user.status}{BaseUI.COLORS['END']}"
            ]
            table_data.append(row)
        
        headers = ["ID", "Username", "Full Name", "Email", "Role", "Status"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def display_user_statistics(stats):
        """Display user statistics"""
        if not stats:
            BaseUI.print_warning("No statistics available.")
            return
        
        BaseUI.print_subheader("User Statistics")
        
        table_data = [
            ["Total Users", stats.get('total_users', 0)],
            ["Super Admins", stats.get('admins', 0)],
            ["Sellers", stats.get('sellers', 0)],
            ["Customers", stats.get('customers', 0)],
            ["Active Users", stats.get('active_users', 0)],
            ["Pending Approvals", stats.get('pending_users', 0)],
            ["Suspended Users", stats.get('suspended_users', 0)]
        ]
        
        print(tabulate(table_data, headers=["Metric", "Count"], tablefmt="grid"))


class SellerUI(BaseUI):
    """UI for Seller users"""
    
    @staticmethod
    def show_main_menu(user):
        """Display seller main menu"""
        BaseUI.clear_screen()
        BaseUI.print_header("SELLER DASHBOARD")
        AuthUI.show_user_info(user)
        
        print(f"{BaseUI.COLORS['BOLD']}Main Menu:{BaseUI.COLORS['END']}\n")
        print("  1. My Market")
        print("  2. My Products")
        print("  3. Update Prices")
        print("  4. Orders")
        print("  5. Analytics & Reports")
        print("  6. Logout")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-6): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def show_market_menu():
        """Display market management submenu"""
        BaseUI.clear_screen()
        BaseUI.print_header("MY MARKET")
        
        print(f"{BaseUI.COLORS['BOLD']}Select an option:{BaseUI.COLORS['END']}\n")
        print("  1. View Market Details")
        print("  2. Create Market (First Time)")
        print("  3. Update Market Information")
        print("  4. Market Statistics")
        print("  5. Back to Main Menu")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-5): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def show_products_menu():
        """Display products management submenu"""
        BaseUI.clear_screen()
        BaseUI.print_header("MY PRODUCTS")
        
        print(f"{BaseUI.COLORS['BOLD']}Select an option:{BaseUI.COLORS['END']}\n")
        print("  1. View My Products")
        print("  2. Add New Product")
        print("  3. Edit Product")
        print("  4. Delete Product")
        print("  5. Back to Main Menu")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-5): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def show_orders_menu():
        """Display orders management submenu"""
        BaseUI.clear_screen()
        BaseUI.print_header("ORDER MANAGEMENT")
        
        print(f"{BaseUI.COLORS['BOLD']}Select an option:{BaseUI.COLORS['END']}\n")
        print("  1. View All Orders")
        print("  2. View Pending Orders")
        print("  3. View Confirmed Orders")
        print("  4. Update Order Status")
        print("  5. Order Statistics")
        print("  6. Back to Main Menu")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-6): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def get_market_info():
        """Get market information from seller"""
        BaseUI.print_subheader("Create Your Market")
        
        market_name = BaseUI.get_input("Market Name: ")
        location = BaseUI.get_input("Location: ")
        description = BaseUI.get_input("Description (optional): ", allow_empty=True)
        
        return {
            'market_name': market_name,
            'location': location,
            'description': description
        }


class CustomerUI(BaseUI):
    """UI for Customer users"""
    
    @staticmethod
    def show_main_menu(user):
        """Display customer main menu"""
        BaseUI.clear_screen()
        BaseUI.print_header("CUSTOMER DASHBOARD")
        AuthUI.show_user_info(user)
        
        print(f"{BaseUI.COLORS['BOLD']}Main Menu:{BaseUI.COLORS['END']}\n")
        print("  1. Browse Products & Prices")
        print("  2. Compare Prices Across Markets")
        print("  3. Place Order")
        print("  4. My Orders")
        print("  5. View Price Trends")
        print("  6. Analytics & Reports")
        print("  7. Logout")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-7): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def show_orders_menu():
        """Display customer orders submenu"""
        BaseUI.clear_screen()
        BaseUI.print_header("MY ORDERS")
        
        print(f"{BaseUI.COLORS['BOLD']}Select an option:{BaseUI.COLORS['END']}\n")
        print("  1. View All My Orders")
        print("  2. View Order Details")
        print("  3. Cancel Order")
        print("  4. Back to Main Menu")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-4): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def get_order_info():
        """Get order information from customer"""
        BaseUI.print_subheader("Order Information")
        
        delivery_address = BaseUI.get_input("Delivery Address: ")
        delivery_phone = BaseUI.get_input("Delivery Phone: ")
        notes = BaseUI.get_input("Special Instructions (optional): ", allow_empty=True)
        
        return {
            'delivery_address': delivery_address,
            'delivery_phone': delivery_phone,
            'notes': notes
        }
    
    @staticmethod
    def select_order_items(products, prices):
        """Help customer select items for order"""
        items = []
        
        while True:
            BaseUI.clear_screen()
            BaseUI.print_header("SELECT ORDER ITEMS")
            
            # Display current cart
            if items:
                BaseUI.print_subheader("Current Cart:")
                cart_data = []
                total = 0
                for item in items:
                    subtotal = item['quantity'] * item['unit_price']
                    total += subtotal
                    cart_data.append([
                        item['product_name'],
                        f"{item['quantity']:.2f}",
                        f"{item['unit_price']:.2f}",
                        f"{subtotal:.2f}"
                    ])
                print(tabulate(cart_data, headers=["Product", "Quantity", "Price", "Subtotal"], tablefmt="grid"))
                print(f"\n{BaseUI.COLORS['BOLD']}Total: {total:.2f}{BaseUI.COLORS['END']}\n")
            
            print(f"{BaseUI.COLORS['BOLD']}Options:{BaseUI.COLORS['END']}")
            print("  1. Add item to cart")
            print("  2. Remove item from cart")
            print("  3. Finish and place order")
            print("  4. Cancel")
            
            choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice: {BaseUI.COLORS['END']}").strip()
            
            if choice == '1':
                # Show available products
                BaseUI.display_products(products)
                product_num = BaseUI.get_input("\nSelect product number: ", int)
                
                if 1 <= product_num <= len(products):
                    product = products[product_num - 1]
                    
                    # Find price for this product
                    product_prices = [p for p in prices if p.product_id == product.product_id]
                    if not product_prices:
                        BaseUI.print_error("No price available for this product")
                        BaseUI.pause()
                        continue
                    
                    # Show prices if multiple markets
                    if len(product_prices) > 1:
                        BaseUI.print_subheader(f"Prices for {product.product_name}:")
                        for i, p in enumerate(product_prices, 1):
                            print(f"  {i}. {p.market_name}: {float(p.price):.2f}")
                        price_num = BaseUI.get_input("\nSelect market: ", int)
                        if 1 <= price_num <= len(product_prices):
                            selected_price = product_prices[price_num - 1]
                        else:
                            continue
                    else:
                        selected_price = product_prices[0]
                    
                    quantity = BaseUI.get_input(f"Quantity ({product.unit}): ", float)
                    
                    items.append({
                        'product_id': product.product_id,
                        'product_name': product.product_name,
                        'quantity': quantity,
                        'unit_price': float(selected_price.price),
                        'market_id': selected_price.market_id
                    })
                    
                    BaseUI.print_success("Item added to cart!")
                    BaseUI.pause()
            
            elif choice == '2':
                if items:
                    item_num = BaseUI.get_input("Enter item number to remove: ", int)
                    if 1 <= item_num <= len(items):
                        removed = items.pop(item_num - 1)
                        BaseUI.print_success(f"Removed {removed['product_name']} from cart")
                        BaseUI.pause()
            
            elif choice == '3':
                if items:
                    return items
                else:
                    BaseUI.print_error("Cart is empty!")
                    BaseUI.pause()
            
            elif choice == '4':
                return None


class AnalyticsUI(BaseUI):
    """UI for Analytics and Reporting (common for all roles)"""
    
    @staticmethod
    def show_analytics_menu():
        """Display analytics menu"""
        BaseUI.clear_screen()
        BaseUI.print_header("ANALYTICS & REPORTS")
        
        print(f"{BaseUI.COLORS['BOLD']}Select an option:{BaseUI.COLORS['END']}\n")
        print("  1. View Price Trends")
        print("  2. Market Comparison")
        print("  3. Product Statistics")
        print("  4. Market Activity")
        print("  5. Generate PDF Report")
        print("  6. Export to Excel")
        print("  7. Export to CSV")
        print("  8. Back to Main Menu")
        
        choice = input(f"\n{BaseUI.COLORS['YELLOW']}Enter your choice (1-8): {BaseUI.COLORS['END']}")
        return choice.strip()
    
    @staticmethod
    def display_orders(orders):
        """Display list of orders"""
        if not orders:
            BaseUI.print_warning("No orders found.")
            return
        
        table_data = []
        for order in orders:
            status_color = {
                'pending': BaseUI.COLORS['YELLOW'],
                'confirmed': BaseUI.COLORS['CYAN'],
                'processing': BaseUI.COLORS['BLUE'],
                'ready': BaseUI.COLORS['GREEN'],
                'completed': BaseUI.COLORS['GREEN'],
                'cancelled': BaseUI.COLORS['RED']
            }.get(order.status, '')
            
            row = [
                order.order_id,
                order.customer_name if hasattr(order, 'customer_name') else order.customer_id,
                order.market_name if hasattr(order, 'market_name') else order.market_id,
                f"{float(order.total_amount):.2f}",
                f"{status_color}{order.status}{BaseUI.COLORS['END']}",
                str(order.created_at)[:10]
            ]
            table_data.append(row)
        
        headers = ["Order ID", "Customer", "Market", "Total", "Status", "Date"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def display_order_details(order, items):
        """Display detailed order information"""
        BaseUI.print_subheader(f"Order #{order.order_id} Details")
        
        # Order info
        info_data = [
            ["Customer", order.customer_name if hasattr(order, 'customer_name') else 'N/A'],
            ["Market", order.market_name if hasattr(order, 'market_name') else 'N/A'],
            ["Status", order.status],
            ["Total Amount", f"{float(order.total_amount):.2f}"],
            ["Order Date", str(order.created_at)],
            ["Delivery Address", order.delivery_address or 'N/A'],
            ["Delivery Phone", order.delivery_phone or 'N/A'],
            ["Notes", order.notes or 'N/A']
        ]
        
        print(tabulate(info_data, tablefmt="grid"))
        
        # Order items
        if items:
            print(f"\n{BaseUI.COLORS['BOLD']}Order Items:{BaseUI.COLORS['END']}")
            items_data = []
            for item in items:
                items_data.append([
                    item.product_name,
                    f"{float(item.quantity):.2f}",
                    item.unit if hasattr(item, 'unit') else 'unit',
                    f"{float(item.unit_price):.2f}",
                    f"{float(item.subtotal):.2f}"
                ])
            
            print(tabulate(items_data, headers=["Product", "Quantity", "Unit", "Price", "Subtotal"], tablefmt="grid"))
