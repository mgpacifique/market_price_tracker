#!/bin/bash

# Market Price Tracker - Complete Launcher
# Handles: environment setup, dependencies, and app launch

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          Market Price Tracker - Smart Launch System                 ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Run the Python launcher that handles everything
python3 launcher.py

# Exit with the same code as the Python launcher
exit $?
