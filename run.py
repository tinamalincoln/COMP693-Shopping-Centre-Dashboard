# run.py
"""
Entry point for the Shopping Centre Web Application.
Initializes Flask app, registers blueprints, and starts the server.
"""
from app import app

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)