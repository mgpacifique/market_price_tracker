"""
Data models for the application
Defines the structure for User, Market, Product, Price, Order, and related entities
"""

from datetime import datetime


class User:
    """Represents a system user (admin, seller, or customer)"""
    
    def __init__(self, user_id, username, email, password_hash, full_name, 
                 phone_number=None, role='customer', status='active', 
                 created_at=None, updated_at=None, last_login=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.phone_number = phone_number
        self.role = role
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at
        self.last_login = last_login
    
    def __str__(self):
        return f"{self.full_name} ({self.role})"
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'role': self.role,
            'status': self.status
        }


class Market:
    """Represents a market location"""
    
    def __init__(self, market_id, market_name, location, created_at=None, 
                 user_id=None, status='active', description=None):
        self.market_id = market_id
        self.market_name = market_name
        self.location = location
        self.user_id = user_id
        self.status = status
        self.description = description
        self.created_at = created_at or datetime.now()
    
    def __str__(self):
        return f"{self.market_name} ({self.location})"
    
    def to_dict(self):
        return {
            'market_id': self.market_id,
            'market_name': self.market_name,
            'location': self.location,
            'user_id': self.user_id,
            'status': self.status,
            'description': self.description
        }


class Product:
    """Represents an agricultural product"""
    
    def __init__(self, product_id, product_name, category, unit, created_at=None,
                 user_id=None, market_id=None, description=None, image_url=None):
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.unit = unit
        self.user_id = user_id
        self.market_id = market_id
        self.description = description
        self.image_url = image_url
        self.created_at = created_at or datetime.now()
    
    def __str__(self):
        return f"{self.product_name} ({self.unit})"
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'unit': self.unit,
            'user_id': self.user_id,
            'market_id': self.market_id,
            'description': self.description,
            'image_url': self.image_url
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


class Order:
    """Represents a customer order"""
    
    def __init__(self, order_id, customer_id, market_id, total_amount, status='pending',
                 delivery_address=None, delivery_phone=None, notes=None,
                 created_at=None, updated_at=None, customer_name=None, market_name=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.market_id = market_id
        self.total_amount = total_amount
        self.status = status
        self.delivery_address = delivery_address
        self.delivery_phone = delivery_phone
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at
        self.customer_name = customer_name
        self.market_name = market_name
    
    def __str__(self):
        return f"Order #{self.order_id} - {self.status} ({self.total_amount})"
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'market_id': self.market_id,
            'total_amount': float(self.total_amount),
            'status': self.status,
            'delivery_address': self.delivery_address,
            'delivery_phone': self.delivery_phone,
            'notes': self.notes,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at) if self.updated_at else None,
            'customer_name': self.customer_name,
            'market_name': self.market_name
        }


class OrderItem:
    """Represents an item in an order"""
    
    def __init__(self, order_item_id, order_id, product_id, quantity, unit_price, subtotal,
                 product_name=None, unit=None):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal
        self.product_name = product_name
        self.unit = unit
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity} = {self.subtotal}"
    
    def to_dict(self):
        return {
            'order_item_id': self.order_item_id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': float(self.quantity),
            'unit_price': float(self.unit_price),
            'subtotal': float(self.subtotal),
            'product_name': self.product_name,
            'unit': self.unit
        }
