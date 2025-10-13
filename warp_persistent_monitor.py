#!/usr/bin/env python3
"""
WARP Terminal Persistent Monitor
Persistent background service that monitors WARP terminals and backs up data every 30 minutes
"""

import os
import sys
import time
import json
import psutil
import threading
import subprocess
import signal
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(Path.home() / '.warp-monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WARPMonitor:
    """Monitors WARP terminals and handles automatic backups"""
    
    def __init__(self):
        self.home = Path.home()
        self.config_file = self.home / ".warp-monitor-config.json"
        self.pid_file = self.home / ".warp-monitor.pid"
        self.running = False
        self.backup_interval = 1800  # 30 minutes in seconds
        self.last_backup = None
        self.github_config = self.home / ".warp-manager-config.json"
        
        # Load configuration
        self.load_config()
        
        # WARP data manager path
        self.backup_script = self.find_backup_script()
        
    def load_config(self):
        """Load monitor configuration"""
        default_config = {
            "backup_interval_minutes": 30,
            "auto_start": True,
            "log_level": "INFO",
            "backup_types": ["rules", "mcp", "database", "preferences"],
            "github_sync": True,
            "monitor_processes": [
                "warp-terminal",
                "warp", 
                "Warp",
                "warp-gui"
            ]
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        
        self.config = default_config
        self.backup_interval = self.config["backup_interval_minutes"] * 60
        
        # Save config
        self.save_config()
        
    def save_config(self):
        """Save monitor configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def find_backup_script(self) -> Optional[Path]:
        """Find the WARP data manager script"""
        possible_paths = [
            # Current directory and subdirectories
            Path.cwd() / "warp-manager-enhanced.py",
            Path.cwd() / "warp-data-manager" / "warp-manager-enhanced.py",
            
            # Desktop locations
            self.home / "Desktop" / "warp-data-manager" / "warp-data-manager" / "warp-manager-enhanced.py",
            self.home / "Desktop" / "warp-manager-enhanced.py",
            
            # Home directory
            self.home / "warp-manager-enhanced.py",
            self.home / ".local" / "bin" / "warp-manager-enhanced.py",
            
            # System paths
            Path("/usr/local/bin/warp-manager-enhanced.py"),
            Path("/opt/warp-manager/warp-manager-enhanced.py")
        ]
        
        for path in possible_paths:
            if path.exists() and path.is_file():
                logger.info(f"Found backup script: {path}")
                return path
                
        logger.warning("Backup script not found in standard locations")
        return None
    
    def is_warp_running(self) -> bool:
        """Check if any WARP terminal processes are running"""
        warp_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                proc_info = proc.info
                proc_name = proc_info['name'].lower() if proc_info['name'] else ""
                cmdline = ' '.join(proc_info['cmdline']).lower() if proc_info['cmdline'] else ""
                
                # Check for WARP processes
                for warp_name in self.config["monitor_processes"]:
                    if warp_name.lower() in proc_name or warp_name.lower() in cmdline:
                        warp_processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cmdline': proc_info['cmdline']
                        })
                        break
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if warp_processes:
            logger.debug(f"Found {len(warp_processes)} WARP processes")
            for proc in warp_processes:
                logger.debug(f"  PID {proc['pid']}: {proc['name']}")
        
        return len(warp_processes) > 0
    
    def run_backup(self) -> bool:
        """Execute backup with GitHub sync"""
        if not self.backup_script or not self.backup_script.exists():
            logger.error("Backup script not available")
            return False
        
        try:
            logger.info("Starting automated backup...")
            
            # Prepare command
            cmd = [
                "python3", 
                str(self.backup_script),
                "--backup"
            ] + self.config["backup_types"]
            
            if self.config.get("github_sync", True):
                cmd.append("--upload")
            
            # Execute backup
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                logger.info("✅ Backup completed successfully")
                if "uploaded to GitHub" in result.stdout.lower():
                    logger.info("📤 Backup uploaded to GitHub")
                return True
            else:
                logger.error(f"❌ Backup failed with code {result.returncode}")
                logger.error(f"STDERR: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Backup timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Backup error: {e}")
            return False
    
    def should_backup(self) -> bool:
        """Check if it's time for a backup"""
        if not self.last_backup:
            return True
            
        time_since_backup = time.time() - self.last_backup
        return time_since_backup >= self.backup_interval
    
    def monitor_loop(self):
        """Main monitoring loop"""
        logger.info("🚀 WARP Terminal Monitor started")
        logger.info(f"📊 Backup interval: {self.config['backup_interval_minutes']} minutes")
        logger.info(f"📦 Backup types: {', '.join(self.config['backup_types'])}")
        logger.info(f"☁️  GitHub sync: {'Enabled' if self.config['github_sync'] else 'Disabled'}")
        
        consecutive_failures = 0
        max_failures = 5
        
        while self.running:
            try:
                warp_active = self.is_warp_running()
                
                if warp_active:
                    logger.debug("WARP terminals detected - monitoring active")
                    
                    if self.should_backup():
                        logger.info("⏰ Backup interval reached - starting backup")
                        
                        if self.run_backup():
                            self.last_backup = time.time()
                            consecutive_failures = 0
                            logger.info(f"✅ Next backup scheduled for {datetime.fromtimestamp(self.last_backup + self.backup_interval).strftime('%H:%M:%S')}")
                        else:
                            consecutive_failures += 1
                            logger.warning(f"❌ Backup failed ({consecutive_failures}/{max_failures})")
                            
                            if consecutive_failures >= max_failures:
                                logger.error("🚨 Too many consecutive backup failures - stopping monitor")
                                break
                else:
                    logger.debug("No WARP terminals detected - standby mode")
                
                # Sleep for 60 seconds between checks
                time.sleep(60)
                
            except KeyboardInterrupt:
                logger.info("🛑 Received interrupt signal")
                break
            except Exception as e:
                logger.error(f"❌ Monitor loop error: {e}")
                time.sleep(60)  # Wait before retrying
        
        logger.info("🛑 WARP Terminal Monitor stopped")
    
    def start_daemon(self):
        """Start the monitor as a daemon process"""
        if self.is_running():
            logger.warning("Monitor is already running")
            return False
            
        # Write PID file
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
        
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        self.running = True
        self.monitor_loop()
        
        # Clean up PID file
        if self.pid_file.exists():
            self.pid_file.unlink()
            
        return True
    
    def stop_daemon(self):
        """Stop the running daemon"""
        if not self.is_running():
            logger.warning("Monitor is not running")
            return False
            
        try:
            pid = self.get_running_pid()
            if pid:
                os.kill(pid, signal.SIGTERM)
                logger.info(f"Sent TERM signal to PID {pid}")
                
                # Wait for process to stop
                for _ in range(10):
                    if not self.is_running():
                        logger.info("Monitor stopped successfully")
                        return True
                    time.sleep(1)
                
                # Force kill if still running
                logger.warning("Force killing monitor process")
                os.kill(pid, signal.SIGKILL)
                
        except ProcessLookupError:
            logger.info("Process already stopped")
        except Exception as e:
            logger.error(f"Failed to stop monitor: {e}")
            return False
            
        # Clean up PID file
        if self.pid_file.exists():
            self.pid_file.unlink()
            
        return True
    
    def is_running(self) -> bool:
        """Check if monitor daemon is running"""
        if not self.pid_file.exists():
            return False
            
        try:
            with open(self.pid_file) as f:
                pid = int(f.read().strip())
            
            # Check if process exists and is our monitor
            try:
                proc = psutil.Process(pid)
                cmdline = ' '.join(proc.cmdline())
                return 'warp_persistent_monitor' in cmdline
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return False
                
        except (ValueError, FileNotFoundError):
            return False
    
    def get_running_pid(self) -> Optional[int]:
        """Get PID of running monitor"""
        if not self.pid_file.exists():
            return None
            
        try:
            with open(self.pid_file) as f:
                return int(f.read().strip())
        except (ValueError, FileNotFoundError):
            return None
    
    def get_status(self) -> Dict:
        """Get monitor status"""
        return {
            "running": self.is_running(),
            "pid": self.get_running_pid(),
            "warp_active": self.is_warp_running(),
            "backup_interval": self.config["backup_interval_minutes"],
            "last_backup": datetime.fromtimestamp(self.last_backup).isoformat() if self.last_backup else None,
            "next_backup": datetime.fromtimestamp(self.last_backup + self.backup_interval).isoformat() if self.last_backup else "When WARP starts",
            "backup_script": str(self.backup_script) if self.backup_script else "Not found",
            "github_configured": self.github_config.exists()
        }
    
    def _signal_handler(self, signum, frame):
        """Handle termination signals"""
        logger.info(f"Received signal {signum}")
        self.running = False

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WARP Terminal Persistent Monitor")
    parser.add_argument("action", choices=["start", "stop", "status", "restart"], 
                       help="Action to perform")
    parser.add_argument("--foreground", "-f", action="store_true", 
                       help="Run in foreground (don't daemonize)")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--interval", type=int, metavar="MINUTES",
                       help="Backup interval in minutes (default: 30)")
    
    args = parser.parse_args()
    
    monitor = WARPMonitor()
    
    # Update config if specified
    if args.interval:
        monitor.config["backup_interval_minutes"] = args.interval
        monitor.save_config()
        monitor.backup_interval = args.interval * 60
        logger.info(f"Set backup interval to {args.interval} minutes")
    
    if args.action == "start":
        if monitor.is_running():
            print("❌ Monitor is already running")
            sys.exit(1)
            
        print("🚀 Starting WARP Terminal Monitor...")
        
        if not monitor.backup_script:
            print("❌ WARP backup script not found")
            print("Please ensure warp-manager-enhanced.py is available")
            sys.exit(1)
        
        if not monitor.github_config.exists():
            print("⚠️  GitHub not configured for backups")
            print("Run: python3 warp-manager-enhanced.py --setup-github")
        
        if args.foreground:
            monitor.start_daemon()
        else:
            # Fork to background
            pid = os.fork()
            if pid == 0:
                # Child process - become daemon
                os.setsid()
                monitor.start_daemon()
            else:
                # Parent process
                print(f"✅ Monitor started in background (PID: {pid})")
    
    elif args.action == "stop":
        if not monitor.is_running():
            print("❌ Monitor is not running")
            sys.exit(1)
            
        print("🛑 Stopping WARP Terminal Monitor...")
        if monitor.stop_daemon():
            print("✅ Monitor stopped successfully")
        else:
            print("❌ Failed to stop monitor")
            sys.exit(1)
    
    elif args.action == "restart":
        if monitor.is_running():
            print("🛑 Stopping existing monitor...")
            monitor.stop_daemon()
            time.sleep(2)
        
        print("🚀 Starting WARP Terminal Monitor...")
        if args.foreground:
            monitor.start_daemon()
        else:
            pid = os.fork()
            if pid == 0:
                os.setsid()
                monitor.start_daemon()
            else:
                print(f"✅ Monitor restarted in background (PID: {pid})")
    
    elif args.action == "status":
        status = monitor.get_status()
        
        print("📊 WARP Terminal Monitor Status")
        print("=" * 35)
        print(f"Running: {'✅ Yes' if status['running'] else '❌ No'}")
        if status['pid']:
            print(f"PID: {status['pid']}")
        print(f"WARP Active: {'✅ Yes' if status['warp_active'] else '❌ No'}")
        print(f"Backup Interval: {status['backup_interval']} minutes")
        print(f"Last Backup: {status['last_backup'] or 'Never'}")
        print(f"Next Backup: {status['next_backup']}")
        print(f"Backup Script: {status['backup_script']}")
        print(f"GitHub Config: {'✅ Yes' if status['github_configured'] else '❌ No'}")

if __name__ == "__main__":
    main()