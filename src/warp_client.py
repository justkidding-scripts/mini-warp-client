#!/usr/bin/env python3
"""
Mini WARP Client - Core Implementation
Advanced terminal client with customizable features and API endpoints
"""

import asyncio
import json
import logging
import os
import subprocess
import time
import websocket
import threading
import requests
import importlib.util
import signal
import atexit
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta

from config_manager import config_manager

@dataclass
class ConnectionStatus:
    connected: bool = False
    authenticated: bool = False
    last_ping: Optional[datetime] = None
    reconnect_attempts: int = 0
    error_message: Optional[str] = None

@dataclass
class RequestMetrics:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0
    bandwidth_used: int = 0

class TokenManager:
    def __init__(self, token_file: str):
        self.token_file = Path(token_file)
        self.tokens = {}
        self.load_tokens()
    
    def load_tokens(self):
        """Load tokens from encrypted file"""
        if self.token_file.exists():
            try:
                with open(self.token_file, 'r') as f:
                    encrypted_tokens = json.load(f)
                
                for key, value in encrypted_tokens.items():
                    if isinstance(value, str) and value.startswith('encrypted:'):
                        self.tokens[key] = config_manager.decrypt_data(value[10:])
                    else:
                        self.tokens[key] = value
            except Exception as e:
                logging.error(f"Failed to load tokens: {e}")
    
    def save_tokens(self):
        """Save tokens to encrypted file"""
        encrypted_tokens = {}
        for key, value in self.tokens.items():
            encrypted_tokens[key] = f"encrypted:{config_manager.encrypt_data(value)}"
        
        self.token_file.parent.mkdir(exist_ok=True)
        with open(self.token_file, 'w') as f:
            json.dump(encrypted_tokens, f, indent=2)
        
        os.chmod(self.token_file, 0o600)
    
    def add_token(self, name: str, token: str, metadata: Dict = None):
        """Add a new token"""
        token_data = {
            'token': token,
            'added_at': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.tokens[name] = json.dumps(token_data)
        self.save_tokens()
    
    def get_token(self, name: str) -> Optional[str]:
        """Get token by name"""
        if name in self.tokens:
            try:
                token_data = json.loads(self.tokens[name])
                return token_data['token']
            except (json.JSONDecodeError, KeyError):
                return self.tokens[name]  # Fallback for simple string tokens
        return None
    
    def list_tokens(self) -> List[str]:
        """List all available token names"""
        return list(self.tokens.keys())

class WARPClient:
    def __init__(self):
        self.config = config_manager
        self.status = ConnectionStatus()
        self.metrics = RequestMetrics()
        self.session = requests.Session()
        self.websocket = None
        self.ws_thread = None
        self.event_callbacks = {}
        self.command_history = []
        self.active_sessions = {}
        
        # Initialize token manager
        token_file = self.config.get('authentication.token_file', './data/tokens.json')
        self.token_manager = TokenManager(token_file)
        
        # Setup session headers
        self.setup_session()
        
        # Initialize modules
        self.modules = {}
        self.load_modules()
        
        logging.info(f"Mini WARP Client initialized - Version {self.config.get('warp_client.version')}")
    
    def setup_session(self):
        """Configure HTTP session with security settings"""
        user_agent = self.config.get('security.user_agent', 'Mini-WARP-Client/1.0.0')
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        # Configure SSL verification
        verify_ssl = self.config.get('security.certificate_validation', True)
        self.session.verify = verify_ssl
        
        # Configure proxy if enabled
        if self.config.get('security.proxy_support'):
            proxy_config = self.config.get('security.proxy_config', {})
            if proxy_config:
                self.session.proxies.update(proxy_config)
    
    def load_modules(self):
        """Load custom modules and plugins"""
        if not self.config.get('features.custom_modules.enabled', True):
            return
        
        modules_dir = Path(self.config.get('features.custom_modules.modules_directory', './modules'))
        if not modules_dir.exists():
            modules_dir.mkdir(exist_ok=True)
            return
        
        for module_file in modules_dir.glob('*.py'):
            if module_file.name.startswith('__'):
                continue
            
            try:
                module_name = module_file.stem
                spec = importlib.util.spec_from_file_location(module_name, module_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'initialize'):
                    self.modules[module_name] = module.initialize(self)
                    logging.info(f"Loaded module: {module_name}")
            except Exception as e:
                logging.error(f"Failed to load module {module_file}: {e}")
    
    def add_event_callback(self, event: str, callback: Callable):
        """Add callback for specific events"""
        if event not in self.event_callbacks:
            self.event_callbacks[event] = []
        self.event_callbacks[event].append(callback)
    
    def emit_event(self, event: str, data: Any = None):
        """Emit event to all registered callbacks"""
        # Check if Python is shutting down
        import sys
        if getattr(sys, 'meta_path', None) is None:
            return  # Avoid callbacks during shutdown
        
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                try:
                    callback(data)
                except Exception as e:
                    # Safe logging that handles shutdown gracefully
                    try:
                        logging.error(f"Error in event callback for {event}: {e}")
                    except:
                        # If logging fails during shutdown, silently ignore
                        pass
    
    def authenticate(self, token: str = None, token_name: str = None) -> bool:
        """Authenticate with WARP API"""
        if not token and token_name:
            token = self.token_manager.get_token(token_name)
        
        if not token:
            logging.error("No token provided for authentication")
            return False
        
        auth_endpoint = self.config.get_all_endpoints().get('auth_endpoint')
        if not auth_endpoint:
            logging.error("Auth endpoint not configured")
            return False
        
        try:
            start_time = time.time()
            response = self.session.post(auth_endpoint, json={'token': token})
            response_time = time.time() - start_time
            
            self.update_metrics(response, response_time)
            
            if response.status_code == 200:
                auth_data = response.json()
                self.session.headers.update({
                    'Authorization': f"Bearer {auth_data.get('access_token', token)}"
                })
                self.status.authenticated = True
                self.emit_event('authenticated', auth_data)
                logging.info("Authentication successful")
                return True
            else:
                logging.error(f"Authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Authentication error: {e}")
            return False
    
    def connect_websocket(self):
        """Connect to WARP WebSocket for real-time communication"""
        ws_url = self.config.get('endpoints.websocket_base')
        if not ws_url:
            logging.error("WebSocket URL not configured")
            return False
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                self.handle_websocket_message(data)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON received: {message}")
        
        def on_error(ws, error):
            logging.error(f"WebSocket error: {error}")
            self.status.connected = False
            self.emit_event('connection_error', error)
        
        def on_close(ws, close_status_code, close_msg):
            logging.info("WebSocket connection closed")
            self.status.connected = False
            self.emit_event('disconnected')
        
        def on_open(ws):
            logging.info("WebSocket connection established")
            self.status.connected = True
            self.status.last_ping = datetime.now()
            self.emit_event('connected')
        
        try:
            self.websocket = websocket.WebSocketApp(
                ws_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                header={'Authorization': self.session.headers.get('Authorization')}
            )
            
            # Start WebSocket in separate thread
            self.ws_thread = threading.Thread(target=self.websocket.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to connect WebSocket: {e}")
            return False
    
    def handle_websocket_message(self, data: Dict):
        """Handle incoming WebSocket messages"""
        msg_type = data.get('type')
        
        if msg_type == 'ping':
            self.websocket.send(json.dumps({'type': 'pong'}))
            self.status.last_ping = datetime.now()
        elif msg_type == 'command_response':
            self.emit_event('command_response', data)
        elif msg_type == 'agent_message':
            self.emit_event('agent_message', data)
        elif msg_type == 'file_update':
            self.emit_event('file_update', data)
        else:
            self.emit_event('websocket_message', data)
    
    def send_websocket_message(self, message: Dict) -> bool:
        """Send message via WebSocket"""
        if not self.websocket or not self.status.connected:
            logging.error("WebSocket not connected")
            return False
        
        try:
            self.websocket.send(json.dumps(message))
            return True
        except Exception as e:
            logging.error(f"Failed to send WebSocket message: {e}")
            return False
    
    def execute_command(self, command: str, working_dir: str = None) -> Dict:
        """Execute terminal command"""
        if not self.config.get('features.terminal.enabled', True):
            return {'error': 'Terminal feature disabled'}
        
        working_dir = working_dir or self.config.get('features.terminal.working_directory', os.getcwd())
        shell = self.config.get('features.terminal.shell', '/bin/bash')
        
        try:
            start_time = time.time()
            
            # Log command if enabled
            if self.config.get('features.terminal.command_logging', True):
                self.command_history.append({
                    'command': command,
                    'timestamp': datetime.now().isoformat(),
                    'working_dir': working_dir
                })
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True,
                executable=shell,
                timeout=self.config.get('features.terminal.timeout', 30)
            )
            
            execution_time = time.time() - start_time
            
            response = {
                'command': command,
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'execution_time': execution_time,
                'working_dir': working_dir
            }
            
            self.emit_event('command_executed', response)
            return response
            
        except subprocess.TimeoutExpired:
            return {'error': 'Command timed out'}
        except Exception as e:
            return {'error': str(e)}
    
    def chat_with_agent(self, message: str, context: Dict = None) -> Dict:
        """Send message to AI agent"""
        if not self.config.get('features.ai_agent.enabled', True):
            return {'error': 'AI agent feature disabled'}
        
        agent_endpoint = self.config.get_all_endpoints().get('agent_endpoint')
        if not agent_endpoint:
            return {'error': 'Agent endpoint not configured'}
        
        payload = {
            'message': message,
            'model': self.config.get('features.ai_agent.model'),
            'max_tokens': self.config.get('features.ai_agent.max_tokens'),
            'temperature': self.config.get('features.ai_agent.temperature'),
            'context': context or {}
        }
        
        try:
            start_time = time.time()
            response = self.session.post(agent_endpoint, json=payload)
            response_time = time.time() - start_time
            
            self.update_metrics(response, response_time)
            
            if response.status_code == 200:
                agent_response = response.json()
                self.emit_event('agent_response', agent_response)
                return agent_response
            else:
                return {'error': f'Agent request failed: {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def upload_file(self, file_path: str, metadata: Dict = None) -> Dict:
        """Upload file to WARP"""
        if not self.config.get('features.file_operations.enabled', True):
            return {'error': 'File operations disabled'}
        
        file_path = Path(file_path)
        if not file_path.exists():
            return {'error': 'File not found'}
        
        max_size = self.config.get('features.file_operations.max_file_size', 10485760)
        if file_path.stat().st_size > max_size:
            return {'error': 'File too large'}
        
        file_endpoint = self.config.get_all_endpoints().get('file_endpoint')
        if not file_endpoint:
            return {'error': 'File endpoint not configured'}
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'application/octet-stream')}
                data = {'metadata': json.dumps(metadata or {})}
                
                start_time = time.time()
                response = self.session.post(file_endpoint, files=files, data=data)
                response_time = time.time() - start_time
                
                self.update_metrics(response, response_time)
                
                if response.status_code == 200:
                    upload_response = response.json()
                    self.emit_event('file_uploaded', upload_response)
                    return upload_response
                else:
                    return {'error': f'Upload failed: {response.status_code}'}
                    
        except Exception as e:
            return {'error': str(e)}
    
    def download_file(self, file_id: str, save_path: str) -> Dict:
        """Download file from WARP"""
        if not self.config.get('features.file_operations.enabled', True):
            return {'error': 'File operations disabled'}
        
        file_endpoint = self.config.get_all_endpoints().get('file_endpoint')
        if not file_endpoint:
            return {'error': 'File endpoint not configured'}
        
        try:
            download_url = f"{file_endpoint}/{file_id}"
            
            start_time = time.time()
            response = self.session.get(download_url, stream=True)
            response_time = time.time() - start_time
            
            self.update_metrics(response, response_time)
            
            if response.status_code == 200:
                save_path = Path(save_path)
                save_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                download_response = {
                    'file_id': file_id,
                    'save_path': str(save_path),
                    'size': save_path.stat().st_size
                }
                
                self.emit_event('file_downloaded', download_response)
                return download_response
            else:
                return {'error': f'Download failed: {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def update_metrics(self, response: requests.Response, response_time: float):
        """Update request metrics"""
        self.metrics.total_requests += 1
        
        if response.status_code < 400:
            self.metrics.successful_requests += 1
        else:
            self.metrics.failed_requests += 1
        
        # Update average response time
        total_time = self.metrics.avg_response_time * (self.metrics.total_requests - 1) + response_time
        self.metrics.avg_response_time = total_time / self.metrics.total_requests
        
        # Track bandwidth
        if hasattr(response, 'content'):
            self.metrics.bandwidth_used += len(response.content)
    
    def get_status(self) -> Dict:
        """Get current client status"""
        return {
            'connection': {
                'connected': self.status.connected,
                'authenticated': self.status.authenticated,
                'last_ping': self.status.last_ping.isoformat() if self.status.last_ping else None,
                'reconnect_attempts': self.status.reconnect_attempts,
                'error_message': self.status.error_message
            },
            'metrics': {
                'total_requests': self.metrics.total_requests,
                'successful_requests': self.metrics.successful_requests,
                'failed_requests': self.metrics.failed_requests,
                'success_rate': self.metrics.successful_requests / max(self.metrics.total_requests, 1) * 100,
                'avg_response_time': self.metrics.avg_response_time,
                'bandwidth_used': self.metrics.bandwidth_used
            },
            'features': self.config.get_enabled_features(),
            'endpoints': self.config.get_all_endpoints(),
            'modules': list(self.modules.keys()),
            'tokens': self.token_manager.list_tokens()
        }
    
    def disconnect(self):
        """Disconnect from WARP services"""
        try:
            if self.websocket:
                self.websocket.close()
            
            # Wait for WebSocket thread to finish with timeout
            if self.ws_thread and self.ws_thread.is_alive():
                self.ws_thread.join(timeout=2.0)
            
            self.status.connected = False
            self.status.authenticated = False
            
            # Only emit event if not shutting down
            import sys
            if getattr(sys, 'meta_path', None) is not None:
                self.emit_event('disconnected')
            
            try:
                logging.info("Disconnected from WARP services")
            except:
                pass  # Ignore logging errors during shutdown
                
        except Exception:
            # Ignore all errors during disconnect to prevent shutdown issues
            pass
    
    def __del__(self):
        """Cleanup on destruction"""
        self.disconnect()

# Signal handler for graceful shutdown
def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    try:
        warp_client.disconnect()
    except:
        pass  # Ignore errors during shutdown
    os._exit(0)

# Cleanup function for atexit
def cleanup_on_exit():
    """Cleanup function called on exit"""
    try:
        warp_client.disconnect()
    except:
        pass  # Ignore errors during shutdown

# Global client instance
warp_client = WARPClient()

# Register signal handlers and exit cleanup
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
atexit.register(cleanup_on_exit)
