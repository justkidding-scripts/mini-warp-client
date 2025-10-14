#!/usr/bin/env python3
"""
Mini WARP Client Launcher - GUI Interface
Advanced launcher with full customization capabilities
"""

import sys
import json
import logging
import os
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import importlib.util

from datetime import datetime
# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from config_manager import config_manager
from warp_client import warp_client

class ConfigEditor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("WARP Client Configuration")
        self.setMinimumSize(800, 600)
        self.config = config_manager
        self.setupUI()
    
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Create tabs for different configuration sections
        tabs = QTabWidget()
        
        # General tab
        general_tab = self.createGeneralTab()
        tabs.addTab(general_tab, "General")
        
        # Endpoints tab
        endpoints_tab = self.createEndpointsTab()
        tabs.addTab(endpoints_tab, "Endpoints")
        
        # Authentication tab
        auth_tab = self.createAuthTab()
        tabs.addTab(auth_tab, "Authentication")
        
        # Features tab
        features_tab = self.createFeaturesTab()
        tabs.addTab(features_tab, "Features")
        
        # UI tab
        ui_tab = self.createUITab()
        tabs.addTab(ui_tab, "UI Settings")
        
        # Security tab
        security_tab = self.createSecurityTab()
        tabs.addTab(security_tab, "Security")
        
        # Custom Endpoints tab
        custom_endpoints_tab = self.createCustomEndpointsTab()
        tabs.addTab(custom_endpoints_tab, "Custom Endpoints")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.saveConfig)
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.resetToDefaults)
        
        export_btn = QPushButton("Export Config")
        export_btn.clicked.connect(self.exportConfig)
        
        import_btn = QPushButton("Import Config")
        import_btn.clicked.connect(self.importConfig)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(import_btn)
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def createGeneralTab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Client name
        self.client_name = QLineEdit(self.config.get('warp_client.name', ''))
        layout.addRow("Client Name:", self.client_name)
        
        # Version
        self.version = QLineEdit(self.config.get('warp_client.version', ''))
        layout.addRow("Version:", self.version)
        
        # Debug mode
        self.debug_mode = QCheckBox()
        self.debug_mode.setChecked(self.config.get('warp_client.debug_mode', False))
        layout.addRow("Debug Mode:", self.debug_mode)
        
        # Logs enabled
        self.logs_enabled = QCheckBox()
        self.logs_enabled.setChecked(self.config.get('warp_client.logs_enabled', True))
        layout.addRow("Logs Enabled:", self.logs_enabled)
        
        # Auto connect
        self.auto_connect = QCheckBox()
        self.auto_connect.setChecked(self.config.get('warp_client.auto_connect', False))
        layout.addRow("Auto Connect:", self.auto_connect)
        
        # Log level
        self.log_level = QComboBox()
        self.log_level.addItems(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
        self.log_level.setCurrentText(self.config.get('logging.level', 'INFO'))
        layout.addRow("Log Level:", self.log_level)
        
        widget.setLayout(layout)
        return widget
    
    def createEndpointsTab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # API Base
        self.api_base = QLineEdit(self.config.get('endpoints.api_base', ''))
        layout.addRow("API Base URL:", self.api_base)
        
        # WebSocket Base
        self.websocket_base = QLineEdit(self.config.get('endpoints.websocket_base', ''))
        layout.addRow("WebSocket Base URL:", self.websocket_base)
        
        # Standard endpoints
        endpoints = ['auth_endpoint', 'token_endpoint', 'agent_endpoint', 'command_endpoint', 'file_endpoint', 'mcp_endpoint']
        self.endpoint_fields = {}
        
        for endpoint in endpoints:
            field = QLineEdit(self.config.get(f'endpoints.{endpoint}', ''))
            self.endpoint_fields[endpoint] = field
            layout.addRow(f"{endpoint.replace('_', ' ').title()}:", field)
        
        widget.setLayout(layout)
        return widget
    
    def createAuthTab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Authentication method
        self.auth_method = QComboBox()
        self.auth_method.addItems(['token', 'oauth', 'basic', 'api_key'])
        self.auth_method.setCurrentText(self.config.get('authentication.method', 'token'))
        layout.addRow("Auth Method:", self.auth_method)
        
        # Token file
        token_layout = QHBoxLayout()
        self.token_file = QLineEdit(self.config.get('authentication.token_file', ''))
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browseTokenFile)
        token_layout.addWidget(self.token_file)
        token_layout.addWidget(browse_btn)
        layout.addRow("Token File:", token_layout)
        
        # Refresh threshold
        self.refresh_threshold = QSpinBox()
        self.refresh_threshold.setRange(0, 3600)
        self.refresh_threshold.setValue(self.config.get('authentication.refresh_threshold', 300))
        layout.addRow("Refresh Threshold (sec):", self.refresh_threshold)
        
        # Auto refresh
        self.auto_refresh = QCheckBox()
        self.auto_refresh.setChecked(self.config.get('authentication.auto_refresh', True))
        layout.addRow("Auto Refresh:", self.auto_refresh)
        
        # Encryption enabled
        self.encryption_enabled = QCheckBox()
        self.encryption_enabled.setChecked(self.config.get('authentication.encryption_enabled', True))
        layout.addRow("Encryption Enabled:", self.encryption_enabled)
        
        widget.setLayout(layout)
        return widget
    
    def createFeaturesTab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QFormLayout()
        
        # AI Agent features
        ai_group = QGroupBox("AI Agent")
        ai_layout = QFormLayout()
        
        self.ai_enabled = QCheckBox()
        self.ai_enabled.setChecked(self.config.get('features.ai_agent.enabled', True))
        ai_layout.addRow("Enabled:", self.ai_enabled)
        
        self.ai_model = QComboBox()
        self.ai_model.addItems(['claude-3-5-sonnet-20241022', 'gpt-4', 'gpt-3.5-turbo'])
        self.ai_model.setCurrentText(self.config.get('features.ai_agent.model', 'claude-3-5-sonnet-20241022'))
        ai_layout.addRow("Model:", self.ai_model)
        
        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(1, 8192)
        self.max_tokens.setValue(self.config.get('features.ai_agent.max_tokens', 4096))
        ai_layout.addRow("Max Tokens:", self.max_tokens)
        
        self.temperature = QDoubleSpinBox()
        self.temperature.setRange(0.0, 2.0)
        self.temperature.setSingleStep(0.1)
        self.temperature.setValue(self.config.get('features.ai_agent.temperature', 0.1))
        ai_layout.addRow("Temperature:", self.temperature)
        
        ai_group.setLayout(ai_layout)
        scroll_layout.addRow(ai_group)
        
        # Terminal features
        terminal_group = QGroupBox("Terminal")
        terminal_layout = QFormLayout()
        
        self.terminal_enabled = QCheckBox()
        self.terminal_enabled.setChecked(self.config.get('features.terminal.enabled', True))
        terminal_layout.addRow("Enabled:", self.terminal_enabled)
        
        self.shell = QLineEdit(self.config.get('features.terminal.shell', '/bin/bash'))
        terminal_layout.addRow("Shell:", self.shell)
        
        self.working_dir = QLineEdit(self.config.get('features.terminal.working_directory', '/home/nike'))
        terminal_layout.addRow("Working Directory:", self.working_dir)
        
        self.command_logging = QCheckBox()
        self.command_logging.setChecked(self.config.get('features.terminal.command_logging', True))
        terminal_layout.addRow("Command Logging:", self.command_logging)
        
        terminal_group.setLayout(terminal_layout)
        scroll_layout.addRow(terminal_group)
        
        # File Operations
        file_group = QGroupBox("File Operations")
        file_layout = QFormLayout()
        
        self.file_ops_enabled = QCheckBox()
        self.file_ops_enabled.setChecked(self.config.get('features.file_operations.enabled', True))
        file_layout.addRow("Enabled:", self.file_ops_enabled)
        
        self.max_file_size = QSpinBox()
        self.max_file_size.setRange(1024, 100*1024*1024)
        self.max_file_size.setValue(self.config.get('features.file_operations.max_file_size', 10485760))
        file_layout.addRow("Max File Size (bytes):", self.max_file_size)
        
        file_group.setLayout(file_layout)
        scroll_layout.addRow(file_group)
        
        # Network Monitoring
        network_group = QGroupBox("Network Monitoring")
        network_layout = QFormLayout()
        
        self.network_enabled = QCheckBox()
        self.network_enabled.setChecked(self.config.get('features.network_monitoring.enabled', True))
        network_layout.addRow("Enabled:", self.network_enabled)
        
        self.log_requests = QCheckBox()
        self.log_requests.setChecked(self.config.get('features.network_monitoring.log_requests', True))
        network_layout.addRow("Log Requests:", self.log_requests)
        
        self.bandwidth_monitoring = QCheckBox()
        self.bandwidth_monitoring.setChecked(self.config.get('features.network_monitoring.bandwidth_monitoring', True))
        network_layout.addRow("Bandwidth Monitoring:", self.bandwidth_monitoring)
        
        network_group.setLayout(network_layout)
        scroll_layout.addRow(network_group)
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        widget.setLayout(layout)
        return widget
    
    def createUITab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Theme
        self.theme = QComboBox()
        self.theme.addItems(['dark', 'light', 'auto'])
        self.theme.setCurrentText(self.config.get('ui.theme', 'dark'))
        layout.addRow("Theme:", self.theme)
        
        # Font family
        self.font_family = QFontComboBox()
        self.font_family.setCurrentText(self.config.get('ui.font_family', 'Fira Code'))
        layout.addRow("Font Family:", self.font_family)
        
        # Font size
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(self.config.get('ui.font_size', 12))
        layout.addRow("Font Size:", self.font_size)
        
        # Window size
        size_layout = QHBoxLayout()
        self.window_width = QSpinBox()
        self.window_width.setRange(400, 2560)
        self.window_width.setValue(self.config.get('ui.window_size', [1200, 800])[0])
        
        self.window_height = QSpinBox()
        self.window_height.setRange(300, 1440)
        self.window_height.setValue(self.config.get('ui.window_size', [1200, 800])[1])
        
        size_layout.addWidget(QLabel("Width:"))
        size_layout.addWidget(self.window_width)
        size_layout.addWidget(QLabel("Height:"))
        size_layout.addWidget(self.window_height)
        
        layout.addRow("Window Size:", size_layout)
        
        # UI options
        self.show_status_bar = QCheckBox()
        self.show_status_bar.setChecked(self.config.get('ui.show_status_bar', True))
        layout.addRow("Show Status Bar:", self.show_status_bar)
        
        self.show_debug_panel = QCheckBox()
        self.show_debug_panel.setChecked(self.config.get('ui.show_debug_panel', True))
        layout.addRow("Show Debug Panel:", self.show_debug_panel)
        
        widget.setLayout(layout)
        return widget
    
    def createSecurityTab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Token encryption
        self.token_encryption = QCheckBox()
        self.token_encryption.setChecked(self.config.get('security.token_encryption', True))
        layout.addRow("Token Encryption:", self.token_encryption)
        
        # Request signing
        self.request_signing = QCheckBox()
        self.request_signing.setChecked(self.config.get('security.request_signing', False))
        layout.addRow("Request Signing:", self.request_signing)
        
        # Certificate validation
        self.cert_validation = QCheckBox()
        self.cert_validation.setChecked(self.config.get('security.certificate_validation', True))
        layout.addRow("Certificate Validation:", self.cert_validation)
        
        # Proxy support
        self.proxy_support = QCheckBox()
        self.proxy_support.setChecked(self.config.get('security.proxy_support', True))
        layout.addRow("Proxy Support:", self.proxy_support)
        
        # User agent
        self.user_agent = QLineEdit(self.config.get('security.user_agent', 'Mini-WARP-Client/1.0.0'))
        layout.addRow("User Agent:", self.user_agent)
        
        widget.setLayout(layout)
        return widget
    
    def createCustomEndpointsTab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Custom endpoints list
        self.endpoints_list = QListWidget()
        self.loadCustomEndpoints()
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Endpoint")
        add_btn.clicked.connect(self.addCustomEndpoint)
        
        edit_btn = QPushButton("Edit Endpoint")
        edit_btn.clicked.connect(self.editCustomEndpoint)
        
        remove_btn = QPushButton("Remove Endpoint")
        remove_btn.clicked.connect(self.removeCustomEndpoint)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addStretch()
        
        layout.addWidget(QLabel("Custom Endpoints:"))
        layout.addWidget(self.endpoints_list)
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def loadCustomEndpoints(self):
        endpoints = self.config.get('endpoints.custom_endpoints', [])
        self.endpoints_list.clear()
        for endpoint in endpoints:
            if isinstance(endpoint, dict) and 'name' in endpoint and 'url' in endpoint:
                self.endpoints_list.addItem(f"{endpoint['name']}: {endpoint['url']}")
    
    def addCustomEndpoint(self):
        dialog = CustomEndpointDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            endpoint_data = dialog.getEndpointData()
            endpoints = self.config.get('endpoints.custom_endpoints', [])
            endpoints.append(endpoint_data)
            self.config.set('endpoints.custom_endpoints', endpoints)
            self.loadCustomEndpoints()
    
    def editCustomEndpoint(self):
        current_row = self.endpoints_list.currentRow()
        if current_row >= 0:
            endpoints = self.config.get('endpoints.custom_endpoints', [])
            if current_row < len(endpoints):
                dialog = CustomEndpointDialog(self, endpoints[current_row])
                if dialog.exec_() == QDialog.Accepted:
                    endpoints[current_row] = dialog.getEndpointData()
                    self.config.set('endpoints.custom_endpoints', endpoints)
                    self.loadCustomEndpoints()
    
    def removeCustomEndpoint(self):
        current_row = self.endpoints_list.currentRow()
        if current_row >= 0:
            endpoints = self.config.get('endpoints.custom_endpoints', [])
            if current_row < len(endpoints):
                endpoints.pop(current_row)
                self.config.set('endpoints.custom_endpoints', endpoints)
                self.loadCustomEndpoints()
    
    def browseTokenFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Token File", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
            self.token_file.setText(file_path)
    
    def saveConfig(self):
        # Save all configuration changes
        self.config.set('warp_client.name', self.client_name.text())
        self.config.set('warp_client.version', self.version.text())
        self.config.set('warp_client.debug_mode', self.debug_mode.isChecked())
        self.config.set('warp_client.logs_enabled', self.logs_enabled.isChecked())
        self.config.set('warp_client.auto_connect', self.auto_connect.isChecked())
        self.config.set('logging.level', self.log_level.currentText())
        
        # Endpoints
        self.config.set('endpoints.api_base', self.api_base.text())
        self.config.set('endpoints.websocket_base', self.websocket_base.text())
        for endpoint, field in self.endpoint_fields.items():
            self.config.set(f'endpoints.{endpoint}', field.text())
        
        # Authentication
        self.config.set('authentication.method', self.auth_method.currentText())
        self.config.set('authentication.token_file', self.token_file.text())
        self.config.set('authentication.refresh_threshold', self.refresh_threshold.value())
        self.config.set('authentication.auto_refresh', self.auto_refresh.isChecked())
        self.config.set('authentication.encryption_enabled', self.encryption_enabled.isChecked())
        
        # Features
        self.config.set('features.ai_agent.enabled', self.ai_enabled.isChecked())
        self.config.set('features.ai_agent.model', self.ai_model.currentText())
        self.config.set('features.ai_agent.max_tokens', self.max_tokens.value())
        self.config.set('features.ai_agent.temperature', self.temperature.value())
        
        self.config.set('features.terminal.enabled', self.terminal_enabled.isChecked())
        self.config.set('features.terminal.shell', self.shell.text())
        self.config.set('features.terminal.working_directory', self.working_dir.text())
        self.config.set('features.terminal.command_logging', self.command_logging.isChecked())
        
        self.config.set('features.file_operations.enabled', self.file_ops_enabled.isChecked())
        self.config.set('features.file_operations.max_file_size', self.max_file_size.value())
        
        self.config.set('features.network_monitoring.enabled', self.network_enabled.isChecked())
        self.config.set('features.network_monitoring.log_requests', self.log_requests.isChecked())
        self.config.set('features.network_monitoring.bandwidth_monitoring', self.bandwidth_monitoring.isChecked())
        
        # UI
        self.config.set('ui.theme', self.theme.currentText())
        self.config.set('ui.font_family', self.font_family.currentText())
        self.config.set('ui.font_size', self.font_size.value())
        self.config.set('ui.window_size', [self.window_width.value(), self.window_height.value()])
        self.config.set('ui.show_status_bar', self.show_status_bar.isChecked())
        self.config.set('ui.show_debug_panel', self.show_debug_panel.isChecked())
        
        # Security
        self.config.set('security.token_encryption', self.token_encryption.isChecked())
        self.config.set('security.request_signing', self.request_signing.isChecked())
        self.config.set('security.certificate_validation', self.cert_validation.isChecked())
        self.config.set('security.proxy_support', self.proxy_support.isChecked())
        self.config.set('security.user_agent', self.user_agent.text())
        
        # Save to file
        self.config.save_user_config()
        QMessageBox.information(self, "Success", "Configuration saved successfully!")
    
    def resetToDefaults(self):
        reply = QMessageBox.question(self, "Reset Configuration", 
                                   "Are you sure you want to reset to default configuration?\nThis will overwrite all current settings.",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Reload default configuration
            self.config.load_config()
            self.close()
            QMessageBox.information(self, "Reset Complete", "Configuration has been reset to defaults.")
    
    def exportConfig(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Configuration", "warp_config.json", "JSON Files (*.json)")
        if file_path:
            config_data = self.config.export_config(include_sensitive=False)
            with open(file_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            QMessageBox.information(self, "Export Complete", f"Configuration exported to {file_path}")
    
    def importConfig(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Configuration", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config_data = json.load(f)
                self.config.import_config(config_data, merge=True)
                QMessageBox.information(self, "Import Complete", "Configuration imported successfully!")
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import configuration: {str(e)}")

class CustomEndpointDialog(QDialog):
    def __init__(self, parent=None, endpoint_data=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Endpoint")
        self.setMinimumWidth(400)
        self.endpoint_data = endpoint_data or {}
        self.setupUI()
    
    def setupUI(self):
        layout = QFormLayout()
        
        self.name_field = QLineEdit(self.endpoint_data.get('name', ''))
        layout.addRow("Name:", self.name_field)
        
        self.url_field = QLineEdit(self.endpoint_data.get('url', ''))
        layout.addRow("URL:", self.url_field)
        
        self.method_field = QComboBox()
        self.method_field.addItems(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
        self.method_field.setCurrentText(self.endpoint_data.get('method', 'GET'))
        layout.addRow("Method:", self.method_field)
        
        self.description_field = QTextEdit(self.endpoint_data.get('description', ''))
        self.description_field.setMaximumHeight(100)
        layout.addRow("Description:", self.description_field)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def getEndpointData(self):
        return {
            'name': self.name_field.text(),
            'url': self.url_field.text(),
            'method': self.method_field.currentText(),
            'description': self.description_field.toPlainText()
        }

class TokenManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Token Manager")
        self.setMinimumSize(600, 400)
        self.setupUI()
    
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Tokens list
        self.tokens_list = QListWidget()
        self.loadTokens()
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Token")
        add_btn.clicked.connect(self.addToken)
        
        edit_btn = QPushButton("Edit Token")
        edit_btn.clicked.connect(self.editToken)
        
        remove_btn = QPushButton("Remove Token")
        remove_btn.clicked.connect(self.removeToken)
        
        test_btn = QPushButton("Test Token")
        test_btn.clicked.connect(self.testToken)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addWidget(test_btn)
        btn_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addWidget(QLabel("Available Tokens:"))
        layout.addWidget(self.tokens_list)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def loadTokens(self):
        self.tokens_list.clear()
        tokens = warp_client.token_manager.list_tokens()
        for token_name in tokens:
            self.tokens_list.addItem(token_name)
    
    def addToken(self):
        dialog = TokenDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, token, metadata = dialog.getTokenData()
            warp_client.token_manager.add_token(name, token, metadata)
            self.loadTokens()
    
    def editToken(self):
        current_item = self.tokens_list.currentItem()
        if current_item:
            token_name = current_item.text()
            current_token = warp_client.token_manager.get_token(token_name)
            dialog = TokenDialog(self, token_name, current_token)
            if dialog.exec_() == QDialog.Accepted:
                name, token, metadata = dialog.getTokenData()
                warp_client.token_manager.add_token(name, token, metadata)
                self.loadTokens()
    
    def removeToken(self):
        current_item = self.tokens_list.currentItem()
        if current_item:
            token_name = current_item.text()
            reply = QMessageBox.question(self, "Remove Token", 
                                       f"Are you sure you want to remove token '{token_name}'?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if token_name in warp_client.token_manager.tokens:
                    del warp_client.token_manager.tokens[token_name]
                    warp_client.token_manager.save_tokens()
                    self.loadTokens()
    
    def testToken(self):
        current_item = self.tokens_list.currentItem()
        if current_item:
            token_name = current_item.text()
            if warp_client.authenticate(token_name=token_name):
                QMessageBox.information(self, "Token Test", f"Token '{token_name}' is valid!")
            else:
                QMessageBox.warning(self, "Token Test", f"Token '{token_name}' authentication failed!")

class TokenDialog(QDialog):
    def __init__(self, parent=None, name="", token=""):
        super().__init__(parent)
        self.setWindowTitle("Token Details")
        self.setMinimumWidth(400)
        self.setupUI()
        
        if name:
            self.name_field.setText(name)
        if token:
            self.token_field.setText(token)
    
    def setupUI(self):
        layout = QFormLayout()
        
        self.name_field = QLineEdit()
        layout.addRow("Token Name:", self.name_field)
        
        self.token_field = QLineEdit()
        self.token_field.setEchoMode(QLineEdit.Password)
        layout.addRow("Token:", self.token_field)
        
        show_token_btn = QPushButton("Show/Hide")
        show_token_btn.clicked.connect(self.toggleTokenVisibility)
        layout.addRow("", show_token_btn)
        
        self.description_field = QTextEdit()
        self.description_field.setMaximumHeight(100)
        layout.addRow("Description:", self.description_field)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def toggleTokenVisibility(self):
        if self.token_field.echoMode() == QLineEdit.Password:
            self.token_field.setEchoMode(QLineEdit.Normal)
        else:
            self.token_field.setEchoMode(QLineEdit.Password)
    
    def getTokenData(self):
        return (
            self.name_field.text(),
            self.token_field.text(),
            {'description': self.description_field.toPlainText()}
        )

class WarpLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini WARP Client Launcher")
        self.setGeometry(100, 100, 1000, 700)
        
        # Apply theme
        self.applyTheme()
        
        # Setup UI
        self.setupUI()
        
        # Setup status updates
        self.setupStatusUpdates()
        
        # Load initial status
        self.updateStatus()
    
    def applyTheme(self):
        theme = config_manager.get('ui.theme', 'dark')
        if theme == 'dark':
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #404040;
                    border: 1px solid #555555;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
                QPushButton:pressed {
                    background-color: #606060;
                }
                QTextEdit, QListWidget {
                    background-color: #1e1e1e;
                    border: 1px solid #404040;
                    border-radius: 4px;
                }
                QTabWidget::pane {
                    border: 1px solid #404040;
                    background-color: #2b2b2b;
                }
                QTabBar::tab {
                    background-color: #404040;
                    border: 1px solid #555555;
                    padding: 8px;
                }
                QTabBar::tab:selected {
                    background-color: #505050;
                }
            """)
    
    def setupUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Mini WARP Client")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Status indicator
        self.status_label = QLabel("Disconnected")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)
        
        # Main content
        content_layout = QHBoxLayout()
        
        # Left panel - Configuration and controls
        left_panel = QWidget()
        left_panel.setMinimumWidth(300)
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # Configuration section
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout()
        
        config_btn = QPushButton("Edit Configuration")
        config_btn.clicked.connect(self.openConfigEditor)
        config_layout.addWidget(config_btn)
        
        tokens_btn = QPushButton("Manage Tokens")
        tokens_btn.clicked.connect(self.openTokenManager)
        config_layout.addWidget(tokens_btn)
        
        export_btn = QPushButton("Export Logs")
        export_btn.clicked.connect(self.exportLogs)
        config_layout.addWidget(export_btn)
        
        config_group.setLayout(config_layout)
        left_layout.addWidget(config_group)
        
        # Connection section
        connection_group = QGroupBox("Connection")
        connection_layout = QVBoxLayout()
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.toggleConnection)
        connection_layout.addWidget(self.connect_btn)
        
        self.auth_btn = QPushButton("Authenticate")
        self.auth_btn.clicked.connect(self.authenticate)
        connection_layout.addWidget(self.auth_btn)
        
        test_btn = QPushButton("Test Connection")
        test_btn.clicked.connect(self.testConnection)
        connection_layout.addWidget(test_btn)
        
        connection_group.setLayout(connection_layout)
        left_layout.addWidget(connection_group)
        
        # Features section
        features_group = QGroupBox("Features")
        features_layout = QVBoxLayout()
        
        terminal_btn = QPushButton("Open Terminal")
        terminal_btn.clicked.connect(self.openTerminal)
        features_layout.addWidget(terminal_btn)
        
        agent_btn = QPushButton("Chat with Agent")
        agent_btn.clicked.connect(self.openAgentChat)
        features_layout.addWidget(agent_btn)
        
        files_btn = QPushButton("File Manager")
        files_btn.clicked.connect(self.openFileManager)
        features_layout.addWidget(files_btn)
        
        features_group.setLayout(features_layout)
        left_layout.addWidget(features_group)
        
        left_layout.addStretch()
        content_layout.addWidget(left_panel)
        
        # Right panel - Status and logs
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Tabs for different views
        tabs = QTabWidget()
        
        # Status tab
        status_widget = QWidget()
        status_layout = QVBoxLayout()
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        status_layout.addWidget(self.status_text)
        
        status_widget.setLayout(status_layout)
        tabs.addTab(status_widget, "Status")
        
        # Logs tab
        logs_widget = QWidget()
        logs_layout = QVBoxLayout()
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        logs_layout.addWidget(self.logs_text)
        
        clear_logs_btn = QPushButton("Clear Logs")
        clear_logs_btn.clicked.connect(self.clearLogs)
        logs_layout.addWidget(clear_logs_btn)
        
        logs_widget.setLayout(logs_layout)
        tabs.addTab(logs_widget, "Logs")
        
        # Metrics tab
        metrics_widget = QWidget()
        metrics_layout = QVBoxLayout()
        
        self.metrics_text = QTextEdit()
        self.metrics_text.setReadOnly(True)
        metrics_layout.addWidget(self.metrics_text)
        
        metrics_widget.setLayout(metrics_layout)
        tabs.addTab(metrics_widget, "Metrics")
        
        right_layout.addWidget(tabs)
        content_layout.addWidget(right_panel)
        
        layout.addLayout(content_layout)
        
        # Status bar
        if config_manager.get('ui.show_status_bar', True):
            self.status_bar = self.statusBar()
            self.status_bar.showMessage("Ready")
    
    def setupStatusUpdates(self):
        # Timer for updating status
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.updateStatus)
        self.status_timer.start(5000)  # Update every 5 seconds
        
        # Setup event callbacks
        warp_client.add_event_callback('connected', self.onConnected)
        warp_client.add_event_callback('disconnected', self.onDisconnected)
        warp_client.add_event_callback('authenticated', self.onAuthenticated)
        warp_client.add_event_callback('command_executed', self.onCommandExecuted)
    
    def updateStatus(self):
        status = warp_client.get_status()
        
        # Update connection status
        if status['connection']['connected']:
            self.status_label.setText("Connected")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.connect_btn.setText("Disconnect")
        else:
            self.status_label.setText("Disconnected")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.connect_btn.setText("Connect")
        
        # Update status text
        status_info = f"""
Connection Status: {'Connected' if status['connection']['connected'] else 'Disconnected'}
Authentication: {'Authenticated' if status['connection']['authenticated'] else 'Not Authenticated'}
Last Ping: {status['connection']['last_ping'] or 'Never'}
Total Requests: {status['metrics']['total_requests']}
Success Rate: {status['metrics']['success_rate']:.1f}%
Average Response Time: {status['metrics']['avg_response_time']:.3f}s
Bandwidth Used: {status['metrics']['bandwidth_used']} bytes

Enabled Features:
{chr(10).join(f"- {feature}: {'Yes' if enabled else 'No'}" for feature, enabled in status['features'].items())}

Configured Endpoints:
{chr(10).join(f"- {name}: {url}" for name, url in status['endpoints'].items())}

Available Tokens: {', '.join(status['tokens']) if status['tokens'] else 'None'}
        """
        self.status_text.setPlainText(status_info.strip())
        
        # Update metrics
        metrics_info = f"""
Request Metrics:
- Total Requests: {status['metrics']['total_requests']}
- Successful: {status['metrics']['successful_requests']}
- Failed: {status['metrics']['failed_requests']}
- Success Rate: {status['metrics']['success_rate']:.1f}%
- Average Response Time: {status['metrics']['avg_response_time']:.3f}s
- Bandwidth Used: {self.formatBytes(status['metrics']['bandwidth_used'])}

Connection Metrics:
- Reconnection Attempts: {status['connection']['reconnect_attempts']}
- Current Status: {'Connected' if status['connection']['connected'] else 'Disconnected'}
- Authentication Status: {'Authenticated' if status['connection']['authenticated'] else 'Not Authenticated'}

Loaded Modules: {', '.join(status['modules']) if status['modules'] else 'None'}
        """
        self.metrics_text.setPlainText(metrics_info.strip())
        
        # Update status bar
        if hasattr(self, 'status_bar'):
            self.status_bar.showMessage(f"Status: {'Connected' if status['connection']['connected'] else 'Disconnected'} | "
                                      f"Requests: {status['metrics']['total_requests']} | "
                                      f"Success: {status['metrics']['success_rate']:.1f}%")
    
    def formatBytes(self, bytes_value):
        """Format bytes in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} TB"
    
    def onConnected(self, data):
        self.appendLog("Connected to WARP services")
    
    def onDisconnected(self, data):
        self.appendLog("Disconnected from WARP services")
    
    def onAuthenticated(self, data):
        self.appendLog("Authentication successful")
    
    def onCommandExecuted(self, data):
        self.appendLog(f"Command executed: {data.get('command', 'Unknown')} (Exit code: {data.get('exit_code', 'Unknown')})")
    
    def appendLog(self, message):
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{current_time}] {message}\n"
        self.logs_text.append(log_entry.strip())
        
        # Limit log size
        if self.logs_text.document().lineCount() > 1000:
            cursor = self.logs_text.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, 100)
            cursor.removeSelectedText()
    
    def openConfigEditor(self):
        dialog = ConfigEditor(self)
        dialog.exec_()
        self.updateStatus()
    
    def openTokenManager(self):
        dialog = TokenManager(self)
        dialog.exec_()
    
    def exportLogs(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Logs", "warp_client_logs.txt", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.logs_text.toPlainText())
            QMessageBox.information(self, "Export Complete", f"Logs exported to {file_path}")
    
    def toggleConnection(self):
        if warp_client.status.connected:
            warp_client.disconnect()
        else:
            if warp_client.connect_websocket():
                self.appendLog("Attempting to connect...")
            else:
                self.appendLog("Failed to initiate connection")
    
    def authenticate(self):
        tokens = warp_client.token_manager.list_tokens()
        if not tokens:
            QMessageBox.warning(self, "No Tokens", "No tokens available. Please add a token first.")
            return
        
        token_name, ok = QInputDialog.getItem(self, "Select Token", "Choose a token to authenticate with:", tokens, 0, False)
        if ok and token_name:
            if warp_client.authenticate(token_name=token_name):
                self.appendLog(f"Authentication successful with token: {token_name}")
                QMessageBox.information(self, "Authentication", "Authentication successful!")
            else:
                self.appendLog(f"Authentication failed with token: {token_name}")
                QMessageBox.warning(self, "Authentication", "Authentication failed!")
    
    def testConnection(self):
        # Test basic connectivity
        endpoints = warp_client.config.get_all_endpoints()
        if not endpoints:
            QMessageBox.warning(self, "Test Connection", "No endpoints configured!")
            return
        
        results = []
        for name, url in endpoints.items():
            try:
                response = warp_client.session.get(url, timeout=5)
                status = f"✓ {name}: {response.status_code}"
                results.append(status)
            except Exception as e:
                status = f"✗ {name}: {str(e)[:50]}"
                results.append(status)
        
        result_text = "\n".join(results)
        QMessageBox.information(self, "Connection Test Results", result_text)
    
    def openTerminal(self):
        if not config_manager.get('features.terminal.enabled', True):
            QMessageBox.warning(self, "Feature Disabled", "Terminal feature is disabled in configuration.")
            return
        
        # For now, just show a simple command input dialog
        command, ok = QInputDialog.getText(self, "Terminal Command", "Enter command to execute:")
        if ok and command:
            result = warp_client.execute_command(command)
            
            result_dialog = QDialog(self)
            result_dialog.setWindowTitle("Command Result")
            result_dialog.setMinimumSize(600, 400)
            
            layout = QVBoxLayout()
            
            result_text = QTextEdit()
            result_text.setReadOnly(True)
            
            output = f"Command: {command}\n"
            output += f"Exit Code: {result.get('exit_code', 'Unknown')}\n"
            output += f"Execution Time: {result.get('execution_time', 'Unknown')}s\n\n"
            output += "STDOUT:\n" + result.get('stdout', '') + "\n\n"
            output += "STDERR:\n" + result.get('stderr', '')
            
            result_text.setPlainText(output)
            layout.addWidget(result_text)
            
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(result_dialog.accept)
            layout.addWidget(close_btn)
            
            result_dialog.setLayout(layout)
            result_dialog.exec_()
    
    def openAgentChat(self):
        if not config_manager.get('features.ai_agent.enabled', True):
            QMessageBox.warning(self, "Feature Disabled", "AI agent feature is disabled in configuration.")
            return
        
        message, ok = QInputDialog.getText(self, "Chat with Agent", "Enter your message:")
        if ok and message:
            result = warp_client.chat_with_agent(message)
            
            if 'error' in result:
                QMessageBox.warning(self, "Agent Error", f"Error: {result['error']}")
            else:
                response_text = result.get('response', 'No response received')
                QMessageBox.information(self, "Agent Response", response_text)
    
    def openFileManager(self):
        QMessageBox.information(self, "File Manager", "File manager functionality will be implemented in future updates.")
    
    def clearLogs(self):
        self.logs_text.clear()

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Mini WARP Client")
    app.setApplicationVersion(config_manager.get('warp_client.version', '1.0.0'))
    app.setOrganizationName("WARP Research")
    
    # Create and show launcher
    launcher = WarpLauncher()
    launcher.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
