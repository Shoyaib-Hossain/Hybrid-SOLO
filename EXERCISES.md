# 💪 Programming Exercises and Challenges

This document provides hands-on exercises to help you learn programming by doing. Start with Level 1 and progress to more advanced challenges.

## 📋 Table of Contents
1. [Level 1: Python Basics](#level-1-python-basics)
2. [Level 2: Working with Data](#level-2-working-with-data)
3. [Level 3: Flask Web Development](#level-3-flask-web-development)
4. [Level 4: Database Operations](#level-4-database-operations)
5. [Level 5: APIs and Integration](#level-5-apis-and-integration)
6. [Level 6: Security Features](#level-6-security-features)
7. [Level 7: Advanced Projects](#level-7-advanced-projects)

---

## Level 1: Python Basics

### Exercise 1.1: Variables and Strings

**Task:** Create a program that greets users.

```python
# TODO: Complete this program
name = "Alice"
age = 25

# Print: "Hello, Alice! You are 25 years old."
print(f"Hello, {name}! You are {age} years old.")

# Now make it interactive:
# Ask user for their name and age, then greet them
user_name = input("What's your name? ")
user_age = input("How old are you? ")
print(f"Hello, {user_name}! You are {user_age} years old.")
```

**Expected Output:**
```
What's your name? Bob
How old are you? 30
Hello, Bob! You are 30 years old.
```

### Exercise 1.2: Lists and Loops

**Task:** Work with a list of usernames.

```python
# TODO: Complete these tasks
usernames = ["alice", "bob", "charlie", "diana"]

# 1. Print all usernames in uppercase
for username in usernames:
    print(username.upper())

# 2. Print only usernames that start with 'a'
for username in usernames:
    if username.startswith('a'):
        print(username)

# 3. Count how many usernames have more than 4 letters
count = 0
for username in usernames:
    if len(username) > 4:
        count += 1
print(f"Usernames with more than 4 letters: {count}")

# 4. Add your own username to the list
usernames.append("your_name")
print(usernames)
```

### Exercise 1.3: Dictionaries

**Task:** Store and retrieve user information.

```python
# TODO: Complete this program
user = {
    'username': 'alice',
    'email': 'alice@example.com',
    'role': 'admin',
    'active': True
}

# 1. Print the user's email
print(user['email'])

# 2. Change the role to 'moderator'
user['role'] = 'moderator'

# 3. Add a new field: 'last_login' with today's date
from datetime import datetime
user['last_login'] = datetime.now().isoformat()

# 4. Print all keys and values
for key, value in user.items():
    print(f"{key}: {value}")
```

### Exercise 1.4: Functions

**Task:** Create reusable functions.

```python
# TODO: Implement these functions

def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

def calculate_age(birth_year):
    """Calculate age from birth year."""
    from datetime import datetime
    current_year = datetime.now().year
    return current_year - birth_year

def is_valid_username(username):
    """Check if username is valid (3-20 chars, alphanumeric)."""
    if len(username) < 3 or len(username) > 20:
        return False
    return username.isalnum()

# Test your functions
print(greet("Alice"))  # Should print: Hello, Alice!
print(calculate_age(1995))  # Should print: 29 (if current year is 2024)
print(is_valid_username("alice123"))  # Should print: True
print(is_valid_username("ab"))  # Should print: False
```

### Exercise 1.5: Classes

**Task:** Create a User class.

```python
# TODO: Complete this class
class User:
    def __init__(self, username, email):
        """Initialize a new user."""
        self.username = username
        self.email = email
        self.login_count = 0
    
    def login(self):
        """Record a login."""
        self.login_count += 1
        print(f"{self.username} logged in. Total logins: {self.login_count}")
    
    def get_info(self):
        """Return user information as a string."""
        return f"User: {self.username}, Email: {self.email}, Logins: {self.login_count}"

# Test your class
alice = User("alice", "alice@example.com")
alice.login()  # Should print: alice logged in. Total logins: 1
alice.login()  # Should print: alice logged in. Total logins: 2
print(alice.get_info())  # Should print user info
```

**Challenge:** Extend the User class with:
- A method to change email
- A method to check if user is active (based on last login date)
- A class variable to track total number of users

---

## Level 2: Working with Data

### Exercise 2.1: Reading Files

**Task:** Read and process a log file.

```python
# Create a sample log file first
with open('/tmp/server.log', 'w') as f:
    f.write("2024-01-15 10:30:00 - INFO - Server started\n")
    f.write("2024-01-15 10:31:00 - ERROR - Connection failed\n")
    f.write("2024-01-15 10:32:00 - INFO - Request received\n")
    f.write("2024-01-15 10:33:00 - ERROR - Database timeout\n")

# TODO: Read the file and count ERROR messages
with open('/tmp/server.log', 'r') as f:
    lines = f.readlines()
    error_count = 0
    for line in lines:
        if 'ERROR' in line:
            error_count += 1
            print(line.strip())
    print(f"\nTotal errors: {error_count}")
```

### Exercise 2.2: JSON Processing

**Task:** Work with JSON data.

```python
import json

# Sample user data
users_json = '''[
    {"username": "alice", "age": 25, "role": "admin"},
    {"username": "bob", "age": 30, "role": "user"},
    {"username": "charlie", "age": 35, "role": "user"}
]'''

# TODO: Parse JSON and complete tasks
users = json.loads(users_json)

# 1. Print all admin users
print("Admin users:")
for user in users:
    if user['role'] == 'admin':
        print(user['username'])

# 2. Calculate average age
total_age = sum(user['age'] for user in users)
average_age = total_age / len(users)
print(f"\nAverage age: {average_age}")

# 3. Add a new user and save to file
new_user = {"username": "diana", "age": 28, "role": "user"}
users.append(new_user)

with open('/tmp/users.json', 'w') as f:
    json.dump(users, f, indent=2)

print("\nSaved to users.json")
```

### Exercise 2.3: Regular Expressions

**Task:** Detect patterns in text.

```python
import re

# Sample login attempts
attempts = [
    "username: alice, password: secret123",
    "username: admin' OR '1'='1, password: anything",
    "username: bob, password: <script>alert('xss')</script>",
    "username: charlie, password: MyPass456"
]

# TODO: Create patterns to detect threats
sql_injection_pattern = r"(?i)'\s*or\s*'"
xss_pattern = r"<script.*?>.*?</script>"

# Check each attempt
for attempt in attempts:
    print(f"\nChecking: {attempt}")
    
    if re.search(sql_injection_pattern, attempt, re.IGNORECASE):
        print("  ⚠️ SQL Injection detected!")
    
    if re.search(xss_pattern, attempt, re.IGNORECASE):
        print("  ⚠️ XSS Attack detected!")
    
    if not re.search(sql_injection_pattern, attempt) and not re.search(xss_pattern, attempt):
        print("  ✅ Safe login attempt")
```

**Challenge:** Add patterns to detect:
- Command injection (`;`, `|`, `&&`)
- Path traversal (`../`, `..\\`)
- Email addresses (for validation)

---

## Level 3: Flask Web Development

### Exercise 3.1: Simple Flask App

**Task:** Create your first Flask application.

```python
from flask import Flask

app = Flask(__name__)

# TODO: Add routes
@app.route('/')
def home():
    return "Welcome to My App!"

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/user/<username>')
def user_profile(username):
    return f"Profile page for {username}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Test it:**
```bash
python app.py
# Visit: http://localhost:5000/
# Visit: http://localhost:5000/about
# Visit: http://localhost:5000/user/alice
```

### Exercise 3.2: HTML Templates

**Task:** Use templates to generate HTML.

First, create `templates/greeting.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Greeting</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
    <p>Welcome to the site.</p>
    
    {% if is_admin %}
        <p><strong>You are an administrator.</strong></p>
    {% endif %}
    
    <h2>Your Info:</h2>
    <ul>
    {% for key, value in user_info.items() %}
        <li>{{ key }}: {{ value }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

Then update your Flask app:
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/greet/<name>')
def greet(name):
    user_info = {
        'username': name,
        'email': f'{name}@example.com',
        'joined': '2024-01-15'
    }
    is_admin = (name == 'alice')
    return render_template('greeting.html', 
                          name=name, 
                          is_admin=is_admin,
                          user_info=user_info)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Exercise 3.3: Forms and POST Requests

**Task:** Handle form submissions.

Create `templates/login_form.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <p style="color: {{ 'green' if category == 'success' else 'red' }}">
                    {{ message }}
                </p>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <form method="POST" action="/login">
        <label>Username:</label>
        <input type="text" name="username" required><br><br>
        
        <label>Password:</label>
        <input type="password" name="password" required><br><br>
        
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

Update Flask app:
```python
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# TODO: Implement login functionality
@app.route('/')
def home():
    return render_template('login_form.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Simple validation (in real app, check database)
    if username == 'admin' and password == 'secret':
        flash('Login successful!', 'success')
        return f"Welcome, {username}!"
    else:
        flash('Invalid credentials!', 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## Level 4: Database Operations

### Exercise 4.1: Create and Query Database

**Task:** Work with SQLite database.

```python
import sqlite3
from datetime import datetime

# TODO: Complete the database operations

# 1. Create database and table
conn = sqlite3.connect('/tmp/myapp.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        login_count INTEGER DEFAULT 0
    )
''')
conn.commit()

# 2. Insert users
users_to_add = [
    ('alice', 'alice@example.com'),
    ('bob', 'bob@example.com'),
    ('charlie', 'charlie@example.com')
]

for username, email in users_to_add:
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", 
                      (username, email))
    except sqlite3.IntegrityError:
        print(f"User {username} already exists")

conn.commit()

# 3. Query all users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("\nAll users:")
for user in users:
    print(user)

# 4. Update login count
cursor.execute("UPDATE users SET login_count = login_count + 1 WHERE username = ?", 
              ('alice',))
conn.commit()

# 5. Query specific user
cursor.execute("SELECT username, email, login_count FROM users WHERE username = ?", 
              ('alice',))
alice = cursor.fetchone()
print(f"\nAlice's info: {alice}")

conn.close()
```

### Exercise 4.2: Database with Flask

**Task:** Integrate database with Flask app.

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    """Create database connection."""
    conn = sqlite3.connect('/tmp/myapp.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, login_count FROM users")
    users = cursor.fetchall()
    conn.close()
    
    # Convert to list of dicts
    users_list = [dict(user) for user in users]
    return jsonify(users_list)

@app.route('/api/users/<username>', methods=['GET'])
def get_user(username):
    """Get specific user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create new user."""
    data = request.json
    username = data.get('username')
    email = data.get('email')
    
    if not username or not email:
        return jsonify({'error': 'Username and email required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", 
                      (username, email))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User created', 'username': username}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Username already exists'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Test with curl:**
```bash
# Get all users
curl http://localhost:5000/api/users

# Get specific user
curl http://localhost:5000/api/users/alice

# Create user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "diana", "email": "diana@example.com"}'
```

---

## Level 5: APIs and Integration

### Exercise 5.1: Making API Requests

**Task:** Call external APIs.

```python
import requests
import json

# TODO: Complete these API calls

# 1. Simple GET request
response = requests.get('https://api.github.com/users/github')
if response.status_code == 200:
    user_data = response.json()
    print(f"Username: {user_data['login']}")
    print(f"Name: {user_data['name']}")
    print(f"Public repos: {user_data['public_repos']}")

# 2. POST request with data
data = {
    'username': 'alice',
    'email': 'alice@example.com'
}
response = requests.post('http://localhost:5000/api/users', json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# 3. Error handling
try:
    response = requests.get('http://localhost:9999/api/test', timeout=5)
    response.raise_for_status()  # Raise exception for 4xx/5xx status codes
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Could not connect to server")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Exercise 5.2: Creating a REST API

**Task:** Build a complete REST API for managing tasks.

```python
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    """Initialize database."""
    conn = sqlite3.connect('/tmp/tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# TODO: Implement CRUD operations

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    conn = sqlite3.connect('/tmp/tasks.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get specific task."""
    conn = sqlite3.connect('/tmp/tasks.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    
    if task:
        return jsonify(dict(task))
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create new task."""
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    
    if not title:
        return jsonify({'error': 'Title required'}), 400
    
    conn = sqlite3.connect('/tmp/tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", 
                  (title, description))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': task_id, 'message': 'Task created'}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task."""
    data = request.json
    
    conn = sqlite3.connect('/tmp/tasks.db')
    cursor = conn.cursor()
    
    # Build update query dynamically
    updates = []
    values = []
    
    if 'title' in data:
        updates.append("title = ?")
        values.append(data['title'])
    if 'description' in data:
        updates.append("description = ?")
        values.append(data['description'])
    if 'completed' in data:
        updates.append("completed = ?")
        values.append(data['completed'])
    
    if not updates:
        return jsonify({'error': 'No fields to update'}), 400
    
    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Task updated'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete task."""
    conn = sqlite3.connect('/tmp/tasks.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## Level 6: Security Features

### Exercise 6.1: Input Validation

**Task:** Implement input validation.

```python
import re

# TODO: Implement validation functions

def validate_username(username):
    """Validate username format."""
    if not username:
        return False, "Username is required"
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 20:
        return False, "Username must not exceed 20 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, "Valid"

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Valid"
    return False, "Invalid email format"

def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    return True, "Valid"

# Test validation
test_cases = [
    ('alice', 'valid'),
    ('ab', 'too_short'),
    ('alice@example.com', 'email'),
    ('Password123', 'password')
]

for test_value, test_type in test_cases:
    if test_type == 'valid' or test_type == 'too_short':
        valid, message = validate_username(test_value)
        print(f"Username '{test_value}': {message}")
    elif test_type == 'email':
        valid, message = validate_email(test_value)
        print(f"Email '{test_value}': {message}")
    elif test_type == 'password':
        valid, message = validate_password(test_value)
        print(f"Password: {message}")
```

### Exercise 6.2: SQL Injection Detection

**Task:** Detect SQL injection attempts.

```python
import re

def detect_sql_injection(input_text):
    """Detect SQL injection patterns."""
    patterns = [
        (r"(?i)'\s*or\s*'", "OR condition"),
        (r"(?i)'\s*or\s+\d+\s*=\s*\d+", "Tautology"),
        (r"(?i)'.*?--", "SQL comment"),
        (r"(?i);\s*drop\s+table", "DROP TABLE"),
        (r"(?i);\s*delete\s+from", "DELETE FROM"),
        (r"(?i)union\s+select", "UNION SELECT"),
        (r"(?i)exec\s*\(", "Command execution")
    ]
    
    threats_found = []
    for pattern, description in patterns:
        if re.search(pattern, input_text):
            threats_found.append(description)
    
    return len(threats_found) > 0, threats_found

# TODO: Test with various inputs
test_inputs = [
    "username: alice, password: secret123",
    "admin' OR '1'='1",
    "'; DROP TABLE users--",
    "1' UNION SELECT * FROM passwords--",
    "normal text"
]

for input_text in test_inputs:
    is_threat, threats = detect_sql_injection(input_text)
    print(f"\nInput: {input_text}")
    if is_threat:
        print(f"⚠️ THREAT DETECTED: {', '.join(threats)}")
    else:
        print("✅ Safe")
```

---

## Level 7: Advanced Projects

### Project 7.1: Complete Login System

**Task:** Build a secure login system with all features.

**Requirements:**
1. User registration with validation
2. Password hashing (never store plain passwords!)
3. Login with session management
4. Rate limiting to prevent brute force
5. Logging of all attempts
6. Admin dashboard

**Hint:** Start with this structure:

```python
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# TODO: Implement user registration
# TODO: Implement user login with password hashing
# TODO: Implement session management
# TODO: Implement rate limiting
# TODO: Implement admin dashboard
```

### Project 7.2: API Gateway

**Task:** Create an API gateway that routes requests to different services.

**Requirements:**
1. Accept requests on `/api/*`
2. Route to appropriate backend service
3. Add authentication
4. Log all requests
5. Handle errors gracefully
6. Add rate limiting

### Project 7.3: Real-time Dashboard

**Task:** Build a dashboard that shows live statistics.

**Requirements:**
1. WebSocket connection for real-time updates
2. Display charts and graphs
3. Show login attempts in real-time
4. Alert on suspicious activity
5. Allow filtering and searching

---

## 🎯 Solution Hints

### For Beginners:

1. **Start small**: Complete one exercise at a time
2. **Test frequently**: Run your code after each change
3. **Use print()**: Debug by printing variables
4. **Read errors carefully**: Error messages tell you what's wrong
5. **Google is your friend**: Search for error messages

### For Intermediate:

1. **Read documentation**: Check Flask and SQLite docs
2. **Use debugger**: Step through code line by line
3. **Write tests**: Test your functions
4. **Refactor**: Improve code structure as you learn
5. **Add error handling**: Use try-except blocks

### For Advanced:

1. **Performance**: Profile and optimize slow code
2. **Security**: Always validate and sanitize input
3. **Scalability**: Think about handling many users
4. **Documentation**: Write clear comments and docstrings
5. **Best practices**: Follow PEP 8, use type hints

---

## 📝 Submission Checklist

When completing exercises:

- [ ] Code runs without errors
- [ ] All requirements met
- [ ] Code is properly indented
- [ ] Variables have meaningful names
- [ ] Functions have docstrings
- [ ] Error handling is implemented
- [ ] Code is tested with multiple inputs
- [ ] Comments explain complex logic

---

## 🏆 Achievement Badges

Track your progress:

- [ ] **Python Novice**: Completed Level 1
- [ ] **Data Wrangler**: Completed Level 2
- [ ] **Web Developer**: Completed Level 3
- [ ] **Database Pro**: Completed Level 4
- [ ] **API Master**: Completed Level 5
- [ ] **Security Expert**: Completed Level 6
- [ ] **Full Stack**: Completed Level 7

---

## 💡 Tips for Success

1. **Practice Daily**: Code a little bit every day
2. **Build Projects**: Apply what you learn to real projects
3. **Read Code**: Study code written by others
4. **Ask Questions**: Don't be afraid to ask for help
5. **Teach Others**: Teaching helps you learn better
6. **Stay Curious**: Always be learning new things
7. **Be Patient**: Programming takes time to master

Remember: **Every expert was once a beginner!** Keep practicing and you'll improve. 🚀

---

## 📚 Additional Resources

- Python Documentation: https://docs.python.org/3/
- Flask Documentation: https://flask.palletsprojects.com/
- Real Python Tutorials: https://realpython.com/
- Stack Overflow: https://stackoverflow.com/
- GitHub: Browse open source projects for examples

Good luck with your learning journey! 🎓
