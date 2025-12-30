#!/bin/bash
# Setup script for gov-za-multilingual project
# Run this script to set up your development environment

set -e  # Exit on error

echo "========================================="
echo "Gov-ZA Multilingual Setup Script"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Detected Python $PYTHON_VERSION"

if [ "$PYTHON_VERSION" != "3.8" ]; then
    echo "⚠️  WARNING: Python 3.8 is recommended for sentence alignment (fairseq compatibility)"
    echo "   Current version: $PYTHON_VERSION"
    echo "   Scraping will work, but sentence alignment may fail with other versions"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Please install Python 3.8 (e.g., using pyenv)"
        exit 1
    fi
fi

# Check for Ubuntu (required for sentence alignment)
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$ID" == "ubuntu" ]]; then
        echo "✓ Ubuntu detected: $PRETTY_NAME"
        if [[ "$VERSION_ID" == "22.04" ]]; then
            echo "⚠️  WARNING: Ubuntu 22.04 has known issues with Python 3.8"
            echo "   Ubuntu 20.04 is recommended"
        fi
    else
        echo "⚠️  WARNING: This is not Ubuntu. Sentence alignment requires Ubuntu 20.04"
    fi
fi
echo ""

# Install system dependencies (Ubuntu only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing system dependencies..."
    if command -v apt-get &> /dev/null; then
        echo "This will run: sudo apt-get install build-essential cmake zip"
        read -p "Install system dependencies? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo apt-get update
            sudo apt-get install -y build-essential cmake zip
            echo "✓ System dependencies installed"
        fi
    fi
else
    echo "⚠️  Skipping system dependencies (not on Linux)"
fi
echo ""

# Upgrade pip to the correct version
echo "Setting up pip..."
python3 -m pip install --upgrade pip==24.0
echo "✓ pip 24.0 installed (required for fairseq)"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt
echo "✓ Core dependencies installed"
echo ""

# Install development dependencies
read -p "Install development dependencies? (includes linting, testing tools) (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 -m pip install -r requirements-dev.txt
    echo "✓ Development dependencies installed"

    # Setup pre-commit hooks
    read -p "Setup pre-commit hooks? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pre-commit install
        echo "✓ Pre-commit hooks installed"
    fi
fi
echo ""

# Fix line endings in LASER scripts
if [ -d "src/sentence_alignment/LASER" ]; then
    echo "Fixing line endings in LASER shell scripts..."
    find src/sentence_alignment/LASER -name "*.sh" -type f -exec sed -i 's/\r$//' {} \; 2>/dev/null || \
    find src/sentence_alignment/LASER -name "*.sh" -type f -exec sed -i '' 's/\r$//' {} \;
    echo "✓ Line endings fixed (CRLF → LF)"
else
    echo "⚠️  LASER directory not found - will be downloaded on first alignment run"
fi
echo ""

# Test environment
echo "Testing environment..."
python3 test_environment.py
echo ""

echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Run scraper:         make scrape"
echo "  2. Run alignment:       make align"
echo "  3. View all commands:   make help"
echo ""
echo "Note: First run of sentence alignment will download LASER models (~1GB)"
echo ""
