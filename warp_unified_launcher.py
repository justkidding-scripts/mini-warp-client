#!/usr/bin/env python3
"""
WARP Terminal Unified Ecosystem Launcher
Combines Mini WARP Client + WARP Data Manager for complete terminal management
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

class WARPEcosystemLauncher:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.available_modes = {
            'client-gui': 'Launch Mini WARP Client GUI',
            'client-cli': 'Launch Mini WARP Client CLI', 
            'backup-gui': 'Launch WARP Data Manager GUI',
            'backup-cli': 'Launch WARP Data Manager CLI',
            'manager': 'Launch Integrated Suite Manager',
            'setup': 'Setup complete WARP ecosystem',
            'backup-auto': 'Create automatic backup before launching client',
            'restore': 'Restore WARP data from backup',
            'dashboard': 'Launch unified dashboard'
        }
    
    def show_banner(self):
        print("""
🚀 WARP Terminal Unified Ecosystem
=====================================
🎯 Complete WARP Terminal Management Solution

Components:
📱 Mini WARP Client      - Advanced terminal client with GUI/CLI
💾 WARP Data Manager     - Professional backup & management
🔧 Unified Dashboard     - Integrated control center
⚡ Automated Workflows   - Backup, restore, sync operations

PhD Cybersecurity Research • Copenhagen University
""")

    def launch_client_gui(self):
        """Launch Mini WARP Client GUI"""
        print("🚀 Launching Mini WARP Client GUI...")
        try:
            subprocess.run([sys.executable, str(self.base_dir / 'warp_suite_manager.py')])
        except Exception as e:
            print(f"❌ Failed to launch GUI: {e}")
            print("💡 Try: python warp_suite_manager.py")

    def launch_client_cli(self):
        """Launch Mini WARP Client CLI"""
        print("💻 Launching Mini WARP Client CLI...")
        try:
            subprocess.run([sys.executable, str(self.base_dir / 'launch_warp.py'), 'cli'])
        except Exception as e:
            print(f"❌ Failed to launch CLI: {e}")
            print("💡 Try: python launch_warp.py cli")

    def launch_backup_gui(self):
        """Launch WARP Data Manager GUI"""
        print("💾 Launching WARP Data Manager GUI...")
        try:
            subprocess.run([sys.executable, str(self.base_dir / 'warp-manager.py')])
        except Exception as e:
            print(f"❌ Failed to launch backup GUI: {e}")
            print("💡 Try: python warp-manager.py")

    def launch_backup_cli(self):
        """Launch WARP Data Manager CLI with options"""
        print("🔧 WARP Data Manager CLI Options:")
        print("1. Create snapshot backup")
        print("2. Backup specific components")
        print("3. List backups")
        print("4. Restore from backup")
        print("5. Setup GitHub integration")
        print("6. Schedule automated backups")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            subprocess.run([sys.executable, str(self.base_dir / 'warp-manager-enhanced.py'), '--snapshot'])
        elif choice == '2':
            print("Available components: rules, mcp, database, preferences, logs")
            components = input("Enter components (space-separated): ").strip()
            cmd = [sys.executable, str(self.base_dir / 'warp-manager-enhanced.py'), '--backup'] + components.split()
            subprocess.run(cmd)
        elif choice == '3':
            subprocess.run([sys.executable, str(self.base_dir / 'warp-manager-enhanced.py'), '--list'])
        elif choice == '4':
            subprocess.run([sys.executable, str(self.base_dir / 'warp-manager.py')])
        elif choice == '5':
            subprocess.run([sys.executable, str(self.base_dir / 'warp-manager-enhanced.py'), '--setup-github'])
        elif choice == '6':
            print("Schedule options: daily, weekly")
            schedule = input("Enter schedule type: ").strip()
            time = input("Enter time (HH:MM): ").strip()
            subprocess.run([sys.executable, str(self.base_dir / 'warp-manager-enhanced.py'), 
                          '--schedule', schedule, '--schedule-time', time])

    def launch_unified_manager(self):
        """Launch the integrated suite manager"""
        print("🎛️ Launching Unified WARP Manager...")
        # This would be a future integrated GUI combining both tools
        print("🚧 Unified manager coming soon! For now, choose:")
        print("  - 'client-gui' for Mini WARP Client")
        print("  - 'backup-gui' for Data Manager")

    def auto_backup_and_launch(self):
        """Create backup before launching client"""
        print("💾 Creating automatic backup before launching client...")
        try:
            # Create snapshot backup
            result = subprocess.run([sys.executable, str(self.base_dir / 'warp-manager-enhanced.py'), '--snapshot'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Backup created successfully")
                print("🚀 Launching Mini WARP Client...")
                self.launch_client_gui()
            else:
                print("⚠️ Backup failed, launching client anyway...")
                self.launch_client_gui()
        except Exception as e:
            print(f"❌ Backup error: {e}")
            print("🚀 Launching client without backup...")
            self.launch_client_gui()

    def setup_ecosystem(self):
        """Setup the complete WARP ecosystem"""
        print("🔧 Setting up WARP Terminal Ecosystem...")
        
        # Install dependencies for both systems
        print("📦 Installing dependencies...")
        try:
            subprocess.run([sys.executable, str(self.base_dir / 'deploy-fast.sh')], check=True)
            print("✅ WARP Data Manager dependencies installed")
        except:
            print("⚠️ Manual dependency installation may be required")
        
        # Setup desktop integration
        print("🖥️ Setting up desktop integration...")
        try:
            subprocess.run([str(self.base_dir / 'install_desktop.sh')], check=True)
            print("✅ Desktop integration installed")
        except:
            print("⚠️ Desktop integration optional")
        
        # Create initial backup
        print("💾 Creating initial system backup...")
        try:
            subprocess.run([sys.executable, str(self.base_dir / 'warp-manager-enhanced.py'), '--snapshot'])
            print("✅ Initial backup created")
        except:
            print("⚠️ Backup creation optional")
        
        print("\n🎉 WARP Ecosystem setup complete!")
        print("📋 Available commands:")
        for mode, desc in self.available_modes.items():
            print(f"  python warp_unified_launcher.py {mode}  # {desc}")

    def launch_dashboard(self):
        """Launch unified dashboard (future feature)"""
        print("📊 Unified Dashboard (Preview Mode)")
        print("=" * 50)
        
        # Show system status
        print("🔍 System Status:")
        try:
            # Check if WARP client processes are running
            result = subprocess.run(['pgrep', '-f', 'warp'], capture_output=True, text=True)
            if result.stdout.strip():
                print("  ✅ WARP processes: Running")
            else:
                print("  ⭕ WARP processes: Not running")
        except:
            print("  ❓ WARP processes: Unknown")
        
        # Check backup status
        backup_dir = Path.home() / '.warp-backups'
        if backup_dir.exists():
            backups = list(backup_dir.glob('*.tar.zst'))
            print(f"  📦 Backups available: {len(backups)}")
            if backups:
                latest = max(backups, key=lambda x: x.stat().st_mtime)
                print(f"  📅 Latest backup: {latest.name}")
        else:
            print("  📦 Backups available: 0")
        
        print("\n🚀 Quick Actions:")
        print("  1. Launch Client GUI")
        print("  2. Create Backup")  
        print("  3. View Backups")
        print("  4. Launch CLI")
        print("  5. Exit")
        
        choice = input("\nSelect action (1-5): ").strip()
        if choice == '1':
            self.launch_client_gui()
        elif choice == '2':
            subprocess.run([sys.executable, str(self.base_dir / 'warp-manager-enhanced.py'), '--snapshot'])
        elif choice == '3':
            subprocess.run([sys.executable, str(self.base_dir / 'warp-manager-enhanced.py'), '--list'])
        elif choice == '4':
            self.launch_client_cli()

def main():
    launcher = WARPEcosystemLauncher()
    
    parser = argparse.ArgumentParser(
        description="WARP Terminal Unified Ecosystem Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available modes:
  client-gui    Launch Mini WARP Client GUI
  client-cli    Launch Mini WARP Client CLI  
  backup-gui    Launch WARP Data Manager GUI
  backup-cli    Launch WARP Data Manager CLI
  manager       Launch Integrated Suite Manager
  setup         Setup complete WARP ecosystem
  backup-auto   Create backup before launching client
  restore       Restore WARP data from backup
  dashboard     Launch unified dashboard

Examples:
  python warp_unified_launcher.py client-gui
  python warp_unified_launcher.py backup-auto
  python warp_unified_launcher.py setup
        """
    )
    
    parser.add_argument('mode', nargs='?', choices=launcher.available_modes.keys(),
                       help='Launch mode')
    parser.add_argument('--banner', action='store_true', help='Show banner')
    
    args = parser.parse_args()
    
    if args.banner or not args.mode:
        launcher.show_banner()
    
    if not args.mode:
        print("Available modes:")
        for mode, desc in launcher.available_modes.items():
            print(f"  {mode:<15} - {desc}")
        return
    
    # Route to appropriate launcher
    mode_handlers = {
        'client-gui': launcher.launch_client_gui,
        'client-cli': launcher.launch_client_cli,
        'backup-gui': launcher.launch_backup_gui,
        'backup-cli': launcher.launch_backup_cli,
        'manager': launcher.launch_unified_manager,
        'setup': launcher.setup_ecosystem,
        'backup-auto': launcher.auto_backup_and_launch,
        'restore': launcher.launch_backup_gui,  # GUI is better for restore
        'dashboard': launcher.launch_dashboard
    }
    
    handler = mode_handlers.get(args.mode)
    if handler:
        try:
            handler()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    else:
        print(f"❌ Unknown mode: {args.mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()