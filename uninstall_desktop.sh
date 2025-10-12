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
