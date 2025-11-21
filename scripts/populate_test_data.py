#!/usr/bin/env python3
"""
Populate comprehensive test data for analytics and reporting
Creates realistic data for products, markets, prices, users, and orders
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from src.auth import AuthManager
from src.user_manager import UserManager


def populate_markets(db):
    """Add comprehensive market data"""
    markets = [
        ('Central Market', 'Downtown Kigali, Main Business District'),
        ('Kimironko Market', 'Kimironko Sector, Gasabo District'),
        ('Nyabugogo Market', 'Nyabugogo Commercial Area, Nyarugenge District'),
        ('Remera Market', 'Remera Business Center, Gasabo District'),
        ('Kicukiro Market', 'Kicukiro District, Near Airport'),
        ('Muhima Market', 'Muhima Sector, Central Kigali'),
        ('Nyamirambo Market', 'Nyamirambo, Nyarugenge District'),
        ('Gikondo Market', 'Gikondo Industrial Zone')
    ]
    
    print("\n📍 Populating Markets...")
    for market_name, location in markets:
        query = "INSERT IGNORE INTO markets (market_name, location) VALUES (%s, %s)"
        db.execute_query(query, (market_name, location))
    
    print(f"   ✅ Added {len(markets)} markets")


def populate_products(db):
    """Add comprehensive product catalog"""
    products = [
        # Grains & Cereals
        ('Maize (White)', 'Grains', 'kg'),
        ('Maize (Yellow)', 'Grains', 'kg'),
        ('Beans (Red)', 'Grains', 'kg'),
        ('Beans (White)', 'Grains', 'kg'),
        ('Rice (Local)', 'Grains', 'kg'),
        ('Rice (Imported)', 'Grains', 'kg'),
        ('Wheat Flour', 'Grains', 'kg'),
        ('Sorghum', 'Grains', 'kg'),
        
        # Vegetables
        ('Tomatoes', 'Vegetables', 'kg'),
        ('Potatoes (Irish)', 'Vegetables', 'kg'),
        ('Sweet Potatoes', 'Vegetables', 'kg'),
        ('Onions', 'Vegetables', 'kg'),
        ('Cabbage', 'Vegetables', 'kg'),
        ('Carrots', 'Vegetables', 'kg'),
        ('Green Peppers', 'Vegetables', 'kg'),
        ('Eggplant', 'Vegetables', 'kg'),
        ('Spinach', 'Vegetables', 'bunch'),
        ('Lettuce', 'Vegetables', 'head'),
        
        # Fruits
        ('Bananas (Cooking)', 'Fruits', 'kg'),
        ('Bananas (Sweet)', 'Fruits', 'kg'),
        ('Avocado', 'Fruits', 'kg'),
        ('Passion Fruit', 'Fruits', 'kg'),
        ('Pineapple', 'Fruits', 'each'),
        ('Mango', 'Fruits', 'kg'),
        ('Papaya', 'Fruits', 'kg'),
        ('Watermelon', 'Fruits', 'kg'),
        
        # Livestock & Poultry
        ('Chicken (Live)', 'Livestock', 'each'),
        ('Chicken (Dressed)', 'Livestock', 'kg'),
        ('Goat (Live)', 'Livestock', 'each'),
        ('Eggs', 'Livestock', 'tray'),
        ('Beef', 'Livestock', 'kg'),
        ('Pork', 'Livestock', 'kg'),
        
        # Dairy
        ('Milk (Fresh)', 'Dairy', 'liter'),
        ('Milk (Powder)', 'Dairy', 'kg'),
        ('Cheese (Local)', 'Dairy', 'kg'),
        
        # Legumes
        ('Peas (Green)', 'Legumes', 'kg'),
        ('Peas (Dried)', 'Legumes', 'kg'),
        ('Groundnuts', 'Legumes', 'kg'),
        ('Soybeans', 'Legumes', 'kg'),
    ]
    
    print("\n🌾 Populating Products...")
    for product_name, category, unit in products:
        query = "INSERT IGNORE INTO products (product_name, category, unit) VALUES (%s, %s, %s)"
        db.execute_query(query, (product_name, category, unit))
    
    print(f"   ✅ Added {len(products)} products")


def populate_users(db, auth, user_manager):
    """Create test users across all roles"""
    users = [
        # Super Admins
        ('admin', 'admin123', 'super_admin', 'System Administrator', 'admin@market.rw'),
        ('manager', 'manager123', 'super_admin', 'Market Manager', 'manager@market.rw'),
        
        # Sellers
        ('seller1', 'seller123', 'seller', 'John Mugabo', 'john@market.rw'),
        ('seller2', 'seller123', 'seller', 'Alice Uwase', 'alice@market.rw'),
        ('seller3', 'seller123', 'seller', 'David Nkunda', 'david@market.rw'),
        ('seller4', 'seller123', 'seller', 'Grace Mukamana', 'grace@market.rw'),
        ('seller5', 'seller123', 'seller', 'Eric Habimana', 'eric@market.rw'),
        
        # Customers
        ('customer1', 'customer123', 'customer', 'Sarah Uwera', 'sarah@email.rw'),
        ('customer2', 'customer123', 'customer', 'Peter Kayitare', 'peter@email.rw'),
        ('customer3', 'customer123', 'customer', 'Marie Umutoni', 'marie@email.rw'),
        ('customer4', 'customer123', 'customer', 'James Nsengimana', 'james@email.rw'),
        ('customer5', 'customer123', 'customer', 'Linda Iradukunda', 'linda@email.rw'),
    ]
    
    print("\n👥 Populating Users...")
    created_count = 0
    for username, password, role, full_name, email in users:
        # Check if user exists
        check_query = "SELECT user_id FROM users WHERE username = %s"
        existing = db.execute_query(check_query, (username,), fetch=True)
        
        if not existing:
            hashed_password = auth.hash_password(password)
            status = 'active' if role == 'super_admin' else 'pending'
            
            query = """
            INSERT INTO users (username, password_hash, role, full_name, email, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, (username, hashed_password, role, full_name, email, status))
            
            # Approve sellers automatically
            if role == 'seller':
                update_query = "UPDATE users SET status = 'active' WHERE username = %s"
                db.execute_query(update_query, (username,))
            
            created_count += 1
    
    print(f"   ✅ Added {created_count} users")


def populate_prices(db):
    """Generate realistic price history for the past 90 days"""
    print("\n💰 Populating Price History (this may take a moment)...")
    
    # Get all products and markets
    products = db.execute_query("SELECT product_id, product_name, category FROM products", fetch=True)
    markets = db.execute_query("SELECT market_id, market_name FROM markets", fetch=True)
    
    if not products or not markets:
        print("   ⚠️  No products or markets found!")
        return
    
    # Base prices for products (in RWF)
    base_prices = {
        'Grains': {'min': 400, 'max': 1200},
        'Vegetables': {'min': 200, 'max': 800},
        'Fruits': {'min': 300, 'max': 1500},
        'Livestock': {'min': 2000, 'max': 150000},
        'Dairy': {'min': 800, 'max': 5000},
        'Legumes': {'min': 500, 'max': 1500}
    }
    
    # Generate prices for last 90 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=90)
    
    price_count = 0
    batch_data = []
    
    # Progress indicator
    total_combinations = len(products) * len(markets)
    processed = 0
    
    for product in products:
        product_id = product['product_id']
        category = product['category']
        
        # Get base price range for category
        price_range = base_prices.get(category, {'min': 500, 'max': 2000})
        base_price = random.randint(price_range['min'], price_range['max'])
        
        for market in markets:
            market_id = market['market_id']
            processed += 1
            
            # Show progress every 20%
            if processed % max(1, total_combinations // 5) == 0:
                progress = (processed / total_combinations) * 100
                print(f"   ⏳ Progress: {progress:.0f}% ({processed}/{total_combinations})")
            
            # Market-specific price variation (some markets are more expensive)
            market_multiplier = random.uniform(0.9, 1.15)
            market_base = base_price * market_multiplier
            
            # Generate prices over time with realistic variations
            current_date = start_date
            current_price = market_base
            
            while current_date <= end_date:
                # Add some randomness (seasonal variation, supply/demand)
                # Prices don't change every day, update every 3-7 days
                if random.random() < 0.3:  # 30% chance of price update
                    # Price can go up or down by 5-15%
                    change_percent = random.uniform(-0.15, 0.15)
                    current_price = current_price * (1 + change_percent)
                    
                    # Ensure price stays within reasonable bounds
                    min_price = price_range['min'] * 0.7
                    max_price = price_range['max'] * 1.3
                    current_price = max(min_price, min(max_price, current_price))
                    
                    # Randomly assign recorder
                    recorders = ['System', 'Market Officer', 'Price Monitor', 'Data Collector']
                    recorder = random.choice(recorders)
                    
                    # Add to batch
                    batch_data.append((
                        product_id,
                        market_id,
                        round(current_price, 2),
                        current_date,
                        recorder
                    ))
                    price_count += 1
                    
                    # Insert in batches of 100 for better performance
                    if len(batch_data) >= 100:
                        query = """
                        INSERT INTO prices (product_id, market_id, price, date, recorded_by)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        for data in batch_data:
                            db.execute_query(query, data)
                        batch_data = []
                
                # Move to next day
                current_date += timedelta(days=random.randint(1, 3))
    
    # Insert remaining batch
    if batch_data:
        query = """
        INSERT INTO prices (product_id, market_id, price, date, recorded_by)
        VALUES (%s, %s, %s, %s, %s)
        """
        for data in batch_data:
            db.execute_query(query, data)
    
    print(f"   ✅ Added {price_count} price records across 90 days")


def populate_orders(db):
    """Generate sample orders for testing"""
    print("\n🛒 Populating Orders...")
    
    # Get customers and products
    customers = db.execute_query(
        "SELECT user_id FROM users WHERE role = 'customer' AND status = 'active'",
        fetch=True
    )
    
    if not customers:
        print("   ⚠️  No active customers found!")
        return
    
    products = db.execute_query(
        "SELECT product_id, product_name FROM products LIMIT 20",
        fetch=True
    )
    
    if not products:
        print("   ⚠️  No products found!")
        return
    
    order_count = 0
    item_count = 0
    
    # Generate 20 orders over the past 30 days
    for i in range(20):
        customer = random.choice(customers)
        customer_id = customer['user_id']
        
        # Random date in last 30 days
        days_ago = random.randint(0, 30)
        order_date = datetime.now() - timedelta(days=days_ago)
        
        # Random status based on order age
        if days_ago > 20:
            statuses = ['completed', 'completed', 'completed']
        elif days_ago > 10:
            statuses = ['completed', 'ready', 'processing']
        elif days_ago > 5:
            statuses = ['processing', 'ready', 'confirmed']
        else:
            statuses = ['pending', 'confirmed', 'processing']
        
        status = random.choice(statuses)
        
        # Create order
        order_query = """
        INSERT INTO orders (customer_id, status, order_date, delivery_address, total_amount)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        addresses = [
            'KG 123 St, Kigali',
            'Kimironko, Gasabo',
            'Nyamirambo, Nyarugenge',
            'Remera, Gasabo',
            'Kicukiro Center'
        ]
        
        address = random.choice(addresses)
        
        # Add 1-5 items per order
        num_items = random.randint(1, 5)
        total_amount = 0
        
        # Create order first (without total)
        db.execute_query(order_query, (customer_id, status, order_date, address, 0))
        
        # Get the order_id
        order_id_result = db.execute_query("SELECT LAST_INSERT_ID() as order_id", fetch=True)
        order_id = order_id_result[0]['order_id']
        
        # Add order items
        selected_products = random.sample(products, min(num_items, len(products)))
        
        for product in selected_products:
            product_id = product['product_id']
            quantity = random.randint(1, 10)
            
            # Get recent price for this product
            price_query = """
            SELECT price FROM prices 
            WHERE product_id = %s 
            ORDER BY date DESC 
            LIMIT 1
            """
            price_result = db.execute_query(price_query, (product_id,), fetch=True)
            
            if price_result:
                unit_price = float(price_result[0]['price'])
            else:
                unit_price = random.uniform(500, 2000)
            
            subtotal = unit_price * quantity
            total_amount += subtotal
            
            # Insert order item
            item_query = """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            """
            db.execute_query(item_query, (order_id, product_id, quantity, unit_price, subtotal))
            item_count += 1
        
        # Update order total
        update_query = "UPDATE orders SET total_amount = %s WHERE order_id = %s"
        db.execute_query(update_query, (total_amount, order_id))
        order_count += 1
    
    print(f"   ✅ Added {order_count} orders with {item_count} items")


def main():
    """Main function to populate all test data"""
    print("=" * 60)
    print("🌾 MARKET PRICE TRACKER - TEST DATA POPULATION")
    print("=" * 60)
    
    # Connect to database
    db = Database()
    if not db.connect():
        print("\n❌ Failed to connect to database!")
        return
    
    print("\n✅ Connected to database")
    
    # Initialize authentication
    auth = AuthManager(db)
    user_manager = UserManager(db)
    
    try:
        # Populate data
        populate_markets(db)
        populate_products(db)
        populate_users(db, auth, user_manager)
        populate_prices(db)
        populate_orders(db)
        
        print("\n" + "=" * 60)
        print("✅ TEST DATA POPULATION COMPLETE!")
        print("=" * 60)
        
        print("\n📊 Summary:")
        
        # Get counts
        market_count = db.execute_query("SELECT COUNT(*) as count FROM markets", fetch=True)[0]['count']
        product_count = db.execute_query("SELECT COUNT(*) as count FROM products", fetch=True)[0]['count']
        user_count = db.execute_query("SELECT COUNT(*) as count FROM users", fetch=True)[0]['count']
        price_count = db.execute_query("SELECT COUNT(*) as count FROM prices", fetch=True)[0]['count']
        order_count = db.execute_query("SELECT COUNT(*) as count FROM orders", fetch=True)[0]['count']
        
        print(f"   • Markets: {market_count}")
        print(f"   • Products: {product_count}")
        print(f"   • Users: {user_count}")
        print(f"   • Price Records: {price_count}")
        print(f"   • Orders: {order_count}")
        
        print("\n👤 Test Login Credentials:")
        print("   Super Admin: admin / admin123")
        print("   Seller: seller1 / seller123")
        print("   Customer: customer1 / customer123")
        
        print("\n🚀 You can now test analytics and reporting features!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error populating data: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()
