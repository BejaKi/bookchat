# BookChat

A lightweight, Git-backed web-based messaging application that allows users to communicate through a simple interface while storing messages in a Git repository.

## Features

- Simple web-based messaging interface
- Message persistence using SQLite database
- Git integration for message backup and version control
- Basic user authentication
- Real-time message updates
- Markdown support for messages

## Tech Stack

- Backend: Python (no frameworks)
- Database: SQLite
- Frontend: HTML, CSS, JavaScript (vanilla)
- Version Control: Git (using GitHub API)
- Authentication: GitHub OAuth

## Project Structure

```
bookchat/
├── .env                 # Environment variables (GitHub tokens)
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
├── static/             # Static files
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
├── templates/          # HTML templates
├── database/          # Database files
├── server.py          # Main Python server
└── requirements.txt   # Python dependencies
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/BejaKi/bookchat.git
   cd bookchat
   ```

2. Create and configure `.env` file with your GitHub token:
   ```
   GITHUB_TOKEN=your_token_here
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python server.py --init-db
   ```

5. Run the server:
   ```bash
   python server.py
   ```

6. Open your browser and navigate to `http://localhost:8000`

## Development Status

This project is under active development. Features will be implemented incrementally.

## Contributing

Feel free to submit issues and pull requests.

## License

MIT License
