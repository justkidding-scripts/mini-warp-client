#!/bin/bash
# WARP Client Desktop Integration Installer

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER_HOME="$HOME"
DESKTOP_FILE="$SCRIPT_DIR/warp-client.desktop"
ICON_FILE="$SCRIPT_DIR/assets/icons/warp_client.png"

echo "🚀 WARP Client Desktop Integration Installer"
echo "============================================="
echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run this script as root (sudo)"
    echo "   Run it as your regular user."
    exit 1
fi

# Verify required files exist
if [ ! -f "$DESKTOP_FILE" ]; then
    echo "❌ Desktop file not found: $DESKTOP_FILE"
    exit 1
fi

if [ ! -f "$ICON_FILE" ]; then
    echo "❌ Icon file not found: $ICON_FILE"
    echo "   Creating icon first..."
    cd "$SCRIPT_DIR" && source venv/bin/activate && python assets/create_icon.py
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p "$USER_HOME/.local/share/applications"
mkdir -p "$USER_HOME/.local/share/icons/hicolor/256x256/apps"
mkdir -p "$USER_HOME/.config/warp-client"

# Copy desktop file
echo "🖥️  Installing desktop entry..."
cp "$DESKTOP_FILE" "$USER_HOME/.local/share/applications/"

# Copy icons in different sizes
echo "🎨 Installing icons..."
for size in 16 24 32 48 64 128 256; do
    icon_dir="$USER_HOME/.local/share/icons/hicolor/${size}x${size}/apps"
    mkdir -p "$icon_dir"
    
    if [ -f "$SCRIPT_DIR/assets/icons/warp_client_${size}.png" ]; then
        cp "$SCRIPT_DIR/assets/icons/warp_client_${size}.png" "$icon_dir/warp-client.png"
    else
        # Use main icon as fallback
        cp "$SCRIPT_DIR/assets/icons/warp_client.png" "$icon_dir/warp-client.png"
    fi
done

# Update desktop database
echo "🔄 Updating desktop database..."
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$USER_HOME/.local/share/applications"
fi

# Update icon cache
echo "🔄 Updating icon cache..."
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -t "$USER_HOME/.local/share/icons/hicolor/" 2>/dev/null || true
fi

# Create desktop shortcuts
echo "🖥️  Creating desktop shortcuts..."

# Desktop shortcut
if [ -d "$USER_HOME/Desktop" ]; then
    cp "$DESKTOP_FILE" "$USER_HOME/Desktop/"
    chmod +x "$USER_HOME/Desktop/warp-client.desktop"
    echo "   ✓ Desktop shortcut created"
fi

# Create menu categories
echo "📋 Setting up application menu..."

# Create custom menu category if needed
MENU_DIR="$USER_HOME/.local/share/desktop-directories"
mkdir -p "$MENU_DIR"

cat > "$MENU_DIR/warp-security.directory" << 'MENU_EOF'
[Desktop Entry]
Name=Security Tools
Name[da]=Sikkerhedsværktøjer
Comment=Security and Penetration Testing Tools
Comment[da]=Sikkerhed og penetrationstest værktøjer
Icon=security-high
Type=Directory
MENU_EOF

# Register MIME types
echo "📄 Registering MIME types..."
MIME_DIR="$USER_HOME/.local/share/mime/packages"
mkdir -p "$MIME_DIR"

cat > "$MIME_DIR/warp-client.xml" << 'MIME_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="application/x-warp-config">
        <comment>WARP Client Configuration</comment>
        <glob pattern="*.warp"/>
        <glob pattern="*.warp-config"/>
    </mime-type>
</mime-info>
MIME_EOF

# Update MIME database
if command -v update-mime-database >/dev/null 2>&1; then
    update-mime-database "$USER_HOME/.local/share/mime"
fi

# Create quick access scripts
echo "🔧 Creating system integration scripts..."

# Command line launcher
cat > "$USER_HOME/.local/bin/warp-client" << 'CLI_EOF'
#!/bin/bash
exec /home/nike/mini-warp-client/launcher.sh "$@"
CLI_EOF

mkdir -p "$USER_HOME/.local/bin"
chmod +x "$USER_HOME/.local/bin/warp-client"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$USER_HOME/.local/bin:"* ]]; then
    echo "🔧 Adding ~/.local/bin to PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$USER_HOME/.bashrc"
    echo "   (You may need to restart your terminal or run: source ~/.bashrc)"
fi

# Create uninstaller
echo "🗑️  Creating uninstaller..."
cat > "$SCRIPT_DIR/uninstall_desktop.sh" << 'UNINSTALL_EOF'
#!/bin/bash
# WARP Client Desktop Integration Uninstaller

USER_HOME="$HOME"

echo "🗑️ Removing WARP Client desktop integration..."

# Remove desktop files
rm -f "$USER_HOME/.local/share/applications/warp-client.desktop"
rm -f "$USER_HOME/Desktop/warp-client.desktop"

# Remove icons
for size in 16 24 32 48 64 128 256; do
    rm -f "$USER_HOME/.local/share/icons/hicolor/${size}x${size}/apps/warp-client.png"
done

# Remove other files
rm -f "$USER_HOME/.local/share/desktop-directories/warp-security.directory"
rm -f "$USER_HOME/.local/share/mime/packages/warp-client.xml"
rm -f "$USER_HOME/.local/bin/warp-client"

# Update databases
update-desktop-database "$USER_HOME/.local/share/applications" 2>/dev/null || true
gtk-update-icon-cache -t "$USER_HOME/.local/share/icons/hicolor/" 2>/dev/null || true
update-mime-database "$USER_HOME/.local/share/mime" 2>/dev/null || true

echo "✅ Desktop integration removed successfully"
echo "   (WARP Client files in this directory are preserved)"
UNINSTALL_EOF

chmod +x "$SCRIPT_DIR/uninstall_desktop.sh"

# Final setup
echo "🔧 Final setup..."

# Make launcher executable
chmod +x "$SCRIPT_DIR/launcher.sh"

# Set correct permissions on desktop file
chmod 644 "$USER_HOME/.local/share/applications/warp-client.desktop"

echo
echo "✅ Installation completed successfully!"
echo
echo "WARP Client is now integrated into your desktop environment:"
echo "  • Application Menu: Look for 'WARP Client' in Network/Security tools"
echo "  • Desktop: Double-click the WARP Client icon on your desktop"
echo "  • Command Line: Run 'warp-client' from anywhere in terminal"
echo "  • File Manager: Right-click .warp files to open with WARP Client"
echo
echo "Quick Start:"
echo "  1. Click the WARP Client icon in your application menu"
echo "  2. Or run: warp-client"
echo "  3. Or double-click the desktop shortcut"
echo
echo "To uninstall desktop integration: ./uninstall_desktop.sh"
echo
echo "🎉 Enjoy your new WARP Client!"

# Test desktop file
echo "🧪 Testing desktop file..."
if command -v desktop-file-validate >/dev/null 2>&1; then
    if desktop-file-validate "$USER_HOME/.local/share/applications/warp-client.desktop"; then
        echo "   ✓ Desktop file is valid"
    else
        echo "   ⚠️ Desktop file validation failed (but may still work)"
    fi
else
    echo "   ℹ️ desktop-file-validate not available (skipping validation)"
fi

echo
echo "Installation log: Check above for any errors or warnings"
echo "Ready to launch WARP Client! 🚀"
