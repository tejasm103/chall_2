import sqlite3
import json
from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import check_password_hash
from database.init_db import get_db_connection
from services.progress_service import ProgressService

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/health", methods=["GET"])
def health_check():
    """
    Application health check.
    Verifies runtime status and database connectivity without exposing secrets.
    """
    db_status = "connected"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        conn.close()
    except Exception as e:
        db_status = f"unhealthy: {type(e).__name__}"
        return jsonify({
            "status": "unhealthy",
            "database": db_status,
            "version": "1.0.0"
        }), 503

    return jsonify({
        "status": "healthy",
        "database": db_status,
        "app": "MindVerse — Inclusive Learning Lab",
        "version": "1.0.0"
    }), 200

# ----------------- Students API -----------------

@api_bp.route("/students", methods=["GET"])
def list_students():
    """List all learners/students."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id ASC;")
    rows = cursor.fetchall()
    conn.close()
    return jsonify({
        "success": True,
        "students": [dict(r) for r in rows]
    }), 200

@api_bp.route("/students", methods=["POST"])
def create_student():
    """Create a new learner profile."""
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"success": False, "error": "Learner name is required."}), 400

    avatar = data.get("avatar", "robot-milo")
    learning_level = data.get("learning_level", 1)
    if not isinstance(learning_level, int) or not (1 <= learning_level <= 6):
        return jsonify({"success": False, "error": "learning_level must be an integer between 1 and 6."}), 400

    preferred_theme = data.get("preferred_theme", "default")
    font_size = data.get("font_size", "standard")
    voice_enabled = 1 if data.get("voice_enabled", True) else 0
    sound_enabled = 1 if data.get("sound_enabled", True) else 0
    reduced_motion = 1 if data.get("reduced_motion", False) else 0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (name, avatar, learning_level, preferred_theme, font_size, voice_enabled, sound_enabled, reduced_motion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (name, avatar, learning_level, preferred_theme, font_size, voice_enabled, sound_enabled, reduced_motion))
    new_id = cursor.lastrowid
    conn.commit()

    cursor.execute("SELECT * FROM students WHERE id = ?;", (new_id,))
    student = dict(cursor.fetchone())
    conn.close()

    return jsonify({"success": True, "student": student}), 201

@api_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """Retrieve details for a single student."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?;", (student_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404

    return jsonify({"success": True, "student": dict(row)}), 200

@api_bp.route("/students/<int:student_id>", methods=["PATCH"])
def update_student(student_id):
    """Update student profile details."""
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?;", (student_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404

    name = data.get("name", existing["name"]).strip()
    avatar = data.get("avatar", existing["avatar"])
    learning_level = data.get("learning_level", existing["learning_level"])
    preferred_theme = data.get("preferred_theme", existing["preferred_theme"])
    font_size = data.get("font_size", existing["font_size"])
    voice_enabled = 1 if data.get("voice_enabled", existing["voice_enabled"]) else 0
    sound_enabled = 1 if data.get("sound_enabled", existing["sound_enabled"]) else 0
    reduced_motion = 1 if data.get("reduced_motion", existing["reduced_motion"]) else 0

    if not isinstance(learning_level, int) or not (1 <= learning_level <= 6):
        conn.close()
        return jsonify({"success": False, "error": "learning_level must be between 1 and 6."}), 400

    cursor.execute("""
        UPDATE students
        SET name = ?, avatar = ?, learning_level = ?, preferred_theme = ?, font_size = ?, voice_enabled = ?, sound_enabled = ?, reduced_motion = ?
        WHERE id = ?;
    """, (name, avatar, learning_level, preferred_theme, font_size, voice_enabled, sound_enabled, reduced_motion, student_id))
    conn.commit()

    cursor.execute("SELECT * FROM students WHERE id = ?;", (student_id,))
    updated = dict(cursor.fetchone())
    conn.close()

    return jsonify({"success": True, "student": updated}), 200

# ----------------- Accessibility Preferences API -----------------

@api_bp.route("/preferences/<int:student_id>", methods=["GET"])
def get_preferences(student_id):
    """Get accessibility preferences for a student."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id as student_id, preferred_theme, font_size, voice_enabled, sound_enabled, reduced_motion
        FROM students WHERE id = ?;
    """, (student_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        # Return graceful defaults if student doesn't exist
        return jsonify({
            "success": True,
            "preferences": {
                "student_id": student_id,
                "preferred_theme": "default",
                "font_size": "standard",
                "voice_enabled": 1,
                "sound_enabled": 1,
                "reduced_motion": 0,
                "is_fallback": True
            }
        }), 200

    return jsonify({"success": True, "preferences": dict(row)}), 200

@api_bp.route("/preferences/<int:student_id>", methods=["PUT"])
def update_preferences(student_id):
    """Save updated accessibility preferences for a student."""
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE id = ?;", (student_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404

    theme = data.get("preferred_theme", "default")
    font_size = data.get("font_size", "standard")
    voice = 1 if data.get("voice_enabled", 1) else 0
    sound = 1 if data.get("sound_enabled", 1) else 0
    motion = 1 if data.get("reduced_motion", 0) else 0

    cursor.execute("""
        UPDATE students
        SET preferred_theme = ?, font_size = ?, voice_enabled = ?, sound_enabled = ?, reduced_motion = ?
        WHERE id = ?;
    """, (theme, font_size, voice, sound, motion, student_id))
    conn.commit()

    cursor.execute("""
        SELECT id as student_id, preferred_theme, font_size, voice_enabled, sound_enabled, reduced_motion
        FROM students WHERE id = ?;
    """, (student_id,))
    prefs = dict(cursor.fetchone())
    conn.close()

    return jsonify({"success": True, "preferences": prefs}), 200

# ----------------- Caregiver Portal APIs -----------------

@api_bp.route("/caregiver/stats/<int:student_id>", methods=["GET"])
def caregiver_stats(student_id):
    """Retrieve comprehensive learning statistics for a student."""
    stats = ProgressService.get_caregiver_stats(student_id)
    if not stats:
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404
    return jsonify({"success": True, "stats": stats}), 200

@api_bp.route("/caregiver/reset/<int:student_id>", methods=["POST"])
def caregiver_reset_progress(student_id):
    """Reset learning progress for a student with confirmation flag."""
    data = request.get_json(silent=True) or {}
    confirm = data.get("confirm", False)
    if not confirm:
        return jsonify({"success": False, "error": "Confirmation flag 'confirm: true' is required to reset progress."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE id = ?;", (student_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404
    conn.close()

    ProgressService.reset_student_progress(student_id)
    return jsonify({
        "success": True,
        "message": f"Successfully reset progress for student ID {student_id}."
    }), 200

@api_bp.route("/caregiver/login", methods=["POST"])
def caregiver_login():
    """Caregiver PIN/Password verification for protected operations."""
    data = request.get_json(silent=True) or {}
    pin = str(data.get("pin", "")).strip()
    password = str(data.get("password", "")).strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM caregiver_auth LIMIT 1;")
    auth_row = cursor.fetchone()
    conn.close()

    if not auth_row:
        # Default fallback
        if pin == "1234" or password == "password123":
            return jsonify({"success": True, "message": "Authenticated as Caregiver."}), 200
        return jsonify({"success": False, "error": "Invalid caregiver credentials."}), 401

    # Check PIN or Password
    if pin and auth_row["pin"] and pin == auth_row["pin"]:
        return jsonify({"success": True, "message": "PIN verified successfully."}), 200

    if password and auth_row["password_hash"] and check_password_hash(auth_row["password_hash"], password):
        return jsonify({"success": True, "message": "Password verified successfully."}), 200

    return jsonify({"success": False, "error": "Invalid PIN or password."}), 401
