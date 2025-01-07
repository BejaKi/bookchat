#!/usr/bin/env python3

import sqlite3
import os
from datetime import datetime

# Use the same database path as db_init
DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(DATABASE_DIR, "messages.db")

class DatabaseConnection:
    """Context manager for database connections"""
    def __init__(self):
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

def get_messages(limit=100, offset=0):
    """Retrieve messages from the database"""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, content, author, timestamp, git_commit_hash, parent_message_id 
            FROM messages 
            WHERE is_deleted = 0
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        """, (limit, offset))
        return cursor.fetchall()

def get_message_by_id(message_id):
    """Retrieve a specific message by its ID"""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, content, author, timestamp, git_commit_hash, parent_message_id 
            FROM messages 
            WHERE id = ? AND is_deleted = 0
        """, (message_id,))
        return cursor.fetchone()

def insert_message(content, author, parent_message_id=None):
    """Insert a new message into the database"""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (content, author, parent_message_id)
            VALUES (?, ?, ?)
        """, (content, author, parent_message_id))
        conn.commit()
        return cursor.lastrowid

def update_message(message_id, content):
    """Update an existing message"""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE messages 
            SET content = ?
            WHERE id = ? AND is_deleted = 0
        """, (content, message_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_message(message_id):
    """Soft delete a message"""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE messages 
            SET is_deleted = 1
            WHERE id = ?
        """, (message_id,))
        conn.commit()
        return cursor.rowcount > 0

def update_git_commit_hash(message_id, commit_hash):
    """Update the git commit hash for a message"""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE messages 
            SET git_commit_hash = ?
            WHERE id = ?
        """, (commit_hash, message_id))
        conn.commit()
        return cursor.rowcount > 0
