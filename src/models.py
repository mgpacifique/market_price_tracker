"""
Data models for the application
Defines the structure for Market, Product, and Price
"""

from datetime import datetime


class Market:
    """Represents a market location"""
    
    def __init__(self, market_id, market_name, location, created_at=None):
        self.market_id = market_id
        self.market_name = market_name
        self.location = location
        self.created_at = created_at or datetime.now()
    
    def __str__(self):
        return f"{self.market_name} ({self.location})"
    
    def to_dict(self):
        return {
            'market_id': self.market_id,
            'market_name': self.market_name,
            'location': self.location
        }


class Product:
    """Represents an agricultural product"""
    
    def __init__(self, product_id, product_name, category, unit, created_at=None):
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.unit = unit
        self.created_at = created_at or datetime.now()
    
    def __str__(self):
        return f"{self.product_name} ({self.unit})"
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'unit': self.unit
        }


class Price:
    """Represents a price record"""
    
    def __init__(self, price_id, product_id, market_id, price, date, 
                 recorded_by=None, created_at=None, product_name=None, 
                 market_name=None, unit=None):
        self.price_id = price_id
        self.product_id = product_id
        self.market_id = market_id
        self.price = price
        self.date = date
        self.recorded_by = recorded_by
        self.created_at = created_at or datetime.now()
        self.product_name = product_name
        self.market_name = market_name
        self.unit = unit
    
    def __str__(self):
        return f"{self.product_name}: {self.price} ({self.market_name}, {self.date})"
    
    def to_dict(self):
        return {
            'price_id': self.price_id,
            'product_id': self.product_id,
            'market_id': self.market_id,
            'price': float(self.price),
            'date': str(self.date),
            'recorded_by': self.recorded_by,
            'product_name': self.product_name,
            'market_name': self.market_name,
            'unit': self.unit
        }
