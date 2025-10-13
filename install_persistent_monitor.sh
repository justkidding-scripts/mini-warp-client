#!/bin/bash
# WARP Persistent Monitor Installation Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITOR_SCRIPT="$SCRIPT_DIR/warp_persistent_monitor.py"
SERVICE_FILE="$SCRIPT_DIR/warp-monitor.service"

echo "🚀 WARP Persistent Monitor Installation"
echo "======================================"

# Check if Python and required modules are available
echo "📋 Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed"
    exit 1
fi

# Install Python dependencies if needed
python3 -c "import psutil" 2>/dev/null || {
    echo "📦 Installing psutil..."
    pip3 install --user psutil || {
        echo "❌ Failed to install psutil. Please install manually:"
        echo "    pip3 install --user psutil"
        exit 1
    }
}

# Make monitor script executable
echo "🔧 Setting up monitor script..."
chmod +x "$MONITOR_SCRIPT"

# Copy to user's local bin if it exists
if [ -d "$HOME/.local/bin" ]; then
    echo "📁 Installing to ~/.local/bin..."
    cp "$MONITOR_SCRIPT" "$HOME/.local/bin/warp-monitor"
    chmod +x "$HOME/.local/bin/warp-monitor"
    MONITOR_PATH="$HOME/.local/bin/warp-monitor"
else
    MONITOR_PATH="$MONITOR_SCRIPT"
fi

# Setup systemd user service
echo "⚙️  Setting up systemd service..."

# Create user systemd directory
mkdir -p "$HOME/.config/systemd/user"

# Update service file with correct paths
sed "s|%h/Desktop/mini-warp-client/warp_persistent_monitor.py|$MONITOR_PATH|g" \
    "$SERVICE_FILE" > "$HOME/.config/systemd/user/warp-monitor.service"

# Reload systemd and enable service
systemctl --user daemon-reload

echo "✅ Installation complete!"
echo ""
echo "📝 Usage:"
echo "  Start monitor:    systemctl --user start warp-monitor"
echo "  Stop monitor:     systemctl --user stop warp-monitor"
echo "  Enable at login:  systemctl --user enable warp-monitor"
echo "  Check status:     systemctl --user status warp-monitor"
echo ""
echo "Or use the script directly:"
echo "  Start:   $MONITOR_PATH start"
echo "  Stop:    $MONITOR_PATH stop"
echo "  Status:  $MONITOR_PATH status"
echo ""

# Check if WARP backup manager is available
if [ -f "$HOME/Desktop/warp-data-manager/warp-data-manager/warp-manager-enhanced.py" ]; then
    echo "✅ WARP backup manager found"
    
    # Check if GitHub is configured
    if [ -f "$HOME/.warp-manager-config.json" ]; then
        echo "✅ GitHub backup configuration found"
        echo ""
        echo "🎉 Ready to start! The monitor will:"
        echo "   • Detect when WARP terminals are running"
        echo "   • Backup your data every 30 minutes"
        echo "   • Upload backups to GitHub automatically"
        echo ""
        echo "Start the monitor now?"
        read -p "Start monitor? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🚀 Starting WARP monitor..."
            systemctl --user start warp-monitor
            sleep 2
            systemctl --user status warp-monitor --no-pager
            echo ""
            echo "✅ Monitor is running! Check status with:"
            echo "   $MONITOR_PATH status"
        fi
    else
        echo "⚠️  GitHub backup not configured"
        echo "   Run: python3 ~/Desktop/warp-data-manager/warp-data-manager/warp-manager-enhanced.py --setup-github"
    fi
else
    echo "⚠️  WARP backup manager not found at expected location"
    echo "   Please ensure warp-manager-enhanced.py is available"
fi

echo ""
echo "📖 For more information, check the log:"
echo "   tail -f ~/.warp-monitor.log"