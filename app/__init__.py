"""
AgriSense - Application Factory
Initializes Flask app, registers blueprints, and ensures SQLite database tables exist.
"""

import os
from flask import Flask, jsonify
from app.database.db import init_db
from app.routes.views import views_bp
from app.routes.api import api_bp

def create_app():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, "templates")
    static_dir = os.path.join(base_dir, "static")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Configuration
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "agrisense-academic-secret-key-2026")
    app.config["JSON_SORT_KEYS"] = False

    # Initialize SQLite database
    init_db()

    # Register Blueprints
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "Resource not found", "status": 404}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error", "status": 500}), 500

    return app
