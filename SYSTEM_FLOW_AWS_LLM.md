# Updated System Flow - Hybrid Threat Detection with AWS Cloud LLM

**Date:** October 22, 2025  
**Configuration:** AWS EC2 Remote LLM (CodeLlama 13B)

---

## 🏗️ System Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────────┐
│   User Browser  │────────>│  Web Application │────────>│  Threat Detector    │
│  localhost:3000 │         │   (Flask)        │         │    (Flask API)      │
└─────────────────┘         │  Port: 3000      │         │   Port: 8081        │
                            └──────────────────┘         └─────────────────────┘
                                                                     │
                                                                     │ HTTP
                                                                     ▼
                                                          ┌─────────────────────┐
                                                          │   AWS EC2 Instance  │
                                                          │  98.92.213.6:11434  │
                                                          │                     │
                                                          │  Ollama Server      │
                                                          │  CodeLlama 13B      │
                                                          │  (19GB Model)       │
                                                          └─────────────────────┘
```

---

## 📊 Detailed Request Flow

### **Step 1: User Login Attempt**
```
User submits login form
  ↓
POST http://localhost:3000/login
  ├─ username: "admin' OR '1'='1"
  └─ password: "test123"
```

### **Step 2: Web Application Processing**
**File:** `host-b-webapp/login_app.py`

```python
1. Extract credentials from form
2. Validate input (not empty)
3. Create analysis request:
   {
     "input": "username: admin' OR '1'='1, password: test123",
     "ip_address": "127.0.0.1"
   }
4. Send to Threat Detector API
   POST http://localhost:8081/analyze
5. Wait for response (timeout: 30s)
```

### **Step 3: Threat Detector Analysis**
**File:** `host-c-detection/threat_detector.py`

```python
┌─────────────────────────────────────────────────────────┐
│ THREAT DETECTOR PROCESSING                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ 1. Input Normalization                                  │
│    ├─ URL decode: unquote(input_text)                   │
│    ├─ Replace '+' with spaces                           │
│    └─ Normalize whitespace                              │
│                                                          │
│ 2. Whitelist Check (LOCAL - FAST)                       │
│    ├─ Check against legitimate patterns:                │
│    │   • AAA/Aston1, BBB/Aston2, etc.                   │
│    ├─ If MATCH:                                         │
│    │   ├─ threat_detected: False                        │
│    │   ├─ threat_type: "BENIGN_LOGIN"                   │
│    │   ├─ detection_method: "whitelist"                 │
│    │   ├─ api_called: False                             │
│    │   └─ processing_time: ~0.002s                      │
│    └─ BYPASS LLM ✓                                      │
│                                                          │
│ 3. LLM Analysis (AWS REMOTE - SLOWER)                   │
│    If NOT in whitelist:                                 │
│    ├─ Create Ollama client:                             │
│    │   client = ollama.Client(                          │
│    │       host='http://98.92.213.6:11434'              │
│    │   )                                                 │
│    │                                                     │
│    ├─ Prepare security prompt:                          │
│    │   """                                               │
│    │   You are a cybersecurity expert analyzing         │
│    │   login inputs for security threats.               │
│    │                                                     │
│    │   Input: "username: admin' OR '1'='1, ..."         │
│    │                                                     │
│    │   Response format (JSON only):                     │
│    │   {"decision": "THREAT"} OR {"decision": "SAFE"}   │
│    │   """                                               │
│    │                                                     │
│    ├─ Send to AWS EC2:                                  │
│    │   response = client.generate(                      │
│    │       model='codellama:13b',                       │
│    │       prompt=prompt,                               │
│    │       options={"temperature": 0.0}                 │
│    │   )                                                 │
│    │                                                     │
│    └─ Parse LLM response:                               │
│        ├─ Extract JSON decision                         │
│        ├─ If "THREAT":                                  │
│        │   ├─ threat_detected: True                     │
│        │   └─ threat_type: "LLM_DETECTED_THREAT"        │
│        ├─ If "SAFE":                                    │
│        │   ├─ threat_detected: False                    │
│        │   └─ threat_type: "LLM_ANALYSIS_SAFE"          │
│        └─ processing_time: ~40-50s (network latency)    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### **Step 4: AWS LLM Processing**
**Location:** AWS EC2 (t4g.xlarge, Ubuntu 24.04, ARM64)  
**IP:** 98.92.213.6:11434

```
┌─────────────────────────────────────────────────┐
│ AWS EC2 INSTANCE                                │
├─────────────────────────────────────────────────┤
│                                                  │
│ Ollama Server (systemd service)                 │
│ ├─ Model: codellama:13b                         │
│ ├─ Size: 7.4 GB on disk                         │
│ ├─ RAM Usage: ~8-10 GB when loaded              │
│ ├─ Quantization: Q4_0 (4-bit)                   │
│ └─ Parameter Count: 13 Billion                  │
│                                                  │
│ Processing:                                     │
│ 1. Receive HTTP POST request                    │
│ 2. Load model into memory (if not loaded)       │
│ 3. Tokenize input prompt                        │
│ 4. Run inference on CodeLlama 13B               │
│ 5. Generate JSON response:                      │
│    {                                            │
│      "decision": "THREAT",                      │
│      "reason": "SQL injection detected..."      │
│    }                                            │
│ 6. Return response to MacBook                   │
│                                                  │
│ Typical Processing Time: 30-50 seconds          │
│ (Includes network latency + inference)          │
│                                                  │
└─────────────────────────────────────────────────┘
```

### **Step 5: Response to Web Application**
```json
{
  "threat_detected": true,
  "threat_type": "LLM_DETECTED_THREAT",
  "detection_method": "llm_analysis",
  "processing_time": 44.218,
  "model_version": "advanced-security-v1.0",
  "pattern_matched": "none",
  "api_called": true,
  "ai_response": "{\"decision\": \"THREAT\", \"reason\": \"SQL injection attempt\"}",
  "timestamp": "2025-10-22T02:09:38.525722",
  "detection_latency": 44.219
}
```

### **Step 6: Web Application Response**
```python
# In login_app.py
if threat_detected:
    # Still allow login (fail-open for monitoring)
    login_blocked = False
    logger.warning(f"Threat detected but login allowed")

# Store in database
store_session_record(attempt_data)

# Always show success page
return render_template('success.html', username=username)
```

### **Step 7: Dashboard Display**
**URL:** http://localhost:3000/monitor

Real-time display shows:
- ✅ Timestamp
- 🌐 IP Address
- 👤 Username
- 🤖 Detection Engine: "AI (PHI)" or "Whitelist"
- 🎯 LLM Analysis Status
- ⚠️ Threat Type
- ⏱️ Processing Time
- 📝 Raw LLM Response

---

## 🔧 Current Configuration

### **MacBook (Local)**
```yaml
Host: localhost
Services:
  - Web Application:
      Port: 3000
      File: host-b-webapp/login_app.py
      Python: /Users/mdshoyaibhossain/Desktop/Hybrid/.venv/bin/python
      
  - Threat Detector:
      Port: 8081
      File: host-c-detection/threat_detector.py
      Python: /Users/mdshoyaibhossain/Desktop/Hybrid/.venv/bin/python
      Environment:
        OLLAMA_HOST: "http://98.92.213.6:11434"
        OLLAMA_MODEL: "codellama:13b"
```

### **AWS EC2 Instance**
```yaml
Instance Details:
  ID: i-0787d08dd870595c4
  Type: t4g.xlarge (ARM64)
  vCPUs: 4
  RAM: 16 GB
  Storage: 50 GB (was 30 GB, increased)
  OS: Ubuntu Server 24.04 LTS
  
Network:
  Public IP: 98.92.213.6
  Security Groups:
    - Port 22 (SSH): 0.0.0.0/0
    - Port 11434 (Ollama): 0.0.0.0/0
    
Ollama Configuration:
  Service: systemd (always running)
  Host: 0.0.0.0:11434
  Config: /etc/systemd/system/ollama.service.d/override.conf
  Environment: OLLAMA_HOST=0.0.0.0:11434
  
Models Installed:
  - codellama:13b (ACTIVE - 7.4 GB)
  - codellama:34b (TOO LARGE - needs 19.3 GB RAM)
```

---

## 📈 Performance Metrics

### **Legitimate Login (Whitelist)**
- Detection Method: Local whitelist check
- Processing Time: ~0.002 seconds (2 milliseconds)
- API Called: No (bypasses LLM)
- Network: No external calls

### **Threat Detection (LLM)**
- Detection Method: AWS CodeLlama 13B
- Processing Time: ~40-50 seconds
- API Called: Yes
- Network: MacBook → AWS EC2 (HTTP)
- Breakdown:
  - Network latency: ~5-10s
  - LLM inference: ~30-40s
  - Response processing: ~0.1s

---

## 🔒 Security Features

### **Whitelist Patterns (Fast Path)**
```python
legitimate_patterns = [
    ('AAA', 'Aston1'),  ('BBB', 'Aston2'),  ('CCC', 'Aston3'),
    ('DDD', 'Aston4'),  ('EEE', 'Aston5'),  ('ZZZ', 'Aston6'),
    ('GGG', 'Aston7'),  ('HHH', 'Aston8'),  ('III', 'Aston10'),
    ('JJJ', 'Aston11'), ('KKK', 'Aston22'), ('LLL', 'Aston33'),
    ('MMM', 'Aston44'), ('PPP', 'Aston55'), ('QQQ', 'Aston77')
]
```

### **Threat Detection Capabilities**
AWS CodeLlama 13B can detect:
- ✅ SQL Injection (`' OR 1=1`, `admin'--`, etc.)
- ✅ Command Injection (`; rm -rf /`, `| cat /etc/passwd`)
- ✅ XSS Attempts (`<script>alert(1)</script>`)
- ✅ Path Traversal (`../../etc/passwd`)
- ✅ LDAP Injection
- ✅ NoSQL Injection
- ✅ Unusual patterns and anomalies

---

## 💰 Cost Analysis

### **AWS EC2 Costs**
```
Instance: t4g.xlarge
Hourly Rate: $0.1344 USD/hour

Monthly Costs:
- Running 24/7:  ~$97/month  (compute) + $5/month  (50GB storage) = $102/month
- Running 8h/day: ~$32/month  (compute) + $5/month  (storage)    = $37/month
- Stopped:        $0/month    (compute) + $5/month  (storage)    = $5/month

Recommendation: Stop when not in use to save ~90% on costs
```

---

## 🚀 Starting the System

### **Method 1: Start Services Individually**
```bash
# Terminal 1: Start Threat Detector
cd ~/Desktop/Hybrid/host-c-detection
~/.../Hybrid/.venv/bin/python threat_detector.py

# Terminal 2: Start Web Application  
cd ~/Desktop/Hybrid/host-b-webapp
~/.../Hybrid/.venv/bin/python login_app.py

# Access:
# - Web App: http://localhost:3000
# - Monitor: http://localhost:3000/monitor
# - API: http://localhost:8081/analyze
```

### **Method 2: Background Processes**
```bash
cd ~/Desktop/Hybrid

# Start both in background
.venv/bin/python start_all.py &

# Check status
lsof -i:3000,8081

# View logs
tail -f /tmp/hybrid.log
```

---

## 🧪 Testing Examples

### **Test 1: Legitimate Login (Whitelist)**
```bash
curl -X POST http://localhost:3000/login \
  -d "username=AAA&password=Aston1"

Expected:
- Processing: ~2ms
- Detection: Whitelist (no LLM call)
- Result: Success page
```

### **Test 2: SQL Injection (LLM Detection)**
```bash
curl -X POST http://localhost:3000/login \
  -d "username=admin' OR '1'='1&password=test"

Expected:
- Processing: ~40-50s
- Detection: AWS CodeLlama 13B
- Result: Threat detected + Success page (fail-open)
- Dashboard: Shows "LLM_DETECTED_THREAT"
```

### **Test 3: Direct API Call**
```bash
curl -X POST http://localhost:8081/analyze \
  -H "Content-Type: application/json" \
  -d '{"input":"test attack","ip_address":"127.0.0.1"}'

Expected JSON Response:
{
  "threat_detected": true/false,
  "threat_type": "LLM_DETECTED_THREAT" or "LLM_ANALYSIS_SAFE",
  "detection_method": "llm_analysis",
  "processing_time": 44.218,
  "ai_response": "{\"decision\": \"THREAT\", ...}"
}
```

---

## 🗄️ Data Storage

### **Threat Detector Database**
```
Location: host-c-detection/data/regex_analytics.db
Table: hybrid_detections
Stores:
- Input data
- Threat detection results
- Processing times
- IP addresses
- LLM responses
```

### **Web Application Database**
```
Location: host-b-webapp/data/web_sessions.db
Table: login_sessions
Stores:
- Username/password attempts
- Timestamps
- Threat analysis results
- Login blocked status
```

---

## 🔄 Stop/Manage AWS Instance

### **Stop Instance (Save Money)**
```bash
# From AWS Console:
EC2 → Instances → Select i-0787d08dd870595c4 → Instance State → Stop

# From Terminal:
aws ec2 stop-instances --instance-ids i-0787d08dd870595c4

# Note: Public IP will change when restarted
# Update threat_detector.py with new IP
```

### **Restart Instance**
```bash
aws ec2 start-instances --instance-ids i-0787d08dd870595c4

# Get new IP:
aws ec2 describe-instances --instance-ids i-0787d08dd870595c4 \
  --query 'Reservations[0].Instances[0].PublicIpAddress'
```

---

## 📝 Key Differences from Previous Setup

### **Before (Local)**
- LLM: Local Ollama on MacBook
- Model: llama3.1:8b (wouldn't work with 8GB RAM)
- Processing: All local
- Cost: $0

### **After (AWS Cloud)**
- LLM: Remote Ollama on AWS EC2
- Model: CodeLlama 13B (specifically for code/security)
- Processing: MacBook sends HTTP requests to AWS
- Cost: ~$0.13/hour when running
- Benefit: Can use larger, more capable models

---

## 🎯 System Status Commands

```bash
# Check if services are running
lsof -i:3000,8081

# Test AWS LLM connection
curl http://98.92.213.6:11434/api/tags

# Test threat detector
curl http://localhost:8081/health

# Test web app
curl http://localhost:3000/health

# View real-time logs
tail -f host-c-detection/data/*.log
tail -f host-b-webapp/data/*.log

# Kill all services
lsof -ti:3000,8081 | xargs kill -9
```

---

## ✅ Verification Checklist

- [x] AWS EC2 instance running (i-0787d08dd870595c4)
- [x] Ollama service running on AWS (0.0.0.0:11434)
- [x] CodeLlama 13B model installed on AWS
- [x] Security groups allow port 11434
- [x] Threat detector using AWS LLM (98.92.213.6:11434)
- [x] Web application running (localhost:3000)
- [x] Threat detector running (localhost:8081)
- [x] Dashboard accessible (localhost:3000/monitor)
- [x] LLM successfully detecting threats
- [x] Processing time: ~40-50s for LLM analysis
- [x] Whitelist bypass working (~2ms)

---

**System is fully operational with AWS cloud LLM! 🎉**
