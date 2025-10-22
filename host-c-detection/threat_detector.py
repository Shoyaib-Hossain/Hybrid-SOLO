"""
LLM-Based Threat Detection System
----------------------------------
This module implements an LLM-powered security threat detection system:
1. Whitelist check for legitimate login credentials (bypass LLM)
2. AI/LLM-based analysis for all other inputs (LLM decides independently)

The LLM analyzes user inputs and determines if they are THREAT or SAFE.
All security decisions are made by the LLM server without preset patterns.
"""

from flask import Flask, request, jsonify
import sqlite3
import datetime
import os
import re
import time
import logging
from typing import Dict, Optional
from urllib.parse import unquote
import ollama

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AdvancedSecurityAnalyzer:
    """
    Advanced Security Analyzer - LLM-Based Threat Detection Engine

    LLM-powered threat detection:
    - Whitelist Check: Bypass LLM for known legitimate logins
    - AI/LLM Analysis: All other inputs analyzed by LLM server

    Detection Flow:
    1. Input normalization
    2. Whitelist check (legitimate logins bypass LLM)
    3. LLM analysis (LLM decides THREAT or SAFE independently)
    """

    def __init__(self):
        """Initialize the security analyzer with AI configuration and legitimate login patterns."""
        # AI Configuration - AWS Remote LLM
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://54.83.245.211:11434')
        self.ai_model = os.getenv('OLLAMA_MODEL', 'codellama:13b')

        # Legitimate authentication patterns (whitelist)
        self.legitimate_auth_patterns = {
            'pattern_combinations': [
                ('AAA', 'Aston1'), ('BBB', 'Aston2'), ('CCC', 'Aston3'),
                ('DDD', 'Aston4'), ('EEE', 'Aston5'), ('ZZZ', 'Aston6'),
                ('GGG', 'Aston7'), ('HHH', 'Aston8'), ('III', 'Aston10'),
                ('JJJ', 'Aston11'), ('KKK', 'Aston22'), ('LLL', 'Aston33'),
                ('MMM', 'Aston44'), ('PPP', 'Aston55'), ('QQQ', 'Aston77')
            ]
        }

        self.setup_database()

    def setup_database(self):
        """Set up the SQLite database for logging detections and analytics."""
        try:
            data_dir = os.getenv('DATA_DIR', 'data')
            os.makedirs(data_dir, exist_ok=True)

            db_path = os.path.join(data_dir, 'regex_analytics.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Main detection logging table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hybrid_detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    input_data TEXT,
                    threat_detected BOOLEAN,
                    threat_type TEXT,
                    processing_time REAL,
                    ip_address TEXT,
                    pattern_matched TEXT,
                    detection_method TEXT,
                    api_called BOOLEAN DEFAULT 0,
                    ai_response TEXT
                )
            ''')

            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON hybrid_detections(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_threat_detected ON hybrid_detections(threat_detected)')

            conn.commit()
            conn.close()
            logger.info(f"Database setup complete at {db_path}")
        except Exception as e:
            logger.error(f"Database setup error: {e}")

    def validate_legitimate_login(self, input_text: str) -> bool:
        """Check if input matches a whitelisted legitimate login pattern."""
        input_lower = input_text.lower().strip()

        for username, password in self.legitimate_auth_patterns['pattern_combinations']:
            if username.lower() in input_lower and password.lower() in input_lower:
                return True

        return False

    def comprehensive_security_scan(self, input_text: str, ip_address: str = None) -> Optional[Dict]:
        """
        Perform security threat analysis with LLM-based detection.

        Detection Flow:
        1. Input Normalization
        2. Whitelist Check (legitimate logins bypass LLM)
        3. LLM Analysis (all other inputs sent to LLM server)
        """
        start_time = time.time()

        # Input normalization
        decoded_input = unquote(input_text)
        normalized_input = decoded_input.replace('+', ' ')
        normalized_input = re.sub(r'\s+', ' ', normalized_input).strip()

        # Whitelist check - legitimate logins bypass LLM
        if self.validate_legitimate_login(normalized_input):
            processing_time = time.time() - start_time
            result = {
                'threat_detected': False,
                'threat_type': 'BENIGN_LOGIN',
                'detection_method': 'legitimate_pattern_whitelist',
                'processing_time': processing_time,
                'model_version': 'advanced-security-v1.0',
                'pattern_matched': 'legitimate_login_pattern',
                'api_called': False
            }
            self.refresh_stats('legitimate_login', processing_time)
            return result

        # All other inputs go directly to LLM for analysis
        ai_result = self.perform_ai_analysis(normalized_input)
        total_processing_time = time.time() - start_time

        result = {
            'threat_detected': ai_result['threat_detected'],
            'threat_type': ai_result['threat_type'],
            'detection_method': 'llm_analysis',
            'processing_time': total_processing_time,
            'model_version': 'advanced-security-v1.0',
            'pattern_matched': 'none',
            'api_called': True,
            'ai_response': ai_result['ai_response']
        }

        return result

    def perform_ai_analysis(self, input_text: str) -> Dict:
        """Send input to LLM with structured JSON output for reliable parsing."""
        try:
            # Create Ollama client with remote host
            client = ollama.Client(host=self.ollama_host)

            # Force structured JSON output with security context
            prompt = f"""You are a cybersecurity expert analyzing login inputs for security threats.

Analyze this login input and respond ONLY with valid JSON:

Input: "{input_text}"

Response format (no other text):
{{"decision": "THREAT"}} OR {{"decision": "SAFE"}}"""

            response = client.generate(
                model=self.ai_model,
                prompt=prompt,
                options={"temperature": 0.0}  # Set to 0 for deterministic output
            )

            # Get LLM's complete response
            llm_response = response['response'].strip()

            # Log the raw LLM response
            logger.info(f"LLM raw response for input '{input_text[:50]}...': {llm_response}")

            # Parse JSON response
            import json
            decision_data = json.loads(llm_response)
            decision = decision_data.get('decision', '').upper()

            # Determine if a threat is detected
            threat_detected = decision == 'THREAT'

            logger.info(f"LLM decision for input '{input_text[:50]}...': {decision}")

            return {
                'threat_detected': threat_detected,
                'threat_type': 'LLM_DETECTED_THREAT' if threat_detected else 'LLM_ANALYSIS_SAFE',
                'ai_response': llm_response
            }
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return {
                'threat_detected': None,
                'threat_type': 'AI_ANALYSIS_ERROR',
                'ai_response': f'Error: {str(e)}'
            }

    def store_detection_record(self, input_data: str, result: Dict, ip_address: str = None):
        """Store detection results in database for audit trails and analytics."""
        conn = sqlite3.connect('data/regex_analytics.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO hybrid_detections
            (input_data, threat_detected, threat_type, processing_time, ip_address,
             pattern_matched, detection_method, api_called, ai_response)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            input_data,
            result.get('threat_detected', False),
            result.get('threat_type', 'NONE'),
            result.get('processing_time', 0.0),
            ip_address,
            result.get('pattern_matched', ''),
            result.get('detection_method', ''),
            result.get('api_called', False),
            result.get('ai_response', '')[:1000] if result.get('ai_response') else ''
        ))

        conn.commit()
        conn.close()

    def refresh_stats(self, detection_type: str, processing_time: float):
        """Update internal runtime statistics for monitoring."""
        if not hasattr(self, 'internal_stats'):
            self.internal_stats = {
                'legitimate_logins': 0,
                'total_processing_time': 0.0,
                'detections_by_type': {}
            }

        if detection_type not in self.internal_stats['detections_by_type']:
            self.internal_stats['detections_by_type'][detection_type] = 0

        self.internal_stats['detections_by_type'][detection_type] += 1
        self.internal_stats['total_processing_time'] += processing_time

        if detection_type == 'legitimate_login':
            self.internal_stats['legitimate_logins'] += 1

        logger.info(f"Stats updated: {detection_type} processed in {processing_time:.6f}s")


# Flask Web API Setup
app = Flask(__name__)
security_analyzer = AdvancedSecurityAnalyzer()


@app.route('/analyze', methods=['POST'])
def execute_security_analysis():
    """
    Main threat detection API endpoint.

    POST /analyze
    Request body: {"input": "user input to analyze", "ip_address": "optional"}
    Response: JSON with detection results
    """
    start_time = time.time()

    try:
        data = request.json
        user_input = data.get('input', '')
        ip_address = request.remote_addr or data.get('ip_address', '')

        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        # Perform threat analysis
        hybrid_result = security_analyzer.comprehensive_security_scan(user_input, ip_address)

        # Add metadata
        hybrid_result.update({
            'timestamp': datetime.datetime.now().isoformat(),
            'detection_latency': time.time() - start_time
        })

        # Store result in database
        security_analyzer.store_detection_record(user_input, hybrid_result, ip_address)

        return jsonify(hybrid_result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/stats', methods=['GET'])
def retrieve_statistics():
    """
    Get aggregated statistics and performance metrics.

    GET /stats
    Response: JSON with analytics summary
    """
    try:
        conn = sqlite3.connect('data/regex_analytics.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN threat_detected = 1 THEN 1 ELSE 0 END) as threats_blocked,
                SUM(CASE WHEN threat_detected = 0 THEN 1 ELSE 0 END) as safe_inputs,
                AVG(processing_time) as avg_processing_time,
                MIN(processing_time) as min_processing_time,
                MAX(processing_time) as max_processing_time,
                SUM(CASE WHEN api_called = 1 THEN 1 ELSE 0 END) as ai_calls
            FROM hybrid_detections
        ''')

        stats = cursor.fetchone()
        conn.close()

        total = stats[0] if stats and stats[0] else 0
        threats_blocked = stats[1] if stats and stats[1] else 0
        safe_inputs = stats[2] if stats and stats[2] else 0
        avg_processing_time = stats[3] if stats and stats[3] else 0.0
        min_processing_time = stats[4] if stats and stats[4] else 0.0
        max_processing_time = stats[5] if stats and stats[5] else 0.0
        ai_calls = stats[6] if stats and stats[6] else 0

        return jsonify({
            'service': 'advanced-security',
            'status': 'healthy',
            'detection_mode': 'llm-based',
            'total_requests': total,
            'threats_blocked': threats_blocked,
            'safe_inputs': safe_inputs,
            'threat_detection_rate': (threats_blocked / max(total, 1)) * 100,
            'llm_enabled': True,
            'performance_metrics': {
                'avg_processing_time': avg_processing_time,
                'min_processing_time': min_processing_time,
                'max_processing_time': max_processing_time
            },
            'llm_usage_metrics': {
                'total_llm_calls': ai_calls
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/detailed-requests', methods=['GET'])
def fetch_detailed_requests():
    """
    Get paginated list of individual detection records.

    GET /detailed-requests?page=1&per_page=100
    """
    try:
        conn = sqlite3.connect('data/regex_analytics.db')
        cursor = conn.cursor()

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))
        offset = (page - 1) * per_page

        cursor.execute('SELECT COUNT(*) FROM hybrid_detections')
        total_count = cursor.fetchone()[0]

        cursor.execute('''
            SELECT id, timestamp, input_data, threat_detected, threat_type,
                   processing_time, ip_address, detection_method, api_called
            FROM hybrid_detections
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (per_page, offset))

        records = []
        for idx, row in enumerate(cursor.fetchall(), offset + 1):
            records.append({
                'number': idx,
                'id': row[0],
                'timestamp': row[1],
                'username': row[2][:50] + '...' if len(row[2]) > 50 else row[2],
                'threat_detected': bool(row[3]),
                'threat_type': row[4] or 'NONE',
                'processing_time': row[5],
                'ip_address': row[6],
                'detection_method': row[7],
                'api_called': bool(row[8]),
                'status': 'THREAT' if row[3] else 'SAFE'
            })

        conn.close()

        return jsonify({
            'service': 'advanced-security',
            'total_requests': len(records),
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'requests': records
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/clear-data', methods=['POST'])
def purge_security_records():
    """
    Delete all detection records from the database.

    POST /clear-data
    Request body: {"confirm": "YES_DELETE_ALL"}
    """
    try:
        if not request.json or request.json.get('confirm') != 'YES_DELETE_ALL':
            return jsonify({
                'error': 'Missing confirmation. Send {"confirm": "YES_DELETE_ALL"} to proceed.'
            }), 400

        conn = sqlite3.connect('data/regex_analytics.db')
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM hybrid_detections')
        record_count = cursor.fetchone()[0]

        cursor.execute('DELETE FROM hybrid_detections')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="hybrid_detections"')

        conn.commit()
        conn.close()

        if hasattr(security_analyzer, 'client_threat_stats'):
            security_analyzer.client_threat_stats.clear()

        return jsonify({
            'success': True,
            'message': f'Successfully deleted {record_count} records',
            'timestamp': datetime.datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/health', methods=['GET'])
def service_health_status():
    """Health check endpoint for monitoring and load balancers."""
    return jsonify({
        'status': 'healthy',
        'service': 'advanced-security',
        'mode': 'llm-based-detection'
    })


if __name__ == '__main__':
    print("🚀 Starting Advanced Security Detection Service...")
    print("🤖 LLM-based detection: All inputs analyzed by AI")
    print("💡 Detection flow: Whitelist check → LLM decides (THREAT or SAFE)")
    print("🌐 Server listening on http://0.0.0.0:8081")
    print("\n📋 Available endpoints:")
    print("   POST   /analyze              - Analyze input for threats")
    print("   GET    /stats                - Get statistics (JSON)")
    print("   GET    /detailed-requests    - Get detection records")
    print("   POST   /clear-data           - Clear all records")
    print("   GET    /health               - Health check")
    print("\n✅ Service ready!")

    app.run(host='0.0.0.0', port=8081, debug=False)
