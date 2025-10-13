# WARP Terminal Unified Ecosystem

**Complete WARP Terminal Management Solution**

[![Platform](https/img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-blue)](#)
[![Python](https/img.shields.io/badge/Python-3.8%2B-green)](#)
[![GUI](https/img.shields.io/badge/GUI-PyQt5-orange)](#)
[![License](https/img.shields.io/badge/License-MIT-yellow)](#)

> A comprehensive WARP Terminal ecosystem combining advanced client functionality with professional backup & data management. Perfect for cybersecurity research, terminal power users, and development teams.

---

## What's New: Unified Ecosystem

**Two Powerful Tools, One Solution:**

 **Mini WARP Client** - Advanced terminal client with GUI/CLI modes
 **WARP Data Manager** - Professional backup & management with GitHub sync
 **Unified Launcher** - Integrated control center for complete workflow
 **Automated Workflows** - Backup-before-launch, scheduled backups, restore operations

---

## Ultra-Quick Start (30 Seconds)

```bash
# Clone the unified ecosystem
git clone https/github.com/FoundationAgents/mini-warp-client.git
cd mini-warp-client

# Setup everything in one command
python warp_unified_launcher.py setup

# Launch unified dashboard
python warp_unified_launcher.py dashboard
```

**That's it!** Your complete WARP ecosystem is ready.

---

## Available Launch Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `client-gui` | Mini WARP Client GUI | Advanced terminal interface |
| `client-cli` | Mini WARP Client CLI | Command-line terminal client |
| `backup-gui` | WARP Data Manager GUI | Visual backup management |
| `backup-cli` | WARP Data Manager CLI | Automated backup operations |
| `backup-auto` | Auto-backup + Launch Client | Safe workflow with backups |
| `dashboard` | Unified Control Center | System overview and quick actions |
| `setup` | Complete Ecosystem Setup | First-time installation |
| `restore` | Data Recovery Operations | Restore from backups |

---

## Mini WARP Client Features

### Core Functionality
- **GUI & CLI Modes** - Professional PyQt5 interface or command-line
- **WebSocket Integration** - Real-time WARP Terminal communication
- **Token Management** - Encrypted authentication handling
- **Module System** - Extensible plugin architecture
- **Configuration Manager** - Advanced settings with encryption
- **Event System** - Robust callback handling with shutdown protection

### ️ Security & Research Features
- **Command Execution** - Secure subprocess handling
- **File Operations** - Upload/download with integrity verification
- **AI Agent Integration** - Chat interface for WARP AI
- **Session Management** - Multiple connection handling
- **Audit Logging** - Complete activity tracking

### ️ Desktop Integration
- **System Menu** - Native desktop launcher
- **Desktop Icons** - Click-to-launch functionality
- **Process Monitoring** - Live session management
- **Theme Support** - Dark/light mode options

---

## WARP Data Manager Features

### Backup Operations
- **Complete Snapshots** - All WARP data in one backup
- **Component Selection** - Rules, MCP, databases, preferences
- **Automated Scheduling** - Daily/weekly backup automation
- **GitHub Integration** - Cloud sync and version control
- **Integrity Verification** - SHA256 checksums for all data

### Restore & Recovery
- **GUI Restore** - Visual backup browser and recovery
- **Safety Backups** - Auto-backup before any restore
- **Selective Restore** - Choose specific components
- **Quarantine Mode** - Safe data reset without deletion

### ️ Cloud & Automation
- **GitHub Sync** - Private repository backup storage
- **Automated Workflows** - Background scheduling service
- **Cross-Platform** - Linux, macOS, Windows support
- **Proxy Support** - Network proxy configuration

---

## Quick Usage Examples

### Launch Modes
```bash
# Start with automatic backup
python warp_unified_launcher.py backup-auto

# Quick dashboard access
python warp_unified_launcher.py dashboard

# Direct client launch
python warp_unified_launcher.py client-gui

# Backup management
python warp_unified_launcher.py backup-cli
```

### Backup Operations
```bash
# Create complete snapshot
./warp-manager-enhanced.py --snapshot

# Backup specific components
./warp-manager-enhanced.py --backup rules mcp database

# Upload to GitHub
./warp-manager-enhanced.py --snapshot --upload

# Schedule daily backups
./warp-manager-enhanced.py --schedule daily --schedule-time 02:00
```

### Client Operations
```bash
# CLI interactive mode
python launch_warp.py cli

# GUI manager
python warp_suite_manager.py

# Direct commands
echo "status" | python launch_warp.py cli
```

---

## Installation Options

### Option 1: Complete Ecosystem (Recommended)
```bash
git clone https/github.com/FoundationAgents/mini-warp-client.git
cd mini-warp-client
python warp_unified_launcher.py setup
```

### Option 2: Client Only
```bash
python warp_suite_manager.py # GUI mode
python launch_warp.py cli # CLI mode
```

### Option 3: Data Manager Only
```bash
./deploy-fast.sh # Quick setup
./warp-manager.py # GUI mode
./warp-manager-enhanced.py # Enhanced CLI
```

### Option 4: Desktop Integration
```bash
./install_desktop.sh # Install desktop launcher
```

---

## System Architecture

```
 WARP Terminal Unified Ecosystem
├── Mini WARP Client
│ ├── ️ GUI Manager (PyQt5)
│ ├── CLI Interface
│ ├── WebSocket Client
│ ├── Token Manager
│ └── Module System
├── WARP Data Manager
│ ├── Backup Engine
│ ├── ️ GitHub Integration
│ ├── ⏰ Scheduler Service
│ └── Restore System
├── Unified Launcher
│ ├── Dashboard
│ ├── ️ Mode Router
│ └── Workflow Manager
└── ️ Desktop Integration
 ├── System Menu
 └── ️ Click Launchers
```

---

## Academic Research Context

**Perfect for Cybersecurity Research:**

- **Professional Codebase** - Academic-quality code demonstrating advanced Python skills
- **Research Applications** - Terminal-based security tool development
- **Modular Architecture** - Extensible for custom research modules
- **Complete Documentation** - Academic documentation standards
- **Reliable Operation** - Error-free, production-ready functionality

**Copenhagen University Integration:**
- Cybersecurity research workflows
- Criminal methodology analysis tools
- Digital forensics terminal integration
- Automated research data backup
- Collaborative academic projects

---

## ️ Development & Extension

### Custom Module Development
```python
# modules/research_module.py
def initialize(warp_client):
 """Initialize custom research module"""
 return ResearchModule(warp_client)

class ResearchModule:
 def __init__(self, client):
 self.client = client
 # Custom research functionality
```

### Configuration Extension
```json
{
 "research": {
 "forensics_mode": true,
 "data_collection": "automated",
 "output_format": "academic"
 }
}
```

### Workflow Integration
```bash
# Custom workflow script
python warp_unified_launcher.py backup-auto
# Your research scripts here
./your_research_tool.py
python warp_unified_launcher.py backup-cli
```

---

## Troubleshooting

### Common Issues

 **"Module not found"**
```bash
# Ensure Python path is correct
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python warp_unified_launcher.py setup
```

 **"GUI won't start"**
```bash
# Install PyQt5 dependencies
pip install PyQt5
sudo apt install python3-pyqt5
```

 **"Backup failed"**
```bash
# Check WARP Terminal installation
ls ~/.config/warp-terminal/
# Verify permissions
chmod +x warp-manager*.py
```

 **"GitHub sync error"**
```bash
# Re-setup GitHub integration
./warp-manager-enhanced.py --setup-github
```

### Debug Mode
```bash
# Enable detailed logging
export PYTHONDEBUG=1
python warp_unified_launcher.py dashboard --verbose
```

---

## Version History

### v2.0.0 - Unified Ecosystem (Current)
- Combined Mini WARP Client + Data Manager
- Unified launcher with multiple modes
- Integrated dashboard and control center
- Automated backup-before-launch workflows
- Enhanced desktop integration

### v1.2.0 - Data Manager Enhanced
- GitHub sync and cloud backup
- ⏰ Automated scheduling system
- Advanced restore operations

### v1.1.0 - Client Stabilization
- ️ Event callback shutdown fix
- Enhanced security and token management
- Modular architecture implementation

### v1.0.0 - Initial Release
- Basic Mini WARP Client
- GUI and CLI modes
- WARP Terminal integration

---

## Contributing

We welcome contributions to the WARP ecosystem!

### Areas for Contribution
- Additional platform support
- UI/UX improvements for both tools
- Mobile companion applications
- New backup formats and storage options
- Documentation and tutorials
- Test coverage and quality assurance

### Development Setup
```bash
git clone https/github.com/FoundationAgents/mini-warp-client.git
cd mini-warp-client
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python warp_unified_launcher.py setup
```

---

## License & Credits

**MIT License** - Free for personal, academic, and commercial use

### Credits
- **Mini WARP Client**: Advanced terminal client development
- **WARP Data Manager**: Professional backup solution based on [warp-data-manager](https/github.com/justkidding-scripts/warp-data-manager)
- **Academic Context**: Cybersecurity Research, Copenhagen University
- **Community**: Built with ️ for the WARP Terminal community

---

## Links & Resources

- **GitHub Repository**: https/github.com/FoundationAgents/mini-warp-client
- **Issues & Bug Reports**: https/github.com/FoundationAgents/mini-warp-client/issues
- **Discussions**: https/github.com/FoundationAgents/mini-warp-client/discussions
- **Releases**: https/github.com/FoundationAgents/mini-warp-client/releases
- **WARP Terminal Docs**: https/docs.warp.dev/

---

## Quick Start Checklist

- [ ] Clone repository
- [ ] Run ecosystem setup: `python warp_unified_launcher.py setup`
- [ ] Launch dashboard: `python warp_unified_launcher.py dashboard`
- [ ] Create first backup: Select option 2 in dashboard
- [ ] Launch client: Select option 1 in dashboard
- [ ] Setup GitHub sync (optional): `./warp-manager-enhanced.py --setup-github`
- [ ] Schedule automation (optional): `./warp-manager-enhanced.py --schedule daily`
- [ ] Bookmark this README for reference!

---

 **Fast** • **Secure** • **Reliable** • **Cross-Platform** • **Research-Ready**

**Built with ️ for cybersecurity researchers, terminal power users, and the WARP community**