#!/usr/bin/env python3
import subprocess
import sys
import time
from datetime import datetime

def check_ssh_service():
    """Check if SSH service is running"""
    try:
        result = subprocess.run(['pgrep', '-f', 'sshd'], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking SSH: {e}")
        return False

def get_ssh_connections():
    """Get active SSH connections"""
    try:
        result = subprocess.run(['netstat', '-tnp'], capture_output=True, text=True)
        ssh_connections = [line for line in result.stdout.split('\n') if ':22' in line]
        return ssh_connections
    except:
        try:
            result = subprocess.run(['ss', '-tnp'], capture_output=True, text=True)
            ssh_connections = [line for line in result.stdout.split('\n') if ':22' in line]
            return ssh_connections
        except Exception as e:
            print(f"Error getting SSH connections: {e}")
            return []

def get_ssh_port():
    """Get SSH listening port"""
    try:
        result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'ssh' in line.lower() or 'sshd' in line.lower():
                return line
    except:
        try:
            result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'ssh' in line.lower() or 'sshd' in line.lower():
                    return line
        except Exception as e:
            print(f"Error getting SSH port: {e}")
    return "SSH port not found"

def check_ssh_config():
    """Check SSH configuration file"""
    ssh_config_path = '/etc/ssh/sshd_config'
    try:
        with open(ssh_config_path, 'r') as f:
            config = f.readlines()
        return config
    except Exception as e:
        return [f"Cannot read SSH config: {e}"]

def monitor_ssh():
    """Main monitoring function"""
    print("=" * 60)
    print(f"SSH Service Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check service status
    is_running = check_ssh_service()
    status = "✓ RUNNING" if is_running else "✗ STOPPED"
    print(f"\n[Service Status]: {status}")
    
    # Get SSH port
    print(f"\n[SSH Port Info]:")
    port_info = get_ssh_port()
    print(port_info if port_info else "No SSH port found")
    
    # Get active connections
    print(f"\n[Active SSH Connections]:")
    connections = get_ssh_connections()
    if connections:
        for conn in connections:
            if conn.strip():
                print(f"  {conn}")
    else:
        print("  No active connections")
    
    print("\n" + "=" * 60)

def continuous_monitor(interval=5):
    """Continuous monitoring mode"""
    try:
        while True:
            monitor_ssh()
            print(f"Next check in {interval} seconds... Press Ctrl+C to exit\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-c":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        continuous_monitor(interval)
    else:
        monitor_ssh()