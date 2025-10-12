#!/usr/bin/env pwsh
# WARP Terminal Universal PowerShell Launcher
# Cross-platform PowerShell launcher for Windows, Linux, macOS

param(
    [Parameter(Position=0)]
    [ValidateSet("gui", "cli", "setup", "status", "config", "backup", "install", "help")]
    [string]$Command = "gui"
)

# Colors for output
$Colors = @{
    Red    = "Red"
    Green  = "Green"
    Yellow = "Yellow"
    Blue   = "Blue"
    Cyan   = "Cyan"
    White  = "White"
}

function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Show-Banner {
    Write-Host ""
    Write-ColorText "🚀 WARP Terminal Universal Launcher (PowerShell)" -Color $Colors.Cyan
    Write-ColorText "=================================================" -Color $Colors.Cyan
    Write-Host ""
}

function Test-PythonInstallation {
    Write-ColorText "🔍 Checking Python installation..." -Color $Colors.Blue
    
    $pythonCommands = @("python", "python3", "py")
    $pythonPath = $null
    
    foreach ($cmd in $pythonCommands) {
        try {
            $version = & $cmd --version 2>$null
            if ($LASTEXITCODE -eq 0 -and $version -match "Python 3\.(\d+)\.(\d+)") {
                $major = [int]$matches[1]
                $minor = [int]$matches[2]
                if ($major -ge 8) {
                    $pythonPath = $cmd
                    Write-ColorText "🐍 Python $version detected using '$cmd'" -Color $Colors.Green
                    return $pythonPath
                }
            }
        }
        catch {
            continue
        }
    }
    
    Write-ColorText "❌ Python 3.8+ not found. Please install Python." -Color $Colors.Red
    Write-ColorText "📥 Download from: https://www.python.org/downloads/" -Color $Colors.Yellow
    return $null
}

function Test-GuiEnvironment {
    Write-ColorText "🖼️  Checking GUI environment..." -Color $Colors.Blue
    
    if ($IsWindows -or $PSVersionTable.PSVersion.Major -lt 6) {
        Write-ColorText "✅ GUI environment available (Windows)" -Color $Colors.Green
        return $true
    }
    elseif ($IsLinux) {
        if ($env:DISPLAY -or $env:WAYLAND_DISPLAY) {
            Write-ColorText "✅ GUI environment detected (Linux)" -Color $Colors.Green
            return $true
        }
        else {
            Write-ColorText "⚠️  No GUI environment detected - CLI mode only" -Color $Colors.Yellow
            return $false
        }
    }
    elseif ($IsMacOS) {
        Write-ColorText "✅ GUI environment available (macOS)" -Color $Colors.Green
        return $true
    }
    else {
        Write-ColorText "❓ Unknown platform - assuming GUI available" -Color $Colors.Yellow
        return $true
    }
}

function Test-Dependencies {
    param([string]$PythonPath)
    
    Write-ColorText "📦 Checking dependencies..." -Color $Colors.Blue
    
    $dependencies = @("PyQt5", "zstandard", "requests")
    $missing = @()
    
    foreach ($dep in $dependencies) {
        $importCmd = $dep.ToLower().Replace("pyqt5", "PyQt5.QtWidgets")
        try {
            & $PythonPath -c "import $importCmd" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-ColorText "  ✅ $dep" -Color $Colors.Green
            }
            else {
                Write-ColorText "  ❌ $dep" -Color $Colors.Red
                $missing += $dep
            }
        }
        catch {
            Write-ColorText "  ❌ $dep" -Color $Colors.Red
            $missing += $dep
        }
    }
    
    if ($missing.Count -eq 0) {
        Write-ColorText "✅ All dependencies satisfied" -Color $Colors.Green
        return $true
    }
    else {
        Write-ColorText "⚠️  Missing dependencies: $($missing -join ', ')" -Color $Colors.Yellow
        Write-ColorText "💡 Run with 'install' command to auto-install" -Color $Colors.Blue
        return $false
    }
}

function Show-Help {
    Write-Host "WARP Terminal Universal PowerShell Launcher"
    Write-Host ""
    Write-Host "Usage: .\warp_launcher.ps1 [command]"
    Write-Host ""
    Write-Host "Available commands:"
    Write-Host "  gui      Launch GUI interface (default)"
    Write-Host "  cli      Launch CLI interface"
    Write-Host "  setup    Complete system setup"
    Write-Host "  status   Show system status"
    Write-Host "  config   Configure launcher"
    Write-Host "  backup   Create backup"
    Write-Host "  install  Install dependencies"
    Write-Host "  help     Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\warp_launcher.ps1           # Launch GUI (default)"
    Write-Host "  .\warp_launcher.ps1 cli       # Launch CLI"
    Write-Host "  .\warp_launcher.ps1 setup     # Complete setup"
}

function Invoke-WarpCommand {
    param(
        [string]$PythonPath,
        [string]$WarpCommand
    )
    
    $scriptDir = Split-Path -Parent $MyInvocation.ScriptName
    $launcherScript = Join-Path $scriptDir "warp_launcher.py"
    
    if (-not (Test-Path $launcherScript)) {
        Write-ColorText "❌ warp_launcher.py not found in $scriptDir" -Color $Colors.Red
        return $false
    }
    
    try {
        & $PythonPath $launcherScript $WarpCommand
        return ($LASTEXITCODE -eq 0)
    }
    catch {
        Write-ColorText "❌ Error executing command: $_" -Color $Colors.Red
        return $false
    }
}

function Start-WarpGui {
    param([string]$PythonPath)
    
    Write-ColorText "🚀 Launching WARP Terminal GUI..." -Color $Colors.Cyan
    
    if (-not (Test-GuiEnvironment)) {
        Write-ColorText "⚠️  Falling back to CLI mode..." -Color $Colors.Yellow
        return Start-WarpCli -PythonPath $PythonPath
    }
    
    return Invoke-WarpCommand -PythonPath $PythonPath -WarpCommand "gui"
}

function Start-WarpCli {
    param([string]$PythonPath)
    
    Write-ColorText "💻 Launching WARP Terminal CLI..." -Color $Colors.Cyan
    return Invoke-WarpCommand -PythonPath $PythonPath -WarpCommand "cli"
}

function Start-Setup {
    param([string]$PythonPath)
    
    Write-ColorText "🔧 Running complete setup..." -Color $Colors.Cyan
    return Invoke-WarpCommand -PythonPath $PythonPath -WarpCommand "setup"
}

function Show-Status {
    param([string]$PythonPath)
    
    Write-ColorText "📊 Showing system status..." -Color $Colors.Cyan
    return Invoke-WarpCommand -PythonPath $PythonPath -WarpCommand "status"
}

function Start-Config {
    param([string]$PythonPath)
    
    Write-ColorText "⚙️  Opening configuration..." -Color $Colors.Cyan
    return Invoke-WarpCommand -PythonPath $PythonPath -WarpCommand "config"
}

function New-Backup {
    param([string]$PythonPath)
    
    Write-ColorText "💾 Creating backup..." -Color $Colors.Cyan
    return Invoke-WarpCommand -PythonPath $PythonPath -WarpCommand "backup"
}

function Install-Dependencies {
    param([string]$PythonPath)
    
    Write-ColorText "📦 Installing dependencies..." -Color $Colors.Cyan
    return Invoke-WarpCommand -PythonPath $PythonPath -WarpCommand "install"
}

# Main execution
function Main {
    Show-Banner
    
    # Check Python installation
    $pythonPath = Test-PythonInstallation
    if (-not $pythonPath) {
        exit 1
    }
    
    # Change to script directory
    $scriptDir = Split-Path -Parent $MyInvocation.ScriptName
    Set-Location $scriptDir
    
    # Check dependencies (non-fatal)
    Test-Dependencies -PythonPath $pythonPath | Out-Null
    
    $success = $false
    
    switch ($Command) {
        "gui" {
            $success = Start-WarpGui -PythonPath $pythonPath
        }
        "cli" {
            $success = Start-WarpCli -PythonPath $pythonPath
        }
        "setup" {
            $success = Start-Setup -PythonPath $pythonPath
        }
        "status" {
            $success = Show-Status -PythonPath $pythonPath
        }
        "config" {
            $success = Start-Config -PythonPath $pythonPath
        }
        "backup" {
            $success = New-Backup -PythonPath $pythonPath
        }
        "install" {
            $success = Install-Dependencies -PythonPath $pythonPath
        }
        "help" {
            Show-Help
            $success = $true
        }
        default {
            Write-ColorText "❌ Unknown command: $Command" -Color $Colors.Red
            Write-Host ""
            Show-Help
            exit 1
        }
    }
    
    Write-Host ""
    if ($success) {
        Write-ColorText "✅ Command completed successfully" -Color $Colors.Green
    }
    else {
        Write-ColorText "❌ Command failed" -Color $Colors.Red
        exit 1
    }
}

# Handle Ctrl+C gracefully
try {
    Main
}
catch {
    Write-Host ""
    Write-ColorText "👋 Goodbye!" -Color $Colors.Yellow
    exit 0
}
