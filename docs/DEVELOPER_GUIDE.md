# Developer Quick Reference

## 🔐 Authentication API

```python
from src.auth import AuthManager

# Initialize
auth = AuthManager(database)

# Register new user
success, message = auth.register_user(
    username="john_doe",
    email="john@example.com",
    password="SecurePass123!",
    full_name="John Doe",
    phone_number="+250788123456",
    role="customer"  # 'customer', 'seller', 'super_admin'
)

# Login
success, message = auth.login("john_doe", "SecurePass123!")

# Check authentication
if auth.is_authenticated():
    user = auth.get_current_user()
    print(f"Logged in as: {user.full_name}")

# Check roles
if auth.is_super_admin():
    # Admin operations

if auth.is_seller():
    # Seller operations

if auth.is_customer():
    # Customer operations

# Logout
auth.logout()
```

## 👥 User Management API (Admin Only)

```python
from src.user_manager import UserManager

user_mgr = UserManager(database)

# Get all users
all_users = user_mgr.get_all_users()

# Get users by role
sellers = user_mgr.get_all_users(role='seller')
customers = user_mgr.get_all_users(role='customer')

# Get pending sellers
pending = user_mgr.get_pending_sellers()

# Approve seller
success, msg = user_mgr.approve_seller(user_id=5)

# Suspend user
success, msg = user_mgr.suspend_user(user_id=10)

# Activate user
success, msg = user_mgr.activate_user(user_id=10)

# Delete user (soft delete)
success, msg = user_mgr.delete_user(user_id=15)

# Update user info
success, msg = user_mgr.update_user_info(
    user_id=5,
    full_name="New Name",
    email="newemail@example.com",
    phone_number="+250788999999"
)

# Get statistics
stats = user_mgr.get_user_statistics()
print(f"Total users: {stats['total_users']}")
print(f"Active sellers: {stats['sellers']}")

# Search users
results = user_mgr.search_users("john")
```

## 🛒 Order Management API

```python
from src.order_manager import OrderManager

order_mgr = OrderManager(database)

# Create order
items = [
    {'product_id': 1, 'quantity': 5.0, 'unit_price': 450.00},
    {'product_id': 2, 'quantity': 3.0, 'unit_price': 800.00}
]

success, order_id = order_mgr.create_order(
    customer_id=user_id,
    market_id=1,
    items=items,
    delivery_address="123 Main St",
    delivery_phone="+250788123456",
    notes="Morning delivery preferred"
)

# Get order details
order = order_mgr.get_order_by_id(order_id)
print(f"Order total: {order.total_amount}")

# Get order items
items = order_mgr.get_order_items(order_id)
for item in items:
    print(f"{item.product_name}: {item.quantity} x {item.unit_price}")

# Get customer orders
customer_orders = order_mgr.get_customer_orders(customer_id)
pending_orders = order_mgr.get_customer_orders(customer_id, status='pending')

# Get market orders (seller view)
market_orders = order_mgr.get_market_orders(market_id)
confirmed_orders = order_mgr.get_market_orders(market_id, status='confirmed')

# Update order status
success, msg = order_mgr.update_order_status(order_id, 'confirmed')
# Valid statuses: pending, confirmed, processing, ready, completed, cancelled

# Cancel order
success, msg = order_mgr.cancel_order(order_id, user_id, user_role)

# Get statistics
stats = order_mgr.get_order_statistics(market_id=1)
print(f"Total orders: {stats['total_orders']}")
print(f"Total revenue: {stats['total_revenue']}")
```

## 📊 Analytics API

```python
from src.analytics import Analytics

analytics = Analytics(database)

# Price trend over time
trend_data = analytics.get_price_trend_data(
    product_id=1,
    market_id=2,  # Optional
    days=30
)

# Market price comparison
comparison = analytics.get_market_price_comparison(
    product_id=1,
    date=None  # None = latest prices
)

# Product price statistics
stats = analytics.get_product_price_statistics(
    product_id=1,
    market_id=None,  # Optional
    days=30
)
print(f"Min: {stats['min_price']}")
print(f"Max: {stats['max_price']}")
print(f"Avg: {stats['avg_price']}")
print(f"Trend: {stats['trend']}")  # increasing, decreasing, stable

# Top products by trading volume
top_products = analytics.get_top_products_by_volume(limit=10)

# Most volatile products
volatile = analytics.get_most_volatile_products(limit=10, days=30)

# Market activity
activity = analytics.get_market_activity(days=30)

# Seasonal patterns
patterns = analytics.get_seasonal_patterns(product_id=1, months=12)

# Forecast data (moving average)
forecast = analytics.get_price_forecast_data(product_id=1, market_id=2)

# Market report
report = analytics.generate_market_report(market_id=1, days=30)
```

## 📄 Export & Reporting API

```python
from src.export import ReportExporter
from src.analytics import Analytics

analytics = Analytics(database)
exporter = ReportExporter(analytics)

# Check dependencies
missing = exporter.check_dependencies()
if missing:
    print(f"Install: pip install {' '.join(missing)}")

# Generate price trend chart
chart_path, msg = exporter.generate_price_trend_chart(
    product_id=1,
    product_name="Maize",
    market_id=2,
    market_name="Kimironko Market",
    days=30
)

# Generate market comparison chart
chart_path, msg = exporter.generate_market_comparison_chart(
    product_id=1,
    product_name="Maize"
)

# Export to Excel
filepath, msg = exporter.export_to_excel(
    data=trend_data,
    filename="price_trends",
    sheet_name="Prices"
)

# Export to CSV
filepath, msg = exporter.export_to_csv(
    data=trend_data,
    filename="price_data"
)

# Generate PDF report
filepath, msg = exporter.generate_pdf_report(
    product_id=1,
    product_name="Maize",
    market_id=None,  # None = compare all markets
    market_name=None,
    days=30
)

# Generate market analytics PDF
filepath, msg = exporter.generate_market_analytics_pdf(
    market_id=1,
    market_name="Central Market",
    days=30
)
```

## 🗃️ Database Models

### User Model
```python
from src.models import User

user = User(
    user_id=1,
    username="john_doe",
    email="john@example.com",
    password_hash="hashed_password",
    full_name="John Doe",
    phone_number="+250788123456",
    role="customer",  # super_admin, seller, customer
    status="active",  # active, pending, suspended, deleted
    created_at=datetime.now(),
    updated_at=datetime.now(),
    last_login=datetime.now()
)

# Convert to dict
user_dict = user.to_dict()
```

### Market Model (Enhanced)
```python
from src.models import Market

market = Market(
    market_id=1,
    market_name="Central Market",
    location="Kigali Downtown",
    user_id=5,  # Seller who owns this market
    status="active",  # active, inactive
    description="Main market in downtown",
    created_at=datetime.now()
)
```

### Product Model (Enhanced)
```python
from src.models import Product

product = Product(
    product_id=1,
    product_name="Maize",
    category="Grains",
    unit="kg",
    user_id=5,  # Seller who added this
    market_id=1,  # Market where it's sold
    description="Local maize",
    image_url="/images/maize.jpg",
    created_at=datetime.now()
)
```

### Order Model
```python
from src.models import Order

order = Order(
    order_id=1,
    customer_id=10,
    market_id=1,
    total_amount=3650.00,
    status="pending",
    delivery_address="123 Main St",
    delivery_phone="+250788123456",
    notes="Morning delivery",
    created_at=datetime.now(),
    updated_at=datetime.now(),
    customer_name="Jane Doe",
    market_name="Central Market"
)
```

### OrderItem Model
```python
from src.models import OrderItem

item = OrderItem(
    order_item_id=1,
    order_id=1,
    product_id=1,
    quantity=5.0,
    unit_price=450.00,
    subtotal=2250.00,
    product_name="Maize",
    unit="kg"
)
```

## 🔍 Common Queries

### Get seller's market
```python
market_query = "SELECT * FROM markets WHERE user_id = %s"
result = db.execute_query(market_query, (seller_id,), fetch=True)
```

### Get products by seller
```python
product_query = "SELECT * FROM products WHERE user_id = %s"
products = db.execute_query(product_query, (seller_id,), fetch=True)
```

### Get customer order history
```python
order_query = """
SELECT o.*, m.market_name 
FROM orders o 
JOIN markets m ON o.market_id = m.market_id
WHERE o.customer_id = %s
ORDER BY o.created_at DESC
"""
orders = db.execute_query(order_query, (customer_id,), fetch=True)
```

## 🛡️ Permission Checks

```python
# Check if user can edit product
def can_edit_product(user, product):
    if user.role == 'super_admin':
        return True
    if user.role == 'seller' and product.user_id == user.user_id:
        return True
    return False

# Check if user can view order
def can_view_order(user, order):
    if user.role == 'super_admin':
        return True
    if user.role == 'customer' and order.customer_id == user.user_id:
        return True
    if user.role == 'seller':
        # Check if order is for seller's market
        market = user_mgr.get_seller_market(user.user_id)
        if market and order.market_id == market.market_id:
            return True
    return False
```

## 📝 Best Practices

1. **Always check authentication** before operations
2. **Validate user permissions** for sensitive actions
3. **Use transactions** for multi-step operations
4. **Hash passwords** with bcrypt (never store plain text)
5. **Clean expired sessions** periodically
6. **Validate input data** before database operations
7. **Use try-except** blocks for error handling
8. **Log important operations** for audit trail
9. **Cache analytics results** for performance
10. **Test with all user roles** before deployment

## 🔄 Workflow Examples

### Seller Registration Flow
```python
# 1. Customer registers as seller
auth.register_user(..., role='seller')  # Status: pending

# 2. Admin reviews and approves
user_mgr.approve_seller(user_id)  # Status: active

# 3. Seller creates market
# (Use existing market creation code)

# 4. Seller adds products
# (Use existing product creation code)
```

### Order Processing Flow
```python
# 1. Customer creates order
order_mgr.create_order(...)  # Status: pending

# 2. Seller confirms order
order_mgr.update_order_status(order_id, 'confirmed')

# 3. Seller processes order
order_mgr.update_order_status(order_id, 'processing')

# 4. Order ready for pickup/delivery
order_mgr.update_order_status(order_id, 'ready')

# 5. Order completed
order_mgr.update_order_status(order_id, 'completed')
```

This quick reference should help you integrate and use all the new features!
