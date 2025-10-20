# 🔍 Step-by-Step Code Walkthrough

This document walks through the actual code in this project, explaining **every important line** so you can understand exactly how it works.

## 📋 Table of Contents
1. [Start All Script](#start-all-script)
2. [Login Application](#login-application)
3. [Threat Detector](#threat-detector)
4. [Practical Examples](#practical-examples)

---

## Start All Script

### File: `start_all.py`

This script starts both services (web app and threat detector).

#### Lines 1-23: Imports and Color Definitions

```python
#!/usr/bin/env python3
"""
Hybrid Web Security System - Python Startup Script
Starts all services with one command (cross-platform)
"""
```
**What this means:**
- `#!/usr/bin/env python3`: Tells the system to use Python 3 to run this script
- The triple quotes `"""..."""` are a **docstring** - describes what the file does

```python
import subprocess
import sys
import time
import os
import signal
import requests
from pathlib import Path
```
**What each import does:**
- `subprocess`: Lets us run other programs from Python
- `sys`: System-specific parameters (like command line arguments)
- `time`: Time-related functions (like sleep)
- `os`: Operating system functions (like environment variables)
- `signal`: Handle system signals (like Ctrl+C)
- `requests`: Make HTTP requests to check if services are running
- `pathlib.Path`: Modern way to work with file paths

```python
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
```
**What this means:**
- These are **ANSI escape codes** for colored terminal output
- `\033[92m` makes text green
- `\033[0m` resets to normal
- Example: `print(f"{Colors.GREEN}Success!{Colors.END}")` prints green text

#### Lines 25-40: Helper Functions

```python
def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
```
**Breakdown:**
- `def print_header(text):`: Defines a function named `print_header` that takes one parameter `text`
- `f"..."`: f-string (formatted string) - lets us insert variables into strings
- `'='*70`: Repeats the `=` character 70 times
- `\n`: Newline (moves to next line)
- Result: Prints a fancy header with colored text

**Example:**
```python
print_header("Welcome")
# Output:
# ======================================================================
#   Welcome
# ======================================================================
```

```python
def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")
```
**What this means:**
- Prints green text with a checkmark
- Example: `print_success("Server started")` → ✅ Server started (in green)

#### Lines 42-60: Checking Ollama

```python
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
```
**Breakdown:**
- `try:`: Start a try block (for error handling)
- `requests.get(url, timeout=2)`: Send HTTP GET request, wait max 2 seconds
- `response.status_code == 200`: Check if request succeeded (200 = OK)
- `return True`: Send back True to indicate success
- `except: pass`: If any error occurs, ignore it and continue
- If Ollama is not running, this returns `None` (implicit)

**Why check Ollama?**
The threat detector uses Ollama (AI engine) for intelligent analysis. If it's not running, the system won't work properly.

#### Lines 62-100: Starting Services

```python
def start_service(name, port, directory, script):
    """Start a service in background"""
    print_info(f"Starting {name} on port {port}...")
    
    script_dir = Path(__file__).parent
    service_dir = script_dir / directory
    script_path = service_dir / script
```
**Breakdown:**
- `Path(__file__)`: Path to current script file
- `.parent`: Get the directory containing this script
- `script_dir / directory`: Join paths (like `os.path.join`)
- Result: Build full path to the service script

**Example:**
```python
# If start_all.py is in /home/user/project/
script_dir = Path("/home/user/project/")
service_dir = script_dir / "host-b-webapp"  # /home/user/project/host-b-webapp
script_path = service_dir / "login_app.py"  # /home/user/project/host-b-webapp/login_app.py
```

```python
    if not script_path.exists():
        print_error(f"Script not found: {script_path}")
        return None
```
**What this means:**
- Check if the script file exists
- If not, print error and return None
- `return None`: Exit function early

```python
    try:
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=str(service_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
```
**Breakdown:**
- `subprocess.Popen`: Start a new process
- `sys.executable`: Path to Python interpreter (like `/usr/bin/python3`)
- `[sys.executable, str(script_path)]`: Command to run: `python3 /path/to/script.py`
- `cwd=str(service_dir)`: Set working directory for the process
- `stdout=subprocess.PIPE`: Capture standard output
- `stderr=subprocess.PIPE`: Capture error output
- `text=True`: Return output as text (not bytes)

```python
        time.sleep(2)
        
        if process.poll() is None:
            print_success(f"{name} started (PID: {process.pid})")
            return process
        else:
            print_error(f"{name} failed to start")
            return None
```
**Breakdown:**
- `time.sleep(2)`: Wait 2 seconds
- `process.poll()`: Check if process is still running
  - Returns `None` if still running
  - Returns exit code if it stopped
- `process.pid`: Process ID (unique identifier)
- If still running: Success! Return the process object
- If stopped: Failure. Return None

#### Lines 102-174: Main Function

```python
def main():
    print_header("🚀 Starting Hybrid Web Security System")
    
    if not check_ollama():
        print_error("Ollama check failed. Exiting.")
        return 1
```
**What this means:**
- Call `check_ollama()` function
- If it returns False or None: Print error and exit with code 1
- Exit code 1 indicates an error occurred

```python
    processes = []
    
    services = [
        ("Threat Detector", "8081", "host-c-detection", "threat_detector.py"),
        ("Web Application", "3000", "host-b-webapp", "login_app.py")
    ]
```
**Breakdown:**
- `processes = []`: Empty list to store running processes
- `services`: List of tuples (each tuple has 4 elements)
- Each tuple: (name, port, directory, script_file)

```python
    for name, port, directory, script in services:
        process = start_service(name, port, directory, script)
        if process:
            processes.append((name, process))
        time.sleep(1)
```
**Breakdown:**
- `for ... in services:`: Loop through each service
- **Tuple unpacking**: Assign each element to a variable
  - `name = "Threat Detector"`
  - `port = "8081"`
  - `directory = "host-c-detection"`
  - `script = "threat_detector.py"`
- Start the service
- If successful: Add to processes list
- Wait 1 second before starting next service

```python
    try:
        while True:
            time.sleep(5)
            for name, process in processes:
                if process.poll() is not None:
                    print_error(f"{name} has stopped unexpectedly")
    
    except KeyboardInterrupt:
        print("\n" + "="*70)
        print_info("Shutting down services...")
```
**Breakdown:**
- `while True:`: Infinite loop (keeps running forever)
- Every 5 seconds: Check if processes are still alive
- `except KeyboardInterrupt:`: Catch Ctrl+C
- When user presses Ctrl+C: Exit loop and shut down services

```python
        for name, process in processes:
            print_info(f"Stopping {name}...")
            process.terminate()
            try:
                process.wait(timeout=5)
                print_success(f"{name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print_warning(f"{name} force killed")
```
**Breakdown:**
- `process.terminate()`: Ask process to stop nicely (SIGTERM)
- `process.wait(timeout=5)`: Wait up to 5 seconds for it to stop
- If it doesn't stop in time: Raise `TimeoutExpired` exception
- `process.kill()`: Force kill the process (SIGKILL)

---

## Login Application

### File: `host-b-webapp/login_app.py`

#### Lines 1-33: Imports and Configuration

```python
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import requests
import json
import logging
import os
from datetime import datetime
import sqlite3
```
**What we're importing:**
- **Flask**: Web framework
- **render_template**: Show HTML pages
- **request**: Get data from HTTP requests
- **jsonify**: Convert Python dict to JSON
- **redirect**: Send user to different page
- **url_for**: Generate URL for a route
- **flash**: Show temporary messages to user
- **session**: Store data between requests
- **requests**: Make HTTP requests to other services
- **json**: Work with JSON data
- **logging**: Log messages (better than print)
- **os**: Operating system functions
- **datetime**: Work with dates and times
- **sqlite3**: Database operations

```python
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
```
**Breakdown:**
- `Flask(__name__)`: Create Flask application
  - `__name__` is `__main__` when script is run directly
  - Used by Flask to locate templates and static files
- `app.secret_key`: Used to encrypt session data
- `os.getenv('SECRET_KEY', 'default')`: Get environment variable, or use default
  - **Environment variable**: Configuration set outside the code
  - Good practice: Keep secrets out of code

```python
THREAT_DETECTOR_HOST = os.getenv('THREAT_DETECTOR_HOST', 'localhost')
THREAT_DETECTOR_PORT = os.getenv('THREAT_DETECTOR_PORT', '8081')
SECURITY_DETECTION_URL = os.getenv('THREAT_DETECTOR_URL', 
                                   f'http://{THREAT_DETECTOR_HOST}:{THREAT_DETECTOR_PORT}/analyze')
```
**What this means:**
- Get configuration from environment variables (or use defaults)
- Build URL: `http://localhost:8081/analyze`
- This is where we'll send login attempts for analysis

```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```
**Breakdown:**
- `basicConfig`: Configure logging system
- `level=logging.INFO`: Show INFO level and above (INFO, WARNING, ERROR)
- `getLogger(__name__)`: Create logger for this module
- Now we can use: `logger.info("message")`, `logger.warning("warning")`, etc.

#### Lines 35-72: AuthenticationTracker Class

```python
class AuthenticationTracker:
    """
    Authentication Tracker - Manages Login Attempts and Security Analysis
    """
    
    def __init__(self):
        """Initialize the authentication tracker."""
        self.setup_database()
```
**Breakdown:**
- `class AuthenticationTracker:`: Define a new class
- Docstring explains what the class does
- `__init__`: Constructor (runs when creating an instance)
- `self.setup_database()`: Call method to set up database

```python
    def setup_database(self):
        """Create SQLite database and table for storing login attempts."""
        os.makedirs('data', exist_ok=True)
```
**What this means:**
- `os.makedirs('data')`: Create 'data' directory
- `exist_ok=True`: Don't error if directory already exists

```python
        conn = sqlite3.connect('data/web_sessions.db')
        cursor = conn.cursor()
```
**Breakdown:**
- `sqlite3.connect()`: Connect to database (creates file if it doesn't exist)
- `cursor()`: Create cursor object (used to execute SQL commands)
- Think of cursor as a pointer that executes commands

```python
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                threat_detected BOOLEAN,
                login_blocked BOOLEAN DEFAULT 0,
                threat_analysis TEXT
            )
        ''')
```
**SQL Breakdown:**
- `CREATE TABLE IF NOT EXISTS`: Create table only if it doesn't exist
- `login_sessions`: Table name
- Each line defines a column:
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`: Auto-incrementing ID (1, 2, 3, ...)
  - `timestamp DATETIME DEFAULT CURRENT_TIMESTAMP`: Auto-set to current time
  - `username TEXT`: Text field for username
  - `threat_detected BOOLEAN`: True/False value
  - `DEFAULT 0`: Default value is 0 (False)

```python
        conn.commit()
        conn.close()
```
**What this means:**
- `commit()`: Save changes to database
- `close()`: Close database connection
- **Always close connections!** Otherwise you'll leak resources

#### Lines 73-158: Recording Login Attempts

```python
    def record_attempt(self, username, password, ip_address):
        """
        Record a login attempt and forward it to threat detection service.
        """
        attempt_data = {
            'timestamp': datetime.now().isoformat(),
            'username': username,
            'password': password,
            'ip_address': ip_address,
            'threat_analysis': None,
            'threat_detected': False,
            'login_blocked': False
        }
```
**Breakdown:**
- `def record_attempt(self, ...):`: Method of the class
- `self`: Reference to the instance
- Create dictionary to store attempt data
- `datetime.now().isoformat()`: Current time as ISO string (e.g., "2024-01-15T10:30:00")
- Initialize fields with default values

```python
        try:
            analysis_request = {
                'input': f"username: {username}, password: {password}",
                'ip_address': ip_address
            }
            
            response = requests.post(
                SECURITY_DETECTION_URL,
                json=analysis_request,
                timeout=30
            )
```
**Breakdown:**
- `try:`: Start error handling block
- Create request data
- `requests.post()`: Send POST request
  - `json=`: Automatically converts dict to JSON and sets Content-Type header
  - `timeout=30`: Wait max 30 seconds for response

```python
            if response.status_code == 200:
                security_analysis = response.json()
                attempt_data['threat_analysis'] = security_analysis
                attempt_data['threat_detected'] = security_analysis.get('threat_detected', False)
                attempt_data['login_blocked'] = False
                
                if security_analysis.get('threat_detected', False):
                    logger.warning(f"Threat detected from {ip_address}")
                else:
                    logger.info(f"Safe login attempt from {ip_address}")
```
**Breakdown:**
- `response.status_code`: HTTP status code (200 = success)
- `response.json()`: Parse JSON response into Python dict
- `.get('threat_detected', False)`: Get value, return False if key doesn't exist
- Update attempt_data with results
- Log the outcome

```python
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to contact security detection service: {str(e)}")
            attempt_data['threat_detected'] = False
            attempt_data['login_blocked'] = False
```
**What this means:**
- If request fails (timeout, connection error, etc.): Catch the exception
- Log the error
- **Fail-open**: Allow login if threat detector is unreachable
- Alternative: **Fail-closed**: Block login if threat detector is unreachable

#### Lines 165-202: Flask Routes

```python
@app.route('/')
def authentication_portal():
    """Home page - Display login form."""
    response = app.make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
```
**Breakdown:**
- `@app.route('/')`: Map URL `/` to this function
- `render_template('login.html')`: Load and render HTML template
- `app.make_response()`: Create response object (so we can modify headers)
- Setting cache headers: Tell browser not to cache this page
  - Why? Login pages should always be fresh
- Return the response

```python
@app.route('/login', methods=['POST'])
def process_authentication():
    """Process login form submission with threat detection."""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip_address = request.remote_addr
```
**Breakdown:**
- `methods=['POST']`: Only accept POST requests
- `request.form`: Data from HTML form
- `.get('username', '')`: Get username field, return '' if not present
- `request.remote_addr`: Client's IP address

```python
    if not username or not password:
        flash('Please provide both username and password', 'error')
        return redirect(url_for('authentication_portal'))
```
**Breakdown:**
- `if not username`: Check if username is empty
- `flash()`: Store message to show on next page
  - First parameter: message text
  - Second parameter: category ('error', 'success', 'info')
- `redirect()`: Send user to different page
- `url_for('authentication_portal')`: Generate URL for the function named 'authentication_portal'
  - Better than hardcoding `/` because if route changes, code still works

```python
    attempt_record = auth_tracker.record_attempt(username, password, ip_address)
    
    flash('Authentication successful!', 'success')
    return render_template('success.html', username=username)
```
**Breakdown:**
- Call `record_attempt()` to log and analyze
- Show success message
- Render success page, passing username as variable
- In template: Can use `{{ username }}` to display it

#### Lines 204-266: API Endpoints

```python
@app.route('/api/attempts')
def get_authentication_attempts():
    """API endpoint to retrieve login attempt history."""
    try:
        conn = sqlite3.connect('data/web_sessions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, password, ip_address, timestamp,
                   threat_detected, login_blocked, threat_analysis
            FROM login_sessions
            ORDER BY timestamp DESC
            LIMIT 100
        ''')
        
        results = cursor.fetchall()
        conn.close()
```
**SQL Breakdown:**
- `SELECT ... FROM login_sessions`: Get data from table
- `ORDER BY timestamp DESC`: Sort by timestamp, newest first (DESCending)
- `LIMIT 100`: Return maximum 100 rows
- `cursor.fetchall()`: Get all results as list of tuples

```python
        attempt_records = []
        for row in results:
            username, password, ip_address, timestamp, threat_detected, login_blocked, threat_analysis = row
            
            parsed_analysis = None
            if threat_analysis:
                try:
                    parsed_analysis = json.loads(threat_analysis)
                except json.JSONDecodeError:
                    parsed_analysis = None
```
**Breakdown:**
- Create empty list for records
- Loop through each row
- **Tuple unpacking**: Assign each value to a variable
- `json.loads(threat_analysis)`: Parse JSON string to Python dict
- If JSON is invalid: Catch exception and set to None

```python
            attempt_records.append({
                'username': username,
                'password': password[:10] + '...' if len(password) > 10 else password,
                'ip_address': ip_address,
                'timestamp': timestamp,
                'threat_detected': bool(threat_detected),
                'login_blocked': bool(login_blocked),
                'threat_analysis': parsed_analysis
            })
```
**Breakdown:**
- Add dictionary to list
- `password[:10] + '...'`: Truncate long passwords (show first 10 chars + ...)
- `bool(threat_detected)`: Convert to boolean (SQLite stores as 0/1)

```python
        return jsonify(attempt_records)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```
**Breakdown:**
- `jsonify()`: Convert Python list/dict to JSON response
- If error: Return error message with status code 500 (Internal Server Error)

---

## Threat Detector

### File: `host-c-detection/threat_detector.py`

#### Lines 31-82: AdvancedSecurityAnalyzer Class Setup

```python
class AdvancedSecurityAnalyzer:
    """
    Advanced Security Analyzer - Core Threat Detection Engine
    """
    
    def __init__(self):
        """Initialize the security analyzer with AI configuration and threat signatures."""
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.ai_model = os.getenv('OLLAMA_MODEL', 'phi:2.7b')
```
**What this means:**
- Get Ollama configuration from environment variables
- Default: Use local Ollama at localhost:11434
- Default model: phi:2.7b (a small, fast AI model)

```python
        self.security_signatures = {
            'SQL_INJECTION': [
                r"(?i)'\s*or\s*'",
                r"(?i)'\s*or\s+\d+\s*=\s*\d+",
                r"(?i)'.*?--",
                r"(?i);\s*drop\s+table",
                r"(?i);\s*delete\s+from",
                r"(?i)union\s+select",
            ],
        }
```
**Regex Breakdown:**
Let's understand each pattern:

1. `r"(?i)'\s*or\s*'"`:
   - `r"..."`: Raw string (backslashes treated literally)
   - `(?i)`: Case insensitive flag
   - `'`: Match single quote
   - `\s*`: Match zero or more whitespace characters
   - `or`: Match the word "or"
   - `\s*`: Match zero or more whitespace
   - `'`: Match single quote
   - **Matches**: `' or '`, `' OR '`, `'  or  '`

2. `r"(?i)'\s*or\s+\d+\s*=\s*\d+"`:
   - `\s+`: Match one or more whitespace
   - `\d+`: Match one or more digits
   - `=`: Match equals sign
   - **Matches**: `' or 1=1`, `' OR 2=2`

3. `r"(?i)'.*?--"`:
   - `.*?`: Match any characters (non-greedy)
   - `--`: Match two hyphens (SQL comment)
   - **Matches**: `admin' --`, `' --`

4. `r"(?i);\s*drop\s+table"`:
   - `;`: Semicolon (ends SQL statement)
   - **Matches**: `; DROP TABLE`, `;drop table`

5. `r"(?i)union\s+select"`:
   - **Matches**: `UNION SELECT`, `union select`

```python
        self.legitimate_auth_patterns = {
            'pattern_combinations': [
                ('AAA', 'Aston1'), ('BBB', 'Aston2'), ('CCC', 'Aston3'),
                ('DDD', 'Aston4'), ('EEE', 'Aston5'), ('ZZZ', 'Aston6'),
            ]
        }
```
**What this means:**
- Whitelist of known legitimate username/password combinations
- Tuple format: (username, password)
- If input matches these: It's definitely safe, skip other checks

#### Lines 120-162: Legitimate Login Validation

```python
    def validate_legitimate_login(self, input_text: str) -> bool:
        """Check if input matches a whitelisted legitimate login pattern."""
        input_lower = input_text.lower().strip()
        
        for username, password in self.legitimate_auth_patterns['pattern_combinations']:
            if username.lower() in input_lower and password.lower() in input_lower:
                return True
        
        return False
```
**Breakdown:**
- `input_text: str`: Type hint (parameter should be string)
- `-> bool`: Type hint (function returns boolean)
- `.lower()`: Convert to lowercase
- `.strip()`: Remove leading/trailing whitespace
- Loop through each (username, password) pair
- Check if both are in the input string
- Return True if match found, False otherwise

**Example:**
```python
input_text = "username: AAA, password: Aston1"
# After normalization: "username: aaa, password: aston1"
# Check: "aaa" in input_text? YES
# Check: "aston1" in input_text? YES
# Return: True
```

#### Lines 130-199: Comprehensive Security Scan

```python
    def comprehensive_security_scan(self, input_text: str, ip_address: str = None) -> Optional[Dict]:
        """
        Perform comprehensive security threat analysis using hybrid detection.
        """
        start_time = time.time()
```
**Breakdown:**
- `ip_address: str = None`: Optional parameter (default is None)
- `-> Optional[Dict]`: Returns Dict or None
- `time.time()`: Current time in seconds (for measuring performance)

```python
        decoded_input = unquote(input_text)
        normalized_input = decoded_input.replace('+', ' ')
        normalized_input = re.sub(r'\s+', ' ', normalized_input).strip()
        input_lower = normalized_input.lower()
```
**Normalization Steps:**
1. `unquote()`: Decode URL encoding (`%20` → space, `%27` → ')
2. `replace('+', ' ')`: Convert + to space (URL encoding)
3. `re.sub(r'\s+', ' ', ...)`: Replace multiple spaces with single space
4. `.strip()`: Remove leading/trailing whitespace
5. `.lower()`: Convert to lowercase

**Example:**
```python
input_text = "admin%27+OR+%271%27%3D%271"
decoded = "admin' OR '1'='1"
normalized = "admin' or '1'='1"  # After all steps
```

```python
        if self.validate_legitimate_login(normalized_input):
            processing_time = time.time() - start_time
            result = {
                'threat_detected': False,
                'threat_type': 'BENIGN_LOGIN',
                'explanation': 'Detected legitimate login pattern',
                'mitigation_advice': 'Input appears to be legitimate login attempt',
                'detection_method': 'legitimate_pattern_regex',
                'processing_time': processing_time,
                'model_version': 'advanced-security-v1.0',
                'pattern_matched': 'legitimate_login_pattern'
            }
            self.refresh_stats('legitimate_login', processing_time)
            return result
```
**What this means:**
- Check whitelist first (fastest check)
- If match: Return immediately (no threat)
- Calculate processing time: `current_time - start_time`
- Create result dictionary with all details
- Update statistics
- Return result

```python
        for threat_type, patterns in self.security_signatures.items():
            for pattern in patterns:
                if re.search(pattern, input_lower, re.IGNORECASE):
                    processing_time = time.time() - start_time
                    result = {
                        'threat_detected': True,
                        'threat_type': threat_type,
                        'explanation': f'Detected {threat_type.lower()} pattern',
                        'mitigation_advice': f'Input blocked due to {threat_type.lower()} detection',
                        'detection_method': 'security_signatures',
                        'processing_time': processing_time,
                        'model_version': 'advanced-security-v1.0',
                        'pattern_matched': pattern,
                        'api_called': False
                    }
                    return result
```
**Breakdown:**
- `.items()`: Get key-value pairs from dictionary
  - `threat_type`: 'SQL_INJECTION'
  - `patterns`: List of regex patterns
- Loop through each pattern
- `re.search(pattern, text, flags)`: Check if pattern matches
- If match found: Return immediately (threat detected)
- `api_called: False`: Didn't need AI (regex caught it)

```python
        ai_result = self.perform_ai_analysis(normalized_input)
        total_processing_time = time.time() - start_time
        
        result = {
            'threat_detected': ai_result['threat_detected'],
            'threat_type': ai_result['threat_type'],
            'explanation': ai_result['explanation'],
            'mitigation_advice': ai_result['mitigation_advice'],
            'detection_method': 'hybrid_ai_analysis',
            'processing_time': total_processing_time,
            'model_version': 'advanced-security-v1.0',
            'pattern_matched': 'none',
            'api_called': True,
            'ai_response': ai_result['ai_response']
        }
        
        return result
```
**What this means:**
- If no regex match: Use AI for analysis
- Get AI result and merge with standard fields
- `api_called: True`: We used AI
- Return combined result

#### Lines 201-256: AI Analysis

```python
    def perform_ai_analysis(self, input_text: str) -> Dict:
        """Send input to LLM and let it decide if threat or safe."""
        try:
            ollama.host = self.ollama_host
            
            prompt = f"""Analyze this login input for security threats. Respond with ONLY one word first (THREAT or SAFE), then explain your decision.

Input: {input_text}

Response format: Start with THREAT or SAFE, then provide explanation."""
```
**Breakdown:**
- Set Ollama host
- Create prompt for AI
- **Prompt engineering**: We tell AI exactly how to respond
- Format: Start with THREAT or SAFE (makes parsing easier)

```python
            response = ollama.generate(
                model=self.ai_model,
                prompt=prompt,
                options={"temperature": 0.8}
            )
            
            llm_response = response['response'].strip()
```
**Breakdown:**
- `ollama.generate()`: Call Ollama API
- `model`: Which AI model to use
- `prompt`: Our question
- `temperature`: 0.0-1.0 (lower = more deterministic, higher = more creative)
  - 0.8 is balanced
- `response['response']`: Extract AI's text response
- `.strip()`: Remove whitespace

```python
            is_threat = False
            threat_type = 'LLM_ANALYSIS_SAFE'
            
            if llm_response.upper().startswith('THREAT'):
                is_threat = True
                threat_type = 'LLM_DETECTED_THREAT'
                logger.info(f"LLM detected threat in input: {input_text[:50]}...")
            elif llm_response.upper().startswith('SAFE'):
                is_threat = False
                threat_type = 'LLM_ANALYSIS_SAFE'
                logger.info(f"LLM classified input as safe: {input_text[:50]}...")
            else:
                logger.warning(f"LLM response didn't start with THREAT/SAFE: {llm_response[:100]}")
                is_threat = False
                threat_type = 'LLM_ANALYSIS_UNCERTAIN'
```
**Breakdown:**
- Initialize default values
- `.upper().startswith('THREAT')`: Check if starts with "THREAT" (case insensitive)
- If THREAT: Set flags appropriately
- If SAFE: Set flags for safe
- If neither: Log warning and default to safe
  - **Fail-safe**: If AI doesn't follow format, assume safe
- `input_text[:50]`: First 50 characters (for logging)

```python
            return {
                'threat_detected': is_threat,
                'threat_type': threat_type,
                'explanation': f'LLM Decision: {llm_response[:200]}',
                'mitigation_advice': 'Blocked by AI analysis' if is_threat else 'Allowed by AI analysis',
                'ai_response': llm_response
            }
```
**What this means:**
- Return structured dictionary
- Include AI's full response (for debugging)
- Truncate explanation to 200 chars

```python
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return {
                'threat_detected': False,
                'threat_type': 'ERROR',
                'explanation': f'Error in AI analysis: {str(e)}',
                'mitigation_advice': 'Error - could not get LLM response',
                'ai_response': f'Error: {str(e)}'
            }
```
**Error Handling:**
- If anything goes wrong: Catch exception
- Log the error
- Return safe result (fail-open)
- Include error details in response

---

## Practical Examples

### Example 1: Normal Login Flow

**Input:** username: `alice`, password: `MyPassword123`

```
1. User submits form
   ↓
2. login_app.py receives:
   username = "alice"
   password = "MyPassword123"
   ip = "192.168.1.100"
   ↓
3. Create request:
   {
     "input": "username: alice, password: MyPassword123",
     "ip_address": "192.168.1.100"
   }
   ↓
4. Send to threat_detector.py
   ↓
5. Threat detector analyzes:
   - Normalize: "username: alice, password: mypassword123"
   - Check whitelist: NO MATCH
   - Check regex: NO MATCH (no attack patterns)
   - Ask AI: "Analyze: username: alice, password: mypassword123"
   - AI responds: "SAFE - Normal login credentials"
   ↓
6. Return result:
   {
     "threat_detected": false,
     "threat_type": "LLM_ANALYSIS_SAFE",
     "explanation": "LLM Decision: SAFE - Normal login credentials"
   }
   ↓
7. login_app.py stores in database
   ↓
8. Show success page to user
```

### Example 2: SQL Injection Attack

**Input:** username: `admin' OR '1'='1`, password: `anything`

```
1. User submits form
   ↓
2. login_app.py receives:
   username = "admin' OR '1'='1"
   password = "anything"
   ↓
3. Send to threat_detector.py
   ↓
4. Threat detector analyzes:
   - Normalize: "username: admin' or '1'='1, password: anything"
   - Check whitelist: NO MATCH
   - Check regex patterns:
     * Pattern: r"(?i)'\s*or\s*'"
     * Input: "admin' or '1'='1"
     * MATCH FOUND! ✓
   ↓
5. Return immediately (no AI needed):
   {
     "threat_detected": true,
     "threat_type": "SQL_INJECTION",
     "explanation": "Detected sql_injection pattern",
     "pattern_matched": "(?i)'\\s*or\\s*'",
     "api_called": false
   }
   ↓
6. login_app.py stores in database with threat flag
   ↓
7. Show success page (system allows all logins for monitoring)
```

### Example 3: Legitimate Whitelisted Login

**Input:** username: `AAA`, password: `Aston1`

```
1. Send to threat_detector.py
   ↓
2. Threat detector analyzes:
   - Normalize: "username: aaa, password: aston1"
   - Check whitelist:
     * Look for ('AAA', 'Aston1') pair
     * Check: "aaa" in input? YES
     * Check: "aston1" in input? YES
     * MATCH FOUND! ✓
   ↓
3. Return immediately (skip regex and AI):
   {
     "threat_detected": false,
     "threat_type": "BENIGN_LOGIN",
     "explanation": "Detected legitimate login pattern",
     "detection_method": "legitimate_pattern_regex",
     "processing_time": 0.0001  (very fast!)
   }
```

---

## 🎯 Key Takeaways

1. **Modular Design**: Each function does one thing well
2. **Error Handling**: Try-except blocks prevent crashes
3. **Type Hints**: Make code more readable and catch bugs
4. **Logging**: Better than print() for production code
5. **Configuration**: Use environment variables for flexibility
6. **Database**: Persist data between runs
7. **API Communication**: Services talk via HTTP/JSON
8. **Fail-Safe**: Default to safe when unsure
9. **Performance**: Track timing, optimize hot paths
10. **Documentation**: Comments and docstrings explain why

---

## 🚀 Next Steps

1. **Run the code** with print statements to see data flow
2. **Modify patterns** to detect other attacks
3. **Add features** like email notifications
4. **Experiment** with different AI models
5. **Build your own** project using these patterns!

Happy Learning! 🎓
