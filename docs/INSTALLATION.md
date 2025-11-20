# Installation and Setup Guide

## 🚀 Quick Start

Follow these steps to set up the enhanced Market Price Tracker with all new features.

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- ✅ mysql-connector-python (Database)
- ✅ bcrypt (Password security)
- ✅ pandas (Data analysis)
- ✅ matplotlib (Charts)
- ✅ numpy (Numerical operations)
- ✅ reportlab (PDF generation)
- ✅ tabulate (Table formatting)

### Step 2: Configure Database

Make sure your `config.ini` has your Aiven MySQL connection details:

```ini
[database]
host = your-aiven-host.aivencloud.com
port = your-port-number
user = avnadmin
password = your-password
database = defaultdb
```

### Step 3: Run Database Migration

Apply the new database schema:

```bash
python scripts/run_migrations.py
```

This will create:
- ✅ Users and authentication tables
- ✅ Orders and order items tables
- ✅ Enhanced markets and products tables
- ✅ Analytics tables
- ✅ Notifications system
- ✅ Default admin account

### Step 4: Login as Admin

Default credentials (change immediately!):
- **Username**: `admin`
- **Email**: `admin@marketpricetracker.com`
- **Password**: `admin123`

### Step 5: Start Using the System

Run the main application:

```bash
python main.py
```

## 📚 What's New?

### 1. **Three User Roles**

#### 🔑 Super Admin
- Manage all users
- Approve seller registrations
- Full CRUD on all data
- View system-wide analytics
- Generate reports for any market/product

#### 🏪 Sellers/Markets
- Register and await approval
- Create and manage own market
- Add/edit/delete own products
- Update product prices
- View and manage orders
- Export own market analytics

#### 👤 Customers
- Browse products and prices
- Compare prices across markets
- Place orders
- Track order status
- View price trends and analytics
- Export reports for decision-making

### 2. **Order Management**

Customers can:
- Add products to orders
- Specify delivery address and phone
- Add notes for sellers
- Track order status

Sellers can:
- View incoming orders
- Update order status
- Process orders

Order Status Flow:
```
pending → confirmed → processing → ready → completed
```

### 3. **Advanced Analytics**

- 📊 **Price Trends**: See how prices change over time
- 📈 **Market Comparison**: Compare prices across markets
- 📉 **Volatility Analysis**: Find products with biggest price swings
- 🔄 **Seasonal Patterns**: Identify seasonal price changes
- 📌 **Market Activity**: Track market activity levels

### 4. **Professional Reports**

Generate:
- 📄 **PDF Reports** with charts and statistics
- 📊 **Excel Files** for data analysis
- 📋 **CSV Exports** for raw data

## 🔐 Security Features

1. **Password Hashing**: bcrypt with salt
2. **Session Management**: 7-day expiring sessions
3. **Role-based Access**: Enforced permissions
4. **Status Management**: active, pending, suspended, deleted

## 📁 New Files Created

```
market_price_tracker/
├── src/
│   ├── auth.py              ← Authentication
│   ├── user_manager.py      ← User management
│   ├── order_manager.py     ← Order processing
│   ├── analytics.py         ← Analytics engine
│   ├── export.py            ← Report generation
│   └── models.py            ← Updated models
├── migrations/
│   └── 001_add_auth_and_orders.sql
├── scripts/
│   └── run_migrations.py
├── NEW_FEATURES.md
└── INSTALLATION.md (this file)
```

## 🧪 Testing the Features

### Test as Super Admin

1. Login with admin credentials
2. Create a seller account
3. Approve the seller
4. View user statistics
5. Generate system-wide reports

### Test as Seller

1. Register a seller account
2. Wait for admin approval (or approve yourself as admin)
3. Create your market
4. Add products to your market
5. Update prices
6. View orders
7. Export market analytics

### Test as Customer

1. Register a customer account
2. Browse available products
3. Compare prices across markets
4. Place an order
5. View order history
6. Export price trend reports

## 🛠️ Troubleshooting

### Migration Fails

**Issue**: Tables already exist
**Solution**: Drop conflicting tables or modify migration script

**Issue**: Permission denied
**Solution**: Ensure database user has CREATE, ALTER, INSERT privileges

### Cannot Login

**Issue**: Invalid credentials
**Solution**: 
- Check if migration created admin account
- Verify user status is 'active'
- Check password (case-sensitive)

### Charts Not Generating

**Issue**: matplotlib not installed
**Solution**: 
```bash
pip install matplotlib numpy
```

### PDF Reports Not Working

**Issue**: reportlab not installed
**Solution**:
```bash
pip install reportlab
```

## 📊 Sample Usage Scenarios

### Scenario 1: New Market Owner

1. Register as seller → Status: pending
2. Admin approves → Status: active
3. Create market profile
4. Add products (Maize, Beans, Rice, etc.)
5. Update daily prices
6. Receive and process customer orders

### Scenario 2: Customer Price Comparison

1. Register as customer
2. Search for "Maize"
3. View prices across all markets
4. See price trend chart (last 30 days)
5. Find cheapest market
6. Place order

### Scenario 3: Admin Oversight

1. Login as admin
2. View user statistics
3. Approve pending sellers
4. Review system-wide analytics
5. Generate market comparison reports
6. Monitor market activity

## 🎯 Next Development Steps

The following features are planned but not yet implemented:

1. **Enhanced UI**: Update ui.py for role-based menus
2. **Notifications**: Real-time notifications for orders
3. **Email Integration**: Email confirmations for orders
4. **SMS Alerts**: Price alerts via SMS
5. **API**: REST API for mobile apps
6. **Payment Integration**: Mobile money integration
7. **Image Upload**: Product images
8. **Reviews**: Customer reviews and ratings

## 📞 Need Help?

1. Read `NEW_FEATURES.md` for detailed feature documentation
2. Check `README.md` for basic usage
3. Review `QUICKSTART.md` for initial setup
4. Examine code comments in source files

## ✅ Checklist

After installation, verify:

- [ ] All dependencies installed
- [ ] Database migration completed
- [ ] Can login as admin
- [ ] Admin password changed
- [ ] Created test seller account
- [ ] Created test customer account
- [ ] Placed a test order
- [ ] Generated a test report

## 🎉 You're Ready!

Start exploring the enhanced Market Price Tracker with authentication, orders, and analytics!
