#!/usr/bin/env python3
"""
Market Price Tracker - Complete Launcher
Handles: venv setup, dependency installation, environment validation, and app launch
"""

import sys
import subprocess
import os
from pathlib import Path

# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
NC = "\033[0m"

def print_step(message):
    print(f"\n{BLUE}{BOLD}▶ {message}{NC}")

def print_success(message):
    print(f"{GREEN}✓ {message}{NC}")

def print_error(message):
    print(f"{RED}✗ {message}{NC}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{NC}")

def check_python():
    """Check Python version"""
    print_step("Step 1: Checking Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} found")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} is too old. Need Python 3.7+")
        return False

def setup_venv():
    """Setup or verify virtual environment"""
    print_step("Step 2: Setting up virtual environment...")
    venv_path = Path(".venv")
    
    if venv_path.exists():
        # Check if it's valid
        if (venv_path / "bin" / "python3").exists() or (venv_path / "Scripts" / "python.exe").exists():
            print_success("Virtual environment already exists")
            return True
        else:
            print_warning("Existing venv is corrupted, recreating...")
            import shutil
            shutil.rmtree(venv_path)
    
    # Create virtual environment
    try:
        print("   Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], 
                      check=True, capture_output=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print_warning("Can't create venv (python3-venv may be missing)")
        print_warning("Will install packages globally with --break-system-packages")
        return False

def get_python_executable():
    """Get the Python executable path (venv or system)"""
    venv_path = Path(".venv")
    
    # Try venv first
    if (venv_path / "bin" / "python3").exists():
        return str(venv_path / "bin" / "python3")
    elif (venv_path / "Scripts" / "python.exe").exists():
        return str(venv_path / "Scripts" / "python.exe")
    else:
        return sys.executable

def install_dependencies(python_exe, use_venv):
    """Install all required dependencies"""
    print_step("Step 3: Installing dependencies...")
    
    packages = [
        "mysql-connector-python",
        "bcrypt",
        "pandas",
        "matplotlib",
        "reportlab",
        "openpyxl",
        "tabulate"
    ]
    
    # Prepare pip command
    pip_cmd = [python_exe, "-m", "pip", "install", "-q"]
    
    if not use_venv:
        pip_cmd.append("--break-system-packages")
    
    pip_cmd.extend(packages)
    
    try:
        print(f"   Installing {len(packages)} packages...")
        result = subprocess.run(pip_cmd, capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            print_success("All dependencies installed")
            return True
        else:
            print_warning("Some packages may have failed, trying individually...")
            # Try one by one
            for package in packages:
                try:
                    cmd = [python_exe, "-m", "pip", "install", "-q"]
                    if not use_venv:
                        cmd.append("--break-system-packages")
                    cmd.append(package)
                    
                    subprocess.run(cmd, capture_output=True, timeout=60, check=True)
                    print(f"   ✓ {package}")
                except:
                    print(f"   ✗ {package} (skipped)")
            print_success("Dependencies installed (some may be missing)")
            return True
            
    except subprocess.TimeoutExpired:
        print_warning("Installation timed out (slow connection)")
        print_warning("You may need to install manually:")
        print(f"   {python_exe} -m pip install {' '.join(packages)}")
        return False
    except Exception as e:
        print_error(f"Installation failed: {e}")
        return False

def verify_imports(python_exe):
    """Verify all required modules can be imported"""
    print_step("Step 4: Verifying imports...")
    
    test_imports = """
try:
    import mysql.connector
    import bcrypt
    import pandas
    import matplotlib
    import reportlab
    import openpyxl
    import tabulate
    print("OK")
except ImportError as e:
    print(f"MISSING:{e.name}")
"""
    
    try:
        result = subprocess.run([python_exe, "-c", test_imports],
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "OK" in result.stdout:
            print_success("All modules can be imported")
            return True
        else:
            print_warning("Some imports failed")
            if "MISSING:" in result.stdout:
                missing = result.stdout.split("MISSING:")[1].strip()
                print_warning(f"Missing module: {missing}")
            return False
    except:
        print_warning("Could not verify imports")
        return False

def check_config():
    """Check if config.ini exists"""
    print_step("Step 5: Checking configuration...")
    
    if Path("config.ini").exists():
        print_success("config.ini found")
        return True
    elif Path("config.ini.sample").exists():
        print_warning("config.ini not found, creating from sample...")
        import shutil
        shutil.copy("config.ini.sample", "config.ini")
        print_success("config.ini created")
        print_warning("⚠  Please edit config.ini with your database credentials!")
        print("   Run: nano config.ini")
        print("")
        input("Press Enter after editing config.ini to continue...")
        return True
    else:
        print_error("No config.ini or config.ini.sample found!")
        return False

def launch_app(python_exe):
    """Launch the main application"""
    print_step("Step 6: Launching application...")
    print("")
    print("="*70)
    print("")
    
    # Launch the app
    try:
        subprocess.run([python_exe, "main_enhanced.py"])
        return True
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print(f"{GREEN}✓ Application closed by user{NC}")
        return True
    except Exception as e:
        print_error(f"Failed to launch: {e}")
        return False

def main():
    """Main launcher function"""
    os.chdir(Path(__file__).parent)
    
    # Check Python
    if not check_python():
        return 1
    
    # Setup venv
    use_venv = setup_venv()
    
    # Get Python executable
    python_exe = get_python_executable()
    print(f"   Using: {python_exe}")
    
    # Install dependencies
    if not install_dependencies(python_exe, use_venv):
        response = input(f"\n{YELLOW}Dependencies installation had issues. Continue anyway? (y/N): {NC}").lower()
        if response != 'y':
            return 1
    
    # Verify imports
    imports_ok = verify_imports(python_exe)
    if not imports_ok:
        response = input(f"\n{YELLOW}Import verification failed. Try to launch anyway? (y/N): {NC}").lower()
        if response != 'y':
            return 1
    
    # Check config
    if not check_config():
        return 1
    
    # Launch app
    if not launch_app(python_exe):
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
