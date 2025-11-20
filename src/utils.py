"""
Utility functions for the application
"""

from datetime import datetime
import re


def validate_date(date_string):
    """Validate date string format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def format_currency(amount):
    """Format amount as currency"""
    return f"{amount:,.2f}"


def validate_price(price_str):
    """Validate price input"""
    try:
        price = float(price_str)
        if price < 0:
            return False, "Price cannot be negative"
        if price > 1000000:
            return False, "Price seems unreasonably high"
        return True, price
    except ValueError:
        return False, "Invalid price format"


def sanitize_input(text):
    """Sanitize user input to prevent SQL injection"""
    # Remove potentially harmful characters
    sanitized = re.sub(r'[^\w\s\-\.]', '', text)
    return sanitized.strip()


def validate_name(name):
    """Validate product or market name"""
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    if len(name) > 100:
        return False, "Name is too long (max 100 characters)"
    return True, name.strip()


def get_date_today():
    """Get today's date in YYYY-MM-DD format"""
    return datetime.now().strftime('%Y-%m-%d')


def format_date(date_obj):
    """Format date object to string"""
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime('%Y-%m-%d')
