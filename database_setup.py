#!/usr/bin/env python3
"""
Database setup script for AI Job Demand Forecasting System
Creates SQLite database with user authentication and prediction history
"""

import sqlite3
import hashlib
from datetime import datetime, timedelta

DATABASE_PATH = 'job_forecaster.db'

def create_database():
    """Create and initialize the database with tables and sample data"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create user sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create predictions history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            industry TEXT NOT NULL,
            experience_level TEXT NOT NULL,
            predictions_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create user preferences table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            preferred_industries TEXT,
            preferred_experience_level TEXT,
            notification_settings TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            prediction_id INTEGER,
            rating INTEGER CHECK (rating >= 1 AND rating <= 5),
            feedback_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (prediction_id) REFERENCES prediction_history (id)
        )
    ''')
    
    print("Database tables created successfully!")
    
    # Create sample admin user
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute(
        "INSERT OR IGNORE INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Admin User", "admin@jobforecaster.com", admin_password)
    )
    
    # Create sample regular user
    user_password = hashlib.sha256("user123".encode()).hexdigest()
    cursor.execute(
        "INSERT OR IGNORE INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("John Doe", "john@example.com", user_password)
    )
    
    conn.commit()
    conn.close()
    
    print("Sample users created:")
    print("Admin: admin@jobforecaster.com / admin123")
    print("User: john@example.com / user123")

def verify_database():
    """Verify database structure and display statistics"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\nDatabase tables: {[table[0] for table in tables]}")
    
    # Check users count
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"Total users: {user_count}")
    
    # Check recent predictions
    cursor.execute("SELECT COUNT(*) FROM prediction_history")
    prediction_count = cursor.fetchone()[0]
    print(f"Total predictions: {prediction_count}")
    
    conn.close()

if __name__ == "__main__":
    print("Setting up AI Job Demand Forecaster Database...")
    create_database()
    verify_database()
    print("\nDatabase setup completed successfully!")
    print(f"Database file created: {DATABASE_PATH}")