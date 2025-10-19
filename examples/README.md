# 📚 Programming Examples

This directory contains simple, well-commented examples to help you learn programming step by step.

## 🎯 Examples Overview

### 1. Hello World (`01_hello_world.py`)
**Difficulty:** Beginner  
**Concepts:** Variables, print statements, user input

Your first Python program! Learn the basics of variables and output.

```bash
python3 examples/01_hello_world.py
```

### 2. Simple Flask App (`02_simple_flask_app.py`)
**Difficulty:** Beginner  
**Concepts:** Flask, routes, HTML, URL parameters

Create your first web application with multiple pages.

```bash
python3 examples/02_simple_flask_app.py
# Visit: http://localhost:5000
```

### 3. Database Example (`03_database_example.py`)
**Difficulty:** Intermediate  
**Concepts:** SQLite, CRUD operations, SQL queries

Learn how to store and retrieve data using a database.

```bash
python3 examples/03_database_example.py
```

### 4. API Example (`04_api_example.py`)
**Difficulty:** Intermediate  
**Concepts:** HTTP requests, JSON, error handling, APIs

Make requests to external APIs and handle responses.

```bash
python3 examples/04_api_example.py
```

### 5. Flask with Forms (`05_flask_with_forms.py`)
**Difficulty:** Intermediate  
**Concepts:** HTML forms, validation, flash messages, redirects

Build a complete form with validation and user feedback.

```bash
python3 examples/05_flask_with_forms.py
# Visit: http://localhost:5000
```

## 📖 How to Use These Examples

### Step 1: Read the Code
Each example is heavily commented. Read through the entire file first to understand what it does.

### Step 2: Run the Example
Execute the example and observe the output:
```bash
python3 examples/01_hello_world.py
```

### Step 3: Experiment
Modify the code and see what happens:
- Change values
- Add new features
- Break things and fix them

### Step 4: Complete Exercises
Each example has exercises at the bottom. Try to complete them!

## 🎓 Learning Path

Follow this order if you're new to programming:

1. **01_hello_world.py** - Start here!
2. **03_database_example.py** - Learn about data storage
3. **02_simple_flask_app.py** - Build your first web app
4. **05_flask_with_forms.py** - Handle user input
5. **04_api_example.py** - Communicate with other services

## 💡 Tips for Learning

### For Each Example:
1. **Read** the entire code first
2. **Run** it without modifications
3. **Understand** what each part does
4. **Modify** small parts
5. **Experiment** freely
6. **Complete** the exercises

### Debugging Tips:
- Add `print()` statements to see variable values
- Read error messages carefully - they tell you what's wrong
- Google error messages - others have had the same problems
- Use the Python debugger (`import pdb; pdb.set_trace()`)

### Best Practices:
- Type code yourself (don't copy-paste)
- Use meaningful variable names
- Add comments to explain complex logic
- Test your code frequently
- Keep it simple at first

## 🔧 Troubleshooting

### "Module not found" Error
```bash
# Install required packages
pip install flask requests
```

### Port Already in Use
```bash
# Find and kill the process
lsof -i :5000
kill -9 <PID>

# Or change the port in the code
app.run(debug=True, port=5001)
```

### Database Locked
```bash
# Close all connections or delete the database file
rm /tmp/learning.db
```

## 📚 Additional Resources

- **Python Basics:** https://docs.python.org/3/tutorial/
- **Flask Tutorial:** https://flask.palletsprojects.com/tutorial/
- **SQL Tutorial:** https://www.sqlitetutorial.net/
- **API Guide:** https://realpython.com/python-requests/

## 🎯 Next Steps

After completing these examples:

1. **Read the full tutorials:**
   - [BEGINNERS_GUIDE.md](../BEGINNERS_GUIDE.md)
   - [TUTORIAL.md](../TUTORIAL.md)
   - [CODE_WALKTHROUGH.md](../CODE_WALKTHROUGH.md)

2. **Try the exercises:**
   - [EXERCISES.md](../EXERCISES.md)

3. **Study the main project:**
   - `host-b-webapp/login_app.py`
   - `host-c-detection/threat_detector.py`

4. **Build your own projects!**

## 🤝 Contributing

Found an error or have a suggestion? Feel free to improve these examples!

## 📝 Notes

- All examples are self-contained
- No external dependencies except Flask and requests
- Database examples use `/tmp` directory
- Web examples use port 5000 (can be changed)

---

**Happy Learning!** 🚀

*Remember: Every expert was once a beginner. Take your time and enjoy the journey!*
