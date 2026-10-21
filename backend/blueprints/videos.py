from flask import Blueprint, jsonify, request
from database.init_db import get_db_connection

videos_bp = Blueprint("videos", __name__, url_prefix="/api")

@videos_bp.route("/videos", methods=["GET"])
def list_videos():
    """Retrieve all accessible educational videos in the library."""
    category = request.args.get("category")
    conn = get_db_connection()
    cursor = conn.cursor()

    if category:
        cursor.execute("SELECT * FROM videos WHERE category = ? ORDER BY id ASC;", (category,))
    else:
        cursor.execute("SELECT * FROM videos ORDER BY id ASC;")

    rows = cursor.fetchall()
    conn.close()

    return jsonify({
        "success": True,
        "count": len(rows),
        "videos": [dict(r) for r in rows]
    }), 200

@videos_bp.route("/videos/<int:video_id>", methods=["GET"])
def get_video(video_id):
    """Retrieve full video metadata including caption and transcript details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos WHERE id = ?;", (video_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"success": False, "error": f"Video with ID {video_id} not found."}), 404

    return jsonify({
        "success": True,
        "video": dict(row)
    }), 200

@videos_bp.route("/videos/<int:video_id>/play", methods=["POST"])
def track_video_play(video_id):
    """Increment the view counter for an educational video."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE videos SET plays_count = plays_count + 1 WHERE id = ?;", (video_id,))
    affected = cursor.rowcount
    conn.commit()

    if affected == 0:
        conn.close()
        return jsonify({"success": False, "error": f"Video with ID {video_id} not found."}), 404

    cursor.execute("SELECT plays_count FROM videos WHERE id = ?;", (video_id,))
    plays = cursor.fetchone()[0]
    conn.close()

    return jsonify({
        "success": True,
        "video_id": video_id,
        "plays_count": plays
    }), 200
