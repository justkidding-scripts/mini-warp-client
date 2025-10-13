# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is the **WARP Data Manager** - a professional backup and management solution for WARP Terminal data with GitHub sync capabilities. It provides both GUI and CLI interfaces for managing WARP Terminal configurations, MCP servers, databases, and other critical data.

The project includes:
- **Basic Manager** (`warp-manager.py`) - Core backup/restore with GUI
- **Enhanced Manager** (`warp-manager-enhanced.py`) - GitHub sync, automation, and scheduling
- **Suite Manager** (`warp_suite_manager.py`) - PyQt5 desktop application for WARP Terminal management
- **WARP Client** (`src/warp_client.py`) - Core client implementation with WebSocket support

## Common Development Commands

### Setup and Installation

```bash
# Quick deployment (recommended for first-time setup)
./deploy-fast.sh

# Basic installation (creates virtual environment and desktop integration)
./install.sh

# Enhanced installation (includes GitHub sync and automation)
./install-enhanced.sh

# Desktop integration (PyQt5 GUI application)
./install_desktop.sh
```

### Running the Applications

```bash
# Basic backup manager (CLI/GUI)
./warp-manager.py --help
./warp-manager.py  # Launches GUI

# Enhanced manager with GitHub sync
./warp-manager-enhanced.py --help
./warp-manager-enhanced.py --snapshot
./warp-manager-enhanced.py --backup rules mcp

# Desktop suite manager (PyQt5)
python warp_suite_manager.py

# Quick launcher
python quick_start.py
```

### Common Backup Operations

```bash
# Take complete snapshot
./warp-manager-enhanced.py --snapshot

# Selective backups
./warp-manager-enhanced.py --backup rules
./warp-manager-enhanced.py --backup mcp database preferences

# List backups
./warp-manager-enhanced.py --list
./warp-manager-enhanced.py --list-remote

# GitHub operations
./warp-manager-enhanced.py --setup-github
./warp-manager-enhanced.py --sync-all
./warp-manager-enhanced.py --upload
```

### Testing and Development

```bash
# Run dependency checks
python -c "import zstandard, keyring, gi; print('All dependencies OK')"

# Test GUI components (requires PyQt5)
python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 OK')"

# Validate configuration
python -c "import json; print(json.load(open('config/default_config.json')))"
```

## Architecture Overview

### Core Components

1. **WARPManagerEnhanced** (`warp-manager-enhanced.py`)
   - GitHub integration with private repo sync
   - Automated scheduling (daily/weekly)
   - Enhanced backup manifests with SHA256 verification
   - Zstandard compression for efficient storage

2. **WARPClient** (`src/warp_client.py`) 
   - WebSocket client for real-time WARP communication
   - Token management with encryption support
   - Modular plugin system
   - Request metrics and monitoring

3. **WarpSuiteManager** (`warp_suite_manager.py`)
   - PyQt5-based desktop application
   - Tabbed interface (Dashboard, Terminal, Configuration, Logs)
   - Process monitoring and management
   - Real-time configuration editing

4. **Configuration Manager** (`src/config_manager.py`)
   - Centralized configuration handling
   - Environment-specific settings
   - Secure credential storage

### Data Flow Architecture

```
WARP Terminal Data → Backup Manager → Compression (Zstandard) → Local Storage → GitHub Sync
     ↓                    ↓                     ↓                    ↓              ↓
  Rules/MCP/DB      File Collection     Archive Creation      ~/.warp-backups   Private Repo
```

### File Locations by OS

- **Linux**: `~/.config/warp-terminal/`, `~/.local/state/warp-terminal/`
- **macOS**: `~/Library/Application Support/warp-terminal/`
- **Windows**: `%APPDATA%/warp-terminal/`

Backups stored in: `~/.warp-backups/`

## Development Patterns

### Error Handling
- All backup operations create safety backups before modifications
- Comprehensive exception handling with detailed error messages
- Graceful degradation when optional dependencies unavailable

### Configuration Management
- JSON-based configuration with validation
- Environment variable support
- Hot-reload capabilities in GUI applications

### Security Practices
- Encrypted token storage using keyring library
- Private GitHub repositories for backups
- File permission restrictions (600) for sensitive files
- SSL/TLS verification enabled by default

### Backup Naming Convention
```
YYYY-MM-DDTHHMMSSZ-{version}-{profile}-{scope}.tar.zst
2025-10-07T143022Z-1.2.0-default-snapshot.tar.zst
```

## Key Dependencies

- **zstandard**: Fast compression for backup archives
- **keyring**: Secure credential storage (optional but recommended)
- **PyGObject/GTK3**: For basic GUI components
- **PyQt5**: For advanced desktop application
- **requests**: HTTP client for GitHub API
- **websocket-client**: Real-time WARP communication

## Integration Points

### GitHub Integration
- Automatic private repository creation
- Secure token storage
- Batch upload/download operations
- Remote backup listing and management

### WARP Terminal Integration
- Automatic path detection for all supported platforms
- Real-time WebSocket communication
- Token-based authentication
- Session management and persistence

### Desktop Environment Integration
- .desktop files for application launchers
- MIME type associations for .warp files
- System tray integration (where supported)
- Menu categories and icon themes

## Monitoring and Logging

### Backup Verification
- SHA256 checksums for all files
- Manifest generation with metadata
- Integrity verification on restore
- Automated backup testing

### Performance Monitoring  
- Request metrics (success rate, response times)
- Bandwidth usage tracking
- Process monitoring for active sessions
- System resource utilization

## Troubleshooting Common Issues

### Missing Dependencies
```bash
# Install system dependencies (Debian/Ubuntu)
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Install Python dependencies
pip install zstandard keyring requests
```

### GUI Issues
- Ensure PyQt5 installed for suite manager
- Check GTK3 bindings for basic GUI
- Verify display environment variables set

### GitHub Sync Issues
- Verify token permissions (repo access required)
- Check network connectivity and proxy settings
- Ensure private repository creation rights

### Backup Failures
- Check disk space availability
- Verify WARP Terminal data paths exist
- Ensure write permissions to backup directory

## Development Notes

- Use virtual environments for isolation
- Follow semantic versioning for releases
- Test on multiple platforms before commits
- Document API changes in configuration schema
- Maintain backwards compatibility for backup formats

## Automation Features

### Persistent Monitor
- Automatic backup detection when WARP terminals running
- 30-minute interval scheduling
- GitHub sync with failure recovery
- Systemd service integration

### Traditional Scheduling
- Cron-like daily/weekly scheduling
- Background daemon support
- Email notification capabilities
- Custom time configuration

This WARP Data Manager provides enterprise-grade backup and management for WARP Terminal installations with professional automation and GitHub integration capabilities.