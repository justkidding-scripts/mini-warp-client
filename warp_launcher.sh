#!/bin/bash
# WARP Terminal Universal Linux Launcher
# Automatically detects environment and launches appropriate interface

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_banner() {
    echo
    print_color $CYAN "🚀 WARP Terminal Universal Launcher (Linux)"
    print_color $CYAN "============================================="
    echo
}

check_python() {
    print_color $BLUE "🔍 Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_color $GREEN "🐍 Python $PYTHON_VERSION detected"
        return 0
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        if [[ $PYTHON_VERSION == 3.* ]]; then
            print_color $GREEN "🐍 Python $PYTHON_VERSION detected"
            return 0
        else
            print_color $RED "❌ Python 2 detected. Python 3.8+ required."
            return 1
        fi
    else
        print_color $RED "❌ Python not found. Please install Python 3.8 or newer."
        print_color $YELLOW "📥 Install with: sudo apt install python3 python3-pip"
        return 1
    fi
}

check_gui() {
    print_color $BLUE "🖼️  Checking GUI environment..."
    
    if [ -n "$DISPLAY" ]; then
        print_color $GREEN "✅ GUI environment detected (X11)"
        return 0
    elif [ -n "$WAYLAND_DISPLAY" ]; then
        print_color $GREEN "✅ GUI environment detected (Wayland)"
        return 0
    else
        print_color $YELLOW "⚠️  No GUI environment detected - CLI mode only"
        return 1
    fi
}

check_dependencies() {
    print_color $BLUE "📦 Checking dependencies..."
    
    local missing_deps=()
    
    # Check Python packages
    if ! $PYTHON_CMD -c "import PyQt5" &> /dev/null; then
        missing_deps+=("PyQt5")
    fi
    
    if ! $PYTHON_CMD -c "import zstandard" &> /dev/null; then
        missing_deps+=("zstandard")
    fi
    
    if [ ${#missing_deps[@]} -eq 0 ]; then
        print_color $GREEN "✅ All dependencies satisfied"
        return 0
    else
        print_color $YELLOW "⚠️  Missing dependencies: ${missing_deps[*]}"
        print_color $BLUE "💡 Run with 'install' command to auto-install"
        return 1
    fi
}

show_help() {
    echo "WARP Terminal Universal Launcher"
    echo
    echo "Usage: $0 [command]"
    echo
    echo "Available commands:"
    echo "  gui      Launch GUI interface (default)"
    echo "  cli      Launch CLI interface"
    echo "  setup    Complete system setup"
    echo "  status   Show system status"
    echo "  config   Configure launcher"
    echo "  backup   Create backup"
    echo "  install  Install dependencies"
    echo "  help     Show this help message"
    echo
    echo "Examples:"
    echo "  $0              # Launch GUI (default)"
    echo "  $0 cli          # Launch CLI"
    echo "  $0 setup        # Complete setup"
    echo "  $0 status       # Show status"
}

launch_gui() {
    print_color $CYAN "🚀 Launching WARP Terminal GUI..."
    
    if ! check_gui; then
        print_color $YELLOW "⚠️  Falling back to CLI mode..."
        launch_cli
        return
    fi
    
    $PYTHON_CMD "$(dirname "$0")/warp_launcher.py" gui
}

launch_cli() {
    print_color $CYAN "💻 Launching WARP Terminal CLI..."
    $PYTHON_CMD "$(dirname "$0")/warp_launcher.py" cli
}

run_setup() {
    print_color $CYAN "🔧 Running complete setup..."
    $PYTHON_CMD "$(dirname "$0")/warp_launcher.py" setup
}

show_status() {
    print_color $CYAN "📊 Showing system status..."
    $PYTHON_CMD "$(dirname "$0")/warp_launcher.py" status
}

run_config() {
    print_color $CYAN "⚙️  Opening configuration..."
    $PYTHON_CMD "$(dirname "$0")/warp_launcher.py" config
}

create_backup() {
    print_color $CYAN "💾 Creating backup..."
    $PYTHON_CMD "$(dirname "$0")/warp_launcher.py" backup
}

install_deps() {
    print_color $CYAN "📦 Installing dependencies..."
    $PYTHON_CMD "$(dirname "$0")/warp_launcher.py" install
}

main() {
    local command=${1:-gui}
    
    print_banner
    
    # Check Python first
    if ! check_python; then
        exit 1
    fi
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    # Check dependencies (non-fatal)
    check_dependencies
    
    case "$command" in
        "gui")
            launch_gui
            ;;
        "cli")
            launch_cli
            ;;
        "setup")
            run_setup
            ;;
        "status")
            show_status
            ;;
        "config")
            run_config
            ;;
        "backup")
            create_backup
            ;;
        "install")
            install_deps
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_color $RED "❌ Unknown command: $command"
            echo
            show_help
            exit 1
            ;;
    esac
    
    local exit_code=$?
    echo
    if [ $exit_code -eq 0 ]; then
        print_color $GREEN "✅ Command completed successfully"
    else
        print_color $RED "❌ Command failed with exit code $exit_code"
    fi
    
    return $exit_code
}

# Handle Ctrl+C gracefully
trap 'echo; print_color $YELLOW "👋 Goodbye!"; exit 0' INT

# Run main function
main "$@"
