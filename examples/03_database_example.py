#!/usr/bin/env python3
"""
Example 3: SQLite Database Operations
======================================

This demonstrates:
- Connecting to a database
- Creating tables
- Inserting data
- Querying data
- Updating and deleting data
"""

import sqlite3
from datetime import datetime

def create_database():
    """Create database and table."""
    print("Creating database...")
    
    # Connect to database (creates file if doesn't exist)
    conn = sqlite3.connect('/tmp/learning.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            enrolled_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database created!")

def add_student(name, email, age):
    """Add a new student to the database."""
    conn = sqlite3.connect('/tmp/learning.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO students (name, email, age) VALUES (?, ?, ?)",
            (name, email, age)
        )
        conn.commit()
        print(f"✅ Added student: {name}")
    except sqlite3.IntegrityError:
        print(f"❌ Error: Email {email} already exists!")
    
    conn.close()

def get_all_students():
    """Get all students from database."""
    conn = sqlite3.connect('/tmp/learning.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    
    conn.close()
    return students

def get_student_by_name(name):
    """Find a student by name."""
    conn = sqlite3.connect('/tmp/learning.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
    student = cursor.fetchone()
    
    conn.close()
    return student

def update_student_age(name, new_age):
    """Update a student's age."""
    conn = sqlite3.connect('/tmp/learning.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE students SET age = ? WHERE name = ?",
        (new_age, name)
    )
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"✅ Updated {name}'s age to {new_age}")
    else:
        print(f"❌ Student {name} not found")
    
    conn.close()

def delete_student(name):
    """Delete a student from database."""
    conn = sqlite3.connect('/tmp/learning.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM students WHERE name = ?", (name,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"✅ Deleted student: {name}")
    else:
        print(f"❌ Student {name} not found")
    
    conn.close()

def display_students():
    """Display all students in a nice format."""
    students = get_all_students()
    
    if not students:
        print("No students in database")
        return
    
    print("\n" + "="*60)
    print("All Students:")
    print("="*60)
    for student in students:
        id, name, email, age, enrolled_date = student
        print(f"ID: {id}")
        print(f"  Name: {name}")
        print(f"  Email: {email}")
        print(f"  Age: {age}")
        print(f"  Enrolled: {enrolled_date}")
        print("-" * 60)

def main():
    """Main program to demonstrate database operations."""
    print("📚 SQLite Database Example")
    print("="*60)
    
    # 1. Create database
    create_database()
    
    # 2. Add some students
    print("\n📝 Adding students...")
    add_student("Alice Johnson", "alice@example.com", 22)
    add_student("Bob Smith", "bob@example.com", 24)
    add_student("Charlie Brown", "charlie@example.com", 23)
    add_student("Diana Prince", "diana@example.com", 25)
    
    # Try to add duplicate email
    add_student("Eve Wilson", "alice@example.com", 21)  # This will fail
    
    # 3. Display all students
    display_students()
    
    # 4. Find specific student
    print("\n🔍 Finding Alice...")
    alice = get_student_by_name("Alice Johnson")
    if alice:
        print(f"Found: {alice[1]} ({alice[2]}), Age: {alice[3]}")
    
    # 5. Update student
    print("\n✏️ Updating Bob's age...")
    update_student_age("Bob Smith", 25)
    
    # 6. Display after update
    display_students()
    
    # 7. Delete student
    print("\n🗑️ Deleting Charlie...")
    delete_student("Charlie Brown")
    
    # 8. Final display
    display_students()
    
    print("\n✅ Database operations completed!")
    print(f"Database file: /tmp/learning.db")

if __name__ == '__main__':
    main()

"""
Try running this:
    python3 examples/03_database_example.py

Exercise:
1. Add a new field 'grade' to the students table
2. Create a function to search students by age range
3. Add a function to get average age of all students
4. Create a function to list students sorted by name
5. Add error handling for all database operations
"""
