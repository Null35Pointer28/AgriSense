"""
AgriSense: Intelligent Crop Management and Agricultural Decision Support System
Main entry point for local execution.
Start with: python app.py
"""

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env
load_dotenv()

app = create_app()

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ["true", "1", "yes"]

    print("=" * 65)
    print("  AGRISENSE: Intelligent Crop Management & Decision Support System")
    print(f"  Starting server at: http://{host}:{port}")
    print("=" * 65)

    app.run(host=host, port=port, debug=debug)
