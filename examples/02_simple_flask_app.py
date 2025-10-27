#!/usr/bin/env python3
"""
Example 2: Simple Flask Web Application
========================================

This demonstrates:
- Creating a Flask app
- Defining routes
- Returning HTML
- URL parameters
"""

from flask import Flask

# Create Flask application
app = Flask(__name__)

# Route 1: Home page
@app.route('/')
def home():
    """Display home page."""
    return """
    <html>
        <head><title>My First Flask App</title></head>
        <body>
            <h1>Welcome to My Flask App!</h1>
            <p>Visit <a href="/about">/about</a> for more info</p>
            <p>Visit <a href="/greet/Alice">/greet/Alice</a> to see dynamic content</p>
        </body>
    </html>
    """

# Route 2: About page
@app.route('/about')
def about():
    """Display about page."""
    return """
    <html>
        <head><title>About</title></head>
        <body>
            <h1>About This App</h1>
            <p>This is a simple Flask web application for learning.</p>
            <a href="/">Back to Home</a>
        </body>
    </html>
    """

# Route 3: Dynamic greeting with URL parameter
@app.route('/greet/<name>')
def greet(name):
    """Display personalized greeting."""
    return f"""
    <html>
        <head><title>Greeting</title></head>
        <body>
            <h1>Hello, {name}!</h1>
            <p>Welcome to the Flask app.</p>
            <a href="/">Back to Home</a>
        </body>
    </html>
    """

# Route 4: Multiple URL parameters
@app.route('/user/<username>/age/<int:age>')
def user_info(username, age):
    """Display user information."""
    return f"""
    <html>
        <head><title>User Info</title></head>
        <body>
            <h1>User Information</h1>
            <p><strong>Username:</strong> {username}</p>
            <p><strong>Age:</strong> {age}</p>
            <a href="/">Back to Home</a>
        </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    print("📍 Visit: http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(debug=True, port=5000)

"""
Try running this:
    python3 examples/02_simple_flask_app.py
    
Then visit:
    http://localhost:5000
    http://localhost:5000/about
    http://localhost:5000/greet/YourName
    http://localhost:5000/user/alice/age/25

Exercise:
1. Add a new route /goodbye that says goodbye
2. Create a route that accepts two numbers and shows their sum
3. Add an /info page with information about yourself
"""
