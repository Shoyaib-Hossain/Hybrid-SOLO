# 📚 Programming Tutorial: Building a Web Security System Step by Step

Welcome to this comprehensive programming tutorial! This guide will teach you programming concepts using a real-world project: a **Hybrid Web Security System** that combines web development, APIs, databases, and artificial intelligence.

## 🎯 What You'll Learn

By following this tutorial, you'll understand:
- **Python programming fundamentals**
- **Web development with Flask**
- **Database operations with SQLite**
- **API design and integration**
- **AI/Machine Learning integration**
- **Security concepts**
- **Multi-service architecture**

## 📖 Table of Contents

1. [Understanding the Project](#1-understanding-the-project)
2. [Python Basics Review](#2-python-basics-review)
3. [Building the Web Application](#3-building-the-web-application)
4. [Creating the Threat Detection Service](#4-creating-the-threat-detection-service)
5. [Connecting the Services](#5-connecting-the-services)
6. [Running and Testing](#6-running-and-testing)
7. [Exercises and Challenges](#7-exercises-and-challenges)

---

## 1. Understanding the Project

### 1.1 What Does This System Do?

This is a **security monitoring system** that:
1. Provides a login page for users
2. Analyzes every login attempt for security threats (SQL injection, XSS attacks, etc.)
3. Uses both pattern matching (regex) and AI to detect threats
4. Logs all attempts in a database
5. Provides a dashboard to monitor security events

### 1.2 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                            │
│                (Views login page, enters credentials)        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              WEB APPLICATION (Port 3000)                     │
│              File: host-b-webapp/login_app.py                │
│                                                              │
│  • Serves HTML login page                                   │
│  • Receives username/password                               │
│  • Sends data to Threat Detector                            │
│  • Shows results to user                                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ HTTP POST Request
                            ▼
┌─────────────────────────────────────────────────────────────┐
│         THREAT DETECTOR SERVICE (Port 8081)                  │
│         File: host-c-detection/threat_detector.py            │
│                                                              │
│  • Analyzes input for threats                               │
│  • Uses regex patterns                                       │
│  • Uses AI (Ollama/LLM) for smart detection                 │
│  • Returns threat assessment                                │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Technology Stack

- **Language**: Python 3
- **Web Framework**: Flask (for creating web APIs)
- **Database**: SQLite (for storing data)
- **AI Engine**: Ollama (for intelligent threat detection)
- **Frontend**: HTML/CSS/JavaScript

---

## 2. Python Basics Review

### 2.1 Variables and Data Types

```python
# Variables store data
username = "Alice"           # String (text)
age = 25                     # Integer (whole number)
height = 5.6                 # Float (decimal number)
is_admin = True              # Boolean (True/False)
```

### 2.2 Lists and Dictionaries

```python
# Lists - ordered collections
users = ["Alice", "Bob", "Charlie"]
print(users[0])  # Output: Alice

# Dictionaries - key-value pairs
user_data = {
    'username': 'Alice',
    'age': 25,
    'role': 'admin'
}
print(user_data['username'])  # Output: Alice
```

### 2.3 Functions

Functions are reusable blocks of code:

```python
def greet_user(name):
    """This function greets a user by name."""
    message = f"Hello, {name}!"
    return message

# Using the function
result = greet_user("Alice")
print(result)  # Output: Hello, Alice!
```

### 2.4 Classes and Objects

Classes are blueprints for creating objects:

```python
class User:
    """Represents a user in our system."""
    
    def __init__(self, username, email):
        """Constructor - runs when creating a new User."""
        self.username = username
        self.email = email
    
    def display_info(self):
        """Method to display user information."""
        print(f"User: {self.username}, Email: {self.email}")

# Creating an object (instance) of the class
alice = User("alice", "alice@example.com")
alice.display_info()  # Output: User: alice, Email: alice@example.com
```

### 2.5 Importing Modules

Python has many built-in modules and libraries:

```python
# Import entire module
import datetime
current_time = datetime.datetime.now()

# Import specific function
from datetime import datetime
current_time = datetime.now()

# Import with alias
import pandas as pd
data = pd.DataFrame()
```

---

## 3. Building the Web Application

### 3.1 Understanding Flask

Flask is a **micro web framework** for Python. It helps you create web applications easily.

#### Basic Flask Example:

```python
from flask import Flask

# Create a Flask application
app = Flask(__name__)

# Define a route (URL endpoint)
@app.route('/')
def home():
    """This function runs when someone visits the home page."""
    return "Hello, World!"

# Run the application
if __name__ == '__main__':
    app.run()
```

**Key Concepts:**
- `@app.route('/')`: This is a **decorator** that maps a URL to a function
- When someone visits `http://localhost:5000/`, Flask calls the `home()` function
- The function returns what to show in the browser

### 3.2 The Login Application Structure

Let's break down `login_app.py` step by step:

#### Step 1: Imports and Setup

```python
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import requests
import json
import logging
import os
from datetime import datetime
import sqlite3

# Create Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # For session management
```

**What's happening:**
- We import necessary modules
- Create a Flask application instance
- Set a secret key (needed for sessions and security)

#### Step 2: Configuration

```python
# Configuration variables
THREAT_DETECTOR_HOST = 'localhost'
THREAT_DETECTOR_PORT = '8081'
SECURITY_DETECTION_URL = f'http://{THREAT_DETECTOR_HOST}:{THREAT_DETECTOR_PORT}/analyze'
```

**What's happening:**
- We define where the threat detector service is running
- This URL is where we'll send login attempts for analysis

#### Step 3: Database Setup

```python
def setup_database(self):
    """Create SQLite database and table for storing login attempts."""
    os.makedirs('data', exist_ok=True)  # Create 'data' folder if it doesn't exist
    
    conn = sqlite3.connect('data/web_sessions.db')  # Connect to database
    cursor = conn.cursor()  # Create a cursor to execute SQL
    
    # Create table if it doesn't exist
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
    
    conn.commit()  # Save changes
    conn.close()   # Close connection
```

**What's happening:**
- Creates a directory to store our database
- Connects to SQLite database (creates it if it doesn't exist)
- Creates a table with columns for storing login information
- The table structure defines what data we can store

**SQL Basics:**
- `INTEGER PRIMARY KEY AUTOINCREMENT`: Auto-incrementing ID
- `TEXT`: Stores text strings
- `BOOLEAN`: Stores True/False values
- `DATETIME`: Stores date and time

#### Step 4: Handling Login Requests

```python
@app.route('/login', methods=['POST'])
def process_authentication():
    """Process login form submission with threat detection."""
    
    # Get data from the form
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip_address = request.remote_addr  # Get user's IP address
    
    # Validate input
    if not username or not password:
        flash('Please provide both username and password', 'error')
        return redirect(url_for('authentication_portal'))
    
    # Send to threat detector for analysis
    attempt_record = auth_tracker.record_attempt(username, password, ip_address)
    
    # Show success page
    flash('Authentication successful!', 'success')
    return render_template('success.html', username=username)
```

**What's happening:**
1. `@app.route('/login', methods=['POST'])`: This function handles POST requests to `/login`
2. `request.form.get()`: Gets data from the HTML form
3. `request.remote_addr`: Gets the user's IP address
4. We validate the input (check it's not empty)
5. Send to threat detector for analysis
6. Show success page to user

#### Step 5: Sending Data to Threat Detector

```python
def record_attempt(self, username, password, ip_address):
    """Record a login attempt and forward it to threat detection service."""
    
    # Prepare data to send
    analysis_request = {
        'input': f"username: {username}, password: {password}",
        'ip_address': ip_address
    }
    
    # Send POST request to threat detector
    response = requests.post(
        SECURITY_DETECTION_URL,
        json=analysis_request,
        timeout=30
    )
    
    # Process the response
    if response.status_code == 200:
        security_analysis = response.json()
        threat_detected = security_analysis.get('threat_detected', False)
        
        if threat_detected:
            logger.warning(f"Threat detected from {ip_address}")
        else:
            logger.info(f"Safe login attempt from {ip_address}")
    
    return attempt_data
```

**What's happening:**
1. Create a dictionary with the data to analyze
2. Use `requests.post()` to send HTTP POST request
3. Get JSON response back
4. Log the result

**API Communication:**
- **Request**: We send data TO the threat detector
- **Response**: Threat detector sends analysis back
- **JSON**: Standard format for exchanging data between services

### 3.3 Understanding Routes and Endpoints

Routes are like addresses for different pages:

```python
@app.route('/')                    # Home page: http://localhost:3000/
@app.route('/login')               # Login page: http://localhost:3000/login
@app.route('/monitor')             # Monitor page: http://localhost:3000/monitor
@app.route('/api/attempts')        # API endpoint: http://localhost:3000/api/attempts
```

**GET vs POST:**
- **GET**: Retrieve data (viewing a page)
- **POST**: Send data (submitting a form)

```python
@app.route('/login', methods=['GET'])    # View login form
@app.route('/login', methods=['POST'])   # Submit login form
```

### 3.4 Working with Templates

Flask uses **Jinja2** templates to generate HTML:

```python
@app.route('/')
def home():
    username = "Alice"
    return render_template('home.html', username=username)
```

In `home.html`:
```html
<h1>Welcome, {{ username }}!</h1>
```

Output: `Welcome, Alice!`

---

## 4. Creating the Threat Detection Service

### 4.1 Understanding the Detection Strategy

The threat detector uses a **hybrid approach**:

1. **Pattern Matching (Regex)**: Fast, checks for known attack patterns
2. **AI Analysis (LLM)**: Intelligent, understands context

```
Input → Check Whitelist → Regex Patterns → AI Analysis → Result
```

### 4.2 Pattern Matching with Regular Expressions

Regular expressions (regex) are patterns used to match text:

```python
import re

# Simple pattern matching
text = "admin' OR '1'='1"
pattern = r"'\s*or\s*'"

if re.search(pattern, text, re.IGNORECASE):
    print("SQL injection detected!")
```

**Common Regex Patterns:**
- `\s`: Whitespace
- `\d`: Digit
- `*`: Zero or more
- `+`: One or more
- `|`: OR
- `(?i)`: Case insensitive

### 4.3 The Security Analyzer Class

```python
class AdvancedSecurityAnalyzer:
    """Core threat detection engine."""
    
    def __init__(self):
        """Initialize with security patterns."""
        self.security_signatures = {
            'SQL_INJECTION': [
                r"(?i)'\s*or\s*'",         # ' or '
                r"(?i);\s*drop\s+table",    # DROP TABLE
                r"(?i)union\s+select"       # UNION SELECT
            ]
        }
    
    def comprehensive_security_scan(self, input_text, ip_address):
        """Main detection method."""
        # 1. Normalize input
        normalized_input = input_text.lower().strip()
        
        # 2. Check whitelist
        if self.validate_legitimate_login(normalized_input):
            return {'threat_detected': False}
        
        # 3. Check regex patterns
        for threat_type, patterns in self.security_signatures.items():
            for pattern in patterns:
                if re.search(pattern, normalized_input):
                    return {
                        'threat_detected': True,
                        'threat_type': threat_type
                    }
        
        # 4. AI analysis
        return self.perform_ai_analysis(normalized_input)
```

**Step-by-Step Flow:**

1. **Normalization**: Convert to lowercase, remove extra spaces
2. **Whitelist Check**: Is it a known legitimate login?
3. **Regex Scan**: Does it match attack patterns?
4. **AI Analysis**: Let AI decide if unclear

### 4.4 AI Integration with Ollama

```python
def perform_ai_analysis(self, input_text):
    """Use AI to analyze input."""
    
    # Create prompt for AI
    prompt = f"""Analyze this login input for security threats. 
    Respond with ONLY one word first (THREAT or SAFE), then explain.
    
    Input: {input_text}
    
    Response format: Start with THREAT or SAFE, then provide explanation."""
    
    # Call Ollama API
    response = ollama.generate(
        model=self.ai_model,
        prompt=prompt,
        options={"temperature": 0.8}
    )
    
    # Parse response
    llm_response = response['response'].strip()
    
    if llm_response.upper().startswith('THREAT'):
        return {
            'threat_detected': True,
            'threat_type': 'LLM_DETECTED_THREAT',
            'explanation': llm_response
        }
    else:
        return {
            'threat_detected': False,
            'threat_type': 'LLM_ANALYSIS_SAFE',
            'explanation': llm_response
        }
```

**How It Works:**
1. Create a prompt asking AI to classify input
2. Send prompt to Ollama (local AI model)
3. Parse response - check if it starts with "THREAT" or "SAFE"
4. Return structured result

### 4.5 Creating API Endpoints

```python
@app.route('/analyze', methods=['POST'])
def execute_security_analysis():
    """Main threat detection API endpoint."""
    
    # Get data from request
    data = request.json
    user_input = data.get('input', '')
    ip_address = data.get('ip_address', '')
    
    # Perform analysis
    result = security_analyzer.comprehensive_security_scan(user_input, ip_address)
    
    # Add timestamp
    result['timestamp'] = datetime.now().isoformat()
    
    # Store in database
    security_analyzer.store_detection_record(user_input, result, ip_address)
    
    # Return JSON response
    return jsonify(result)
```

**API Design:**
- **Endpoint**: `/analyze`
- **Method**: POST
- **Input**: JSON with user input
- **Output**: JSON with threat analysis

---

## 5. Connecting the Services

### 5.1 How Services Communicate

Services communicate using **HTTP requests**:

```python
# Web App (Client)
response = requests.post(
    'http://localhost:8081/analyze',
    json={'input': 'username: admin, password: secret'},
    timeout=30
)

result = response.json()
```

```python
# Threat Detector (Server)
@app.route('/analyze', methods=['POST'])
def execute_security_analysis():
    data = request.json
    # Process and respond
    return jsonify({'threat_detected': False})
```

### 5.2 Error Handling

Always handle errors when communicating between services:

```python
try:
    response = requests.post(SECURITY_DETECTION_URL, json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
    else:
        logger.error(f"Service returned error: {response.status_code}")
        result = {'error': 'Service unavailable'}
        
except requests.exceptions.Timeout:
    logger.error("Request timed out")
    result = {'error': 'Timeout'}
    
except requests.exceptions.ConnectionError:
    logger.error("Could not connect to service")
    result = {'error': 'Connection failed'}
    
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    result = {'error': 'Unknown error'}
```

**Error Types:**
- **Timeout**: Service took too long to respond
- **ConnectionError**: Can't reach the service
- **HTTP Errors**: Service returned error status code

---

## 6. Running and Testing

### 6.1 Installation Steps

```bash
# 1. Install Python dependencies
cd host-b-webapp
pip install -r requirements.txt

cd ../host-c-detection
pip install -r requirements_agents.txt

# 2. Install Ollama (for AI)
# Download from: https://ollama.ai
ollama serve
ollama pull llama2

# 3. Start the system
python3 start_all.py
```

### 6.2 Testing the Application

**Test 1: Normal Login**
```bash
curl -X POST http://localhost:3000/login \
  -d "username=Alice&password=secret123"
```

**Test 2: SQL Injection Attempt**
```bash
curl -X POST http://localhost:3000/login \
  -d "username=admin' OR '1'='1&password=anything"
```

**Test 3: Check Statistics**
```bash
curl http://localhost:8081/stats
```

### 6.3 Viewing the Dashboard

Open your browser:
- Login Page: http://localhost:3000
- Security Monitor: http://localhost:3000/monitor
- API Stats: http://localhost:8081/stats

---

## 7. Exercises and Challenges

### 7.1 Beginner Exercises

**Exercise 1: Add a New Route**
Create a new route in `login_app.py` that shows "About Us" page:

```python
@app.route('/about')
def about_page():
    return "This is a security monitoring system!"
```

**Exercise 2: Add Logging**
Add a log message when someone visits the home page:

```python
@app.route('/')
def home():
    logger.info("Someone visited the home page!")
    return render_template('login.html')
```

**Exercise 3: Modify Database**
Add a new column to track failed login counts:

```sql
ALTER TABLE login_sessions ADD COLUMN failed_attempts INTEGER DEFAULT 0;
```

### 7.2 Intermediate Challenges

**Challenge 1: Add Email Validation**
Create a function to validate email addresses:

```python
import re

def is_valid_email(email):
    """Check if email format is valid."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Test it
print(is_valid_email("user@example.com"))  # True
print(is_valid_email("invalid-email"))      # False
```

**Challenge 2: Rate Limiting**
Implement basic rate limiting to prevent brute force:

```python
from collections import defaultdict
import time

login_attempts = defaultdict(list)

def is_rate_limited(ip_address, max_attempts=5, time_window=60):
    """Check if IP has exceeded rate limit."""
    now = time.time()
    
    # Remove old attempts
    login_attempts[ip_address] = [
        timestamp for timestamp in login_attempts[ip_address]
        if now - timestamp < time_window
    ]
    
    # Check count
    if len(login_attempts[ip_address]) >= max_attempts:
        return True
    
    # Record this attempt
    login_attempts[ip_address].append(now)
    return False
```

**Challenge 3: Add More Threat Patterns**
Add detection for XSS (Cross-Site Scripting):

```python
'XSS': [
    r"(?i)<script[^>]*>.*?</script>",
    r"(?i)javascript:",
    r"(?i)onerror\s*=",
    r"(?i)onload\s*="
]
```

### 7.3 Advanced Projects

**Project 1: User Dashboard**
Create a dashboard showing:
- Number of login attempts
- Success/failure rate
- Most common attack types
- Timeline graph

**Project 2: Email Notifications**
Send email alerts when threats are detected:

```python
import smtplib
from email.mime.text import MIMEText

def send_alert(threat_info):
    """Send email alert for detected threat."""
    msg = MIMEText(f"Threat detected: {threat_info}")
    msg['Subject'] = 'Security Alert'
    msg['From'] = 'security@example.com'
    msg['To'] = 'admin@example.com'
    
    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)
```

**Project 3: Machine Learning Model**
Train a custom ML model for threat detection:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# 1. Prepare training data
X_train = ["normal login", "admin' OR '1'='1", ...]
y_train = [0, 1, ...]  # 0=safe, 1=threat

# 2. Create and train model
vectorizer = TfidfVectorizer()
X_vectors = vectorizer.fit_transform(X_train)

classifier = RandomForestClassifier()
classifier.fit(X_vectors, y_train)

# 3. Predict on new input
def ml_predict(input_text):
    X_new = vectorizer.transform([input_text])
    prediction = classifier.predict(X_new)
    return prediction[0] == 1  # True if threat
```

---

## 📚 Additional Resources

### Python Learning:
- Python.org Official Tutorial: https://docs.python.org/3/tutorial/
- Real Python: https://realpython.com/
- Python for Beginners: https://www.python.org/about/gettingstarted/

### Flask Framework:
- Flask Documentation: https://flask.palletsprojects.com/
- Flask Mega-Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

### Database:
- SQLite Tutorial: https://www.sqlitetutorial.net/
- SQL Basics: https://www.w3schools.com/sql/

### APIs:
- REST API Tutorial: https://restfulapi.net/
- HTTP Methods: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

### Security:
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Web Security: https://developer.mozilla.org/en-US/docs/Web/Security

---

## 🎓 Key Takeaways

1. **Start Simple**: Begin with basic concepts, then build complexity
2. **Break It Down**: Divide large problems into smaller, manageable pieces
3. **Test Often**: Test your code frequently as you build
4. **Read Documentation**: Official docs are your best friend
5. **Practice**: The more you code, the better you get
6. **Learn from Errors**: Errors are learning opportunities
7. **Comment Your Code**: Help your future self understand your code

---

## 🤝 Next Steps

1. **Run the Code**: Get the system running on your machine
2. **Experiment**: Make small changes and see what happens
3. **Add Features**: Try the exercises and challenges
4. **Read the Code**: Study how each part works
5. **Build Something New**: Use what you learned in your own project

Remember: **Every expert was once a beginner!** Keep learning, keep coding, and don't be afraid to make mistakes.

Happy Coding! 🚀
