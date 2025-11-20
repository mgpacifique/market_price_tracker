# 🌾 Local Agricultural Market Price Tracker



> A comprehensive multi-user system for tracking agricultural market prices, managing orders, and generating analytics reports.

## Overview



[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/) :The Local Agricultural Market Price Tracker is a comprehensive Python application designed to help farmers and market participants access fair and reliable market information for agricultural products. The system enables users to track current prices, compare prices across different markets, and analyze price trends over time.

[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)](https://www.mysql.com/)

[![License](https://img.shields.io/badge/License-Educational-green)](LICENSE)

## Features



### Core Functionality



## 📋 Table of Contents1. **View Current Market Prices**

   - Display real-time prices for various agricultural products

- [Overview](#overview)   - Filter by product, market, or category

- [Features](#features)   - View prices across all markets simultaneously

- [Quick Start](#quick-start)

- [Installation](#installation)2. **Enter New Price Data**

- [Usage](#usage)   - Add new price records for products

- [Project Structure](#project-structure)   - Specify product, market, price, and date

- [Documentation](#documentation)   - Track who recorded the data

- [Technology Stack](#technology-stack)

- [Contributing](#contributing)3. **Compare Prices Across Markets**

   - Compare prices of the same product in different markets

---   - Identify the lowest and highest prices

   - Calculate average prices

## 🎯 Overview

4. **View Price Trends**

The Local Agricultural Market Price Tracker is a production-ready Python application that empowers farmers, market sellers, and customers with real-time market information, order management, and comprehensive analytics. Built with enterprise-grade features including authentication, role-based access control, and advanced reporting capabilities.   - Analyze price history over time

   - Identify if prices are increasing, decreasing, or stable

**Perfect for:**   - Calculate percentage changes

- 🌾 Local agricultural markets

- 👨‍🌾 Farmers and sellers5. **Manage Products and Markets**

- 🛒 Customers and buyers   - Add new products and categories

- 📊 Market administrators   - Add new market locations

- 📈 Price analysts   - View all products and markets



---
## Technology Stack



## ✨ Features- **Python 3.x**: Core programming language

- **MySQL**: Database for persistent storage

### 🔐 Authentication & Authorization- **mysql-connector-python**: MySQL database connector

- Secure user registration and login- **tabulate**: For formatted table displays

- Password hashing with bcrypt- **python-dotenv**: Configuration management

- Session management with automatic expiration

- Three user roles: **Super Admin**, **Seller**, **Customer**## Project Structure



### 👥 Multi-User System```

- **Super Admin**: Full system access, user management, approvalsmarket_price_tracker/

- **Seller**: Market/product management, order processing, price updates├── src/

- **Customer**: Browse products, place orders, track deliveries│   ├── __init__.py          # Package initialization

│   ├── database.py          # Database connection and setup

### 🏪 Market & Product Management│   ├── models.py            # Data models (Market, Product, Price)

- Create and manage markets│   ├── price_manager.py     # Business logic for price operations

- Add products with categories and descriptions│   ├── ui.py                # User interface and display formatting

- Real-time price updates│   └── utils.py             # Utility functions

- Price history tracking├── main.py                  # Application entry point

├── config.ini.sample        # Sample configuration file

### 🛒 Complete Order System├── requirements.txt         # Python dependencies

- Shopping cart functionality├── README.md               # This file

- Multi-item orders└── .gitignore              # Git ignore rules

- Order status tracking (pending → confirmed → processing → ready → completed)```

- Delivery management

- Order notifications## Installation



### 📊 Advanced Analytics### Prerequisites

- Price trend analysis

- Market comparison reports- Python 3.7 or higher

- Statistical analysis (min, max, average, volatility)- MySQL Server 5.7 or higher

- Seasonal pattern detection- pip (Python package manager)

- Product popularity tracking

### Step 1: Clone or Download the Project

### 📄 Export & Reporting

- **PDF Reports** with embedded charts```bash

- **Excel exports** with formatted datacd market_price_tracker

- **CSV exports** for raw data```

- Price trend charts

- Market comparison visualizations

### Step 2: Install Python Dependencies



### 🛡️ Robust Error Handling```bash

- Graceful keyboard interrupt (Ctrl+C) handlingpip install -r requirements.txt

- User-friendly error messages```

- Automatic database cleanup

- Session management### Step 3: Set Up MySQL Database



---1. Start your MySQL server

2. Create a database:

## 🚀 Quick Start

```sql

```bashCREATE DATABASE market_price_tracker;

# Clone the repository```

git clone https://github.com/mgpacifique/market_price_tracker.git

cd market_price_tracker3. Create a MySQL user (optional but recommended):



# Create virtual environment```sql

python3 -m venv .venvCREATE USER 'market_user'@'localhost' IDENTIFIED BY 'your_password';

source .venv/bin/activate  # On Windows: .venv\Scripts\activateGRANT ALL PRIVILEGES ON market_price_tracker.* TO 'market_user'@'localhost';

FLUSH PRIVILEGES;

# Install dependencies```

pip install -r requirements.txt

### Step 4: Configure the Application

# Configure database

cp config.ini.sample config.ini1. Copy the sample configuration file:

# Edit config.ini with your database credentials

```bash

# Run migrationscp config.ini.sample config.ini

python scripts/run_migrations.py```



# Start the application2. Edit `config.ini` with your database credentials:

python main_enhanced.py

``````ini

[database]

**Default Login:**host = localhost

- Username: `admin`port = 3306

- Password: `admin123`user = your_mysql_username

password = your_mysql_password

⚠️ **Change the admin password immediately after first login!**database = market_price_tracker



---[application]

default_currency = USD

## 📦 Installationdate_format = %Y-%m-%d

max_records = 1000

### Prerequisites```



- **Python 3.7+**### Step 5: Run the Application

- **MySQL 8.0+** (or Aiven MySQL)

- **pip** (Python package manager)```bash

python main.py

### Step-by-Step Installation```



See **[docs/INSTALLATION.md](docs/INSTALLATION.md)** for detailed installation instructions.The application will:

- Connect to the database

### Quick Setup- Create necessary tables

- Insert sample data (if tables are empty)

1. **Database Setup:**- Display the welcome screen

```sql

CREATE DATABASE market_price_tracker;## Usage Guide

```

### First Time Setup

2. **Configure Application:**

```bashWhen you run the application for the first time:

cp config.ini.sample config.ini1. The system will create all necessary database tables

# Edit config.ini with your credentials2. Sample data will be inserted automatically, including:

```   - 4 markets (Central Market, Kimironko Market, Nyabugogo Market, Remera Market)

   - 10 products (Maize, Beans, Rice, Tomatoes, Potatoes, etc.)

3. **Install Dependencies:**   - Sample price records for demonstration

```bash

pip install -r requirements.txt### Main Menu Options

```

1. **View Current Market Prices**: Browse current prices with various filtering options

4. **Run Migrations:**2. **Enter New Price Data**: Add new price records to the system

```bash3. **Compare Prices Across Markets**: Compare prices for a product across different markets

python scripts/run_migrations.py4. **View Price Trends**: Analyze price history and trends

```5. **Manage Products and Markets**: Add new products or markets

6. **Exit Application**: Close the application safely

5. **Start Application:**

```bash### Example Workflows

python main_enhanced.py

```#### Adding a New Price



---1. Select option 2 from the main menu

2. Choose a product from the list

## 🎓 Usage3. Choose a market from the list

4. Enter the price per unit

### For Super Admins5. Confirm the date (today or specify another date)

- Manage users (approve sellers, suspend accounts)6. Enter your name (optional)

- View system statistics7. Confirm and save

- Access all data (markets, products, orders)

- Generate system-wide reports#### Comparing Prices



### For Sellers1. Select option 3 from the main menu

- Create and manage your market2. Choose a product to compare

- Add products to your inventory3. View prices across all markets where data is available

- Update daily prices4. See which market has the lowest and highest prices

- Process customer orders

- Track market performance#### Viewing Price Trends

- Generate market analytics

1. Select option 4 from the main menu

### For Customers2. Choose a product

- Browse products and compare prices3. Choose a market

- Place orders with shopping cart4. View price history and trend analysis (increased/decreased/stable)

- Track order status

- View price trends## Database Schema

- Export price reports

### Tables

See **[GETTING_STARTED.md](GETTING_STARTED.md)** for detailed usage workflows.

1. **markets**: Stores market information

---   - market_id (Primary Key)

   - market_name

## 📁 Project Structure   - location

   - created_at

```

market_price_tracker/2. **products**: Stores product information

├── main_enhanced.py              # Main application entry point   - product_id (Primary Key)

├── config.ini.sample             # Sample configuration   - product_name

├── requirements.txt              # Python dependencies   - category

├── README.md                     # This file   - unit

├── GETTING_STARTED.md           # User guide   - created_at

│

├── src/                         # Source code3. **prices**: Stores price records

│   ├── __init__.py   - price_id (Primary Key)

│   ├── database.py              # Database connection   - product_id (Foreign Key)

│   ├── models.py                # Data models   - market_id (Foreign Key)

│   ├── auth.py                  # Authentication   - price

│   ├── permissions.py           # Authorization   - date

│   ├── user_manager.py          # User CRUD operations   - recorded_by

│   ├── price_manager.py         # Price management   - created_at

│   ├── order_manager.py         # Order system

│   ├── analytics.py             # Analytics engine## Data Categories

│   ├── export.py                # Report generation

│   ├── ui.py                    # Base UI componentsDefault product categories include:

│   ├── ui_enhanced.py           # Role-based UI- **Grains**: Maize, Beans, Rice

│   └── utils.py                 # Utilities- **Vegetables**: Tomatoes, Potatoes, Onions, Cabbage

│- **Fruits**: Bananas, Avocado

├── migrations/                  # Database migrations- **Livestock**: Goat, Chicken

│   └── 001_add_auth_and_orders.sql

│You can add more categories as needed.

├── scripts/                     # Utility scripts

│   └── run_migrations.py## Troubleshooting

│

├── docs/                        # Documentation### Database Connection Issues

│   ├── INSTALLATION.md          # Installation guide

│   ├── DEVELOPER_GUIDE.md       # API reference**Error**: "Failed to connect to database"

│   ├── NEW_FEATURES.md          # Feature documentation

│   └── KEYBOARD_INTERRUPT_GUIDE.md**Solutions**:

│- Verify MySQL server is running

├── tests/                       # Test files- Check credentials in `config.ini`

│   ├── test_features.py- Ensure the database exists

│   └── demo_interrupt_handling.py- Verify user has proper permissions

│

└── reports/                     # Generated reports (gitignored)### Configuration File Not Found

```

**Error**: "Configuration file 'config.ini' not found"

---

**Solution**:

## 📚 Documentation- Copy `config.ini.sample` to `config.ini`

- Update with your database credentials

| Document | Description |

|----------|-------------|### Import Errors

| [GETTING_STARTED.md](GETTING_STARTED.md) | Quick start guide and user workflows |

| [docs/INSTALLATION.md](docs/INSTALLATION.md) | Detailed installation instructions |**Error**: "ModuleNotFoundError"

| [docs/NEW_FEATURES.md](docs/NEW_FEATURES.md) | Complete feature documentation |

| [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) | API reference for developers |**Solution**:

| [docs/KEYBOARD_INTERRUPT_GUIDE.md](docs/KEYBOARD_INTERRUPT_GUIDE.md) | Error handling documentation |- Install requirements: `pip install -r requirements.txt`

- Ensure you're in the correct directory

---

## Future Enhancements

## 🛠️ Technology Stack

Potential features for future versions:

### Core- Export data to CSV/Excel

- **Python 3.7+** - Programming language- Price alerts and notifications

- **MySQL 8.0** - Database system- Multi-user authentication

- Web-based interface

### Libraries- Mobile application

- **bcrypt 4.1.2** - Password hashing- Data visualization with charts

- **mysql-connector-python 8.2.0** - Database connector- Price predictions using machine learning

- **pandas 2.1.4** - Data analysis- SMS integration for farmers without internet

- **matplotlib 3.8.2** - Chart generation

- **reportlab 4.0.9** - PDF reports## Contributing

- **openpyxl 3.1.2** - Excel exports

- **tabulate 0.9.0** - Table formattingThis project is part of an educational initiative. Contributions are welcome:

1. Fork the repository

---2. Create a feature branch

3. Make your changes

## 🗄️ Database Schema4. Submit a pull request



### Core Tables## License

- `users` - User accounts and authentication

- `user_sessions` - Session managementThis project is created for educational purposes as part of ALU BSE Year 1 coursework.

- `markets` - Market information

- `products` - Product catalog## Support

- `prices` - Price records with history

For issues or questions:

### Order Management- Check the troubleshooting section

- `orders` - Order header information- Review the code comments

- `order_items` - Order line items- Contact the development team

- `notifications` - System notifications

## Acknowledgments

### Analytics

- `price_history_summary` - Aggregated price dataThis project was developed to support agricultural development and promote fair pricing in local markets. Special thanks to farmers and market participants who inspired this solution.



See **[docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** for complete schema documentation.---



---**Version**: 1.0.0  

**Last Updated**: November 19, 2025  

## 🧪 Testing**Authors**: Agricultural Development Team


### Run All Tests
```bash
python tests/test_features.py
```

### Test Keyboard Interrupt Handling
```bash
python tests/demo_interrupt_handling.py
```

### Manual Testing Workflow
See **[GETTING_STARTED.md](GETTING_STARTED.md)** for complete test scenarios.

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

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/test_features.py
```

---

## 📄 License

This project is created for educational purposes as part of ALU BSE coursework.

---

## 🙏 Acknowledgments

- Developed to support agricultural development and fair pricing in local markets
- Special thanks to farmers and market participants who inspired this solution
- Built with ❤️ for the agricultural community

---

## 📞 Support

- 📖 Check the [documentation](docs/)
- 🐛 Report issues via GitHub Issues
- 💬 Contact: Agricultural Development Team

---

## 🎯 Roadmap

### Completed ✅
- Multi-user authentication
- Role-based access control
- Order management system
- Analytics and reporting
- PDF/Excel/CSV exports
- Keyboard interrupt handling

### Future Enhancements 🚀
- Email notifications
- SMS integration
- Payment gateway integration
- REST API for mobile apps
- Product images
- Advanced predictive analytics
- Multi-language support

---

**Version**: 2.0.0  
**Last Updated**: November 20, 2025  
**Status**: Production Ready ✅  
**Authors**: Group Jayz

---

<p align="center">
  Made with 🌾 for local agricultural communities
</p>
