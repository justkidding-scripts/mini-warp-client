#!/usr/bin/env python3
"""
Configuration Manager for Mini WARP Client
Handles all configuration loading, validation, and management
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
import base64

class ConfigManager:
    def __init__(self, config_dir: str = "./config"):
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "default_config.json"
        self.user_config_file = self.config_dir / "user_config.json"
        self.encrypted_config_file = self.config_dir / "encrypted_config.json"
        
        self.config = {}
        self.encryption_key = None
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.load_config()
        
        # Setup logging based on config
        self.setup_logging()
    
    def generate_encryption_key(self) -> bytes:
        """Generate a new encryption key for sensitive data"""
        return Fernet.generate_key()
    
    def load_encryption_key(self) -> Optional[bytes]:
        """Load encryption key from file or environment"""
        key_file = self.config_dir / ".encryption_key"
        
        # Try to load from environment first
        env_key = os.getenv('WARP_CLIENT_ENCRYPTION_KEY')
        if env_key:
            try:
                return base64.urlsafe_b64decode(env_key.encode())
            except Exception:
                pass
        
        # Try to load from file
        if key_file.exists():
            try:
                with open(key_file, 'rb') as f:
                    return f.read()
            except Exception:
                pass
        
        # Generate new key if none exists
        key = self.generate_encryption_key()
        try:
            with open(key_file, 'wb') as f:
                f.write(key)
            # Make file readable only by owner
            os.chmod(key_file, 0o600)
        except Exception as e:
            logging.warning(f"Could not save encryption key: {e}")
        
        return key
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive configuration data"""
        if not self.encryption_key:
            self.encryption_key = self.load_encryption_key()
        
        f = Fernet(self.encryption_key)
        encrypted_data = f.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive configuration data"""
        if not self.encryption_key:
            self.encryption_key = self.load_encryption_key()
        
        f = Fernet(self.encryption_key)
        decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = f.decrypt(decoded_data)
        return decrypted_data.decode()
    
    def load_config(self):
        """Load configuration from files"""
        # Load default configuration
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            raise FileNotFoundError(f"Default config file not found: {self.config_file}")
        
        # Override with user configuration if exists
        if self.user_config_file.exists():
            with open(self.user_config_file, 'r') as f:
                user_config = json.load(f)
                self.merge_configs(self.config, user_config)
        
        # Load encrypted configuration if exists
        if self.encrypted_config_file.exists():
            try:
                with open(self.encrypted_config_file, 'r') as f:
                    encrypted_config = json.load(f)
                    
                for key, value in encrypted_config.items():
                    if isinstance(value, str) and value.startswith('encrypted:'):
                        decrypted_value = self.decrypt_data(value[10:])  # Remove 'encrypted:' prefix
                        self.set_nested_value(self.config, key, decrypted_value)
            except Exception as e:
                logging.warning(f"Could not load encrypted config: {e}")
    
    def save_user_config(self):
        """Save user configuration to file"""
        with open(self.user_config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def save_encrypted_value(self, key_path: str, value: str):
        """Save encrypted value to encrypted config file"""
        encrypted_data = {}
        
        # Load existing encrypted config
        if self.encrypted_config_file.exists():
            with open(self.encrypted_config_file, 'r') as f:
                encrypted_data = json.load(f)
        
        # Encrypt and save value
        encrypted_value = f"encrypted:{self.encrypt_data(value)}"
        encrypted_data[key_path] = encrypted_value
        
        with open(self.encrypted_config_file, 'w') as f:
            json.dump(encrypted_data, f, indent=2)
        
        # Make file readable only by owner
        os.chmod(self.encrypted_config_file, 0o600)
    
    def merge_configs(self, base: Dict, override: Dict):
        """Recursively merge configuration dictionaries"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self.merge_configs(base[key], value)
            else:
                base[key] = value
    
    def get(self, key_path: str, default=None):
        """Get configuration value using dot notation (e.g., 'endpoints.api_base')"""
        keys = key_path.split('.')
        current = self.config
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value):
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        current = self.config
        
        # Navigate to parent key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the value
        current[keys[-1]] = value
    
    def set_nested_value(self, config: Dict, key_path: str, value):
        """Set nested value in configuration"""
        keys = key_path.split('.')
        current = config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def validate_config(self) -> bool:
        """Validate configuration structure and required fields"""
        required_sections = [
            'warp_client',
            'endpoints',
            'authentication',
            'features',
            'ui',
            'security',
            'logging'
        ]
        
        for section in required_sections:
            if section not in self.config:
                logging.error(f"Missing required configuration section: {section}")
                return False
        
        # Validate specific required fields
        required_fields = [
            ('endpoints.api_base', str),
            ('authentication.method', str),
            ('logging.level', str),
            ('ui.theme', str)
        ]
        
        for field_path, expected_type in required_fields:
            value = self.get(field_path)
            if value is None:
                logging.error(f"Missing required configuration field: {field_path}")
                return False
            if not isinstance(value, expected_type):
                logging.error(f"Invalid type for {field_path}: expected {expected_type.__name__}, got {type(value).__name__}")
                return False
        
        return True
    
    def setup_logging(self):
        """Setup logging based on configuration"""
        log_level = self.get('logging.level', 'INFO')
        log_file = self.get('logging.file', './data/warp_client.log')
        log_format = self.get('logging.format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def get_all_endpoints(self) -> Dict[str, str]:
        """Get all configured endpoints"""
        base_url = self.get('endpoints.api_base')
        endpoints = {}
        
        endpoint_config = self.get('endpoints', {})
        for key, value in endpoint_config.items():
            if key != 'api_base' and key != 'custom_endpoints' and isinstance(value, str):
                if value.startswith('/'):
                    endpoints[key] = base_url + value
                else:
                    endpoints[key] = value
        
        # Add custom endpoints
        custom_endpoints = self.get('endpoints.custom_endpoints', [])
        for endpoint in custom_endpoints:
            if isinstance(endpoint, dict) and 'name' in endpoint and 'url' in endpoint:
                endpoints[endpoint['name']] = endpoint['url']
        
        return endpoints
    
    def get_enabled_features(self) -> Dict[str, bool]:
        """Get all enabled features"""
        features = {}
        features_config = self.get('features', {})
        
        for feature, config in features_config.items():
            if isinstance(config, dict) and 'enabled' in config:
                features[feature] = config['enabled']
            elif isinstance(config, bool):
                features[feature] = config
        
        return features
    
    def export_config(self, include_sensitive: bool = False) -> Dict:
        """Export configuration for sharing or backup"""
        config_copy = json.loads(json.dumps(self.config))  # Deep copy
        
        if not include_sensitive:
            # Remove sensitive information
            sensitive_paths = [
                'authentication.token_file',
                'security'
            ]
            
            for path in sensitive_paths:
                keys = path.split('.')
                current = config_copy
                try:
                    for key in keys[:-1]:
                        current = current[key]
                    if keys[-1] in current:
                        del current[keys[-1]]
                except (KeyError, TypeError):
                    pass
        
        return config_copy
    
    def import_config(self, config_data: Dict, merge: bool = True):
        """Import configuration from external source"""
        if merge:
            self.merge_configs(self.config, config_data)
        else:
            self.config = config_data
        
        # Validate after import
        if not self.validate_config():
            raise ValueError("Imported configuration is invalid")

# Singleton instance
config_manager = ConfigManager()
