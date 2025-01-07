#!/usr/bin/env python3

import http.server
import socketserver
import json
import sqlite3
import os
from urllib.parse import parse_qs, urlparse
from http import HTTPStatus

# Configuration
PORT = 8000
DATABASE_DIR = "database"
DATABASE_PATH = os.path.join(DATABASE_DIR, "messages.db")

class ChatRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for the chat application"""

    def __init__(self, *args, **kwargs):
        # Initialize the parent class
        super().__init__(*args, directory="static", **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # Route handling
        if parsed_path.path == "/":
            # Serve the main page
            self.serve_file("templates/index.html")
        elif parsed_path.path == "/messages":
            # Return messages as JSON
            self.serve_messages()
        else:
            # Try to serve static files
            super().do_GET()

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/messages":
            # Handle new message submission
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                message_data = json.loads(post_data.decode('utf-8'))
                self.save_message(message_data)
                
                # Send success response
                self.send_response(HTTPStatus.CREATED)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            except Exception as e:
                # Send error response
                self.send_error(HTTPStatus.BAD_REQUEST, str(e))
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def serve_file(self, filepath):
        """Serve a file with appropriate content type"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            self.send_response(HTTPStatus.OK)
            if filepath.endswith('.html'):
                self.send_header('Content-Type', 'text/html')
            elif filepath.endswith('.js'):
                self.send_header('Content-Type', 'application/javascript')
            elif filepath.endswith('.css'):
                self.send_header('Content-Type', 'text/css')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND)

    def serve_messages(self):
        """Serve messages from the database as JSON"""
        try:
            messages = self.get_messages()
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode('utf-8'))
        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))

    def get_messages(self):
        """Retrieve messages from the database"""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, content, timestamp FROM messages ORDER BY timestamp DESC LIMIT 100')
            messages = cursor.fetchall()
            return [{'id': m[0], 'content': m[1], 'timestamp': m[2]} for m in messages]

    def save_message(self, message_data):
        """Save a new message to the database"""
        if 'content' not in message_data:
            raise ValueError('Message content is required')
            
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (content, timestamp) VALUES (?, DATETIME("now"))',
                (message_data['content'],)
            )
            conn.commit()

def init_database():
    """Initialize the database and create necessary tables"""
    os.makedirs(DATABASE_DIR, exist_ok=True)
    
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def main():
    """Main function to start the server"""
    # Initialize the database
    init_database()
    
    # Create the HTTP server
    handler = ChatRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server...")
            httpd.server_close()

if __name__ == "__main__":
    main()
