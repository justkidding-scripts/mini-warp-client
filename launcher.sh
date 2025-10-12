#!/bin/bash
# WARP Client Desktop Launcher Script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set environment variables
export WARP_CLIENT_HOME="$SCRIPT_DIR"
export WARP_CLIENT_DATA_DIR="$SCRIPT_DIR/data"
export WARP_CLIENT_CONFIG_DIR="$SCRIPT_DIR/config"

# Create desktop notification function
show_notification() {
    if command -v notify-send >/dev/null 2>&1; then
        notify-send -i "$SCRIPT_DIR/assets/icons/warp_client.png" "WARP Client" "$1"
    fi
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    show_notification "Virtual environment not found. Please run setup.sh first."
    zenity --error --text="Virtual environment not found. Please run setup.sh first." 2>/dev/null || \
    kdialog --error "Virtual environment not found. Please run setup.sh first." 2>/dev/null || \
    echo "ERROR: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check dependencies
python -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    show_notification "GUI dependencies missing. Launching CLI mode..."
    # Launch CLI mode if GUI not available
    python quick_start.py cli
else
    # Launch GUI mode
    show_notification "Starting WARP Client..."
    python quick_start.py gui
fi

# Show completion notification
show_notification "WARP Client session ended"
