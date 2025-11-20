"""
Database connection and initialization module
Handles MySQL database setup and connection management
"""

import mysql.connector
from mysql.connector import Error
import configparser
import os


class Database:
    """Manages database connections and operations"""
    
    def __init__(self, config_path='config.ini'):
        """Initialize database connection parameters"""
        self.connection = None
        self.config_path = config_path
        self.load_config()
    
    def load_config(self):
        """Load database configuration from config file"""
        config = configparser.ConfigParser()
        
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Configuration file '{self.config_path}' not found. "
                "Please copy config.ini.sample to config.ini and update it."
            )
        
        config.read(self.config_path)
        
        self.host = config.get('database', 'host')
        self.port = config.getint('database', 'port')
        self.user = config.get('database', 'user')
        self.password = config.get('database', 'password')
        self.database = config.get('database', 'database')
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a SQL query"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            print(f"Error executing query: {e}")
            return None if fetch else False
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        
        # Create markets table
        markets_table = """
        CREATE TABLE IF NOT EXISTS markets (
            market_id INT AUTO_INCREMENT PRIMARY KEY,
            market_name VARCHAR(100) NOT NULL UNIQUE,
            location VARCHAR(200) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create products table
        products_table = """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL UNIQUE,
            category VARCHAR(50) NOT NULL,
            unit VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create prices table
        prices_table = """
        CREATE TABLE IF NOT EXISTS prices (
            price_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            market_id INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            date DATE NOT NULL,
            recorded_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
            FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE,
            INDEX idx_product_market_date (product_id, market_id, date)
        )
        """
        
        try:
            self.execute_query(markets_table)
            self.execute_query(products_table)
            self.execute_query(prices_table)
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
    
    def insert_sample_data(self):
        """Insert sample data for testing"""
        
        # Sample markets
        markets = [
            ('Central Market', 'Kigali Downtown'),
            ('Kimironko Market', 'Kimironko, Kigali'),
            ('Nyabugogo Market', 'Nyabugogo, Kigali'),
            ('Remera Market', 'Remera, Kigali')
        ]
        
        # Sample products
        products = [
            ('Maize', 'Grains', 'kg'),
            ('Beans', 'Grains', 'kg'),
            ('Rice', 'Grains', 'kg'),
            ('Tomatoes', 'Vegetables', 'kg'),
            ('Potatoes', 'Vegetables', 'kg'),
            ('Onions', 'Vegetables', 'kg'),
            ('Cabbage', 'Vegetables', 'kg'),
            ('Bananas', 'Fruits', 'kg'),
            ('Avocado', 'Fruits', 'kg'),
            ('Goat', 'Livestock', 'each')
        ]
        
        # Insert markets
        for market in markets:
            query = "INSERT IGNORE INTO markets (market_name, location) VALUES (%s, %s)"
            self.execute_query(query, market)
        
        # Insert products
        for product in products:
            query = "INSERT IGNORE INTO products (product_name, category, unit) VALUES (%s, %s, %s)"
            self.execute_query(query, product)
        
        # Sample prices (recent data)
        sample_prices = [
            (1, 1, 450.00, '2025-11-19'),  # Maize at Central Market
            (1, 2, 470.00, '2025-11-19'),  # Maize at Kimironko
            (1, 3, 440.00, '2025-11-19'),  # Maize at Nyabugogo
            (2, 1, 800.00, '2025-11-19'),  # Beans at Central Market
            (2, 2, 820.00, '2025-11-19'),  # Beans at Kimironko
            (4, 1, 500.00, '2025-11-19'),  # Tomatoes at Central Market
            (4, 2, 520.00, '2025-11-19'),  # Tomatoes at Kimironko
            (5, 1, 300.00, '2025-11-19'),  # Potatoes at Central Market
            (8, 1, 400.00, '2025-11-19'),  # Bananas at Central Market
            # Previous prices for trend analysis
            (1, 1, 430.00, '2025-11-10'),
            (1, 1, 420.00, '2025-11-01'),
            (4, 1, 480.00, '2025-11-10'),
            (4, 1, 450.00, '2025-11-01'),
        ]
        
        for price_data in sample_prices:
            query = """
            INSERT IGNORE INTO prices (product_id, market_id, price, date, recorded_by)
            VALUES (%s, %s, %s, %s, 'System')
            """
            self.execute_query(query, price_data)
        
        return True
