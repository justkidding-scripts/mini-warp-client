#!/usr/bin/env python3
"""
WARP Terminal Universal Cross-Platform Launcher
Supports Windows, Linux, macOS with automatic platform detection
"""

import sys
import os
import platform
import subprocess
import argparse
import json
from pathlib import Path
import shutil

class WARPUniversalLauncher:
    def __init__(self):
        self.system = platform.system().lower()
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "launcher_config.json"
        self.load_config()
        
    def load_config(self):
        """Load or create launcher configuration"""
        default_config = {
            "auto_install_deps": True,
            "desktop_integration": True,
            "backup_before_launch": False,
            "github_integration": False,
            "discord_webhook": "",
            "preferred_terminal": "auto"
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def detect_environment(self):
        """Detect system environment and capabilities"""
        env_info = {
            "system": self.system,
            "python_version": sys.version,
            "architecture": platform.machine(),
            "has_gui": False,
            "terminal_available": False,
            "package_manager": None
        }
        
        # Check for GUI capability
        if self.system == "linux":
            env_info["has_gui"] = bool(os.environ.get("DISPLAY"))
            # Detect package manager
            if shutil.which("apt"):
                env_info["package_manager"] = "apt"
            elif shutil.which("yum"):
                env_info["package_manager"] = "yum"
            elif shutil.which("pacman"):
                env_info["package_manager"] = "pacman"
        elif self.system == "windows":
            env_info["has_gui"] = True
            env_info["package_manager"] = "pip"
        elif self.system == "darwin":
            env_info["has_gui"] = True
            env_info["package_manager"] = "brew" if shutil.which("brew") else "pip"
        
        return env_info
    
    def install_dependencies(self):
        """Install platform-specific dependencies"""
        print(f"🔧 Installing dependencies for {self.system}...")
        
        # Python dependencies (cross-platform)
        python_deps = [
            "PyQt5",
            "zstandard",
            "requests",
            "psutil",
            "cryptography"
        ]
        
        for dep in python_deps:
            print(f"  📦 Installing {dep}...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True)
                print(f"  ✅ {dep} installed")
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ Failed to install {dep}: {e}")
        
        # Platform-specific dependencies
        if self.system == "linux":
            self._install_linux_deps()
        elif self.system == "windows":
            self._install_windows_deps()
        elif self.system == "darwin":
            self._install_macos_deps()
    
    def _install_linux_deps(self):
        """Install Linux-specific dependencies"""
        print("🐧 Installing Linux system dependencies...")
        
        # Try to install system packages if we have permission
        if os.geteuid() == 0:  # Running as root
            try:
                subprocess.run(["apt", "update"], check=True, capture_output=True)
                subprocess.run(["apt", "install", "-y", "python3-pyqt5", "git"], 
                             check=True, capture_output=True)
                print("  ✅ System packages installed")
            except:
                print("  ⚠️ System package installation failed (non-critical)")
    
    def _install_windows_deps(self):
        """Install Windows-specific dependencies"""
        print("🪟 Installing Windows dependencies...")
        
        # Windows-specific packages
        windows_deps = ["pywin32", "wmi"]
        for dep in windows_deps:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True)
                print(f"  ✅ {dep} installed")
            except:
                print(f"  ⚠️ {dep} installation failed")
    
    def _install_macos_deps(self):
        """Install macOS-specific dependencies"""
        print("🍎 Installing macOS dependencies...")
        
        # macOS-specific packages
        macos_deps = ["pyobjc-framework-Cocoa"]
        for dep in macos_deps:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True)
                print(f"  ✅ {dep} installed")
            except:
                print(f"  ⚠️ {dep} installation failed")
    
    def setup_desktop_integration(self):
        """Setup desktop integration for current platform"""
        print(f"🖥️ Setting up desktop integration for {self.system}...")
        
        if self.system == "linux":
            self._setup_linux_desktop()
        elif self.system == "windows":
            self._setup_windows_desktop()
        elif self.system == "darwin":
            self._setup_macos_desktop()
    
    def _setup_linux_desktop(self):
        """Setup Linux desktop integration"""
        desktop_dir = Path.home() / ".local/share/applications"
        desktop_dir.mkdir(parents=True, exist_ok=True)
        
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=WARP Terminal Client
Comment=Advanced Terminal Client with GUI/CLI modes
Exec={sys.executable} {self.base_dir / 'warp_launcher.py'} gui
Icon={self.base_dir / 'assets' / 'warp-icon.png'}
Terminal=false
Categories=Network;Development;Utility;
StartupNotify=true"""
        
        desktop_file = desktop_dir / "warp-terminal.desktop"
        with open(desktop_file, 'w') as f:
            f.write(desktop_content)
        
        os.chmod(desktop_file, 0o755)
        print("  ✅ Linux desktop entry created")
    
    def _setup_windows_desktop(self):
        """Setup Windows desktop integration"""
        try:
            import winreg
            
            # Create registry entry for Windows
            key_path = r"SOFTWARE\Classes\Applications\warp_launcher.py"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "WARP Terminal Client")
            
            print("  ✅ Windows registry entry created")
            
            # Create batch file for easy launching
            batch_content = f"""@echo off
cd /d "{self.base_dir}"
python warp_launcher.py %*
pause"""
            
            with open(self.base_dir / "warp-terminal.bat", 'w') as f:
                f.write(batch_content)
            
            print("  ✅ Windows batch launcher created")
            
        except ImportError:
            print("  ⚠️ Windows registry integration requires winreg module")
    
    def _setup_macos_desktop(self):
        """Setup macOS desktop integration"""
        # Create .app bundle structure
        app_dir = self.base_dir / "WARP Terminal.app"
        contents_dir = app_dir / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        for d in [app_dir, contents_dir, macos_dir, resources_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # Create Info.plist
        plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>warp-terminal</string>
    <key>CFBundleIdentifier</key>
    <string>com.warp.terminal</string>
    <key>CFBundleName</key>
    <string>WARP Terminal</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>"""
        
        with open(contents_dir / "Info.plist", 'w') as f:
            f.write(plist_content)
        
        # Create executable script
        exec_script = f"""#!/bin/bash
cd "{self.base_dir}"
python3 warp_launcher.py gui"""
        
        exec_file = macos_dir / "warp-terminal"
        with open(exec_file, 'w') as f:
            f.write(exec_script)
        
        os.chmod(exec_file, 0o755)
        print("  ✅ macOS .app bundle created")
    
    def launch_gui(self):
        """Launch GUI application"""
        print("🚀 Launching WARP Terminal GUI...")
        
        env_info = self.detect_environment()
        if not env_info["has_gui"]:
            print("⚠️ No GUI environment detected, falling back to CLI mode")
            return self.launch_cli()
        
        try:
            if self.config.get("backup_before_launch", False):
                self.create_backup()
            
            subprocess.run([sys.executable, str(self.base_dir / "warp_suite_manager.py")])
        except FileNotFoundError:
            print("❌ GUI launcher not found, trying unified launcher...")
            subprocess.run([sys.executable, str(self.base_dir / "warp_unified_launcher.py"), "client-gui"])
    
    def launch_cli(self):
        """Launch CLI application"""
        print("💻 Launching WARP Terminal CLI...")
        
        try:
            subprocess.run([sys.executable, str(self.base_dir / "warp_unified_launcher.py"), "client-cli"])
        except FileNotFoundError:
            print("❌ CLI launcher not found")
    
    def create_backup(self):
        """Create system backup"""
        print("💾 Creating backup...")
        try:
            subprocess.run([sys.executable, str(self.base_dir / "warp-manager-enhanced.py"), "--snapshot"])
        except FileNotFoundError:
            print("⚠️ Backup system not available")
    
    def show_status(self):
        """Show system status dashboard"""
        env_info = self.detect_environment()
        
        print("📊 WARP Terminal System Status")
        print("=" * 40)
        print(f"🖥️  Platform: {env_info['system'].title()}")
        print(f"🐍 Python: {env_info['python_version'].split()[0]}")
        print(f"🏗️  Architecture: {env_info['architecture']}")
        print(f"🖼️  GUI Available: {'✅' if env_info['has_gui'] else '❌'}")
        print(f"📦 Package Manager: {env_info['package_manager'] or 'None'}")
        
        # Check component status
        components = [
            ("warp_suite_manager.py", "GUI Manager"),
            ("warp_unified_launcher.py", "Unified Launcher"),
            ("warp-manager-enhanced.py", "Backup System")
        ]
        
        print("\n📋 Components:")
        for filename, name in components:
            file_path = self.base_dir / filename
            status = "✅" if file_path.exists() else "❌"
            print(f"  {status} {name}")
        
        # Check dependencies
        print("\n📦 Dependencies:")
        deps_to_check = ["PyQt5", "zstandard", "requests"]
        for dep in deps_to_check:
            try:
                __import__(dep.lower().replace("pyqt5", "PyQt5.QtWidgets"))
                print(f"  ✅ {dep}")
            except ImportError:
                print(f"  ❌ {dep}")
    
    def configure(self):
        """Interactive configuration"""
        print("⚙️ WARP Terminal Configuration")
        print("=" * 30)
        
        print(f"Current settings:")
        for key, value in self.config.items():
            print(f"  {key}: {value}")
        
        print("\nConfiguration options:")
        print("1. Toggle auto-install dependencies")
        print("2. Toggle desktop integration")
        print("3. Toggle backup before launch")
        print("4. Set Discord webhook")
        print("5. Save and exit")
        
        while True:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                self.config["auto_install_deps"] = not self.config["auto_install_deps"]
                print(f"Auto-install dependencies: {self.config['auto_install_deps']}")
            elif choice == "2":
                self.config["desktop_integration"] = not self.config["desktop_integration"]
                print(f"Desktop integration: {self.config['desktop_integration']}")
            elif choice == "3":
                self.config["backup_before_launch"] = not self.config["backup_before_launch"]
                print(f"Backup before launch: {self.config['backup_before_launch']}")
            elif choice == "4":
                webhook = input("Enter Discord webhook URL: ").strip()
                self.config["discord_webhook"] = webhook
                print("Discord webhook set")
            elif choice == "5":
                self.save_config()
                print("✅ Configuration saved")
                break
            else:
                print("Invalid option")
    
    def setup_complete(self):
        """Complete setup process"""
        print("🚀 WARP Terminal Complete Setup")
        print("=" * 35)
        
        env_info = self.detect_environment()
        print(f"Platform detected: {env_info['system'].title()}")
        
        if self.config.get("auto_install_deps", True):
            self.install_dependencies()
        
        if self.config.get("desktop_integration", True):
            self.setup_desktop_integration()
        
        # Create initial backup
        backup_dir = Path.home() / ".warp-backups"
        backup_dir.mkdir(exist_ok=True)
        
        print("✅ Setup completed successfully!")
        print("\n🎯 Quick start commands:")
        print(f"  python {Path(__file__).name} gui     # Launch GUI")
        print(f"  python {Path(__file__).name} cli     # Launch CLI")
        print(f"  python {Path(__file__).name} status  # Show status")

def main():
    launcher = WARPUniversalLauncher()
    
    parser = argparse.ArgumentParser(
        description="WARP Terminal Universal Cross-Platform Launcher",
        epilog="""
Available commands:
  gui        Launch GUI application (default)
  cli        Launch CLI application
  backup     Create system backup
  status     Show system status
  config     Configure launcher settings
  setup      Complete setup process
  install    Install dependencies only
        """
    )
    
    parser.add_argument('command', nargs='?', default='gui',
                       choices=['gui', 'cli', 'backup', 'status', 'config', 'setup', 'install'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'gui':
            launcher.launch_gui()
        elif args.command == 'cli':
            launcher.launch_cli()
        elif args.command == 'backup':
            launcher.create_backup()
        elif args.command == 'status':
            launcher.show_status()
        elif args.command == 'config':
            launcher.configure()
        elif args.command == 'setup':
            launcher.setup_complete()
        elif args.command == 'install':
            launcher.install_dependencies()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
