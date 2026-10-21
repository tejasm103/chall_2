from flask import Blueprint, jsonify, request
from services.lesson_service import LessonService
from services.progress_service import ProgressService
from database.init_db import get_db_connection

lessons_bp = Blueprint("lessons", __name__, url_prefix="/api")

@lessons_bp.route("/lessons", methods=["GET"])
def get_lessons():
    """Retrieve all structured curriculum lessons, optionally filtered by level or subject."""
    level_param = request.args.get("level")
    subject_param = request.args.get("subject")

    level = None
    if level_param is not None:
        try:
            level = int(level_param)
            if not (1 <= level <= 6):
                return jsonify({"success": False, "error": "Level parameter must be between 1 and 6."}), 400
        except ValueError:
            return jsonify({"success": False, "error": "Invalid level parameter."}), 400

    lessons = LessonService.get_all_lessons(level=level, subject=subject_param)
    return jsonify({
        "success": True,
        "count": len(lessons),
        "lessons": lessons
    }), 200

@lessons_bp.route("/lessons/<slug>", methods=["GET"])
def get_lesson_detail(slug):
    """Retrieve full lesson curriculum steps and demonstration data by slug."""
    lesson = LessonService.get_lesson_by_slug(slug)
    if not lesson:
        return jsonify({"success": False, "error": f"Lesson '{slug}' not found."}), 404

    return jsonify({
        "success": True,
        "lesson": lesson
    }), 200

@lessons_bp.route("/progress/<int:student_id>", methods=["GET"])
def get_progress(student_id):
    """Get all lesson progress records for a student."""
    # Verify student exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE id = ?;", (student_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404
    conn.close()

    progress_records = ProgressService.get_student_progress(student_id)
    return jsonify({
        "success": True,
        "student_id": student_id,
        "count": len(progress_records),
        "progress": progress_records
    }), 200

@lessons_bp.route("/progress", methods=["POST"])
def save_progress():
    """Record student completion, hints used, attempts, score, and stars."""
    data = request.get_json(silent=True) or {}

    student_id = data.get("student_id")
    lesson_id = data.get("lesson_id")
    status = data.get("status", "completed")
    score = data.get("score", 100)
    hints_used = data.get("hints_used", 0)
    attempts = data.get("attempts", 1)
    stars = data.get("stars", 3)

    if not student_id or not isinstance(student_id, int):
        return jsonify({"success": False, "error": "Valid integer student_id is required."}), 400
    if not lesson_id or not isinstance(lesson_id, int):
        return jsonify({"success": False, "error": "Valid integer lesson_id is required."}), 400

    if status not in ("not_started", "in_progress", "completed"):
        return jsonify({"success": False, "error": "Status must be 'not_started', 'in_progress', or 'completed'."}), 400

    if not isinstance(stars, int) or not (0 <= stars <= 3):
        return jsonify({"success": False, "error": "Stars must be an integer between 0 and 3."}), 400

    if not isinstance(score, (int, float)) or not (0 <= score <= 100):
        return jsonify({"success": False, "error": "Score must be a number between 0 and 100."}), 400

    # Verify entities exist in database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE id = ?;", (student_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": f"Student with ID {student_id} does not exist."}), 404

    cursor.execute("SELECT id FROM lessons WHERE id = ?;", (lesson_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": f"Lesson with ID {lesson_id} does not exist."}), 404
    conn.close()

    result = ProgressService.record_progress(
        student_id=student_id,
        lesson_id=lesson_id,
        status=status,
        score=int(score),
        hints_used=int(hints_used),
        attempts=int(attempts),
        stars=stars
    )

    return jsonify({
        "success": True,
        "message": "Progress recorded successfully.",
        "progress": result
    }), 200
