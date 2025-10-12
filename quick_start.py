#!/usr/bin/env python3
"""
Quick Start Launcher for Mini WARP Client
Automatically detects best launch mode and provides interactive setup
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))
sys.path.append(str(Path(__file__).parent / 'ui'))

def detect_capabilities():
    """Detect what launch modes are available"""
    capabilities = {
        'gui': False,
        'cli': True,  # Always available
        'python_version': sys.version_info,
        'dependencies': {}
    }
    
    # Check GUI dependencies
    try:
        import PyQt5
        capabilities['gui'] = True
        capabilities['dependencies']['pyqt5'] = True
    except ImportError:
        capabilities['dependencies']['pyqt5'] = False
    
    # Check other dependencies
    modules_to_check = ['requests', 'websocket', 'cryptography', 'aiohttp']
    for module in modules_to_check:
        try:
            __import__(module)
            capabilities['dependencies'][module] = True
        except ImportError:
            capabilities['dependencies'][module] = False
    
    return capabilities

def interactive_setup():
    """Interactive setup for first-time users"""
    print("🚀 Welcome to Mini WARP Client!")
    print("=" * 50)
    
    capabilities = detect_capabilities()
    
    print(f"Python Version: {capabilities['python_version'].major}.{capabilities['python_version'].minor}")
    print()
    
    # Check dependencies
    missing_deps = [dep for dep, available in capabilities['dependencies'].items() if not available]
    if missing_deps:
        print("⚠️  Missing Dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print()
        print("To install missing dependencies:")
        print("pip install requests websocket-client pyqt5 cryptography aiohttp pycryptodome")
        print()
        
        if 'pyqt5' in missing_deps:
            print("Note: GUI mode will not be available without PyQt5")
            print()
    
    # Show available modes
    print("Available Launch Modes:")
    if capabilities['gui']:
        print("  1. 🖥️  GUI Mode (Recommended) - Full graphical interface")
    print("  2. 💻 CLI Mode - Command-line interface")
    print("  3. 🔧 Daemon Mode - Background service")
    print("  4. ⚙️  Configuration Setup")
    print("  5. 📖 Show Documentation")
    print()
    
    # Get user choice
    while True:
        try:
            if capabilities['gui']:
                choice = input("Select mode (1-5, or press Enter for GUI): ").strip()
                if choice == '' or choice == '1':
                    return 'gui'
            else:
                choice = input("Select mode (2-5, or press Enter for CLI): ").strip()
                if choice == '' or choice == '2':
                    return 'cli'
            
            if choice == '2':
                return 'cli'
            elif choice == '3':
                return 'daemon'
            elif choice == '4':
                return 'setup'
            elif choice == '5':
                return 'docs'
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

def show_documentation():
    """Show basic documentation"""
    print("\n📖 Mini WARP Client Documentation")
    print("=" * 40)
    print()
    print("CONFIGURATION:")
    print("  - Configuration files are stored in config/")
    print("  - Tokens are stored encrypted in data/tokens.json")
    print("  - Logs are written to data/warp_client.log")
    print()
    print("CLI COMMANDS:")
    print("  status          - Show connection status")
    print("  connect         - Connect to WARP services")
    print("  auth <token>    - Authenticate with named token")
    print("  exec <command>  - Execute terminal command")
    print("  chat <message>  - Chat with AI agent")
    print("  tokens          - List available tokens")
    print("  modules         - List loaded modules")
    print("  help            - Show command help")
    print()
    print("MODULES:")
    print("  - penetration_testing: Network scans, vulnerability checks")
    print("  - warp_enhancements: Token analysis, endpoint fuzzing, config extraction")
    print()
    print("CONFIGURATION EDITING:")
    print("  - GUI: Use built-in Configuration Editor")
    print("  - Manual: Edit config/default_config.json")
    print()
    print("For detailed documentation, see README.md")
    print()

def run_setup():
    """Run initial setup"""
    print("\n⚙️  Mini WARP Client Setup")
    print("=" * 30)
    
    from config_manager import config_manager
    from warp_client import warp_client
    
    # Check if setup is needed
    if not Path("data").exists():
        Path("data").mkdir(exist_ok=True)
        print("✓ Created data directory")
    
    if not Path("logs").exists():
        Path("logs").mkdir(exist_ok=True)
        print("✓ Created logs directory")
    
    # Token setup
    tokens = warp_client.token_manager.list_tokens()
    if not tokens:
        print("\n🔑 Token Setup")
        print("No tokens found. You can add tokens later using:")
        print("  - GUI: Token Manager")
        print("  - CLI: Will prompt when needed")
    else:
        print(f"\n✓ Found {len(tokens)} token(s): {', '.join(tokens)}")
    
    # Configuration check
    endpoints = config_manager.get_all_endpoints()
    if endpoints:
        print(f"\n✓ Configuration loaded with {len(endpoints)} endpoint(s)")
    
    # Module check
    modules = list(warp_client.modules.keys())
    if modules:
        print(f"✓ Loaded {len(modules)} module(s): {', '.join(modules)}")
    else:
        print("ℹ️  No custom modules loaded")
    
    print("\n✅ Setup complete!")
    print("\nRecommended next steps:")
    print("1. Add authentication tokens (via GUI Token Manager)")
    print("2. Configure endpoints if needed (via GUI Configuration Editor)")
    print("3. Test connection with 'status' command")
    print()

def main():
    """Main entry point"""
    try:
        # Quick argument check
        if len(sys.argv) > 1:
            mode = sys.argv[1].lower()
            if mode in ['gui', 'cli', 'daemon']:
                # Use main launcher
                os.execv(sys.executable, [sys.executable, 'launch_warp.py'] + sys.argv[1:])
            else:
                print(f"Unknown mode: {mode}")
                print("Available modes: gui, cli, daemon")
                sys.exit(1)
        
        # Interactive mode
        choice = interactive_setup()
        
        if choice == 'docs':
            show_documentation()
            input("\nPress Enter to continue...")
            main()  # Return to menu
        elif choice == 'setup':
            run_setup()
            input("\nPress Enter to continue...")
            main()  # Return to menu
        else:
            # Launch selected mode
            if choice == 'gui':
                try:
                    from launcher import main as gui_main
                    gui_main()
                except ImportError as e:
                    print(f"GUI not available: {e}")
                    print("Falling back to CLI mode...")
                    choice = 'cli'
            
            if choice == 'cli':
                from launch_warp import launch_cli
                launch_cli()
            elif choice == 'daemon':
                from launch_warp import launch_daemon
                launch_daemon()
    
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
