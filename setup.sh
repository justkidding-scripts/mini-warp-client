#!/bin/bash
# Mini WARP Client Setup Script

echo "=== Mini WARP Client Setup ==="
echo

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install requests websocket-client pyqt5 cryptography aiohttp pycryptodome

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies"
    exit 1
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p data logs

# Set permissions
chmod 600 config/*.json 2>/dev/null || true
chmod 600 data/* 2>/dev/null || true
chmod +x launch_warp.py

echo
echo "=== Setup Complete ==="
echo
echo "Usage:"
echo "  ./launch_warp.py gui      - Launch GUI mode"
echo "  ./launch_warp.py cli      - Launch CLI mode"
echo "  ./launch_warp.py daemon   - Launch daemon mode"
echo
echo "Configuration:"
echo "  - Edit config/default_config.json for basic settings"
echo "  - Use GUI Configuration Editor for advanced settings"
echo "  - Add tokens via GUI Token Manager or CLI"
echo
echo "Documentation:"
echo "  - See README.md for detailed usage instructions"
echo "  - Check logs in data/warp_client.log for troubleshooting"
echo
