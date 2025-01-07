#!/usr/bin/env python3

import sqlite3
import os
import sys
from datetime import datetime

# Database configuration
DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(DATABASE_DIR, "messages.db")

# SQL statements
CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    author TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    git_commit_hash TEXT,
    parent_message_id INTEGER,
    is_deleted BOOLEAN DEFAULT 0,
    FOREIGN KEY (parent_message_id) REFERENCES messages(id)
)
"""

CREATE_MESSAGE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_messages_timestamp 
ON messages(timestamp)
"""

CREATE_TRIGGERS = """
CREATE TRIGGER IF NOT EXISTS update_timestamp
AFTER UPDATE ON messages
BEGIN
    UPDATE messages 
    SET timestamp = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;
"""

def init_database():
    """Initialize the database with the messages table and necessary indexes"""
    try:
        # Ensure database directory exists
        os.makedirs(DATABASE_DIR, exist_ok=True)
        
        # Connect to database
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            
            # Enable foreign key support
            cursor.execute("PRAGMA foreign_keys = ON")
            
            # Create messages table
            cursor.execute(CREATE_MESSAGES_TABLE)
            
            # Create indexes
            cursor.execute(CREATE_MESSAGE_INDEX)
            
            # Create triggers
            cursor.execute(CREATE_TRIGGERS)
            
            # Commit changes
            conn.commit()
            
        print(f"Database initialized successfully at {DATABASE_PATH}")
        return True
        
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}", file=sys.stderr)
        return False

def reset_database():
    """Reset the database by dropping and recreating the tables"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            
            # Drop existing tables
            cursor.execute("DROP TABLE IF EXISTS messages")
            
            # Reinitialize database
            init_database()
            
        print("Database reset successfully")
        return True
        
    except sqlite3.Error as e:
        print(f"Error resetting database: {e}", file=sys.stderr)
        return False

def insert_test_data():
    """Insert some test data into the database"""
    test_messages = [
        ("Hello, this is a test message!", "user1"),
        ("Testing the chat application.", "user2"),
        ("This is a reply to the first message.", "user3", 1),
    ]
    
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            
            # Insert messages
            for message in test_messages:
                if len(message) == 2:
                    content, author = message
                    cursor.execute(
                        "INSERT INTO messages (content, author) VALUES (?, ?)",
                        (content, author)
                    )
                else:
                    content, author, parent_id = message
                    cursor.execute(
                        "INSERT INTO messages (content, author, parent_message_id) VALUES (?, ?, ?)",
                        (content, author, parent_id)
                    )
            
            conn.commit()
            
        print("Test data inserted successfully")
        return True
        
    except sqlite3.Error as e:
        print(f"Error inserting test data: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "--reset":
            reset_database()
        elif command == "--test-data":
            insert_test_data()
    else:
        init_database()
