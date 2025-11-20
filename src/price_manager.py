"""
Price management module
Handles all price-related operations including CRUD operations,
comparisons, and trend analysis
"""

from datetime import datetime, date
from src.models import Market, Product, Price


class PriceManager:
    """Manages price operations and queries"""
    
    def __init__(self, database):
        """Initialize with database connection"""
        self.db = database
    
    # =============== MARKET OPERATIONS ===============
    
    def get_all_markets(self):
        """Retrieve all markets from database"""
        query = "SELECT * FROM markets ORDER BY market_name"
        results = self.db.execute_query(query, fetch=True)
        
        if results:
            return [Market(**row) for row in results]
        return []
    
    def get_market_by_id(self, market_id):
        """Get a specific market by ID"""
        query = "SELECT * FROM markets WHERE market_id = %s"
        results = self.db.execute_query(query, (market_id,), fetch=True)
        
        if results:
            return Market(**results[0])
        return None
    
    def add_market(self, market_name, location):
        """Add a new market"""
        query = "INSERT INTO markets (market_name, location) VALUES (%s, %s)"
        success = self.db.execute_query(query, (market_name, location))
        return success
    
    # =============== PRODUCT OPERATIONS ===============
    
    def get_all_products(self):
        """Retrieve all products from database"""
        query = "SELECT * FROM products ORDER BY category, product_name"
        results = self.db.execute_query(query, fetch=True)
        
        if results:
            return [Product(**row) for row in results]
        return []
    
    def get_products_by_category(self, category):
        """Get products filtered by category"""
        query = "SELECT * FROM products WHERE category = %s ORDER BY product_name"
        results = self.db.execute_query(query, (category,), fetch=True)
        
        if results:
            return [Product(**row) for row in results]
        return []
    
    def get_product_by_id(self, product_id):
        """Get a specific product by ID"""
        query = "SELECT * FROM products WHERE product_id = %s"
        results = self.db.execute_query(query, (product_id,), fetch=True)
        
        if results:
            return Product(**results[0])
        return None
    
    def add_product(self, product_name, category, unit):
        """Add a new product"""
        query = "INSERT INTO products (product_name, category, unit) VALUES (%s, %s, %s)"
        success = self.db.execute_query(query, (product_name, category, unit))
        return success
    
    # =============== PRICE OPERATIONS ===============
    
    def add_price(self, product_id, market_id, price, date_str=None, recorded_by=None):
        """Add a new price record"""
        if date_str is None:
            date_str = date.today().strftime('%Y-%m-%d')
        
        query = """
        INSERT INTO prices (product_id, market_id, price, date, recorded_by)
        VALUES (%s, %s, %s, %s, %s)
        """
        success = self.db.execute_query(
            query, 
            (product_id, market_id, price, date_str, recorded_by or 'User')
        )
        return success
    
    def get_current_prices(self, product_id=None, market_id=None):
        """Get the most recent prices for products"""
        query = """
        SELECT p.*, pr.product_name, pr.unit, m.market_name
        FROM prices p
        JOIN products pr ON p.product_id = pr.product_id
        JOIN markets m ON p.market_id = m.market_id
        WHERE p.date = (
            SELECT MAX(p2.date) 
            FROM prices p2 
            WHERE p2.product_id = p.product_id 
            AND p2.market_id = p.market_id
        )
        """
        
        params = []
        if product_id:
            query += " AND p.product_id = %s"
            params.append(product_id)
        if market_id:
            query += " AND p.market_id = %s"
            params.append(market_id)
        
        query += " ORDER BY pr.product_name, m.market_name"
        
        results = self.db.execute_query(query, tuple(params), fetch=True)
        
        if results:
            return [Price(**row) for row in results]
        return []
    
    def compare_prices(self, product_id):
        """Compare prices of a product across different markets"""
        query = """
        SELECT p.*, pr.product_name, pr.unit, m.market_name
        FROM prices p
        JOIN products pr ON p.product_id = pr.product_id
        JOIN markets m ON p.market_id = m.market_id
        WHERE p.product_id = %s
        AND p.date = (
            SELECT MAX(p2.date) 
            FROM prices p2 
            WHERE p2.product_id = p.product_id 
            AND p2.market_id = p.market_id
        )
        ORDER BY p.price ASC
        """
        
        results = self.db.execute_query(query, (product_id,), fetch=True)
        
        if results:
            return [Price(**row) for row in results]
        return []
    
    def get_price_trend(self, product_id, market_id):
        """Get price trend for a product in a specific market"""
        query = """
        SELECT p.*, pr.product_name, pr.unit, m.market_name
        FROM prices p
        JOIN products pr ON p.product_id = pr.product_id
        JOIN markets m ON p.market_id = m.market_id
        WHERE p.product_id = %s AND p.market_id = %s
        ORDER BY p.date DESC
        LIMIT 10
        """
        
        results = self.db.execute_query(query, (product_id, market_id), fetch=True)
        
        if results:
            return [Price(**row) for row in results]
        return []
    
    def analyze_trend(self, product_id, market_id):
        """Analyze if price is increasing, decreasing, or stable"""
        prices = self.get_price_trend(product_id, market_id)
        
        if len(prices) < 2:
            return "insufficient_data", None, None
        
        latest_price = float(prices[0].price)
        previous_price = float(prices[1].price)
        
        change = latest_price - previous_price
        change_percent = (change / previous_price) * 100 if previous_price != 0 else 0
        
        if change > 0:
            trend = "increased"
        elif change < 0:
            trend = "decreased"
        else:
            trend = "stable"
        
        return trend, change, change_percent
    
    def get_all_categories(self):
        """Get all unique product categories"""
        query = "SELECT DISTINCT category FROM products ORDER BY category"
        results = self.db.execute_query(query, fetch=True)
        
        if results:
            return [row['category'] for row in results]
        return []
    
    def search_products(self, search_term):
        """Search products by name"""
        query = """
        SELECT * FROM products 
        WHERE product_name LIKE %s 
        ORDER BY product_name
        """
        search_pattern = f"%{search_term}%"
        results = self.db.execute_query(query, (search_pattern,), fetch=True)
        
        if results:
            return [Product(**row) for row in results]
        return []
