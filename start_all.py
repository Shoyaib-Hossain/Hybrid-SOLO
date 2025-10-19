#!/usr/bin/env python3
"""
Hybrid Web Security System - Python Startup Script
Starts all services with one command (cross-platform)
"""

import subprocess
import sys
import time
import os
import signal
import requests
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_ollama():
    """Check if Ollama is running"""
    print_info("Checking Ollama service...")
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        if response.status_code == 200:
            print_success("Ollama is running on port 11434")
            return True
    except:
        pass

    print_warning("Ollama is not running!")
    print("   Please start Ollama first:")
    print("   • Download from: https://ollama.ai")
    print("   • Run: ollama serve")
    print("   • Pull model: ollama pull llama2")

    response = input("\n   Continue anyway? (y/n): ").lower().strip()
    return response == 'y'

def start_service(name, port, directory, script):
    """Start a service in background"""
    print_info(f"Starting {name} on port {port}...")

    script_dir = Path(__file__).parent
    service_dir = script_dir / directory
    script_path = service_dir / script

    if not script_path.exists():
        print_error(f"Script not found: {script_path}")
        return None

    # Start the service
    try:
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=str(service_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Give it a moment to start
        time.sleep(2)

        # Check if process is still running
        if process.poll() is None:
            print_success(f"{name} started (PID: {process.pid})")
            return process
        else:
            print_error(f"{name} failed to start")
            stdout, stderr = process.communicate()
            if stderr:
                print(f"   Error: {stderr[:200]}")
            return None

    except Exception as e:
        print_error(f"Failed to start {name}: {e}")
        return None

def main():
    print_header("🚀 Starting Hybrid Web Security System")

    # Check Ollama
    if not check_ollama():
        print_error("Ollama check failed. Exiting.")
        return 1

    print("\n" + "="*70 + "\n")

    # Store processes
    processes = []

    # Start services
    services = [
        ("Threat Detector", "8081", "host-c-detection", "threat_detector.py"),
        ("Web Application", "3000", "host-b-webapp", "login_app.py")
    ]

    for name, port, directory, script in services:
        process = start_service(name, port, directory, script)
        if process:
            processes.append((name, process))
        time.sleep(1)

    if not processes:
        print_error("No services started successfully")
        return 1

    print_header("✅ All Services Started!")

    print("🌐 Access the system:")
    print("   • Web Application:      http://localhost:3000")
    print("   • Security Dashboard:   http://localhost:3000/monitor")
    print("   • Full Statistics:      http://localhost:3000/stats/comprehensive")
    print("   • Threat Detector API:  http://localhost:8081/stats")
    print()
    print("📊 Test the system:")
    print("   • Try legitimate login: Username: AAA, Password: winchester1")
    print("   • Try SQL injection:    Username: admin' OR '1'='1")
    print()
    print("🧪 Run automated tests:")
    print(f"   python3 jsonl_threat_tester.py --url http://localhost:3000 --max-payloads 100")
    print()
    print("🛑 Press Ctrl+C to stop all services")
    print("="*70 + "\n")

    # Keep script running and monitor processes
    try:
        while True:
            time.sleep(5)
            # Check if processes are still alive
            for name, process in processes:
                if process.poll() is not None:
                    print_error(f"{name} has stopped unexpectedly")

    except KeyboardInterrupt:
        print("\n" + "="*70)
        print_info("Shutting down services...")

        # Terminate all processes
        for name, process in processes:
            print_info(f"Stopping {name}...")
            process.terminate()
            try:
                process.wait(timeout=5)
                print_success(f"{name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print_warning(f"{name} force killed")

        print_header("✅ All Services Stopped!")
        return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
