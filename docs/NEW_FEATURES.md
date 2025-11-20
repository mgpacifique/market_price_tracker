# New Features Guide - Market Price Tracker

## 🎯 Overview

The Market Price Tracker has been enhanced with authentication, role-based access control, order management, and advanced analytics features.

## 🚀 New Features

### 1. **Authentication & Authorization System**

#### User Roles
- **Super Admin**: Full system access and user management
- **Seller/Market Owner**: Manage own market and products
- **Customer**: Browse, compare prices, and place orders

#### Features
- Secure password hashing with bcrypt
- Session management
- Role-based access control
- User registration and login

### 2. **Order Management System**

Customers can now place orders for products:
- Add items to cart
- Place orders with delivery details
- Track order status
- View order history

Sellers can:
- View orders for their market
- Update order status
- Manage order fulfillment

### 3. **Advanced Analytics**

Comprehensive price analysis tools:
- **Price Trends**: Track price changes over time
- **Market Comparison**: Compare prices across different markets
- **Statistical Analysis**: Min, max, average, standard deviation
- **Volatility Analysis**: Identify products with highest price fluctuations
- **Seasonal Patterns**: Analyze price patterns over months
- **Market Activity**: Track market activity and product coverage

### 4. **Export & Reporting**

Generate professional reports with visualizations:
- **PDF Reports**: Comprehensive reports with charts and statistics
- **Excel Export**: Data exports for further analysis
- **CSV Export**: Raw data exports
- **Charts**: Line charts for trends, bar charts for comparisons

## 📋 Installation

### 1. Install New Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `bcrypt`: Password hashing
- `pandas`: Data manipulation
- `matplotlib`: Chart generation
- `numpy`: Numerical operations
- `reportlab`: PDF generation

### 2. Run Database Migration

Apply the new database schema:

```bash
python scripts/run_migrations.py
```

This will:
- Create users table
- Create sessions table
- Add user relationships to markets and products
- Create orders and order_items tables
- Create analytics tables
- Create notifications table

### 3. Default Admin Account

After migration, a default super admin account is created:
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change this password immediately after first login!

## 🔐 User Management

### Registration

**Customers**: 
- Can register directly and start using the system immediately
- Status: `active` upon registration

**Sellers**:
- Register but require super admin approval
- Status: `pending` until approved
- Can create and manage their own market after approval

**Super Admin**:
- Created manually or through migration
- Can create other admin accounts

### User Statuses

- `active`: Can use the system
- `pending`: Awaiting approval (sellers only)
- `suspended`: Account suspended by admin
- `deleted`: Soft deleted account

## 📊 Using Analytics

### Price Trend Analysis

```python
from src.analytics import Analytics

analytics = Analytics(database)

# Get price trend for last 30 days
trend_data = analytics.get_price_trend_data(
    product_id=1,
    market_id=2,
    days=30
)

# Get statistics
stats = analytics.get_product_price_statistics(
    product_id=1,
    days=30
)
```

### Market Comparison

```python
# Compare prices across all markets
comparison = analytics.get_market_price_comparison(product_id=1)
```

### Volatility Analysis

```python
# Find most volatile products
volatile = analytics.get_most_volatile_products(limit=10, days=30)
```

## 📄 Generating Reports

### PDF Report with Charts

```python
from src.export import ReportExporter
from src.analytics import Analytics

analytics = Analytics(database)
exporter = ReportExporter(analytics)

# Generate comprehensive PDF report
filepath, message = exporter.generate_pdf_report(
    product_id=1,
    product_name="Maize",
    market_id=None,  # Compare across all markets
    days=30
)

print(f"Report saved to: {filepath}")
```

### Excel Export

```python
# Export price trend data to Excel
trend_data = analytics.get_price_trend_data(product_id=1, days=30)
filepath, message = exporter.export_to_excel(
    data=trend_data,
    filename="maize_price_trend",
    sheet_name="Price Data"
)
```

### CSV Export

```python
# Export to CSV
filepath, message = exporter.export_to_csv(
    data=trend_data,
    filename="price_data"
)
```

## 🛒 Order Management

### Creating an Order (Customer)

```python
from src.order_manager import OrderManager

order_mgr = OrderManager(database)

# Define order items
items = [
    {'product_id': 1, 'quantity': 5.0, 'unit_price': 450.00},
    {'product_id': 2, 'quantity': 3.0, 'unit_price': 800.00}
]

# Create order
success, order_id = order_mgr.create_order(
    customer_id=user.user_id,
    market_id=1,
    items=items,
    delivery_address="123 Main St, Kigali",
    delivery_phone="+250788123456",
    notes="Please deliver in the morning"
)
```

### Managing Orders (Seller)

```python
# Get all orders for your market
orders = order_mgr.get_market_orders(market_id=1)

# Update order status
success, msg = order_mgr.update_order_status(
    order_id=1,
    status='confirmed'
)
```

### Order Status Flow

```
pending → confirmed → processing → ready → completed
                  ↓
              cancelled
```

## 👥 User Management (Super Admin)

```python
from src.user_manager import UserManager

user_mgr = UserManager(database)

# View pending seller registrations
pending_sellers = user_mgr.get_pending_sellers()

# Approve a seller
success, msg = user_mgr.approve_seller(user_id=5)

# Suspend a user
success, msg = user_mgr.suspend_user(user_id=10)

# Get user statistics
stats = user_mgr.get_user_statistics()
```

## 📁 File Structure

```
market_price_tracker/
├── src/
│   ├── auth.py              # Authentication module
│   ├── user_manager.py      # User management (admin)
│   ├── order_manager.py     # Order management
│   ├── analytics.py         # Analytics engine
│   ├── export.py            # Report export & visualization
│   └── models.py            # Updated data models
├── migrations/
│   └── 001_add_auth_and_orders.sql
├── scripts/
│   └── run_migrations.py
├── reports/                 # Generated reports (created automatically)
└── requirements.txt
```

## 🔒 Security Best Practices

1. **Change Default Password**: Immediately change the admin password after first login
2. **Use Strong Passwords**: Enforce strong password policies
3. **Session Management**: Sessions expire after 7 days
4. **Clean Sessions**: Regularly run `auth.clean_expired_sessions()`
5. **Validate Inputs**: Always validate user inputs before processing

## 📈 Performance Tips

1. **Indexes**: The migration creates indexes on frequently queried fields
2. **Cache Analytics**: Cache analytics results for frequently viewed reports
3. **Batch Operations**: Use batch operations for bulk data imports
4. **Clean Old Data**: Periodically archive old price data

## 🐛 Troubleshooting

### Migration Issues

If migration fails:
1. Check database connection in `config.ini`
2. Ensure user has necessary permissions (CREATE, ALTER, INSERT)
3. Check for existing tables with same names
4. Review error messages in migration output

### Missing Dependencies

If charts or reports don't generate:
```bash
pip install matplotlib pandas reportlab numpy
```

### Permission Errors

If seller cannot access features:
1. Check user status is `active`
2. Verify market is linked to seller's user_id
3. Ensure proper role assignment

## 🎓 Next Steps

1. **Run the migration**: `python scripts/run_migrations.py`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Login as admin**: Use `admin`/`admin123`
4. **Change admin password**
5. **Create test users** for each role
6. **Explore the new features**!

## 📞 Support

For issues or questions:
1. Check the main README.md
2. Review QUICKSTART.md
3. Check error logs
4. Verify configuration in config.ini

## 🎉 Enjoy the new features!
