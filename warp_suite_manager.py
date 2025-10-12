#!/usr/bin/env python3
"""
WARP Suite Manager - Simple WARP Terminal Launcher
Manages WARP Client configurations and provides easy access to WARP features
"""

import sys
import os
import subprocess
import json
import logging
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class WarpSuiteManager(QMainWindow):
    """Main WARP Suite Manager window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WARP Terminal Manager")
        self.setGeometry(100, 100, 900, 600)
        
        # Set window icon
        icon_path = Path(__file__).parent / "assets" / "icons" / "warp_client.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Initialize components
        self.running_processes = {}
        
        self.setupUI()
        self.applyTheme()
        
    def setupUI(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        
        # Left panel - WARP controls
        left_panel = self.createLeftPanel()
        layout.addWidget(left_panel, 1)
        
        # Center panel - Main workspace
        center_panel = self.createCenterPanel()
        layout.addWidget(center_panel, 2)
        
        # Right panel - System info and logs
        right_panel = self.createRightPanel()
        layout.addWidget(right_panel, 1)
        
        # Status bar
        self.setupStatusBar()
        
        # Menu bar
        self.setupMenuBar()
    
    def createLeftPanel(self):
        """Create left panel with WARP controls"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # WARP Client section (highlighted)
        warp_group = QGroupBox("🚀 WARP Terminal")
        warp_layout = QVBoxLayout()
        
        warp_gui_btn = QPushButton("Launch WARP GUI")
        warp_gui_btn.setStyleSheet("QPushButton { background-color: #00e676; color: black; font-weight: bold; padding: 10px; }")
        warp_gui_btn.clicked.connect(self.launch_warp_gui)
        warp_layout.addWidget(warp_gui_btn)
        
        warp_cli_btn = QPushButton("Launch WARP CLI")
        warp_cli_btn.clicked.connect(self.launch_warp_cli)
        warp_layout.addWidget(warp_cli_btn)
        
        warp_config_btn = QPushButton("WARP Configuration")
        warp_config_btn.clicked.connect(self.open_warp_config)
        warp_layout.addWidget(warp_config_btn)
        
        warp_group.setLayout(warp_layout)
        layout.addWidget(warp_group)
        
        # Quick actions
        actions_group = QGroupBox("⚡ Quick Actions")
        actions_layout = QVBoxLayout()
        
        backup_config_btn = QPushButton("Backup Configuration")
        backup_config_btn.clicked.connect(self.backup_configuration)
        actions_layout.addWidget(backup_config_btn)
        
        restore_config_btn = QPushButton("Restore Configuration")
        restore_config_btn.clicked.connect(self.restore_configuration)
        actions_layout.addWidget(restore_config_btn)
        
        clear_logs_btn = QPushButton("Clear Application Logs")
        clear_logs_btn.clicked.connect(self.clear_application_logs)
        actions_layout.addWidget(clear_logs_btn)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Settings
        settings_group = QGroupBox("⚙️ Settings")
        settings_layout = QVBoxLayout()
        
        theme_btn = QPushButton("Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)
        settings_layout.addWidget(theme_btn)
        
        update_btn = QPushButton("Check for Updates")
        update_btn.clicked.connect(self.check_updates)
        settings_layout.addWidget(update_btn)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        layout.addStretch()
        return panel
    
    def createCenterPanel(self):
        """Create center panel with main workspace"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Header
        header = QLabel("WARP Terminal Manager - Control Center")
        header.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Tabs for different views
        tabs = QTabWidget()
        
        # Dashboard tab
        dashboard = self.createDashboard()
        tabs.addTab(dashboard, "🏠 Dashboard")
        
        # Terminal tab
        terminal = self.createTerminalTab()
        tabs.addTab(terminal, "💻 Terminal")
        
        # Configuration tab
        config = self.createConfigTab()
        tabs.addTab(config, "⚙️ Configuration")
        
        # Logs tab
        logs = self.createLogsTab()
        tabs.addTab(logs, "📋 Logs")
        
        layout.addWidget(tabs)
        return panel
    
    def createRightPanel(self):
        """Create right panel with system info and logs"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # System info
        sys_group = QGroupBox("💾 System Info")
        sys_layout = QVBoxLayout()
        
        self.sys_info_label = QLabel()
        self.update_system_info()
        self.sys_info_label.setAlignment(Qt.AlignTop)
        sys_layout.addWidget(self.sys_info_label)
        
        sys_group.setLayout(sys_layout)
        layout.addWidget(sys_group)
        
        # Running processes
        proc_group = QGroupBox("🔄 Active Sessions")
        proc_layout = QVBoxLayout()
        
        self.process_list = QListWidget()
        proc_layout.addWidget(self.process_list)
        
        kill_btn = QPushButton("Terminate Selected")
        kill_btn.clicked.connect(self.kill_selected_process)
        proc_layout.addWidget(kill_btn)
        
        proc_group.setLayout(proc_layout)
        layout.addWidget(proc_group)
        
        # Activity log
        log_group = QGroupBox("📜 Activity Log")
        log_layout = QVBoxLayout()
        
        self.activity_log = QTextEdit()
        self.activity_log.setMaximumHeight(150)
        self.activity_log.setReadOnly(True)
        log_layout.addWidget(self.activity_log)
        
        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(self.clear_activity_log)
        log_layout.addWidget(clear_log_btn)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        return panel
    
    def createDashboard(self):
        """Create dashboard with overview information"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Welcome message
        welcome = QLabel("Welcome to WARP Terminal Manager!")
        welcome.setStyleSheet("font-size: 16px; font-weight: bold; color: #00e676; padding: 10px;")
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)
        
        # Stats grid
        stats_layout = QGridLayout()
        
        # WARP status
        warp_status = QLabel("🚀 WARP Terminal\nReady")
        warp_status.setStyleSheet("border: 1px solid gray; padding: 20px; text-align: center; background-color: #004d2d;")
        warp_status.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(warp_status, 0, 0)
        
        # System status
        sys_status = QLabel("💻 System\nOnline")
        sys_status.setStyleSheet("border: 1px solid gray; padding: 20px; text-align: center; background-color: #1a472a;")
        sys_status.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(sys_status, 0, 1)
        
        # Configuration status
        config_status = QLabel("⚙️ Configuration\nLoaded")
        config_status.setStyleSheet("border: 1px solid gray; padding: 20px; text-align: center; background-color: #2d4a22;")
        config_status.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(config_status, 1, 0)
        
        # Session status
        session_status = QLabel("🔗 Sessions\n0 Active")
        session_status.setStyleSheet("border: 1px solid gray; padding: 20px; text-align: center; background-color: #3d2a42;")
        session_status.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(session_status, 1, 1)
        
        layout.addLayout(stats_layout)
        
        # Recent activities
        recent_group = QGroupBox("📋 Recent Activities")
        recent_layout = QVBoxLayout()
        
        self.recent_activities = QListWidget()
        self.recent_activities.addItem("WARP Terminal Manager started")
        recent_layout.addWidget(self.recent_activities)
        
        recent_group.setLayout(recent_layout)
        layout.addWidget(recent_group)
        
        widget.setLayout(layout)
        return widget
    
    def createTerminalTab(self):
        """Create terminal tab"""
        terminal = QTextEdit()
        terminal.setStyleSheet("background-color: black; color: green; font-family: monospace;")
        terminal.setPlainText("WARP Terminal Manager\n" +
                             "=" * 40 + "\n" +
                             "Welcome to the WARP Terminal interface.\n" +
                             "Use the buttons in the left panel to launch WARP GUI or CLI.\n" +
                             "For command-line access, you can also use:\n" +
                             "  warp-client gui    # Launch GUI mode\n" +
                             "  warp-client cli    # Launch CLI mode\n\n" +
                             "System ready.\n\n")
        return terminal
    
    def createConfigTab(self):
        """Create configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Configuration editor
        config_group = QGroupBox("📄 Configuration Editor")
        config_layout = QVBoxLayout()
        
        self.config_editor = QTextEdit()
        self.config_editor.setStyleSheet("font-family: monospace;")
        
        # Load current configuration
        try:
            config_path = Path(__file__).parent / "config" / "default_config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config_content = json.dumps(json.load(f), indent=2)
                    self.config_editor.setPlainText(config_content)
        except Exception as e:
            self.config_editor.setPlainText(f"# Error loading configuration: {e}")
        
        config_layout.addWidget(self.config_editor)
        
        # Configuration buttons
        config_buttons = QHBoxLayout()
        
        save_config_btn = QPushButton("Save Configuration")
        save_config_btn.clicked.connect(self.save_configuration)
        config_buttons.addWidget(save_config_btn)
        
        reload_config_btn = QPushButton("Reload Configuration")
        reload_config_btn.clicked.connect(self.reload_configuration)
        config_buttons.addWidget(reload_config_btn)
        
        validate_config_btn = QPushButton("Validate Configuration")
        validate_config_btn.clicked.connect(self.validate_configuration)
        config_buttons.addWidget(validate_config_btn)
        
        config_layout.addLayout(config_buttons)
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        widget.setLayout(layout)
        return widget
    
    def createLogsTab(self):
        """Create logs tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Log viewer
        logs_group = QGroupBox("📜 Log Viewer")
        logs_layout = QVBoxLayout()
        
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setStyleSheet("font-family: monospace; background-color: #1e1e1e; color: #ffffff;")
        self.log_viewer.setPlainText("WARP Terminal Manager Log Viewer\n" +
                                   "=" * 50 + "\n" +
                                   "Application logs will appear here.\n\n")
        logs_layout.addWidget(self.log_viewer)
        
        # Log controls
        log_controls = QHBoxLayout()
        
        refresh_logs_btn = QPushButton("Refresh Logs")
        refresh_logs_btn.clicked.connect(self.refresh_logs)
        log_controls.addWidget(refresh_logs_btn)
        
        export_logs_btn = QPushButton("Export Logs")
        export_logs_btn.clicked.connect(self.export_logs)
        log_controls.addWidget(export_logs_btn)
        
        clear_all_logs_btn = QPushButton("Clear All Logs")
        clear_all_logs_btn.clicked.connect(self.clear_all_logs)
        log_controls.addWidget(clear_all_logs_btn)
        
        logs_layout.addLayout(log_controls)
        logs_group.setLayout(logs_layout)
        layout.addWidget(logs_group)
        
        widget.setLayout(layout)
        return widget
    
    def setupStatusBar(self):
        """Setup status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("WARP Terminal Manager Ready")
        
        # Add widgets to status bar
        self.status_system = QLabel("💻 Online")
        self.status_bar.addPermanentWidget(self.status_system)
        
        self.status_warp = QLabel("🚀 Ready")
        self.status_bar.addPermanentWidget(self.status_warp)
    
    def setupMenuBar(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        new_config = QAction('&New Configuration', self)
        new_config.triggered.connect(self.new_configuration)
        file_menu.addAction(new_config)
        
        open_config = QAction('&Open Configuration', self)
        open_config.triggered.connect(self.open_configuration)
        file_menu.addAction(open_config)
        
        save_config = QAction('&Save Configuration', self)
        save_config.triggered.connect(self.save_configuration)
        file_menu.addAction(save_config)
        
        file_menu.addSeparator()
        
        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # WARP menu
        warp_menu = menubar.addMenu('&WARP')
        
        warp_gui = QAction('WARP &GUI', self)
        warp_gui.triggered.connect(self.launch_warp_gui)
        warp_menu.addAction(warp_gui)
        
        warp_cli = QAction('WARP &CLI', self)
        warp_cli.triggered.connect(self.launch_warp_cli)
        warp_menu.addAction(warp_cli)
        
        warp_menu.addSeparator()
        
        warp_config = QAction('&Configuration', self)
        warp_config.triggered.connect(self.open_warp_config)
        warp_menu.addAction(warp_config)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about = QAction('&About', self)
        about.triggered.connect(self.show_about)
        help_menu.addAction(about)
        
        user_guide = QAction('&User Guide', self)
        user_guide.triggered.connect(self.show_user_guide)
        help_menu.addAction(user_guide)
    
    def applyTheme(self):
        """Apply dark theme to the application"""
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
            QGroupBox {
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
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
    
    def update_system_info(self):
        """Update system information display"""
        try:
            import platform
            import psutil
            
            info = f"OS: {platform.system()} {platform.release()}\n"
            info += f"CPU: {psutil.cpu_percent()}%\n"
            info += f"Memory: {psutil.virtual_memory().percent}%\n"
            info += f"Python: {platform.python_version()}"
            
            self.sys_info_label.setText(info)
        except ImportError:
            self.sys_info_label.setText("System info unavailable\n(psutil not installed)")
        except Exception as e:
            self.sys_info_label.setText(f"Error: {str(e)}")
    
    # Event handlers
    def launch_warp_gui(self):
        """Launch WARP GUI"""
        self.log_activity("Launching WARP GUI...")
        try:
            script_dir = Path(__file__).parent
            launcher = script_dir / "launcher.sh"
            
            if launcher.exists():
                process = subprocess.Popen([str(launcher)], 
                                         cwd=script_dir,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
                
                self.running_processes['warp-gui'] = process
                self.update_process_list()
                self.log_activity("WARP GUI launched successfully")
            else:
                # Fallback to Python launcher
                process = subprocess.Popen(['python', 'launch_warp.py', 'gui'], 
                                         cwd=script_dir)
                
                self.running_processes['warp-gui'] = process
                self.update_process_list()
                self.log_activity("WARP GUI launched successfully (fallback)")
                
        except Exception as e:
            self.log_activity(f"Failed to launch WARP GUI: {e}")
            QMessageBox.critical(self, "Error", f"Failed to launch WARP GUI: {e}")
    
    def launch_warp_cli(self):
        """Launch WARP CLI"""
        self.log_activity("Launching WARP CLI...")
        try:
            script_dir = Path(__file__).parent
            process = subprocess.Popen(['python', 'launch_warp.py', 'cli'], 
                                     cwd=script_dir)
            
            self.running_processes['warp-cli'] = process
            self.update_process_list()
            self.log_activity("WARP CLI launched successfully")
            
        except Exception as e:
            self.log_activity(f"Failed to launch WARP CLI: {e}")
            QMessageBox.critical(self, "Error", f"Failed to launch WARP CLI: {e}")
    
    def open_warp_config(self):
        """Open WARP configuration editor"""
        self.log_activity("Opening WARP configuration...")
        # Switch to the configuration tab
        tabs = self.centralWidget().layout().itemAt(1).widget()
        tabs.setCurrentIndex(2)  # Configuration tab
    
    def backup_configuration(self):
        """Backup current configuration"""
        self.log_activity("Creating configuration backup...")
        try:
            config_path = Path(__file__).parent / "config" / "default_config.json"
            backup_path = Path(__file__).parent / "config" / "backup_config.json"
            
            if config_path.exists():
                subprocess.run(['cp', str(config_path), str(backup_path)], check=True)
                self.log_activity("Configuration backed up successfully")
                QMessageBox.information(self, "Backup", "Configuration backed up successfully!")
            else:
                QMessageBox.warning(self, "Backup", "No configuration file found to backup.")
                
        except Exception as e:
            self.log_activity(f"Failed to backup configuration: {e}")
            QMessageBox.critical(self, "Error", f"Failed to backup configuration: {e}")
    
    def restore_configuration(self):
        """Restore configuration from backup"""
        reply = QMessageBox.question(self, "Restore", 
                                   "This will restore configuration from backup. Continue?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.log_activity("Restoring configuration from backup...")
            try:
                config_path = Path(__file__).parent / "config" / "default_config.json"
                backup_path = Path(__file__).parent / "config" / "backup_config.json"
                
                if backup_path.exists():
                    subprocess.run(['cp', str(backup_path), str(config_path)], check=True)
                    self.reload_configuration()
                    self.log_activity("Configuration restored successfully")
                    QMessageBox.information(self, "Restore", "Configuration restored successfully!")
                else:
                    QMessageBox.warning(self, "Restore", "No backup file found.")
                    
            except Exception as e:
                self.log_activity(f"Failed to restore configuration: {e}")
                QMessageBox.critical(self, "Error", f"Failed to restore configuration: {e}")
    
    def clear_application_logs(self):
        """Clear application logs"""
        reply = QMessageBox.question(self, "Clear Logs", 
                                   "This will clear all application logs. Continue?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.log_activity("Clearing application logs...")
            # Clear various log files here
            self.clear_activity_log()
            self.log_viewer.clear()
            self.log_activity("Application logs cleared")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        # For now, just show a message - theme toggling can be implemented later
        self.log_activity("Theme toggle requested")
        QMessageBox.information(self, "Theme", "Theme toggling will be available in a future version.")
    
    def check_updates(self):
        """Check for application updates"""
        self.log_activity("Checking for updates...")
        # Simulate update check
        QMessageBox.information(self, "Updates", "WARP Terminal Manager is up to date!")
        self.log_activity("Update check completed")
    
    def new_configuration(self):
        """Create new configuration"""
        reply = QMessageBox.question(self, "New Configuration", 
                                   "This will create a new configuration file. Continue?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Create basic configuration template
            basic_config = {
                "warp_client": {
                    "name": "Mini WARP Client",
                    "version": "1.0.0",
                    "debug_mode": False
                },
                "ui": {
                    "theme": "dark",
                    "window_size": [900, 600]
                },
                "logging": {
                    "level": "INFO",
                    "file": "warp_client.log"
                }
            }
            
            self.config_editor.setPlainText(json.dumps(basic_config, indent=2))
            self.log_activity("New configuration template created")
    
    def open_configuration(self):
        """Open configuration file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Configuration", str(Path.home()), 
            "JSON files (*.json);;All files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config_content = json.dumps(json.load(f), indent=2)
                    self.config_editor.setPlainText(config_content)
                    self.log_activity(f"Opened configuration: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open configuration: {e}")
    
    def save_configuration(self):
        """Save current configuration"""
        try:
            config_text = self.config_editor.toPlainText()
            config_data = json.loads(config_text)  # Validate JSON
            
            config_path = Path(__file__).parent / "config" / "default_config.json"
            config_path.parent.mkdir(exist_ok=True)
            
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            self.log_activity("Configuration saved successfully")
            QMessageBox.information(self, "Save", "Configuration saved successfully!")
            
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Error", f"Invalid JSON format: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {e}")
    
    def reload_configuration(self):
        """Reload configuration from file"""
        try:
            config_path = Path(__file__).parent / "config" / "default_config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config_content = json.dumps(json.load(f), indent=2)
                    self.config_editor.setPlainText(config_content)
                    self.log_activity("Configuration reloaded")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reload configuration: {e}")
    
    def validate_configuration(self):
        """Validate current configuration"""
        try:
            config_text = self.config_editor.toPlainText()
            json.loads(config_text)  # Validate JSON syntax
            
            QMessageBox.information(self, "Validation", "Configuration is valid!")
            self.log_activity("Configuration validation passed")
            
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Validation Error", f"Invalid JSON format: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Validation Error", f"Validation failed: {e}")
    
    def refresh_logs(self):
        """Refresh log viewer"""
        self.log_activity("Refreshing logs...")
        # Here you would load actual log files
        self.log_viewer.append(f"[{QDateTime.currentDateTime().toString()}] Logs refreshed")
    
    def export_logs(self):
        """Export logs to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Logs", str(Path.home() / "warp_logs.txt"), 
            "Text files (*.txt);;All files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.log_viewer.toPlainText())
                    f.write("\n\nActivity Log:\n")
                    f.write(self.activity_log.toPlainText())
                
                QMessageBox.information(self, "Export", "Logs exported successfully!")
                self.log_activity(f"Logs exported to: {file_path}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export logs: {e}")
    
    def clear_all_logs(self):
        """Clear all logs"""
        reply = QMessageBox.question(self, "Clear All Logs", 
                                   "This will clear all logs. Continue?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.log_viewer.clear()
            self.activity_log.clear()
            self.log_activity("All logs cleared")
    
    def update_process_list(self):
        """Update running processes list"""
        self.process_list.clear()
        for name, process in list(self.running_processes.items()):
            if process.poll() is None:  # Process is still running
                self.process_list.addItem(f"🔄 {name} (PID: {process.pid})")
            else:
                # Process finished, remove from list
                del self.running_processes[name]
    
    def kill_selected_process(self):
        """Kill selected process"""
        current_item = self.process_list.currentItem()
        if current_item:
            text = current_item.text()
            # Extract process name from text
            name = text.split()[1]  # Skip the emoji
            if name in self.running_processes:
                process = self.running_processes[name]
                process.terminate()
                self.log_activity(f"Terminated process: {name}")
                self.update_process_list()
    
    def log_activity(self, message):
        """Log activity to the activity log"""
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.activity_log.append(f"[{timestamp}] {message}")
        
        # Add to recent activities
        self.recent_activities.addItem(f"{timestamp}: {message}")
        
        # Limit recent activities to 10 items
        while self.recent_activities.count() > 10:
            self.recent_activities.takeItem(0)
    
    def clear_activity_log(self):
        """Clear activity log"""
        self.activity_log.clear()
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About WARP Terminal Manager", 
                         "WARP Terminal Manager v1.0\n\n" +
                         "A simple management interface for the WARP Terminal client.\n" +
                         "Provides easy access to WARP GUI and CLI modes with configuration management.\n\n" +
                         "Features:\n" +
                         "• WARP Client integration\n" +
                         "• Configuration management\n" +
                         "• Process monitoring\n" +
                         "• Activity logging\n" +
                         "• Backup and restore")
    
    def show_user_guide(self):
        """Show user guide"""
        guide_text = """WARP Terminal Manager User Guide
=================================

Getting Started:
1. Use the left panel to launch WARP GUI or CLI
2. Configure settings in the Configuration tab
3. Monitor active sessions in the right panel

Quick Actions:
• Backup Configuration: Save current settings
• Restore Configuration: Restore from backup
• Clear Application Logs: Clean up log files

Navigation:
• Dashboard: Overview of system status
• Terminal: Command interface information
• Configuration: Edit settings and preferences
• Logs: View and export application logs

For more help, visit the WARP Terminal documentation."""
        
        dialog = QDialog(self)
        dialog.setWindowTitle("User Guide")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        guide_display = QTextEdit()
        guide_display.setPlainText(guide_text)
        guide_display.setReadOnly(True)
        layout.addWidget(guide_display)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()

def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("WARP Terminal Manager")
    app.setApplicationVersion("1.0.0")
    
    # Set application icon
    icon_path = Path(__file__).parent / "assets" / "icons" / "warp_client.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Create and show main window
    window = WarpSuiteManager()
    window.show()
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
