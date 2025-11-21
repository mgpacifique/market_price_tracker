#!/bin/bash
# Quick start script for Market Price Tracker
# This script performs a complete setup and runs the application

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          Market Price Tracker - Quick Start                          ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Make scripts executable
chmod +x setup.sh run.sh

# Run setup
echo -e "${GREEN}${BOLD}Running setup...${NC}"
echo ""
bash setup.sh

# Check if setup was successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}${BOLD}Setup completed! Starting application...${NC}"
    echo ""
    sleep 2
    
    # Run the application
    bash run.sh
else
    echo ""
    echo -e "${RED}Setup failed. Please check the errors above.${NC}"
    exit 1
fi
