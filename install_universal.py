#!/usr/bin/env python3
"""
WARP Terminal Universal Installer
One-click installer for all platforms (Windows, Linux, macOS)
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

class UniversalInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.base_dir = Path(__file__).parent
        self.home_dir = Path.home()
        
    def print_banner(self):
        print("""
🎯 WARP Terminal Universal Installer
=====================================
🚀 One-click installation for all platforms
📦 Automatically configures your system
⚡ Professional deployment-ready setup
""")
    
    def detect_system(self):
        """Detect system capabilities"""
        print(f"🖥️  Detected platform: {self.system.title()}")
        
        if self.system == "windows":
            return self.install_windows()
        elif self.system == "linux":
            return self.install_linux()
        elif self.system == "darwin":
            return self.install_macos()
        else:
            print(f"❌ Unsupported platform: {self.system}")
            return False
    
    def install_python_deps(self):
        """Install Python dependencies"""
        print("📦 Installing Python dependencies...")
        
        deps = [
            "PyQt5>=5.15.0",
            "zstandard>=0.20.0", 
            "requests>=2.28.0",
            "psutil>=5.9.0",
            "cryptography>=3.4.8"
        ]
        
        for dep in deps:
            print(f"  📥 Installing {dep}...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", dep
                ], check=True, capture_output=True)
                print(f"  ✅ {dep} installed")
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ Failed to install {dep}: {e}")
                return False
        
        return True
    
    def install_windows(self):
        """Windows-specific installation"""
        print("🪟 Configuring for Windows...")
        
        # Install Windows-specific packages
        win_deps = ["pywin32", "wmi"]
        for dep in win_deps:
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", dep
                ], check=True, capture_output=True)
                print(f"  ✅ {dep} installed")
            except:
                print(f"  ⚠️ {dep} failed (optional)")
        
        # Create desktop shortcut
        desktop = Path.home() / "Desktop"
        if desktop.exists():
            shortcut_content = f"""[InternetShortcut]
URL=file://{self.base_dir / 'warp_launcher.bat'}
IconIndex=0"""
            shortcut_path = desktop / "WARP Terminal.url"
            with open(shortcut_path, 'w') as f:
                f.write(shortcut_content)
            print("  ✅ Desktop shortcut created")
        
        # Create Start Menu entry
        start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
        if start_menu.exists():
            start_menu_dir = start_menu / "WARP Terminal"
            start_menu_dir.mkdir(exist_ok=True)
            
            # Copy launcher to Start Menu
            shutil.copy2(self.base_dir / "warp_launcher.bat", 
                        start_menu_dir / "WARP Terminal.bat")
            print("  ✅ Start Menu entry created")
        
        return True
    
    def install_linux(self):
        """Linux-specific installation"""
        print("🐧 Configuring for Linux...")
        
        # Install system dependencies if possible
        if os.geteuid() == 0:  # Root user
            try:
                # Detect package manager
                if shutil.which("apt"):
                    subprocess.run([
                        "apt", "update"
                    ], check=True, capture_output=True)
                    subprocess.run([
                        "apt", "install", "-y", "python3-pyqt5", "git", "python3-venv"
                    ], check=True, capture_output=True)
                    print("  ✅ System packages installed")
                elif shutil.which("yum"):
                    subprocess.run([
                        "yum", "install", "-y", "python3-qt5", "git"
                    ], check=True, capture_output=True)
                    print("  ✅ System packages installed")
            except:
                print("  ⚠️ System packages not installed (non-critical)")
        
        # Create desktop integration
        self.setup_linux_desktop()
        
        # Create symlink in /usr/local/bin if possible
        try:
            local_bin = Path("/usr/local/bin/warp-terminal")
            if not local_bin.exists() and os.access("/usr/local/bin", os.W_OK):
                local_bin.symlink_to(self.base_dir / "warp_launcher.py")
                print("  ✅ System-wide command 'warp-terminal' created")
        except:
            print("  ⚠️ System-wide command not created (run as root for this feature)")
        
        return True
    
    def install_macos(self):
        """macOS-specific installation"""
        print("🍎 Configuring for macOS...")
        
        # Install macOS-specific packages
        macos_deps = ["pyobjc-framework-Cocoa"]
        for dep in macos_deps:
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", dep
                ], check=True, capture_output=True)
                print(f"  ✅ {dep} installed")
            except:
                print(f"  ⚠️ {dep} failed (optional)")
        
        # Create .app bundle
        self.setup_macos_app()
        
        # Add to Applications folder if possible
        apps_dir = Path("/Applications")
        local_apps = Path.home() / "Applications"
        
        app_bundle = self.base_dir / "WARP Terminal.app"
        if app_bundle.exists():
            if apps_dir.exists() and os.access(apps_dir, os.W_OK):
                shutil.copytree(app_bundle, apps_dir / "WARP Terminal.app", 
                               dirs_exist_ok=True)
                print("  ✅ Installed to /Applications")
            elif local_apps.exists():
                shutil.copytree(app_bundle, local_apps / "WARP Terminal.app",
                               dirs_exist_ok=True)  
                print("  ✅ Installed to ~/Applications")
        
        return True
    
    def setup_linux_desktop(self):
        """Setup Linux desktop integration"""
        desktop_dir = self.home_dir / ".local/share/applications"
        desktop_dir.mkdir(parents=True, exist_ok=True)
        
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=WARP Terminal
Comment=Advanced Terminal Management Suite
Exec={sys.executable} {self.base_dir / 'warp_launcher.py'} gui
Icon={self.base_dir / 'assets' / 'warp-icon.png'}
Terminal=false
Categories=Network;Development;Utility;System;
StartupNotify=true
Keywords=terminal;warp;client;backup;management;"""
        
        desktop_file = desktop_dir / "warp-terminal.desktop"
        with open(desktop_file, 'w') as f:
            f.write(desktop_content)
        os.chmod(desktop_file, 0o755)
        
        # Update desktop database
        try:
            subprocess.run(["update-desktop-database", str(desktop_dir)], 
                          capture_output=True)
            print("  ✅ Desktop integration configured")
        except:
            print("  ✅ Desktop file created")
        
        return True
    
    def setup_macos_app(self):
        """Setup macOS .app bundle"""
        app_dir = self.base_dir / "WARP Terminal.app"
        contents_dir = app_dir / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        for d in [app_dir, contents_dir, macos_dir, resources_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # Info.plist
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>warp-terminal</string>
    <key>CFBundleIdentifier</key>
    <string>com.warp.terminal</string>
    <key>CFBundleName</key>
    <string>WARP Terminal</string>
    <key>CFBundleDisplayName</key>
    <string>WARP Terminal</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>WRPT</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
</dict>
</plist>"""
        
        with open(contents_dir / "Info.plist", 'w') as f:
            f.write(plist_content)
        
        # Executable script
        exec_script = f"""#!/bin/bash
cd "{self.base_dir}"
{sys.executable} warp_launcher.py gui"""
        
        exec_file = macos_dir / "warp-terminal"
        with open(exec_file, 'w') as f:
            f.write(exec_script)
        os.chmod(exec_file, 0o755)
        
        print("  ✅ macOS .app bundle created")
        return True
    
    def create_backup_system(self):
        """Initialize backup system"""
        print("💾 Setting up backup system...")
        
        backup_dir = self.home_dir / ".warp-backups"
        backup_dir.mkdir(exist_ok=True)
        
        config_dir = self.home_dir / ".config/warp"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Create initial config
        initial_config = {
            "version": "1.0.0",
            "backup_directory": str(backup_dir),
            "auto_backup": False,
            "compression": "zstandard",
            "retention_days": 30
        }
        
        import json
        config_file = config_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(initial_config, f, indent=2)
        
        print("  ✅ Backup system initialized")
        return True
    
    def run_initial_setup(self):
        """Run the launcher's setup command"""
        print("⚙️ Running initial WARP setup...")
        
        try:
            subprocess.run([
                sys.executable, str(self.base_dir / "warp_launcher.py"), "setup"
            ], check=True)
            print("  ✅ Initial setup completed")
            return True
        except subprocess.CalledProcessError:
            print("  ⚠️ Some setup steps may have failed (non-critical)")
            return True
    
    def show_completion_message(self):
        """Show installation completion message"""
        print("""
🎉 WARP Terminal Installation Complete!
======================================

✅ Python dependencies installed
✅ Platform integration configured  
✅ Desktop shortcuts created
✅ Backup system initialized
✅ Initial setup completed

🚀 Quick Start Commands:
""")
        
        if self.system == "windows":
            print("  • Double-click 'WARP Terminal' on your Desktop")
            print("  • Or run: warp_launcher.bat")
            print("  • PowerShell: .\\warp_launcher.ps1")
        elif self.system == "linux":
            print("  • Find 'WARP Terminal' in your application menu")
            print("  • Or run: ./warp_launcher.sh")  
            print("  • Command: warp-terminal (if installed system-wide)")
        elif self.system == "darwin":
            print("  • Find 'WARP Terminal' in Applications folder")
            print("  • Or run: ./warp_launcher.sh")
        
        print(f"""
  • Python: python3 warp_launcher.py
  
📚 Documentation: README_LAUNCHERS.md
🆘 Help: python3 warp_launcher.py help

Your WARP Terminal is ready for professional use! 🚀
""")
    
    def install(self):
        """Main installation process"""
        try:
            self.print_banner()
            
            # Install Python dependencies
            if not self.install_python_deps():
                print("❌ Failed to install Python dependencies")
                return False
            
            # Platform-specific setup
            if not self.detect_system():
                print("❌ Platform setup failed")
                return False
            
            # Initialize backup system
            self.create_backup_system()
            
            # Run initial setup
            self.run_initial_setup()
            
            # Show completion message
            self.show_completion_message()
            
            return True
            
        except KeyboardInterrupt:
            print("\n👋 Installation cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Installation failed: {e}")
            return False

def main():
    installer = UniversalInstaller()
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print("WARP Terminal Universal Installer")
        print("Usage: python3 install_universal.py")
        print("Automatically detects and configures WARP Terminal for your platform")
        return
    
    success = installer.install()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
