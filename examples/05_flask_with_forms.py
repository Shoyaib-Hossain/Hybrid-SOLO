#!/usr/bin/env python3
"""
Example 5: Flask with Forms
============================

This demonstrates:
- HTML forms with Flask
- POST request handling
- Form validation
- Flash messages
- Redirects
"""

from flask import Flask, render_template_string, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'learning-secret-key'

# In-memory storage for simplicity
users = []

# HTML template for the form
FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>User Registration</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 8px; font-size: 14px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .messages { margin: 20px 0; }
        .success { background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; }
        .error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; }
        .user-list { background: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 20px; }
        a { color: #007bff; text-decoration: none; }
    </style>
</head>
<body>
    <h1>User Registration</h1>
    
    <!-- Flash messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="messages">
                {% for category, message in messages %}
                    <div class="{{ category }}">{{ message }}</div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}
    
    <!-- Registration form -->
    <form method="POST" action="/register">
        <div class="form-group">
            <label>Username:</label>
            <input type="text" name="username" required 
                   placeholder="Enter username (3-20 chars)">
        </div>
        
        <div class="form-group">
            <label>Email:</label>
            <input type="email" name="email" required 
                   placeholder="your.email@example.com">
        </div>
        
        <div class="form-group">
            <label>Age:</label>
            <input type="number" name="age" required min="13" max="120"
                   placeholder="Enter your age">
        </div>
        
        <div class="form-group">
            <label>Country:</label>
            <input type="text" name="country" required
                   placeholder="Your country">
        </div>
        
        <button type="submit">Register</button>
    </form>
    
    <p style="margin-top: 30px;">
        <a href="/users">View All Users</a>
    </p>
</body>
</html>
"""

# HTML template for displaying users
USERS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Registered Users</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #007bff; color: white; }
        tr:hover { background: #f5f5f5; }
        a { color: #007bff; text-decoration: none; }
        .no-users { text-align: center; padding: 40px; color: #666; }
    </style>
</head>
<body>
    <h1>Registered Users ({{ users|length }})</h1>
    
    {% if users %}
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Age</th>
                    <th>Country</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.age }}</td>
                    <td>{{ user.country }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <div class="no-users">
            <p>No users registered yet.</p>
        </div>
    {% endif %}
    
    <p><a href="/">← Back to Registration</a></p>
</body>
</html>
"""

@app.route('/')
def home():
    """Display registration form."""
    return render_template_string(FORM_TEMPLATE)

@app.route('/register', methods=['POST'])
def register():
    """Handle form submission and validate data."""
    
    # Get form data
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    age = request.form.get('age', '').strip()
    country = request.form.get('country', '').strip()
    
    # Validation
    errors = []
    
    # Validate username
    if len(username) < 3:
        errors.append("Username must be at least 3 characters")
    if len(username) > 20:
        errors.append("Username must not exceed 20 characters")
    if not username.isalnum():
        errors.append("Username can only contain letters and numbers")
    
    # Check if username already exists
    if any(u['username'] == username for u in users):
        errors.append("Username already taken")
    
    # Validate email
    if '@' not in email or '.' not in email:
        errors.append("Invalid email format")
    
    # Check if email already exists
    if any(u['email'] == email for u in users):
        errors.append("Email already registered")
    
    # Validate age
    try:
        age_int = int(age)
        if age_int < 13:
            errors.append("Must be at least 13 years old")
        if age_int > 120:
            errors.append("Invalid age")
    except ValueError:
        errors.append("Age must be a number")
    
    # Validate country
    if len(country) < 2:
        errors.append("Country must be at least 2 characters")
    
    # If there are errors, show them
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('home'))
    
    # If validation passes, add user
    new_user = {
        'username': username,
        'email': email,
        'age': int(age),
        'country': country
    }
    users.append(new_user)
    
    flash(f'Successfully registered {username}!', 'success')
    return redirect(url_for('show_users'))

@app.route('/users')
def show_users():
    """Display all registered users."""
    return render_template_string(USERS_TEMPLATE, users=users)

if __name__ == '__main__':
    print("🚀 Starting Flask Form Example...")
    print("📍 Visit: http://localhost:5000")
    print("✨ Try registering some users!")
    print("\nPress Ctrl+C to stop")
    app.run(debug=True, port=5000)

"""
Try running this:
    python3 examples/05_flask_with_forms.py
    
Then:
1. Visit http://localhost:5000
2. Try to register with invalid data (see validation)
3. Register valid users
4. View all users at http://localhost:5000/users

Exercise:
1. Add a password field with validation
2. Add a "delete user" button
3. Add search functionality
4. Add pagination if more than 10 users
5. Save users to a database instead of memory
6. Add email format validation using regex
"""
