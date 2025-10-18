#!/bin/bash
# Deep Decoder - Installation Script for Linux/Mac
# Run this script from the project directory: bash install.sh

echo "========================================"
echo "Deep Decoder - Quick Installation"
echo "========================================"
echo ""

# Check Python
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✓ Found: $PYTHON_VERSION"
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "✗ Python not found! Please install Python 3.7+ first."
    exit 1
fi

echo ""

# Ask user if they want to create virtual environment
read -p "Create virtual environment? (Recommended) [Y/n]: " CREATE_VENV
if [[ ! "$CREATE_VENV" =~ ^[Nn]$ ]]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "✓ Virtual environment created and activated"
    echo ""
    
    # Update pip in venv
    pip install --upgrade pip
fi

# Install package
echo "Installing deep-decoder package..."
pip install -e .

if [ $? -eq 0 ]; then
    echo "✓ Package installed successfully!"
else
    echo "✗ Installation failed!"
    exit 1
fi

echo ""

# Ask to install dev dependencies
read -p "Install development dependencies? [y/N]: " INSTALL_DEV
if [[ "$INSTALL_DEV" =~ ^[Yy]$ ]]; then
    echo "Installing dev dependencies..."
    pip install -e ".[dev]"
    echo "✓ Dev dependencies installed"
    echo ""
fi

# Run tests
echo "Running tests..."
python examples/test_package.py

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ Installation Complete!"
    echo "========================================"
    echo ""
    echo "Quick Start:"
    echo "  from deep_decoder import quick_decode"
    echo '  result = quick_decode("SGVsbG8gV29ybGQh")'
    echo '  print(result)  # Hello World!'
    echo ""
    echo "Examples:"
    echo "  python examples/basic_usage.py"
    echo "  python examples/advanced_usage.py"
    echo ""
    echo "Documentation:"
    echo "  README.md - Full documentation"
    echo "  QUICKSTART.md - Quick start guide"
    echo "  INSTALL.md - Installation guide"
else
    echo ""
    echo "✗ Some tests failed. Please check the output above."
fi

echo ""
