# Quick Start Guide

## Get Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Create `config.ini` from the sample:

```bash
cp config.ini.sample config.ini
```

Edit `config.ini`:

```ini
[database]
host = mysql-c06c293-ovouzzy-55f3.e.aivencloud.com
port = 14702
user = avnadmin
password = AVNS_Bs1LAdrI_IH5eCB3aDX
database = market_price_tracker
```

### 3. Create Database

Open MySQL and run:

```sql
CREATE DATABASE market_price_tracker;
```

### 4. Run the Application

```bash
python main.py
```

That's it! The application will:
- Create all necessary tables
- Insert sample data
- Open the main menu

## Sample Data Included

The application comes with sample data:
- 4 markets in Kigali
- 10 products (grains, vegetables, fruits, livestock)
- Price records for demonstration

## First Steps

Try these actions:
1. View current prices (Option 1)
2. Compare maize prices across markets (Option 3)
3. View price trends for tomatoes (Option 4)
4. Add a new price record (Option 2)

## Need Help?

Check the full README.md for detailed documentation.
