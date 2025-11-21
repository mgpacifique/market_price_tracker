# 🚀 Quick Start Guide for Teammates

## For First Time Setup (New Users)

If this is your first time running the application:

### Option 1: One Command Setup & Run (Recommended)
```bash
bash start.sh
```
This will:
- Check Python installation
- Create virtual environment
- Install all dependencies
- Create config.ini
- Run migrations
- Start the application

### Option 2: Step by Step

```bash
# 1. Run setup
bash setup.sh

# 2. Edit config.ini with your database credentials
nano config.ini

# 3. Run the application
bash run.sh
```

---

## For Regular Use (After Initial Setup)

Once setup is complete, just run:
```bash
bash run.sh
```

or simply:
```bash
./run.sh
```

---

## Available Scripts

### 🔧 `setup.sh` - First Time Setup
Complete setup including virtual environment, dependencies, and configuration.
```bash
bash setup.sh
```

### ▶️  `run.sh` - Run Application
Start the application (after setup).
```bash
bash run.sh              # Start app
bash run.sh --migrate    # Run database migrations
bash run.sh --test       # Run test suite
bash run.sh --help       # Show help
```

### 🚀 `start.sh` - Quick Start
Setup + Run in one command.
```bash
bash start.sh
```

---

## Default Login Credentials

```
Username: admin
Password: admin123
```

⚠️ **IMPORTANT:** Change the admin password after first login!

---

## Prerequisites

Before running the scripts, make sure you have:

1. **Python 3.7+** installed
   ```bash
   python3 --version
   ```

2. **pip3** installed
   ```bash
   pip3 --version
   ```

3. **MySQL database** accessible (or Aiven MySQL)
   - Database name: `market_price_tracker`
   - User with proper permissions

---

## Database Configuration

The setup script will create `config.ini` from the template. Edit it with your database credentials:

```ini
[database]
host = your_database_host
port = 3306
user = your_database_user
password = your_database_password
database = market_price_tracker
```

For Aiven MySQL, it looks like:
```ini
[database]
host = mysql-xxxxx.aivencloud.com
port = 14702
user = avnadmin
password = your_aiven_password
database = market_price_tracker
```

**⚠️ IMPORTANT: About Database Migrations**

Since you're using **Aiven** (cloud-hosted shared database):
- **Migrations only need to run ONCE** - by the first person setting up
- If a teammate already ran migrations, **skip it** when `setup.sh` asks
- The database is shared among all team members
- You'll see "table already exists" errors if trying to migrate an already-set-up database (this is normal and OK!)

**When to run migrations:**
- ✅ First person setting up the project
- ✅ After pulling new database schema changes from git
- ❌ Every time you start the app (not needed!)
- ❌ When a teammate already set up the database

---

## Troubleshooting

### Script Permission Denied
```bash
chmod +x setup.sh run.sh start.sh
```

### Python Not Found
Install Python 3.7+:
- **Ubuntu/Debian:** `sudo apt install python3 python3-pip`
- **macOS:** `brew install python3`
- **Windows:** Download from https://www.python.org/downloads/

### Virtual Environment Issues
Remove and recreate:
```bash
rm -rf .venv
bash setup.sh
```

### Database Connection Failed
1. Check `config.ini` credentials
2. Verify database exists
3. Test connection:
   ```bash
   mysql -h hostname -u username -p database_name
   ```

### Dependencies Installation Failed
Try manual installation:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

## What Each Script Does

### setup.sh
1. ✓ Checks Python & pip installation
2. ✓ Creates virtual environment (.venv)
3. ✓ Activates virtual environment
4. ✓ Upgrades pip
5. ✓ Installs all dependencies from requirements.txt
6. ✓ Creates config.ini from template
7. ✓ Prompts to edit database credentials
8. ✓ Offers to run database migrations
9. ✓ Creates run.sh script

### run.sh
1. ✓ Checks virtual environment exists
2. ✓ Activates virtual environment
3. ✓ Checks config.ini exists
4. ✓ Runs migrations (if --migrate flag)
5. ✓ Runs tests (if --test flag)
6. ✓ Starts main application
7. ✓ Deactivates virtual environment on exit

### start.sh
1. ✓ Makes scripts executable
2. ✓ Runs setup.sh
3. ✓ Runs application automatically

---

## For Windows Users

If you're on Windows, use:

```bash
# Git Bash (recommended)
bash setup.sh
bash run.sh

# Or PowerShell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main_enhanced.py
```

---

## Testing

Run the test suite:
```bash
bash run.sh --test
```

Or manually:
```bash
source .venv/bin/activate
python tests/test_features.py
```

---

## Common Workflows

### First Day Setup
```bash
git clone https://github.com/mgpacifique/market_price_tracker.git
cd market_price_tracker
bash start.sh
```

### Daily Use
```bash
cd market_price_tracker
bash run.sh
```

### After Database Changes
```bash
bash run.sh --migrate
```

### Before Committing Code
```bash
bash run.sh --test
```

---

## Need Help?

1. Check [GETTING_STARTED.md](GETTING_STARTED.md) for detailed usage
2. Read [docs/INSTALLATION.md](docs/INSTALLATION.md) for manual setup
3. See [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) for development
4. Contact team lead or check project issues

---

## Summary

**Absolute Beginner?** → Use `bash start.sh`  
**Already Setup?** → Use `bash run.sh`  
**Need Migrations?** → Use `bash run.sh --migrate`  
**Want to Test?** → Use `bash run.sh --test`  

That's it! 🎉

---

*Last Updated: November 21, 2025*
