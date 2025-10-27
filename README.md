# 🔐 Hybrid Web Security System

A sophisticated web security system that combines traditional pattern matching with AI-powered threat detection. **This project also serves as a comprehensive programming learning resource!**

## 🎓 For Learners

**Want to learn programming?** This repository includes extensive tutorials and guides!

### 📚 Start Learning Here:
- **[README_LEARNING.md](README_LEARNING.md)** - Complete guide for learners (START HERE!)
- **[PROGRAMMING_COURSE.md](PROGRAMMING_COURSE.md)** - Structured course with weekly lessons
- **[TUTORIAL.md](TUTORIAL.md)** - Comprehensive tutorial (23,000+ words)
- **[BEGINNERS_GUIDE.md](BEGINNERS_GUIDE.md)** - Simple explanations for beginners
- **[CODE_WALKTHROUGH.md](CODE_WALKTHROUGH.md)** - Line-by-line code explanation
- **[EXERCISES.md](EXERCISES.md)** - 7 levels of practice exercises
- **[examples/](examples/)** - 5 simple example scripts to get started

**Choose your path:**
- 🆕 **New to programming?** → Start with [README_LEARNING.md](README_LEARNING.md)
- 📖 **Want structured lessons?** → Follow [PROGRAMMING_COURSE.md](PROGRAMMING_COURSE.md)
- 💪 **Learn by doing?** → Try [EXERCISES.md](EXERCISES.md)
- 🔍 **Want to understand the code?** → Read [CODE_WALKTHROUGH.md](CODE_WALKTHROUGH.md)

---

## 🚀 For Developers

### Project Overview

This system provides:
1. **Web Application** - User authentication interface with real-time monitoring
2. **Threat Detection Service** - Hybrid AI + regex pattern matching for security threats
3. **Multi-layered Security** - Combines fast pattern matching with intelligent AI analysis

### Architecture

```
┌─────────────────────┐
│   User Browser      │
│  (Login Interface)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐      ┌──────────────────────┐
│  Web Application    │─────▶│  Threat Detector     │
│  (Flask)            │      │  (Hybrid AI + Regex) │
│  Port 3000          │◀─────│  Port 8081           │
└─────────────────────┘      └──────────────────────┘
           │                            │
           ▼                            ▼
    ┌──────────┐                ┌──────────┐
    │ SQLite   │                │ SQLite   │
    │ (Login   │                │ (Threat  │
    │  Data)   │                │  Data)   │
    └──────────┘                └──────────┘
```

### Features

#### Web Application (`host-b-webapp/login_app.py`)
- ✅ User login interface
- ✅ Real-time threat detection integration
- ✅ Security monitoring dashboard
- ✅ Comprehensive statistics
- ✅ RESTful API endpoints

#### Threat Detection (`host-c-detection/threat_detector.py`)
- ✅ **Hybrid Detection:**
  - Fast regex pattern matching for known threats
  - AI-powered analysis for sophisticated attacks
- ✅ SQL injection detection
- ✅ XSS prevention
- ✅ Command injection detection
- ✅ Whitelist validation
- ✅ Performance metrics and logging

### Technology Stack

- **Backend:** Python 3, Flask
- **Database:** SQLite
- **AI Engine:** Ollama (Local LLM)
- **Security:** Regex patterns + AI analysis
- **Frontend:** HTML, CSS, JavaScript

---

## 🛠️ Installation & Setup

### Prerequisites

```bash
# Required
Python 3.7+
pip

# For AI features
Ollama (https://ollama.ai)
```

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Shoyaib-Hossain/Hybrid-.git
cd Hybrid-

# 2. Install dependencies
cd host-b-webapp
pip install -r requirements.txt

cd ../host-c-detection
pip install -r requirements_agents.txt

# 3. Install and setup Ollama
# Download from: https://ollama.ai
ollama serve
ollama pull phi:2.7b

# 4. Start the system
cd ..
python3 start_all.py
```

### Access the Application

Once running, visit:
- **Web Interface:** http://localhost:3000
- **Security Dashboard:** http://localhost:3000/monitor
- **Threat Detector API:** http://localhost:8081/stats

### Test the System

**Legitimate Login:**
- Username: `AAA`
- Password: `Aston1`

**SQL Injection Test (Safe to try!):**
- Username: `admin' OR '1'='1`
- Password: `anything`

Watch the system detect and log the threat in real-time!

---

## 📊 How It Works

### Detection Flow

```
1. User Input
   ↓
2. Send to Threat Detector
   ↓
3. Normalize Input
   ↓
4. Check Whitelist
   ├─ Match? → Safe (Return immediately)
   └─ No Match ↓
5. Check Regex Patterns
   ├─ Match? → Threat Detected (Return)
   └─ No Match ↓
6. AI Analysis
   ├─ AI says "THREAT" → Threat Detected
   └─ AI says "SAFE" → Safe
   ↓
7. Log Result & Return to Web App
```

### Why Hybrid Detection?

1. **Speed:** Regex catches 90%+ of threats instantly
2. **Intelligence:** AI catches sophisticated/obfuscated attacks
3. **Efficiency:** Only uses AI when needed
4. **Accuracy:** Combines deterministic + probabilistic methods

---

## 🔧 Configuration

### Environment Variables

```bash
# Web Application
export THREAT_DETECTOR_HOST=localhost
export THREAT_DETECTOR_PORT=8081
export SECRET_KEY=your-secret-key

# Threat Detector
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=phi:2.7b
export DATA_DIR=data
```

### Customization

**Add Custom Threat Patterns:**

Edit `threat_detector.py`:
```python
self.security_signatures = {
    'SQL_INJECTION': [
        r"(?i)'\s*or\s*'",
        # Add your patterns here
    ],
    'XSS': [
        r"<script.*?>.*?</script>",
        # Add XSS patterns
    ]
}
```

**Whitelist Legitimate Logins:**

Edit `threat_detector.py`:
```python
self.legitimate_auth_patterns = {
    'pattern_combinations': [
        ('username', 'password'),
        # Add your whitelisted credentials
    ]
}
```

---

## 📖 API Documentation

### Web Application API

#### GET `/api/attempts`
Get login attempt history
```bash
curl http://localhost:3000/api/attempts
```

#### GET `/api/agent-stats`
Get threat detector statistics
```bash
curl http://localhost:3000/api/agent-stats
```

#### POST `/clear-data`
Clear all login data
```bash
curl -X POST http://localhost:3000/clear-data
```

### Threat Detector API

#### POST `/analyze`
Analyze input for threats
```bash
curl -X POST http://localhost:8081/analyze \
  -H "Content-Type: application/json" \
  -d '{"input": "username: admin, password: test"}'
```

#### GET `/stats`
Get detection statistics
```bash
curl http://localhost:8081/stats
```

#### GET `/detailed-requests`
Get detailed detection records
```bash
curl http://localhost:8081/detailed-requests?page=1&per_page=50
```

---

## 🧪 Testing

### Manual Testing

```bash
# Test normal login
curl -X POST http://localhost:3000/login \
  -d "username=AAA&password=Aston1"

# Test SQL injection
curl -X POST http://localhost:3000/login \
  -d "username=admin' OR '1'='1&password=test"

# View statistics
curl http://localhost:8081/stats
```

### Automated Testing

Run the included test script:
```bash
python3 jsonl_threat_tester.py --url http://localhost:3000 --max-payloads 100
```

---

## 📈 Performance

- **Regex Detection:** ~0.001s per request
- **AI Analysis:** ~0.5-2s per request
- **Database Operations:** ~0.01s per operation
- **End-to-End:** ~0.5-2.5s per login attempt

**Optimization:**
- Whitelist check: Instant (~0.0001s)
- 90%+ threats caught by regex (no AI needed)
- AI only used when regex doesn't match

---

## 🔒 Security Considerations

### What This System Does:
✅ Detects common attack patterns  
✅ Logs all attempts for monitoring  
✅ Provides real-time alerting  
✅ Uses AI for intelligent analysis  

### What This System Doesn't Do:
❌ **Does not block logins** (monitoring only)  
❌ **Not a production firewall** (educational project)  
❌ **Not WAF replacement** (use dedicated security tools)  

**For Production:**
- Add authentication and authorization
- Implement rate limiting
- Use HTTPS with valid certificates
- Add proper password hashing
- Deploy behind a firewall
- Use production-grade databases
- Implement proper logging and monitoring

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional threat patterns
- More AI models support
- Enhanced dashboard features
- Performance optimizations
- Additional test cases
- Documentation improvements

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🎓 Learning Resources

This repository includes extensive educational materials:

### Documentation
- [README_LEARNING.md](README_LEARNING.md) - Complete learning guide
- [PROGRAMMING_COURSE.md](PROGRAMMING_COURSE.md) - Structured course
- [TUTORIAL.md](TUTORIAL.md) - Full tutorial
- [BEGINNERS_GUIDE.md](BEGINNERS_GUIDE.md) - Beginner explanations
- [CODE_WALKTHROUGH.md](CODE_WALKTHROUGH.md) - Code explanation
- [EXERCISES.md](EXERCISES.md) - Practice exercises

### Examples
- [examples/01_hello_world.py](examples/01_hello_world.py) - Python basics
- [examples/02_simple_flask_app.py](examples/02_simple_flask_app.py) - Flask intro
- [examples/03_database_example.py](examples/03_database_example.py) - Database operations
- [examples/04_api_example.py](examples/04_api_example.py) - API requests
- [examples/05_flask_with_forms.py](examples/05_flask_with_forms.py) - Forms and validation

---

## 🌟 Features Showcase

### Real-time Monitoring Dashboard
View all login attempts, threat detections, and system statistics in real-time.

### AI-Powered Detection
Uses local LLM (Ollama) for intelligent threat analysis without sending data to external services.

### Comprehensive Logging
Every attempt is logged with full details for audit and analysis.

### Educational Value
Excellent project for learning web development, APIs, databases, and security concepts.

---

## 📞 Support

- **Documentation:** Check the guides in this repository
- **Issues:** Open an issue on GitHub
- **Learning Help:** See [README_LEARNING.md](README_LEARNING.md)

---

## 🎯 Use Cases

### For Learning
- **Students:** Learn full-stack development
- **Bootcamps:** Use as curriculum project
- **Self-study:** Follow structured tutorials
- **Teachers:** Use as teaching material

### For Development
- **Security Research:** Study threat patterns
- **AI Integration:** Learn LLM integration
- **API Design:** Study service architecture
- **Portfolio:** Demonstrate skills

### For Business
- **Security Monitoring:** Monitor application login attempts
- **Threat Intelligence:** Collect attack pattern data
- **Research:** Develop better detection algorithms
- **Training:** Train security teams

---

## 🏆 Achievements

What you can build/learn from this project:
- ✅ Full-stack web application
- ✅ RESTful API design
- ✅ Database operations
- ✅ AI/LLM integration
- ✅ Security implementation
- ✅ Multi-service architecture
- ✅ Real-time monitoring
- ✅ Testing and debugging

---

**Ready to get started?**

- 👨‍💻 **Developers:** Jump to [Installation & Setup](#installation--setup)
- 🎓 **Learners:** Start with [README_LEARNING.md](README_LEARNING.md)
- 📖 **Curious:** Read [TUTORIAL.md](TUTORIAL.md)

---

*Built for learning, designed for security.* 🔐✨
