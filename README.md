# 🌾 Local Agricultural Market Price Tracker

> A production-ready multi-user system for tracking agricultural market prices, managing orders, and generating comprehensive analytics reports.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Educational-green)](LICENSE)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Technology Stack](#️-technology-stack)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The Local Agricultural Market Price Tracker is a production-ready Python application that empowers farmers, market sellers, and customers with real-time market information, order management, and comprehensive analytics. Built with enterprise-grade features including authentication, role-based access control, and advanced reporting capabilities.

**Perfect for:**
- 🌾 Local agricultural markets
- 👨‍🌾 Farmers and sellers
- 🛒 Customers and buyers
- 📊 Market administrators
- 📈 Price analysts

---

## ✨ Features

### 🔐 Authentication & Authorization
- Secure user registration and login
- Password hashing with bcrypt
- Session management with automatic expiration
- Three user roles: **Super Admin**, **Seller**, **Customer**

### 👥 Multi-User System
- **Super Admin**: Full system access, user management, approvals
- **Seller**: Market/product management, order processing, price updates
- **Customer**: Browse products, place orders, track deliveries

### 🏪 Market & Product Management
- Create and manage markets
- Add products with categories and descriptions
- Real-time price updates
- Price history tracking

### 🛒 Complete Order System
- Shopping cart functionality
- Multi-item orders
- Order status tracking (pending → confirmed → processing → ready → completed)
- Delivery management
- Order notifications

### 📊 Advanced Analytics
- Price trend analysis
- Market comparison reports
- Statistical analysis (min, max, average, volatility)
- Seasonal pattern detection
- Product popularity tracking

### 📄 Export & Reporting
- **PDF Reports** with embedded charts
- **Excel exports** with formatted data
- **CSV exports** for raw data
- Price trend charts
- Market comparison visualizations

### 🛡️ Robust Error Handling
- Graceful keyboard interrupt (Ctrl+C) handling
- User-friendly error messages
- Automatic database cleanup
- Session management

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/mgpacifique/market_price_tracker.git
cd market_price_tracker

# One-command setup and run
bash start.sh
```

**That's it!** The script will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Configure database
- ✅ Start the application

**Default Login:**
- Username: `admin`
- Password: `admin123`

⚠️ **Change the admin password after first login!**

For detailed setup instructions, see [GETTING_STARTED.md](GETTING_STARTED.md) or [docs/QUICKSTART_SCRIPTS.md](docs/QUICKSTART_SCRIPTS.md).

---

## �� Installation

### Prerequisites
- **Python 3.7+**
- **MySQL 8.0+** (or Aiven MySQL)
- **pip** (Python package manager)

### Option 1: Automated Setup (Recommended)

```bash
# First-time setup
bash start.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
cp config.ini.sample config.ini
nano config.ini  # Edit with your credentials

# Run migrations (only if setting up database for first time)
python scripts/run_migrations.py

# Start application
python main_enhanced.py
```

For complete installation guide, see [docs/INSTALLATION.md](docs/INSTALLATION.md).

---

## 🎓 Usage

### For Super Admins
- Manage users (approve sellers, suspend accounts)
- View system statistics
- Access all data (markets, products, orders)
- Generate system-wide reports

### For Sellers
- Create and manage your market
- Add products to your inventory
- Update daily prices
- Process customer orders
- Track market performance
- Generate market analytics

### For Customers
- Browse products and compare prices
- Place orders with shopping cart
- Track order status
- View price trends
- Export price reports

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed usage workflows.

---

## 📁 Project Structure

```
market_price_tracker/
├── main_enhanced.py              # Main application entry point
├── setup.sh                      # Automated setup script
├── run.sh                        # Daily launcher script
├── start.sh                      # One-command quickstart
├── config.ini.sample             # Sample configuration
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── GETTING_STARTED.md           # User guide
│
├── src/                         # Source code
│   ├── database.py              # Database connection
│   ├── models.py                # Data models
│   ├── auth.py                  # Authentication
│   ├── permissions.py           # Authorization
│   ├── user_manager.py          # User CRUD operations
│   ├── price_manager.py         # Price management
│   ├── order_manager.py         # Order system
│   ├── analytics.py             # Analytics engine
│   ├── export.py                # Report generation
│   ├── ui.py                    # Base UI components
│   ├── ui_enhanced.py           # Role-based UI
│   └── utils.py                 # Utilities
│
├── migrations/                  # Database migrations
│   └── 001_add_auth_and_orders.sql
│
├── scripts/                     # Utility scripts
│   └── run_migrations.py
│
├── docs/                        # Documentation
│   ├── INSTALLATION.md          # Installation guide
│   ├── QUICKSTART_SCRIPTS.md    # Script documentation
│   ├── DEVELOPER_GUIDE.md       # API reference
│   ├── NEW_FEATURES.md          # Feature documentation
│   └── KEYBOARD_INTERRUPT_GUIDE.md
│
├── tests/                       # Test files
│   ├── test_features.py
│   └── demo_interrupt_handling.py
│
└── reports/                     # Generated reports (gitignored)
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Quick start guide and user workflows |
| [docs/QUICKSTART_SCRIPTS.md](docs/QUICKSTART_SCRIPTS.md) | Automated setup scripts guide |
| [docs/INSTALLATION.md](docs/INSTALLATION.md) | Detailed installation instructions |
| [docs/NEW_FEATURES.md](docs/NEW_FEATURES.md) | Complete feature documentation |
| [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) | API reference for developers |
| [docs/KEYBOARD_INTERRUPT_GUIDE.md](docs/KEYBOARD_INTERRUPT_GUIDE.md) | Error handling documentation |

---

## 🛠️ Technology Stack

### Core
- **Python 3.7+** - Programming language
- **MySQL 8.0** - Database system (Aiven cloud-hosted)

### Key Libraries
- **bcrypt 4.1.2** - Password hashing
- **mysql-connector-python 8.2.0** - Database connector
- **pandas 2.1.4** - Data analysis
- **matplotlib 3.8.2** - Chart generation
- **reportlab 4.0.9** - PDF reports
- **openpyxl 3.1.2** - Excel exports
- **tabulate 0.9.0** - Table formatting

---

## 🗄️ Database Schema

### Core Tables
- `users` - User accounts and authentication
- `user_sessions` - Session management
- `markets` - Market information
- `products` - Product catalog
- `prices` - Price records with history

### Order Management
- `orders` - Order header information
- `order_items` - Order line items
- `notifications` - System notifications

### Analytics
- `price_history_summary` - Aggregated price data

See [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) for complete schema documentation.

---

## 🧪 Testing

### Run All Tests
```bash
# Activate virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run test suite
python tests/test_features.py
```

### Test Keyboard Interrupt Handling
```bash
python tests/demo_interrupt_handling.py
```

### Using Run Script
```bash
# Run tests via launcher
./run.sh --test
```

See [GETTING_STARTED.md](GETTING_STARTED.md) for complete test scenarios.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/market_price_tracker.git
cd market_price_tracker

# Quick setup
bash setup.sh

# Or manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
python tests/test_features.py
```

See [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) for development guidelines.

---

## 📄 License

This project is created for educational purposes as part of ALU BSE coursework.

---

## 📞 Support

- 📖 Check the [documentation](docs/)
- 🐛 [Report issues](https://github.com/mgpacifique/market_price_tracker/issues)
- 💬 Contact: Group Jayz

---

## 🎯 Roadmap

### Completed ✅
- ✅ Multi-user authentication with bcrypt
- ✅ Role-based access control (Super Admin, Seller, Customer)
- ✅ Complete order management system
- ✅ Advanced analytics and reporting
- ✅ PDF/Excel/CSV exports
- ✅ Keyboard interrupt handling
- ✅ Automated setup scripts
- ✅ Cloud database integration (Aiven MySQL)

### Future Enhancements 🚀
- 📧 Email notifications
- 📱 SMS integration for farmers
- 💳 Payment gateway integration
- 🌐 REST API for mobile apps
- 🖼️ Product images
- 🤖 Predictive analytics with ML
- 🌍 Multi-language support

---

## 🙏 Acknowledgments

- Developed to support agricultural development and fair pricing in local markets
- Special thanks to farmers and market participants who inspired this solution
- Built with ❤️ for the agricultural community

---

**Version**: 2.0.0  
**Last Updated**: November 21, 2025  
**Status**: Production Ready ✅  
**Authors**: Group Jayz

---

<p align="center">
  <strong>Made with 🌾 for local agricultural communities</strong>
</p>
