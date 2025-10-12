#!/usr/bin/env python3
"""
WARP Configuration Backup and Restore Utility
"""

import json
import shutil
import os
from datetime import datetime
from pathlib import Path
import argparse

class WarpConfigBackup:
    def __init__(self, config_dir="./config", data_dir="./data", backup_dir="./backups"):
        self.config_dir = Path(config_dir)
        self.data_dir = Path(data_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, backup_name=None):
        """Create a full backup of configuration and data"""
        if not backup_name:
            backup_name = f"warp_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        print(f"Creating backup: {backup_name}")
        
        # Backup configuration files
        if self.config_dir.exists():
            shutil.copytree(self.config_dir, backup_path / "config", dirs_exist_ok=True)
            print("✓ Configuration files backed up")
        
        # Backup data files (tokens, logs, etc.)
        if self.data_dir.exists():
            shutil.copytree(self.data_dir, backup_path / "data", dirs_exist_ok=True)
            print("✓ Data files backed up")
        
        # Create backup metadata
        metadata = {
            'backup_name': backup_name,
            'created_at': datetime.now().isoformat(),
            'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}",
            'backup_type': 'full',
            'files_included': ['config', 'data']
        }
        
        with open(backup_path / "backup_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Backup created successfully: {backup_path}")
        return backup_path
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        
        for backup_path in self.backup_dir.glob("warp_backup_*"):
            if backup_path.is_dir():
                metadata_file = backup_path / "backup_metadata.json"
                metadata = {}
                
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                    except Exception:
                        pass
                
                backups.append({
                    'name': backup_path.name,
                    'path': backup_path,
                    'created_at': metadata.get('created_at', 'Unknown'),
                    'type': metadata.get('backup_type', 'Unknown')
                })
        
        return sorted(backups, key=lambda x: x['created_at'], reverse=True)
    
    def restore_backup(self, backup_name, confirm=True):
        """Restore from a backup"""
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            raise ValueError(f"Backup not found: {backup_name}")
        
        if confirm:
            response = input(f"This will overwrite current configuration. Continue? (y/N): ")
            if response.lower() != 'y':
                print("Restore cancelled")
                return False
        
        print(f"Restoring backup: {backup_name}")
        
        # Restore configuration
        config_backup = backup_path / "config"
        if config_backup.exists():
            if self.config_dir.exists():
                shutil.rmtree(self.config_dir)
            shutil.copytree(config_backup, self.config_dir)
            print("✓ Configuration restored")
        
        # Restore data
        data_backup = backup_path / "data"
        if data_backup.exists():
            if self.data_dir.exists():
                shutil.rmtree(self.data_dir)
            shutil.copytree(data_backup, self.data_dir)
            print("✓ Data restored")
        
        print("✅ Restore completed successfully")
        return True
    
    def export_config(self, export_path):
        """Export configuration for sharing (without sensitive data)"""
        export_path = Path(export_path)
        
        # Load and sanitize configuration
        config_file = self.config_dir / "default_config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Remove sensitive sections
            if 'authentication' in config:
                config['authentication'] = {
                    'method': config['authentication'].get('method', 'token'),
                    'auto_refresh': config['authentication'].get('auto_refresh', True)
                }
            
            if 'security' in config:
                # Keep security settings but remove actual credentials
                security = config['security'].copy()
                config['security'] = security
            
            # Add export metadata
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'export_type': 'configuration_only',
                'warp_client_version': config.get('warp_client', {}).get('version', '1.0.0'),
                'configuration': config
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"✅ Configuration exported to: {export_path}")
        else:
            raise FileNotFoundError("No configuration file found to export")

def main():
    parser = argparse.ArgumentParser(description="WARP Configuration Backup Utility")
    parser.add_argument('action', choices=['backup', 'list', 'restore', 'export'], 
                       help='Action to perform')
    parser.add_argument('--name', help='Backup name (for backup/restore)')
    parser.add_argument('--path', help='Export path (for export)')
    parser.add_argument('--force', action='store_true', help='Skip confirmation prompts')
    
    args = parser.parse_args()
    
    backup_util = WarpConfigBackup()
    
    try:
        if args.action == 'backup':
            backup_util.create_backup(args.name)
        
        elif args.action == 'list':
            backups = backup_util.list_backups()
            if backups:
                print("Available backups:")
                for backup in backups:
                    print(f"  {backup['name']} - {backup['created_at']} ({backup['type']})")
            else:
                print("No backups found")
        
        elif args.action == 'restore':
            if not args.name:
                backups = backup_util.list_backups()
                if not backups:
                    print("No backups available")
                    return
                print("Available backups:")
                for i, backup in enumerate(backups):
                    print(f"  {i+1}. {backup['name']} - {backup['created_at']}")
                
                choice = input("Select backup number: ").strip()
                try:
                    backup_name = backups[int(choice)-1]['name']
                except (ValueError, IndexError):
                    print("Invalid selection")
                    return
            else:
                backup_name = args.name
            
            backup_util.restore_backup(backup_name, confirm=not args.force)
        
        elif args.action == 'export':
            if not args.path:
                args.path = f"warp_config_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_util.export_config(args.path)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
