import json
from datetime import datetime, timezone
from database.init_db import get_db_connection

class ProgressService:
    @staticmethod
    def get_student_progress(student_id):
        """Retrieve all progress records for a student."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, l.title, l.slug, l.level, l.subject, l.icon, l.difficulty
            FROM progress p
            JOIN lessons l ON p.lesson_id = l.id
            WHERE p.student_id = ?
            ORDER BY p.last_accessed DESC;
        """, (student_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def record_progress(student_id, lesson_id, status="completed", score=100, hints_used=0, attempts=1, stars=3):
        """
        Create or update progress for a student on a lesson.
        Maintains the highest score/stars and increments attempts.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check existing progress
        cursor.execute("""
            SELECT id, score, stars, attempts, hints_used
            FROM progress
            WHERE student_id = ? AND lesson_id = ?;
        """, (student_id, lesson_id))
        existing = cursor.fetchone()

        if existing:
            new_attempts = existing["attempts"] + 1
            new_hints = existing["hints_used"] + hints_used
            # Keep highest score and stars
            best_score = max(existing["score"], score)
            best_stars = max(existing["stars"], stars)
            
            cursor.execute("""
                UPDATE progress
                SET status = ?, score = ?, hints_used = ?, attempts = ?, stars = ?, last_accessed = CURRENT_TIMESTAMP
                WHERE id = ?;
            """, (status, best_score, new_hints, new_attempts, best_stars, existing["id"]))
            progress_id = existing["id"]
        else:
            cursor.execute("""
                INSERT INTO progress (student_id, lesson_id, status, score, hints_used, attempts, stars, last_accessed)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
            """, (student_id, lesson_id, status, score, hints_used, attempts, stars))
            progress_id = cursor.lastrowid

        # Log activity
        cursor.execute("""
            INSERT INTO activity_logs (student_id, activity_type, details_json)
            VALUES (?, 'lesson_progress', ?);
        """, (student_id, json.dumps({
            "lesson_id": lesson_id,
            "status": status,
            "score": score,
            "stars": stars,
            "hints_used": hints_used
        })))

        conn.commit()

        # Fetch updated record
        cursor.execute("SELECT * FROM progress WHERE id = ?;", (progress_id,))
        result = dict(cursor.fetchone())
        conn.close()
        return result

    @staticmethod
    def record_game_score(student_id, game_name, difficulty="easy", score=100, stars=3, accuracy=100.0):
        """Record completed mini-game result."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO game_scores (student_id, game_name, difficulty, score, stars, accuracy)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (student_id, game_name, difficulty, score, stars, accuracy))
        score_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO activity_logs (student_id, activity_type, details_json)
            VALUES (?, 'game_completed', ?);
        """, (student_id, json.dumps({
            "game_name": game_name,
            "difficulty": difficulty,
            "score": score,
            "stars": stars,
            "accuracy": accuracy
        })))

        conn.commit()

        cursor.execute("SELECT * FROM game_scores WHERE id = ?;", (score_id,))
        result = dict(cursor.fetchone())
        conn.close()
        return result

    @staticmethod
    def get_caregiver_stats(student_id):
        """Aggregate real statistical metrics for the caregiver/teacher dashboard."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Student details
        cursor.execute("SELECT * FROM students WHERE id = ?;", (student_id,))
        student_row = cursor.fetchone()
        if not student_row:
            conn.close()
            return None
        student_data = dict(student_row)

        # 2. Total active lessons
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE is_active = 1;")
        total_lessons = cursor.fetchone()[0]

        # 3. Lesson progress summary
        cursor.execute("""
            SELECT 
                COUNT(*) as total_started,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_lessons,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_lessons,
                SUM(stars) as lesson_stars,
                SUM(hints_used) as total_hints,
                SUM(attempts) as total_attempts,
                AVG(score) as avg_lesson_score
            FROM progress
            WHERE student_id = ?;
        """, (student_id,))
        prog_summary = dict(cursor.fetchone())

        # 4. Games summary
        cursor.execute("""
            SELECT 
                COUNT(*) as games_played,
                SUM(stars) as game_stars,
                AVG(score) as avg_game_score,
                AVG(accuracy) as avg_accuracy
            FROM game_scores
            WHERE student_id = ?;
        """, (student_id,))
        game_summary = dict(cursor.fetchone())

        # 5. Routine summary
        cursor.execute("SELECT steps_json FROM routines WHERE student_id = ?;", (student_id,))
        routine_rows = cursor.fetchall()
        total_routine_steps = 0
        completed_routine_steps = 0
        for r in routine_rows:
            try:
                steps = json.loads(r["steps_json"])
                for s in steps:
                    total_routine_steps += 1
                    if s.get("completed"):
                        completed_routine_steps += 1
            except (json.JSONDecodeError, TypeError):
                pass

        # 6. Recent activity logs (last 10)
        cursor.execute("""
            SELECT activity_type, details_json, created_at
            FROM activity_logs
            WHERE student_id = ?
            ORDER BY created_at DESC
            LIMIT 10;
        """, (student_id,))
        activities = []
        for row in cursor.fetchall():
            item = dict(row)
            try:
                item["details"] = json.loads(item.get("details_json", "{}"))
            except (json.JSONDecodeError, TypeError):
                item["details"] = {}
            activities.append(item)

        conn.close()

        total_stars = (prog_summary["lesson_stars"] or 0) + (game_summary["game_stars"] or 0)

        return {
            "student": student_data,
            "curriculum": {
                "total_lessons": total_lessons,
                "completed_lessons": prog_summary["completed_lessons"] or 0,
                "in_progress_lessons": prog_summary["in_progress_lessons"] or 0,
                "completion_percentage": round(((prog_summary["completed_lessons"] or 0) / total_lessons * 100), 1) if total_lessons > 0 else 0,
                "avg_score": round(prog_summary["avg_lesson_score"] or 0, 1),
                "total_hints_used": prog_summary["total_hints"] or 0,
                "total_attempts": prog_summary["total_attempts"] or 0
            },
            "games": {
                "played_count": game_summary["games_played"] or 0,
                "avg_score": round(game_summary["avg_game_score"] or 0, 1),
                "avg_accuracy": round(game_summary["avg_accuracy"] or 0, 1),
                "stars": game_summary["game_stars"] or 0
            },
            "routines": {
                "total_tasks": total_routine_steps,
                "completed_tasks": completed_routine_steps,
                "completion_rate": round((completed_routine_steps / total_routine_steps * 100), 1) if total_routine_steps > 0 else 0
            },
            "total_stars": total_stars,
            "recent_activities": activities
        }

    @staticmethod
    def reset_student_progress(student_id):
        """Reset all progress and game scores for a student, with confirmation logging."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete progress
        cursor.execute("DELETE FROM progress WHERE student_id = ?;", (student_id,))
        cursor.execute("DELETE FROM game_scores WHERE student_id = ?;", (student_id,))

        # Reset routine checkmarks
        cursor.execute("SELECT id, steps_json FROM routines WHERE student_id = ?;", (student_id,))
        routines = cursor.fetchall()
        for r in routines:
            try:
                steps = json.loads(r["steps_json"])
                for s in steps:
                    s["completed"] = False
                cursor.execute("UPDATE routines SET steps_json = ? WHERE id = ?;", (json.dumps(steps), r["id"]))
            except (json.JSONDecodeError, TypeError):
                pass

        # Log reset
        cursor.execute("""
            INSERT INTO activity_logs (student_id, activity_type, details_json)
            VALUES (?, 'progress_reset', ?);
        """, (student_id, json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(), "action": "reset_all_progress"})))

        conn.commit()
        conn.close()
        return True
