# WARP Terminal Manager

A simple and intuitive desktop application for managing WARP Terminal sessions and configurations.

## Features

### Core Functionality
- **WARP GUI/CLI Launcher**: Easy access to both WARP Terminal GUI and CLI modes
- **Configuration Management**: Edit, validate, backup, and restore WARP configurations
- **Session Monitoring**: Track active WARP sessions and processes
- **Activity Logging**: Comprehensive logging of all manager activities

### User Interface
- **Modern Dark Theme**: Professional dark theme optimized for developer workflows
- **Tabbed Interface**: Organized tabs for Dashboard, Terminal, Configuration, and Logs
- **System Information**: Real-time system resource monitoring
- **Desktop Integration**: Native desktop application with menu and icon support

### Management Features
- Configuration backup and restore
- JSON configuration editor with validation
- Log viewer and export functionality
- Process management for active sessions
- Update checking capabilities

## Installation

### Quick Install
```bash
cd /home/nike/mini-warp-client
./install_desktop.sh
```

### Manual Setup
1. Ensure Python 3.6+ is installed
2. Install PyQt5: `pip install PyQt5`
3. Install psutil (optional): `pip install psutil`
4. Make scripts executable: `chmod +x launcher.sh install_desktop.sh`
5. Run desktop integration: `./install_desktop.sh`

## Usage

### Launch Options

#### Desktop Integration
- Click the WARP Terminal Manager icon on your desktop
- Access from Applications menu under Development category
- Use the desktop launcher shortcut

#### Command Line
```bash
# Launch the manager GUI
python warp_suite_manager.py

# Quick WARP Terminal access
warp-client gui    # Launch WARP GUI mode
warp-client cli    # Launch WARP CLI mode
```

### Interface Guide

#### Dashboard Tab
- System status overview
- WARP Terminal status
- Configuration status
- Recent activity feed
- Session counters

#### Terminal Tab  
- Information about WARP Terminal usage
- Command reference
- System ready status

#### Configuration Tab
- JSON configuration editor
- Save/Load/Validate configurations
- Backup and restore functionality
- Syntax highlighting and validation

#### Logs Tab
- Application log viewer
- Export logs to file
- Clear log functionality
- Real-time activity monitoring

### Configuration Management

The manager provides full configuration control:

1. **Edit Configuration**: Use the built-in JSON editor with syntax validation
2. **Backup Configuration**: Create snapshots of your current settings
3. **Restore Configuration**: Rollback to previous configurations
4. **Validate Configuration**: Check JSON syntax and structure

### Process Management

Monitor and control WARP sessions:
- View active WARP processes
- Terminate sessions if needed
- Track process IDs and resource usage
- Session activity logging

## File Structure

```
mini-warp-client/
├── warp_suite_manager.py      # Main application
├── launcher.sh                # Desktop launcher script
├── launch_warp.py            # WARP client launcher
├── src/                      # Core application code
├── config/                   # Configuration files
├── assets/                   # Icons and resources
└── utils/                    # Utility scripts
```

## Requirements

### System Requirements
- Linux (Debian/Ubuntu tested)
- Python 3.6 or higher
- PyQt5 for GUI functionality
- psutil for system monitoring (optional)

### WARP Terminal
This manager is designed to work with WARP Terminal installations. Ensure WARP Terminal is properly configured on your system.

## Troubleshooting

### Common Issues

**Manager won't start**
- Check Python installation: `python3 --version`
- Install PyQt5: `pip install PyQt5`
- Check file permissions: `chmod +x launcher.sh`

**WARP GUI/CLI launch fails**
- Verify WARP Terminal installation
- Check configuration file syntax
- Review activity logs in the manager

**Desktop integration missing**
- Run install script: `./install_desktop.sh`
- Update desktop database: `update-desktop-database ~/.local/share/applications`
- Refresh desktop environment

### Log Files

Application logs are available in:
- Activity log (in-app)
- System logs via the Logs tab
- Exported log files (user-specified location)

## Development

### Contributing
1. Fork the repository
2. Create feature branches
3. Submit pull requests
4. Follow existing code style

### Architecture
- PyQt5-based GUI application
- Modular configuration system
- Process management integration
- Desktop environment compliance

## License

This project is open source. See the LICENSE file for details.

## Version History

- **v1.0.0**: Initial release with core WARP Terminal management features
  - WARP GUI/CLI launcher
  - Configuration management
  - Session monitoring
  - Desktop integration
