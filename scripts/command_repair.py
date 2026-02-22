#!/usr/bin/env python3
"""
EvoMap Command Auto-Repair Capsule
Based on: sha256:3976c06fa03dd05cae75017a03369f50a46f0ea7db9c7a6d9e0791e4dccd3bef

Automatically repair 'command not found' errors by detecting the missing tool 
and attempting installation via apt-get, brew, or npm.
"""

import os
import re
import subprocess
import sys
from typing import Optional, Tuple

# Common command to package mappings
COMMAND_PACKAGES = {
    # CLI tools
    "jq": "jq",
    "curl": "curl",
    "wget": "wget",
    "git": "git",
    "vim": "vim",
    "nano": "nano",
    "tmux": "tmux",
    "tree": "tree",
    "ffmpeg": "ffmpeg",
    "convert": "imagemagick",
    "rsync": "rsync",
    "ssh": "openssh",
    "scp": "openssh",
    
    # Development tools
    "npm": "node",
    "node": "node",
    "python": "python3",
    "python3": "python3",
    "pip": "python3-pip",
    "pip3": "python3-pip",
    
    # Network tools
    "ping": "iputils-ping",
    " traceroute": "traceroute",
    "netstat": "net-tools",
    "nslookup": "dnsutils",
    "dig": "dnsutils",
    
    # System tools
    "htop": "htop",
    "top": "procps",
    "ps": "procps",
    "kill": "procps",
    "df": "coreutils",
    "du": "coreutils",
    "free": "procps",
}


def detect_missing_command(error_output: str) -> Optional[str]:
    """Extract the missing command from error output."""
    patterns = [
        r"command not found:\s*(\S+)",
        r"unknown command\s*(\S+)",
        r"'(\S+)' is not recognized",
        r"not found: (\S+)",
        r"No such file or directory: (\S+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, error_output, re.IGNORECASE)
        if match:
            cmd = match.group(1)
            # Clean up any quotes
            cmd = cmd.strip("'\"")
            return cmd
    
    return None


def get_system_package_manager() -> Tuple[Optional[str], list]:
    """Detect available package managers."""
    # Check macOS
    result = subprocess.run(["which", "brew"], capture_output=True)
    if result.returncode == 0:
        return ("brew", ["brew", "install"])
    
    # Check Debian/Ubuntu
    result = subprocess.run(["which", "apt-get"], capture_output=True)
    if result.returncode == 0:
        return ("apt", ["sudo", "apt-get", "install", "-y"])
    
    # Check npm (for JS tools)
    result = subprocess.run(["which", "npm"], capture_output=True)
    if result.returncode == 0:
        return ("npm", ["npm", "install", "-g"])
    
    return None, []


def install_command(command: str) -> bool:
    """Attempt to install missing command."""
    pm_type, install_cmd = get_system_package_manager()
    
    if not pm_type:
        print(f"Could not detect package manager")
        return False
    
    # Try to find package name
    package = COMMAND_PACKAGES.get(command.lower())
    
    if not package:
        # Try the command itself as package name
        package = command
    
    cmd = install_cmd + [package]
    
    print(f"Attempting to install {command} via {pm_type}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"Successfully installed {command}")
            return True
        else:
            print(f"Installation failed: {result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        print(f"Installation timed out")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def check_command_exists(command: str) -> bool:
    """Check if command exists."""
    result = subprocess.run(
        ["which", command],
        capture_output=True
    )
    return result.returncode == 0


def repair_command(command: str) -> Tuple[bool, str]:
    """
    Main function to repair missing command.
    
    Returns: (success, message)
    """
    if check_command_exists(command):
        return True, f"Command '{command}' already exists"
    
    # Try to install
    if install_command(command):
        # Verify installation
        if check_command_exists(command):
            return True, f"Successfully installed and verified '{command}'"
    
    return False, f"Could not install '{command}'"


def run_with_repair(cmd: list, shell: bool = False) -> Tuple[int, str, str]:
    """
    Run command with auto-repair on failure.
    
    Returns: (returncode, stdout, stderr)
    """
    # First try running the command
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        shell=shell
    )
    
    if result.returncode == 0:
        return 0, result.stdout, result.stderr
    
    # Check if it's a "command not found" error
    error_output = result.stderr + result.stdout
    
    missing_cmd = detect_missing_command(error_output)
    
    if missing_cmd:
        print(f"Detected missing command: {missing_cmd}")
        
        # Try to repair
        success, msg = repair_command(missing_cmd)
        
        if success:
            # Retry the original command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=shell
            )
            return result.returncode, result.stdout, result.stderr
    
    return result.returncode, result.stdout, result.stderr


# CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python command_repair.py <command> [args...]")
        print("  python command_repair.py check <command>")
        print("")
        print("Examples:")
        print("  python command_repair.py jq --version")
        print("  python command_repair.py check curl")
        sys.exit(1)
    
    if sys.argv[1] == "check":
        cmd = sys.argv[2]
        exists = check_command_exists(cmd)
        print(f"Command '{cmd}' exists: {exists}")
        sys.exit(0 if exists else 1)
    
    # Run command with auto-repair
    cmd = sys.argv[1:]
    returncode, stdout, stderr = run_with_repair(cmd)
    
    print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)
    
    sys.exit(returncode)
