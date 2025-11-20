# Local Agricultural Market Price Tracker

## Overview

The Local Agricultural Market Price Tracker is a comprehensive Python application designed to help farmers and market participants access fair and reliable market information for agricultural products. The system enables users to track current prices, compare prices across different markets, and analyze price trends over time.

## Features

### Core Functionality

1. **View Current Market Prices**
   - Display real-time prices for various agricultural products
   - Filter by product, market, or category
   - View prices across all markets simultaneously

2. **Enter New Price Data**
   - Add new price records for products
   - Specify product, market, price, and date
   - Track who recorded the data

3. **Compare Prices Across Markets**
   - Compare prices of the same product in different markets
   - Identify the lowest and highest prices
   - Calculate average prices

4. **View Price Trends**
   - Analyze price history over time
   - Identify if prices are increasing, decreasing, or stable
   - Calculate percentage changes

5. **Manage Products and Markets**
   - Add new products and categories
   - Add new market locations
   - View all products and markets

## Technology Stack

- **Python 3.x**: Core programming language
- **MySQL**: Database for persistent storage
- **mysql-connector-python**: MySQL database connector
- **tabulate**: For formatted table displays
- **python-dotenv**: Configuration management

## Project Structure

```
market_price_tracker/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── database.py          # Database connection and setup
│   ├── models.py            # Data models (Market, Product, Price)
│   ├── price_manager.py     # Business logic for price operations
│   ├── ui.py                # User interface and display formatting
│   └── utils.py             # Utility functions
├── main.py                  # Application entry point
├── config.ini.sample        # Sample configuration file
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## Installation

### Prerequisites

- Python 3.7 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd market_price_tracker
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up MySQL Database

1. Start your MySQL server
2. Create a database:

```sql
CREATE DATABASE market_price_tracker;
```

3. Create a MySQL user (optional but recommended):

```sql
CREATE USER 'market_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON market_price_tracker.* TO 'market_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 4: Configure the Application

1. Copy the sample configuration file:

```bash
cp config.ini.sample config.ini
```

2. Edit `config.ini` with your database credentials:

```ini
[database]
host = localhost
port = 3306
user = your_mysql_username
password = your_mysql_password
database = market_price_tracker

[application]
default_currency = USD
date_format = %Y-%m-%d
max_records = 1000
```

### Step 5: Run the Application

```bash
python main.py
```

The application will:
- Connect to the database
- Create necessary tables
- Insert sample data (if tables are empty)
- Display the welcome screen

## Usage Guide

### First Time Setup

When you run the application for the first time:
1. The system will create all necessary database tables
2. Sample data will be inserted automatically, including:
   - 4 markets (Central Market, Kimironko Market, Nyabugogo Market, Remera Market)
   - 10 products (Maize, Beans, Rice, Tomatoes, Potatoes, etc.)
   - Sample price records for demonstration

### Main Menu Options

1. **View Current Market Prices**: Browse current prices with various filtering options
2. **Enter New Price Data**: Add new price records to the system
3. **Compare Prices Across Markets**: Compare prices for a product across different markets
4. **View Price Trends**: Analyze price history and trends
5. **Manage Products and Markets**: Add new products or markets
6. **Exit Application**: Close the application safely

### Example Workflows

#### Adding a New Price

1. Select option 2 from the main menu
2. Choose a product from the list
3. Choose a market from the list
4. Enter the price per unit
5. Confirm the date (today or specify another date)
6. Enter your name (optional)
7. Confirm and save

#### Comparing Prices

1. Select option 3 from the main menu
2. Choose a product to compare
3. View prices across all markets where data is available
4. See which market has the lowest and highest prices

#### Viewing Price Trends

1. Select option 4 from the main menu
2. Choose a product
3. Choose a market
4. View price history and trend analysis (increased/decreased/stable)

## Database Schema

### Tables

1. **markets**: Stores market information
   - market_id (Primary Key)
   - market_name
   - location
   - created_at

2. **products**: Stores product information
   - product_id (Primary Key)
   - product_name
   - category
   - unit
   - created_at

3. **prices**: Stores price records
   - price_id (Primary Key)
   - product_id (Foreign Key)
   - market_id (Foreign Key)
   - price
   - date
   - recorded_by
   - created_at

## Data Categories

Default product categories include:
- **Grains**: Maize, Beans, Rice
- **Vegetables**: Tomatoes, Potatoes, Onions, Cabbage
- **Fruits**: Bananas, Avocado
- **Livestock**: Goat, Chicken

You can add more categories as needed.

## Troubleshooting

### Database Connection Issues

**Error**: "Failed to connect to database"

**Solutions**:
- Verify MySQL server is running
- Check credentials in `config.ini`
- Ensure the database exists
- Verify user has proper permissions

### Configuration File Not Found

**Error**: "Configuration file 'config.ini' not found"

**Solution**:
- Copy `config.ini.sample` to `config.ini`
- Update with your database credentials

### Import Errors

**Error**: "ModuleNotFoundError"

**Solution**:
- Install requirements: `pip install -r requirements.txt`
- Ensure you're in the correct directory

## Future Enhancements

Potential features for future versions:
- Export data to CSV/Excel
- Price alerts and notifications
- Multi-user authentication
- Web-based interface
- Mobile application
- Data visualization with charts
- Price predictions using machine learning
- SMS integration for farmers without internet

## Contributing

This project is part of an educational initiative. Contributions are welcome:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is created for educational purposes as part of ALU BSE Year 1 coursework.

## Support

For issues or questions:
- Check the troubleshooting section
- Review the code comments
- Contact the development team

## Acknowledgments

This project was developed to support agricultural development and promote fair pricing in local markets. Special thanks to farmers and market participants who inspired this solution.

---

**Version**: 1.0.0  
**Last Updated**: November 19, 2025  
**Authors**: Group Jayz
