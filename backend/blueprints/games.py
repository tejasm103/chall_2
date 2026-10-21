from flask import Blueprint, jsonify, request
from services.progress_service import ProgressService
from database.init_db import get_db_connection

games_bp = Blueprint("games", __name__, url_prefix="/api")

EDUCATIONAL_GAMES_CATALOGUE = [
    {
        "id": "color-matcher",
        "name": "Color Matcher",
        "category": "Visual Perception",
        "description": "Identify requested colors using large accessible cards, text labels, and patterns.",
        "skills": ["Color identification", "Visual discrimination", "Word-color association"],
        "icon": "palette",
        "difficulties": ["easy", "medium", "hard"],
        "star_criteria": "3 stars for 90%+ accuracy, 2 stars for 70%+, 1 star for completion."
    },
    {
        "id": "emotion-recognizer",
        "name": "Emotion Recognizer",
        "category": "Social-Emotional",
        "description": "Match friendly illustrated facial expressions to words such as happy, calm, sad, and surprised.",
        "skills": ["Emotion awareness", "Facial cues", "Empathy & context"],
        "icon": "smile",
        "difficulties": ["easy", "medium"],
        "star_criteria": "3 stars for 90%+ accuracy, 2 stars for 70%+, 1 star for completion."
    },
    {
        "id": "object-counter",
        "name": "Object Counter",
        "category": "Early Mathematics",
        "description": "Count familiar objects with optional tactile counting aids and select the correct number.",
        "skills": ["One-to-one counting", "Quantity recognition", "Numeral matching"],
        "icon": "calculator",
        "difficulties": ["easy", "medium", "hard"],
        "star_criteria": "3 stars for 90%+ accuracy, 2 stars for 70%+, 1 star for completion."
    },
    {
        "id": "picture-word-pairing",
        "name": "Picture-Word Pairing",
        "category": "Phonics & Vocabulary",
        "description": "Match cheerful object illustrations with their written words, with optional audio pronunciation.",
        "skills": ["Word recognition", "Sight reading", "Vocabulary building"],
        "icon": "book-open",
        "difficulties": ["easy", "medium"],
        "star_criteria": "3 stars for 90%+ accuracy, 2 stars for 70%+, 1 star for completion."
    }
]

@games_bp.route("/games", methods=["GET"])
def get_games():
    """List all educational games with metadata and rules."""
    return jsonify({
        "success": True,
        "count": len(EDUCATIONAL_GAMES_CATALOGUE),
        "games": EDUCATIONAL_GAMES_CATALOGUE
    }), 200

@games_bp.route("/game-scores", methods=["POST"])
def save_game_score():
    """Save an educational game score and star award to SQLite."""
    data = request.get_json(silent=True) or {}

    student_id = data.get("student_id")
    game_name = data.get("game_name", "").strip()
    difficulty = data.get("difficulty", "easy").lower()
    score = data.get("score", 0)
    stars = data.get("stars", 1)
    accuracy = data.get("accuracy", 100.0)

    if not student_id or not isinstance(student_id, int):
        return jsonify({"success": False, "error": "Valid integer student_id is required."}), 400

    if not game_name:
        return jsonify({"success": False, "error": "game_name is required."}), 400

    if difficulty not in ("easy", "medium", "hard"):
        difficulty = "easy"

    if not isinstance(stars, int) or not (0 <= stars <= 3):
        return jsonify({"success": False, "error": "Stars must be between 0 and 3."}), 400

    try:
        score = int(score)
        accuracy = float(accuracy)
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Score and accuracy must be valid numbers."}), 400

    # Ensure student exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE id = ?;", (student_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "error": f"Student with ID {student_id} not found."}), 404
    conn.close()

    result = ProgressService.record_game_score(
        student_id=student_id,
        game_name=game_name,
        difficulty=difficulty,
        score=score,
        stars=stars,
        accuracy=accuracy
    )

    return jsonify({
        "success": True,
        "message": f"Game score recorded for {game_name}.",
        "game_score": result
    }), 201
