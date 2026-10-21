from flask import Blueprint, jsonify, request
from services.routine_service import RoutineService
from database.init_db import get_db_connection

daily_routine_bp = Blueprint("daily_routine", __name__, url_prefix="/api")

@daily_routine_bp.route("/routines/<int:student_id>", methods=["GET"])
def get_student_routines(student_id):
    """Retrieve all daily routine schedules for a student."""
    # Verify student exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE id = ?;", (student_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404
    conn.close()

    routines = RoutineService.get_routines_by_student(student_id)
    return jsonify({
        "success": True,
        "student_id": student_id,
        "count": len(routines),
        "routines": routines
    }), 200

@daily_routine_bp.route("/routines", methods=["POST"])
def create_routine():
    """Create a new custom daily routine schedule."""
    data = request.get_json(silent=True) or {}

    student_id = data.get("student_id")
    title = data.get("title", "").strip()
    category = data.get("category", "custom").lower()
    steps = data.get("steps", [])

    if not student_id or not isinstance(student_id, int):
        return jsonify({"success": False, "error": "Valid integer student_id is required."}), 400

    if not title:
        return jsonify({"success": False, "error": "Routine title is required."}), 400

    if category not in ("morning", "hygiene", "school", "bedtime", "custom"):
        category = "custom"

    if not isinstance(steps, list):
        return jsonify({"success": False, "error": "Steps must be an array of routine steps."}), 400

    # Ensure student exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE id = ?;", (student_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": f"Student with ID {student_id} does not exist."}), 404
    conn.close()

    new_routine = RoutineService.create_routine(
        student_id=student_id,
        title=title,
        category=category,
        steps=steps,
        is_custom=1
    )

    return jsonify({
        "success": True,
        "message": "Routine created successfully.",
        "routine": new_routine
    }), 201

@daily_routine_bp.route("/routines/<int:routine_id>", methods=["PATCH"])
def update_routine(routine_id):
    """Update an existing routine's title, category, or step completion states."""
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    category = data.get("category")
    steps = data.get("steps")

    existing = RoutineService.get_routine_by_id(routine_id)
    if not existing:
        return jsonify({"success": False, "error": f"Routine with ID {routine_id} not found."}), 404

    updated = RoutineService.update_routine(
        routine_id=routine_id,
        title=title,
        category=category,
        steps=steps
    )

    return jsonify({
        "success": True,
        "message": "Routine updated successfully.",
        "routine": updated
    }), 200

@daily_routine_bp.route("/routines/<int:routine_id>", methods=["DELETE"])
def delete_routine(routine_id):
    """Delete a custom routine."""
    existing = RoutineService.get_routine_by_id(routine_id)
    if not existing:
        return jsonify({"success": False, "error": f"Routine with ID {routine_id} not found."}), 404

    success = RoutineService.delete_routine(routine_id)
    if success:
        return jsonify({"success": True, "message": f"Routine {routine_id} deleted."}), 200
    return jsonify({"success": False, "error": "Failed to delete routine."}), 500
