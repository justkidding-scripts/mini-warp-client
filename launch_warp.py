#!/usr/bin/env python3
"""
Mini WARP Client Launcher
Main entry point for the customizable WARP client
"""

import sys
import os
import argparse
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))
sys.path.append(str(Path(__file__).parent / 'ui'))

def launch_gui():
    """Launch the GUI version"""
    try:
        from launcher import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"GUI dependencies missing: {e}")
        print("Install PyQt5: pip install pyqt5")
        sys.exit(1)

def launch_cli():
    """Launch CLI version"""
    from config_manager import config_manager
    from warp_client import warp_client
    
    print("=== Mini WARP Client - CLI Mode ===")
    print(f"Version: {config_manager.get('warp_client.version', '1.0.0')}")
    print(f"Debug Mode: {config_manager.get('warp_client.debug_mode', False)}")
    print()
    
    # Show current status
    status = warp_client.get_status()
    print(f"Connection Status: {'Connected' if status['connection']['connected'] else 'Disconnected'}")
    print(f"Authentication: {'Authenticated' if status['connection']['authenticated'] else 'Not Authenticated'}")
    print(f"Available Tokens: {', '.join(status['tokens']) if status['tokens'] else 'None'}")
    print()
    
    # Interactive CLI
    while True:
        try:
            command = input("WARP> ").strip()
            
            if command in ['exit', 'quit', 'q']:
                break
            elif command == 'status':
                status = warp_client.get_status()
                print(f"Connected: {status['connection']['connected']}")
                print(f"Authenticated: {status['connection']['authenticated']}")
                print(f"Requests: {status['metrics']['total_requests']}")
                print(f"Success Rate: {status['metrics']['success_rate']:.1f}%")
                
            elif command == 'connect':
                if warp_client.connect_websocket():
                    print("Connection initiated...")
                else:
                    print("Failed to connect")
                    
            elif command == 'disconnect':
                warp_client.disconnect()
                print("Disconnected")
                
            elif command.startswith('auth '):
                token_name = command[5:].strip()
                if warp_client.authenticate(token_name=token_name):
                    print("Authentication successful")
                else:
                    print("Authentication failed")
                    
            elif command.startswith('exec '):
                cmd = command[5:].strip()
                result = warp_client.execute_command(cmd)
                if 'error' in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Exit Code: {result['exit_code']}")
                    if result['stdout']:
                        print("STDOUT:")
                        print(result['stdout'])
                    if result['stderr']:
                        print("STDERR:")
                        print(result['stderr'])
                        
            elif command.startswith('chat '):
                message = command[5:].strip()
                result = warp_client.chat_with_agent(message)
                if 'error' in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Agent: {result.get('response', 'No response')}")
                    
            elif command == 'tokens':
                tokens = warp_client.token_manager.list_tokens()
                if tokens:
                    print("Available tokens:")
                    for token in tokens:
                        print(f"  - {token}")
                else:
                    print("No tokens configured")
                    
            elif command == 'modules':
                modules = list(warp_client.modules.keys())
                if modules:
                    print("Loaded modules:")
                    for module in modules:
                        print(f"  - {module}")
                else:
                    print("No modules loaded")
                    
            elif command == 'endpoints':
                endpoints = warp_client.config.get_all_endpoints()
                if endpoints:
                    print("Configured endpoints:")
                    for name, url in endpoints.items():
                        print(f"  - {name}: {url}")
                else:
                    print("No endpoints configured")
                    
            elif command == 'help':
                print("""
Available commands:
  status          - Show connection status
  connect         - Connect to WARP services
  disconnect      - Disconnect from WARP services
  auth <token>    - Authenticate with named token
  exec <command>  - Execute terminal command
  chat <message>  - Chat with AI agent
  tokens          - List available tokens
  modules         - List loaded modules
  endpoints       - List configured endpoints
  help            - Show this help
  exit/quit/q     - Exit the application
                """)
            
            elif command == '':
                continue
            
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"Error: {e}")

def launch_daemon():
    """Launch daemon mode (headless)"""
    from config_manager import config_manager
    from warp_client import warp_client
    import time
    
    print("Starting Mini WARP Client in daemon mode...")
    
    # Auto-connect if configured
    if config_manager.get('warp_client.auto_connect', False):
        print("Auto-connecting...")
        warp_client.connect_websocket()
        
        # Auto-authenticate if configured
        tokens = warp_client.token_manager.list_tokens()
        if tokens:
            # Use first available token
            if warp_client.authenticate(token_name=tokens[0]):
                print(f"Auto-authenticated with token: {tokens[0]}")
    
    print("Daemon running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down daemon...")
        warp_client.disconnect()

def main():
    parser = argparse.ArgumentParser(description="Mini WARP Client")
    parser.add_argument('mode', choices=['gui', 'cli', 'daemon'], 
                       help='Launch mode: gui (default), cli, or daemon')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--no-gui', action='store_true', help='Force CLI mode if GUI fails')
    
    args = parser.parse_args()
    
    # Set debug mode if requested
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # Load custom config if specified
    if args.config:
        print(f"Loading configuration from: {args.config}")
        # TODO: Implement custom config loading
    
    # Launch appropriate mode
    if args.mode == 'gui':
        try:
            launch_gui()
        except Exception as e:
            if args.no_gui:
                print(f"GUI failed ({e}), falling back to CLI...")
                launch_cli()
            else:
                raise
    elif args.mode == 'cli':
        launch_cli()
    elif args.mode == 'daemon':
        launch_daemon()

if __name__ == "__main__":
    main()
