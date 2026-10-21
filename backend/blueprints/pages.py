from flask import Blueprint, jsonify, send_from_directory, current_app
from pathlib import Path

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/", methods=["GET"])
def index():
    """
    Combined mode landing or API status endpoint.
    If frontend files are colocated, serves index.html; otherwise returns API service info.
    """
    frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return send_from_directory(str(frontend_dir), "index.html")

    return jsonify({
        "app": "MindVerse — Inclusive Learning Lab API",
        "description": "Accessible, predictable, and supportive educational platform API for diverse learners.",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "students": "/api/students",
            "lessons": "/api/lessons",
            "games": "/api/games",
            "videos": "/api/videos",
            "routines": "/api/routines/<student_id>",
            "computer_skills": "/api/computer-skills/activities",
            "caregiver_stats": "/api/caregiver/stats/<student_id>"
        }
    }), 200
