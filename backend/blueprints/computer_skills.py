import json
from flask import Blueprint, jsonify, request
from database.init_db import get_db_connection

computer_skills_bp = Blueprint("computer_skills", __name__, url_prefix="/api")

COMPUTER_SKILLS_ACTIVITIES = [
    {
        "id": "mouse-tracking",
        "name": "Gentle Path Navigator",
        "description": "Move the pointer along a wide, forgiving celestial pathway to guide a glowing star friend.",
        "input_types": ["mouse", "trackpad", "touch", "keyboard arrows"],
        "target_skill": "Hand-eye coordination and smooth cursor steering",
        "icon": "mouse-pointer"
    },
    {
        "id": "bubble-pop",
        "name": "Calm Bubble Pop",
        "description": "Hover over or tap floating bubbles to gently pop them and reveal soft musical chimes.",
        "input_types": ["hover", "click", "tap", "spacebar"],
        "target_skill": "Cursor hovering, click timing, and visual focus",
        "icon": "circle"
    },
    {
        "id": "target-practice",
        "name": "Friendly Target Practice",
        "description": "Click large, high-contrast, welcoming targets at your own comfortable pace.",
        "input_types": ["click", "tap", "enter key"],
        "target_skill": "Direct targeting, accuracy, and intentional pointing",
        "icon": "bullseye"
    },
    {
        "id": "treasure-chest",
        "name": "Treasure Chest Unlock",
        "description": "Practice double-clicking to open the friendly chest, with an accessible single-click button alternative.",
        "input_types": ["double-click", "accessible single-click button", "enter key"],
        "target_skill": "Double-click rhythm and accessible alternative navigation",
        "icon": "archive"
    },
    {
        "id": "shape-sorting",
        "name": "Shape Sorting Box",
        "description": "Drag and drop colorful shapes into matching bins, or use simple tap/keyboard select buttons.",
        "input_types": ["drag-and-drop", "tap to place", "keyboard numbers 1-3"],
        "target_skill": "Spatial manipulation, hold-and-release, categorization",
        "icon": "th-large"
    }
]

@computer_skills_bp.route("/computer-skills/activities", methods=["GET"])
def get_activities():
    """Retrieve list of accessible computer & motor skills activities."""
    return jsonify({
        "success": True,
        "count": len(COMPUTER_SKILLS_ACTIVITIES),
        "activities": COMPUTER_SKILLS_ACTIVITIES
    }), 200

@computer_skills_bp.route("/computer-skills/progress", methods=["POST"])
def record_skills_progress():
    """Record completed motor skills activity into activity log."""
    data = request.get_json(silent=True) or {}
    student_id = data.get("student_id")
    activity_id = data.get("activity_id")
    stars = data.get("stars", 3)
    accuracy = data.get("accuracy", 100.0)

    if not student_id or not isinstance(student_id, int):
        return jsonify({"success": False, "error": "Valid integer student_id is required."}), 400
    if not activity_id:
        return jsonify({"success": False, "error": "activity_id is required."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE id = ?;", (student_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404

    cursor.execute("""
        INSERT INTO activity_logs (student_id, activity_type, details_json)
        VALUES (?, 'computer_skill_completed', ?);
    """, (student_id, json.dumps({
        "activity_id": activity_id,
        "stars": stars,
        "accuracy": accuracy
    })))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": f"Recorded skill completion for {activity_id}."
    }), 200
