"""
Login Web Application with Threat Detection Integration
========================================================

Flask-based web application that provides:
1. User login interface
2. Integration with threat detection service
3. Real-time monitoring dashboard
4. Authentication attempt tracking and logging
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import requests
import json
import logging
import os
from datetime import datetime
import sqlite3

# Flask application setup
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Threat detector service configuration
THREAT_DETECTOR_HOST = os.getenv('THREAT_DETECTOR_HOST', 'localhost')
THREAT_DETECTOR_PORT = os.getenv('THREAT_DETECTOR_PORT', '8081')
SECURITY_DETECTION_URL = os.getenv('THREAT_DETECTOR_URL', f'http://{THREAT_DETECTOR_HOST}:{THREAT_DETECTOR_PORT}/analyze')
SECURITY_METRICS_URL = SECURITY_DETECTION_URL.replace('/analyze', '/stats')

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthenticationTracker:
    """
    Authentication Tracker - Manages Login Attempts and Security Analysis

    Handles:
    - Recording login attempts
    - Forwarding attempts to threat detector service
    - Storing results in local database
    - Tracking authentication events in memory
    """

    def __init__(self):
        """Initialize the authentication tracker."""
        self.setup_database()

    def setup_database(self):
        """Create SQLite database and table for storing login attempts."""
        os.makedirs('data', exist_ok=True)

        conn = sqlite3.connect('data/web_sessions.db')
        cursor = conn.cursor()

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

        conn.commit()
        conn.close()

    def record_attempt(self, username, password, ip_address):
        """
        Record a login attempt and forward it to threat detection service.

        Flow:
        1. Create a record of the login attempt
        2. Send credentials to threat detector API for analysis
        3. Receive threat assessment from the API
        4. Determine whether to allow or block the login
        5. Store the result in both memory and database
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

        try:
            # Prepare request for threat detector
            analysis_request = {
                'input': f"username: {username}, password: {password}",
                'ip_address': ip_address
            }

            # Send request to threat detector API
            response = requests.post(
                SECURITY_DETECTION_URL,
                json=analysis_request,
                timeout=30
            )

            # Process threat analysis response
            if response.status_code == 200:
                security_analysis = response.json()
                attempt_data['threat_analysis'] = security_analysis
                attempt_data['threat_detected'] = security_analysis.get('threat_detected', False)
                attempt_data['login_blocked'] = False  # Never block login

                if security_analysis.get('threat_detected', False):
                    logger.warning(f"Threat detected from {ip_address}: {security_analysis.get('explanation', 'Threat detected')} - Login allowed for monitoring")
                else:
                    logger.info(f"Safe login attempt from {ip_address}")
            else:
                logger.error(f"Security detection service error: {response.status_code}")
                attempt_data['threat_detected'] = False
                attempt_data['login_blocked'] = False

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to contact security detection service: {str(e)}")
            # Fail-open: allow login if threat detector is unreachable
            attempt_data['threat_detected'] = False
            attempt_data['login_blocked'] = False

        # Store result in database
        self.store_session_record(attempt_data)

        return attempt_data

    def store_session_record(self, attempt_data):
        """Store login attempt record in SQLite database."""
        try:
            conn = sqlite3.connect('data/web_sessions.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO login_sessions
                (username, password, ip_address, threat_detected, login_blocked, threat_analysis)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                attempt_data['username'],
                attempt_data['password'],
                attempt_data['ip_address'],
                attempt_data['threat_detected'],
                attempt_data['login_blocked'],
                json.dumps(attempt_data['threat_analysis']) if attempt_data['threat_analysis'] else None
            ))

            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Database error: {str(e)}")


# Create singleton instance of AuthenticationTracker
auth_tracker = AuthenticationTracker()


# Flask route handlers
@app.route('/')
def authentication_portal():
    """Home page - Display login form."""
    response = app.make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/login', methods=['POST'])
def process_authentication():
    """
    Process login form submission with threat detection.

    Login Flow:
    1. Extract username and password from form
    2. Validate inputs
    3. Send to threat detector service for analysis
    4. If threat detected: Block login and show error
    5. If safe: Allow login and show success page
    """
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip_address = request.remote_addr

    # Input validation
    if not username or not password:
        flash('Please provide both username and password', 'error')
        return redirect(url_for('authentication_portal'))

    # Threat detection and logging
    attempt_record = auth_tracker.record_attempt(username, password, ip_address)

    # Login successful (never blocked)
    flash('Authentication successful!', 'success')
    return render_template('success.html', username=username)


@app.route('/monitor')
def security_dashboard():
    """Security monitoring dashboard."""
    return render_template('comprehensive_monitor.html')


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

        attempt_records = []
        for row in results:
            username, password, ip_address, timestamp, threat_detected, login_blocked, threat_analysis = row

            parsed_analysis = None
            if threat_analysis:
                try:
                    parsed_analysis = json.loads(threat_analysis)
                except json.JSONDecodeError:
                    parsed_analysis = None

            attempt_records.append({
                'username': username,
                'password': password[:10] + '...' if len(password) > 10 else password,
                'ip_address': ip_address,
                'timestamp': timestamp,
                'threat_detected': bool(threat_detected),
                'login_blocked': bool(login_blocked),
                'threat_analysis': parsed_analysis
            })

        return jsonify(attempt_records)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/agent-stats')
def get_security_service_stats():
    """Proxy endpoint to fetch statistics from threat detector service."""
    try:
        response = requests.get(SECURITY_METRICS_URL, timeout=10)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to fetch security service stats'}), 502
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Security service unreachable: {str(e)}'}), 503


@app.route('/clear-data', methods=['POST'])
def clear_authentication_data():
    """Clear all login attempt data from the database."""
    try:
        conn = sqlite3.connect('data/web_sessions.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM login_sessions')

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Data cleared'})

    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/health')
def application_health_status():
    """Health check endpoint for monitoring and load balancers."""
    return jsonify({
        'status': 'healthy',
        'service': 'authentication-webapp',
        'security_detector_url': SECURITY_DETECTION_URL
    })


if __name__ == '__main__':
    print("🚀 Starting Authentication Application...")
    print(f"🔗 Security Detector URL: {SECURITY_DETECTION_URL}")
    print("🌐 Web Application listening on http://0.0.0.0:3000")
    print("\n📋 Available endpoints:")
    print("   GET    /                      - Login page")
    print("   POST   /login                 - Process login")
    print("   GET    /monitor               - Security monitoring dashboard")
    print("   GET    /api/attempts          - Get login attempts")
    print("   GET    /api/agent-stats       - Get threat detector stats")
    print("   POST   /clear-data            - Clear all data")
    print("   GET    /health                - Health check")
    print("\n✅ Application ready!")

    app.run(host='0.0.0.0', port=3000, debug=False)
