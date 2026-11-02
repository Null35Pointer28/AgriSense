"""
AgriSense - Web View Routes
Renders the AgriSense Agricultural SaaS Dashboard.
"""

from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def index():
    return render_template("index.html")

@views_bp.route("/about")
def about():
    return render_template("about.html")
