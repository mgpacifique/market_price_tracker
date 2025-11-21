#!/bin/bash
# Run script for Market Price Tracker
# This script activates the virtual environment and runs the application

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}✗ Virtual environment not found!${NC}"
    echo ""
    echo "Please run setup first:"
    echo -e "  ${BOLD}bash setup.sh${NC}"
    echo ""
    exit 1
fi

# Parse command line arguments
MIGRATE=false
TEST=false
HELP=false

for arg in "$@"; do
    case $arg in
        --migrate|-m)
            MIGRATE=true
            shift
            ;;
        --test|-t)
            TEST=true
            shift
            ;;
        --help|-h)
            HELP=true
            shift
            ;;
        *)
            # Unknown option
            ;;
    esac
done

# Show help
if [ "$HELP" = true ]; then
    echo -e "${CYAN}${BOLD}Market Price Tracker - Run Script${NC}"
    echo ""
    echo "Usage: ./run.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  (no options)    Start the application"
    echo "  -m, --migrate   Run database migrations"
    echo "  -t, --test      Run test suite"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run.sh              # Start the app"
    echo "  ./run.sh --migrate    # Run migrations"
    echo "  ./run.sh --test       # Run tests"
    echo ""
    exit 0
fi

# Activate virtual environment
echo -e "${CYAN}Activating virtual environment...${NC}"
source .venv/bin/activate

# Check if config.ini exists
if [ ! -f "config.ini" ]; then
    echo -e "${RED}✗ config.ini not found!${NC}"
    echo ""
    echo "Please copy and configure config.ini:"
    echo -e "  ${BOLD}cp config.ini.sample config.ini${NC}"
    echo "  ${BOLD}nano config.ini${NC}  # Edit with your database credentials"
    echo ""
    exit 1
fi

# Run migrations if requested
if [ "$MIGRATE" = true ]; then
    echo -e "${CYAN}${BOLD}Running database migrations...${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: About Migrations${NC}"
    echo "Since you're using Aiven hosted database:"
    echo "  • This is a shared database among your team"
    echo "  • Migrations only need to run once"
    echo "  • If tables already exist, this will show errors (which is OK)"
    echo ""
    read -p "Continue with migrations? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python scripts/run_migrations.py
        echo ""
        echo -e "${GREEN}If you see 'table already exists' errors, that's normal!${NC}"
        echo -e "${GREEN}It means the database is already set up.${NC}"
    else
        echo "Migrations cancelled."
    fi
    exit 0
fi

# Run tests if requested
if [ "$TEST" = true ]; then
    echo -e "${CYAN}${BOLD}Running test suite...${NC}"
    python tests/test_features.py
    exit 0
fi

# Run the application
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          Starting Market Price Tracker Application...                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Default Login:${NC}"
echo -e "  Username: ${BOLD}admin${NC}"
echo -e "  Password: ${BOLD}admin123${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to exit the application${NC}"
echo ""

# Run the main application
python main_enhanced.py

# Deactivate virtual environment when done
deactivate
