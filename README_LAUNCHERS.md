# WARP Terminal Universal Cross-Platform Launchers

This document describes the comprehensive launcher system for WARP Terminal that provides seamless cross-platform support for Windows, Linux, and macOS.

## Quick Start

### Windows Users
```batch
# Double-click or run from command prompt:
warp_launcher.bat

# Or use PowerShell:
.\warp_launcher.ps1

# With specific commands:
warp_launcher.bat gui
.\warp_launcher.ps1 setup
```

### Linux/macOS Users
```bash
# Make executable and run:
chmod +x warp_launcher.sh
./warp_launcher.sh

# Or use Python directly:
python3 warp_launcher.py

# With specific commands:
./warp_launcher.sh gui
python3 warp_launcher.py setup
```

## Launcher Files Overview

| Launcher File | Platform | Description |
|---------------|----------|-------------|
| `warp_launcher.py` | All | Universal Python launcher with platform detection |
| `warp_launcher.bat` | Windows | Batch file for Windows Command Prompt |
| `warp_launcher.ps1` | All | PowerShell script for Windows/Linux/macOS |
| `warp_launcher.sh` | Linux/macOS | Bash script with colored output |

## Available Commands

All launchers support the same commands:

| Command | Description |
|---------|-------------|
| `gui` | Launch GUI interface (default) |
| `cli` | Launch CLI interface |
| `setup` | Complete system setup |
| `status` | Show system status dashboard |
| `config` | Interactive configuration |
| `backup` | Create system backup |
| `install` | Install dependencies only |
| `help` | Show help information |

## ️ Platform-Specific Features

### Windows Features
- **Registry Integration**: Creates Windows registry entries for file associations
- **Batch Launcher**: Native Windows .bat file for Command Prompt users
- **PowerShell Support**: Full PowerShell integration with parameter validation
- **Auto-Detection**: Automatically finds Python installation (python, py, python3)

### Linux Features
- **Desktop Integration**: Creates .desktop files for application menu
- **GUI Detection**: Automatically detects X11/Wayland environments
- **Package Manager Support**: Detects apt, yum, pacman for system dependencies
- **Colored Output**: Beautiful colored terminal output with status indicators

### macOS Features
- **App Bundle Creation**: Creates proper .app bundle structure
- **Homebrew Integration**: Detects and uses Homebrew when available
- **Cocoa Framework**: Installs macOS-specific Python packages

## Setup and Installation

### Automatic Setup
```bash
# Complete setup for your platform
python3 warp_launcher.py setup

# Or use platform-specific launcher
./warp_launcher.sh setup # Linux/macOS
warp_launcher.bat setup # Windows
.\warp_launcher.ps1 setup # PowerShell
```

The setup process will:
1. Detect your platform and Python installation
2. Install required dependencies (PyQt5, zstandard, etc.)
3. ️ Set up desktop integration
4. Create backup directories
5. ️ Configure system preferences

### Manual Installation

If you prefer manual setup:

```bash
# Install Python dependencies
pip install PyQt5 zstandard requests psutil cryptography

# Platform-specific packages
# Windows:
pip install pywin32 wmi

# macOS:
pip install pyobjc-framework-Cocoa

# Linux: (system packages)
sudo apt install python3-pyqt5 git
```

## ️ Configuration

### Interactive Configuration
```bash
python3 warp_launcher.py config
```

Configuration options:
- **Auto-install dependencies**: Automatically install missing packages
- **Desktop integration**: Create menu entries and file associations
- **Backup before launch**: Create backup before starting GUI
- **Discord webhook**: Set webhook URL for notifications
- **Preferred terminal**: Set default terminal application

### Configuration File
Settings are stored in `launcher_config.json`:
```json
{
 "auto_install_deps": true,
 "desktop_integration": true,
 "backup_before_launch": false,
 "github_integration": false,
 "discord_webhook": "",
 "preferred_terminal": "auto"
}
```

## System Status Dashboard

View comprehensive system information:
```bash
python3 warp_launcher.py status
```

The status dashboard shows:
- ️ Platform and architecture
- Python version and location
- ️ GUI environment availability
- Package manager detected
- Component status (GUI, CLI, backup system)
- Dependency check results

## Backup System Integration

All launchers integrate with the WARP backup system:

```bash
# Create backup before launching
python3 warp_launcher.py backup

# Auto-backup configuration
python3 warp_launcher.py config
# Then enable "backup_before_launch"
```

## Troubleshooting

### Common Issues

**Python Not Found**
- Windows: Install Python from python.org, ensure "Add to PATH" is checked
- Linux: `sudo apt install python3 python3-pip`
- macOS: Install Python via Homebrew or python.org

**GUI Not Available**
- Linux: Ensure X11 or Wayland is running, check `$DISPLAY` variable
- All platforms: Launcher will automatically fall back to CLI mode

**Permission Denied**
- Linux/macOS: Make launchers executable with `chmod +x warp_launcher.sh`
- Windows: Run as Administrator if needed for system-wide installation

**Dependencies Missing**
- Run: `python3 warp_launcher.py install`
- Or use setup: `python3 warp_launcher.py setup`

### Debug Mode
Enable verbose output by setting environment variable:
```bash
export WARP_DEBUG=1
python3 warp_launcher.py gui
```

## Customization

### Custom Icons
Place custom icons in the `assets/` directory:
- `warp-icon.png` - Main application icon
- `warp-icon.ico` - Windows icon format

### Custom Commands
Extend the launcher by modifying the `available_commands` dictionary in `warp_launcher.py`.

### Platform-Specific Customization
Each launcher detects the platform and adapts behavior:
- Windows: Uses Windows-specific paths and registry
- Linux: Respects XDG directories and desktop standards
- macOS: Creates proper .app bundles and uses macOS conventions

## Integration with WARP Ecosystem

The launchers seamlessly integrate with:
- **Mini WARP Client**: Primary GUI/CLI application
- **WARP Data Manager**: Backup and restore functionality
- **GitHub Integration**: Automatic repository sync
- **Discord Notifications**: Status updates via webhook
- **Desktop Environment**: Native platform integration

## Advanced Usage

### Batch Operations
```bash
# Setup multiple machines
for host in server1 server2 server3; do
 scp warp_launcher.py $hosttmp/
 ssh $host "cd /tmp && python3 warp_launcher.py setup"
done
```

### Scripted Deployment
```bash
#!/bin/bash
# Deploy WARP Terminal across your infrastructure
python3 warp_launcher.py setup --silent --config-file production.json
python3 warp_launcher.py backup --schedule daily --time 03:00
```

### CI/CD Integration
```yaml
# .github/workflows/deploy.yml
- name: Deploy WARP Terminal
 run: |
 python3 warp_launcher.py setup --ci-mode
 python3 warp_launcher.py status --json > warp_status.json
```

## What's Next?

The universal launcher system provides:
 **Cross-platform compatibility** - Works on Windows, Linux, macOS
 **Automatic detection** - Finds Python, GUI, dependencies automatically
 **Desktop integration** - Native platform integration
 **Backup integration** - Seamless backup and restore
 **Configuration management** - Easy setup and customization
 **Status monitoring** - Comprehensive system health checks

Your WARP Terminal is now ready for professional deployment across any platform!
