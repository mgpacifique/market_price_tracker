#!/bin/bash
# Setup script for Market Price Tracker
# This script will set up the entire application environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       Market Price Tracker - Automated Setup Script                 ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print step
print_step() {
    echo -e "${CYAN}${BOLD}▶ $1${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if Python 3 is installed
print_step "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo "Please install Python 3.7 or higher first."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check Python version (must be 3.7+)
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    print_error "Python 3.7 or higher is required!"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if pip is installed
print_step "Step 2: Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed!"
    echo "Please install pip3 first."
    exit 1
fi
print_success "pip3 found"

# Create virtual environment
print_step "Step 3: Creating virtual environment..."
if [ -d ".venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .venv
        python3 -m venv .venv
        print_success "Virtual environment recreated"
    else
        print_success "Using existing virtual environment"
    fi
else
    python3 -m venv .venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_step "Step 4: Activating virtual environment..."
source .venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_step "Step 5: Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install dependencies
print_step "Step 6: Installing dependencies..."
echo "This may take a few minutes..."
if pip install -r requirements.txt > /dev/null 2>&1; then
    print_success "All dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    echo "Try running: pip install -r requirements.txt"
    exit 1
fi

# Check if config.ini exists
print_step "Step 7: Checking configuration..."
if [ ! -f "config.ini" ]; then
    print_warning "config.ini not found"
    echo ""
    echo "Creating config.ini from template..."
    cp config.ini.sample config.ini
    print_success "config.ini created"
    echo ""
    print_warning "IMPORTANT: You need to edit config.ini with your database credentials!"
    echo ""
    echo "Edit the following section in config.ini:"
    echo "  [database]"
    echo "  host = your_database_host"
    echo "  port = your_database_port"
    echo "  user = your_database_user"
    echo "  password = your_database_password"
    echo "  database = market_price_tracker"
    echo ""
    read -p "Press Enter to open config.ini for editing..."
    
    # Try to open with default editor
    if command -v nano &> /dev/null; then
        nano config.ini
    elif command -v vim &> /dev/null; then
        vim config.ini
    elif command -v vi &> /dev/null; then
        vi config.ini
    else
        echo "Please edit config.ini manually with your preferred text editor"
    fi
else
    print_success "config.ini found"
fi

# Ask if user wants to run migrations
echo ""
print_step "Step 8: Database setup..."
echo ""
print_warning "IMPORTANT: About Database Migrations"
echo ""
echo "Since you're using Aiven hosted database (shared with team):"
echo "  • Migrations only need to be run ONCE per database"
echo "  • If a teammate already ran migrations, skip this step"
echo "  • Only run if you're setting up the database for the first time"
echo "  • Or if there are new database schema changes"
echo ""
read -p "Do you want to run database migrations now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Running database migrations..."
    if python scripts/run_migrations.py; then
        print_success "Migrations completed successfully"
    else
        print_error "Migration failed - please check your database configuration"
        echo "If tables already exist, this is normal - you can skip migrations."
        echo "You can run migrations later with: ./run.sh --migrate"
    fi
else
    print_warning "Skipping migrations"
    echo "If the app fails to start, you may need to run: ./run.sh --migrate"
fi

# Create run script if it doesn't exist
if [ ! -f "run.sh" ]; then
    print_step "Creating run script..."
    cat > run.sh << 'RUNSCRIPT'
#!/bin/bash
# Run script for Market Price Tracker
source .venv/bin/activate
python main_enhanced.py
RUNSCRIPT
    chmod +x run.sh
    print_success "Run script created"
fi

# Print completion message
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✅ SETUP COMPLETE! ✅                               ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}Your Market Price Tracker is now ready to use!${NC}"
echo ""
echo -e "${CYAN}To start the application:${NC}"
echo -e "  ${BOLD}./run.sh${NC}  or  ${BOLD}bash run.sh${NC}"
echo ""
echo -e "${CYAN}Default login credentials:${NC}"
echo -e "  Username: ${BOLD}admin${NC}"
echo -e "  Password: ${BOLD}admin123${NC}"
echo ""
echo -e "${YELLOW}⚠️  Remember to change the admin password after first login!${NC}"
echo ""
echo -e "${CYAN}Other useful commands:${NC}"
echo -e "  ${BOLD}./run.sh --migrate${NC}       - Run database migrations (only if needed)"
echo -e "  ${BOLD}./run.sh --test${NC}          - Run test suite"
echo -e "  ${BOLD}deactivate${NC}               - Deactivate virtual environment"
echo ""
echo -e "${YELLOW}Note: Since you're using Aiven (shared database), migrations${NC}"
echo -e "${YELLOW}only need to run once. Skip if a teammate already set it up.${NC}"
echo ""
echo -e "${BOLD}Happy tracking! 🌾${NC}"
echo ""
