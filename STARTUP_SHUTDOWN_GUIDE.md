# System Startup & Shutdown Guide

## 🛑 SHUTDOWN PROCEDURE

### **Complete Shutdown (Stop Everything)**

```bash
# Step 1: Stop all local services (MacBook)
cd ~/Desktop/Hybrid
lsof -ti:3000,8081 | xargs kill -9

# Step 2: Verify services stopped
lsof -i:3000,8081
# Should show nothing

# Step 3: Stop AWS EC2 instance (to save money)
# Option A: Via AWS Console
#   1. Go to https://console.aws.amazon.com/ec2
#   2. Click "Instances"
#   3. Select instance i-0787d08dd870595c4
#   4. Click "Instance state" → "Stop instance"
#   5. Wait ~1-2 minutes for status to show "Stopped"

# Option B: Via AWS CLI (if configured)
aws ec2 stop-instances --instance-ids i-0787d08dd870595c4

# Step 4: Verify EC2 stopped
# In AWS Console, instance state should show "Stopped"
# You'll only pay for storage (~$5/month) not compute
```

### **Quick Shutdown (Keep AWS Running)**

```bash
# Only stop local services
lsof -ti:3000,8081 | xargs kill -9

# Note: AWS EC2 keeps running and costs $0.13/hour
# Use this if you'll restart within a few hours
```

---

## 🚀 STARTUP PROCEDURE

### **Full Startup (From Stopped AWS)**

```bash
# Step 1: Start AWS EC2 instance
# Option A: Via AWS Console
#   1. Go to https://console.aws.amazon.com/ec2
#   2. Click "Instances"
#   3. Select instance i-0787d08dd870595c4
#   4. Click "Instance state" → "Start instance"
#   5. Wait ~1-2 minutes for status to show "Running"

# Option B: Via AWS CLI
aws ec2 start-instances --instance-ids i-0787d08dd870595c4

# Step 2: Get the new public IP address
# ⚠️ IMPORTANT: Public IP changes every time you stop/start!
# Option A: From AWS Console
#   - Click on instance i-0787d08dd870595c4
#   - Copy "Public IPv4 address" (e.g., 54.xxx.xxx.xxx)

# Option B: Via AWS CLI
aws ec2 describe-instances \
  --instance-ids i-0787d08dd870595c4 \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text

# Step 3: Update threat_detector.py with new IP
# Open the file and change line 49:
# FROM: self.ollama_host = os.getenv('OLLAMA_HOST', 'http://98.92.213.6:11434')
# TO:   self.ollama_host = os.getenv('OLLAMA_HOST', 'http://NEW_IP_HERE:11434')

# OR set environment variable instead:
export OLLAMA_HOST="http://NEW_IP_HERE:11434"

# Step 4: Verify AWS LLM is accessible
NEW_IP="PUT_YOUR_NEW_IP_HERE"
curl http://$NEW_IP:11434/api/tags

# Should return: {"models":[{"name":"codellama:13b",...}]}

# Step 5: Start threat detector
cd ~/Desktop/Hybrid/host-c-detection
~/.../Hybrid/.venv/bin/python threat_detector.py > /tmp/threat_detector.log 2>&1 &

# Step 6: Wait 2 seconds, then start web application
sleep 2
cd ~/Desktop/Hybrid/host-b-webapp
~/.../Hybrid/.venv/bin/python login_app.py > /tmp/login_app.log 2>&1 &

# Step 7: Verify services started
sleep 3
lsof -i:3000,8081

# Should show:
# Python ... *:8081 (LISTEN)
# Python ... *:3000 (LISTEN)

# Step 8: Test the system
curl http://localhost:3000/health
curl http://localhost:8081/health

# Step 9: Open in browser
# http://localhost:3000           - Login page
# http://localhost:3000/monitor   - Dashboard
```

### **Quick Startup (AWS Already Running)**

```bash
# Step 1: Verify AWS is running
curl http://98.92.213.6:11434/api/tags
# If this works, AWS is running with same IP

# Step 2: Start both services
cd ~/Desktop/Hybrid

# Terminal 1 or background:
cd host-c-detection
~/.../Hybrid/.venv/bin/python threat_detector.py &

# Terminal 2 or background:
cd host-b-webapp
~/.../Hybrid/.venv/bin/python login_app.py &

# Step 3: Verify
lsof -i:3000,8081

# Step 4: Access system
# Browser: http://localhost:3000
```

### **Using start_all.py Script**

```bash
cd ~/Desktop/Hybrid

# Start everything
~/.../Hybrid/.venv/bin/python start_all.py

# Keep terminal open (Ctrl+C to stop)
# OR run in background:
nohup ~/.../Hybrid/.venv/bin/python start_all.py > /tmp/hybrid.log 2>&1 &

# Note: This method assumes AWS IP hasn't changed
# If AWS was stopped/restarted, update IP first!
```

---

## 🔍 VERIFICATION COMMANDS

### **Check What's Running**

```bash
# Check local services
lsof -i:3000,8081 -P | grep LISTEN

# Check processes
ps aux | grep -E "(threat_detector|login_app)" | grep -v grep

# Check AWS LLM
curl -s http://98.92.213.6:11434/api/tags | python3 -m json.tool
```

### **Test Each Component**

```bash
# Test web app
curl http://localhost:3000/health

# Test threat detector
curl http://localhost:8081/health

# Test AWS LLM directly
curl -s http://98.92.213.6:11434/api/generate \
  -d '{"model":"codellama:13b","prompt":"Hello","stream":false}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('response','')[:50])"

# Test full threat detection flow
curl -s -X POST http://localhost:8081/analyze \
  -H "Content-Type: application/json" \
  -d '{"input":"admin OR 1=1","ip_address":"127.0.0.1"}' \
  | python3 -m json.tool
```

---

## 📝 QUICK REFERENCE

### **Common Paths**

```bash
# Virtual environment Python
/Users/mdshoyaibhossain/Desktop/Hybrid/.venv/bin/python

# Threat detector
cd /Users/mdshoyaibhossain/Desktop/Hybrid/host-c-detection
~/.../python threat_detector.py

# Web application
cd /Users/mdshoyaibhossain/Desktop/Hybrid/host-b-webapp
~/.../python login_app.py

# Start script
cd /Users/mdshoyaibhossain/Desktop/Hybrid
~/.../python start_all.py
```

### **AWS Instance Details**

```
Instance ID: i-0787d08dd870595c4
Instance Type: t4g.xlarge
Region: us-east-1
Current IP: 98.92.213.6 (changes when stopped/started)
Port: 11434
SSH Key: ~/.ssh/ollama-server-key.pem
Username: ubuntu
```

### **Important Files to Update After IP Change**

```bash
# Only if you hardcoded IP (not using environment variable)
# File: host-c-detection/threat_detector.py
# Line 49: self.ollama_host = os.getenv('OLLAMA_HOST', 'http://NEW_IP:11434')
```

---

## ⚡ ONE-COMMAND SOLUTIONS

### **Complete Shutdown**

```bash
# Kill local services + stop AWS (requires AWS CLI)
lsof -ti:3000,8081 | xargs kill -9 && \
aws ec2 stop-instances --instance-ids i-0787d08dd870595c4 && \
echo "✅ All services stopped, AWS stopping..."
```

### **Quick Restart (AWS running)**

```bash
# Kill old + start new
lsof -ti:3000,8081 | xargs kill -9 && sleep 1 && \
cd ~/Desktop/Hybrid/host-c-detection && \
~/.../Hybrid/.venv/bin/python threat_detector.py > /tmp/td.log 2>&1 & \
sleep 2 && \
cd ~/Desktop/Hybrid/host-b-webapp && \
~/.../Hybrid/.venv/bin/python login_app.py > /tmp/wa.log 2>&1 & \
sleep 3 && \
lsof -i:3000,8081 && \
echo "✅ Services started"
```

---

## 🆘 TROUBLESHOOTING

### **Problem: AWS IP Changed**

```bash
# Symptom: Error "model 'codellama:13b' not found (status code: 404)"

# Solution:
# 1. Get new IP from AWS Console or CLI
# 2. Update threat_detector.py line 49 OR set environment variable:
export OLLAMA_HOST="http://NEW_IP:11434"

# 3. Restart threat detector
lsof -ti:8081 | xargs kill -9
cd ~/Desktop/Hybrid/host-c-detection
~/.../Hybrid/.venv/bin/python threat_detector.py &
```

### **Problem: Port Already in Use**

```bash
# Symptom: "Address already in use"

# Solution: Kill existing processes
lsof -ti:3000,8081 | xargs kill -9

# Wait 1 second
sleep 1

# Restart services
```

### **Problem: AWS LLM Not Responding**

```bash
# Check if EC2 is running
aws ec2 describe-instances \
  --instance-ids i-0787d08dd870595c4 \
  --query 'Reservations[0].Instances[0].State.Name'

# If "stopped", start it:
aws ec2 start-instances --instance-ids i-0787d08dd870595c4

# If "running", check Ollama service on EC2:
ssh -i ~/.ssh/ollama-server-key.pem ubuntu@98.92.213.6
sudo systemctl status ollama
# If not running: sudo systemctl start ollama
```

### **Problem: Can't Access http://localhost:3000**

```bash
# Check if web app is running
lsof -i:3000

# If nothing, start it:
cd ~/Desktop/Hybrid/host-b-webapp
~/.../Hybrid/.venv/bin/python login_app.py &

# Check logs:
tail -f /tmp/login_app.log
```

---

## 💡 BEST PRACTICES

### **Daily Use**
1. ✅ Keep AWS running if using multiple times per day
2. ✅ Stop AWS overnight/weekends to save money
3. ✅ Always verify IP after restarting AWS

### **Cost Optimization**
1. ✅ Stop AWS when not in use (saves ~$0.13/hour)
2. ✅ Only pay ~$5/month for storage when stopped
3. ✅ Use Elastic IP if you need consistent IP (extra $3.60/month when stopped)

### **Maintenance**
1. ✅ Check logs regularly: `/tmp/threat_detector.log`, `/tmp/login_app.log`
2. ✅ Clear old detection data: `POST http://localhost:8081/clear-data`
3. ✅ Monitor AWS costs in billing dashboard

---

## 📊 STATUS DASHBOARD

### **Check Everything at Once**

```bash
#!/bin/bash
echo "=== SYSTEM STATUS ==="
echo ""
echo "Local Services:"
lsof -i:3000,8081 -P | grep LISTEN || echo "  ❌ No services running"
echo ""
echo "AWS EC2:"
curl -s --max-time 3 http://98.92.213.6:11434/api/tags > /dev/null && \
  echo "  ✅ AWS LLM accessible" || echo "  ❌ AWS LLM not accessible"
echo ""
echo "Web App:"
curl -s --max-time 3 http://localhost:3000/health > /dev/null && \
  echo "  ✅ Web app running" || echo "  ❌ Web app not running"
echo ""
echo "Threat Detector:"
curl -s --max-time 3 http://localhost:8081/health > /dev/null && \
  echo "  ✅ Threat detector running" || echo "  ❌ Threat detector not running"
echo ""
echo "Access URLs:"
echo "  🌐 Login: http://localhost:3000"
echo "  📊 Monitor: http://localhost:3000/monitor"
echo "  🔧 API: http://localhost:8081/stats"
```

Save this as `check_status.sh` and run: `bash check_status.sh`

---

**Need help? Check the full system flow: `SYSTEM_FLOW_AWS_LLM.md`**
