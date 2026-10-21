import os
from flask import Blueprint, jsonify, send_from_directory, abort
from pathlib import Path

pages_bp = Blueprint("pages", __name__)

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

@pages_bp.route("/", methods=["GET"])
@pages_bp.route("/index.html", methods=["GET"])
def index():
    """Serves the main landing page."""
    if (FRONTEND_DIR / "index.html").exists():
        return send_from_directory(str(FRONTEND_DIR), "index.html")
    return jsonify({
        "app": "MindVerse — Inclusive Learning Lab API",
        "description": "Accessible, predictable, and supportive educational platform API for diverse learners.",
        "version": "1.0.0",
        "status": "online"
    }), 200

@pages_bp.route("/pages/<path:filename>", methods=["GET"])
def serve_page(filename):
    """Serves subpages such as videos.html, dashboard.html, etc."""
    pages_dir = FRONTEND_DIR / "pages"
    if (pages_dir / filename).exists():
        return send_from_directory(str(pages_dir), filename)
    abort(404)

@pages_bp.route("/css/<path:filename>", methods=["GET"])
def serve_css(filename):
    """Serves CSS design system files."""
    css_dir = FRONTEND_DIR / "css"
    if (css_dir / filename).exists():
        return send_from_directory(str(css_dir), filename, mimetype="text/css")
    abort(404)

@pages_bp.route("/js/<path:filename>", methods=["GET"])
def serve_js(filename):
    """Serves JavaScript modules."""
    js_dir = FRONTEND_DIR / "js"
    if (js_dir / filename).exists():
        return send_from_directory(str(js_dir), filename, mimetype="application/javascript")
    abort(404)

@pages_bp.route("/assets/<path:filename>", methods=["GET"])
def serve_assets(filename):
    """Serves images, SVG icons, and media assets."""
    assets_dir = FRONTEND_DIR / "assets"
    if (assets_dir / filename).exists():
        return send_from_directory(str(assets_dir), filename)
    abort(404)
