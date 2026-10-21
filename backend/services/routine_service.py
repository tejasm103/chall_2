import json
from database.init_db import get_db_connection

class RoutineService:
    @staticmethod
    def get_routines_by_student(student_id):
        """Fetch all routines for a student with parsed steps."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM routines
            WHERE student_id = ?
            ORDER BY id ASC;
        """, (student_id,))
        rows = cursor.fetchall()
        conn.close()

        routines = []
        for r in rows:
            r_dict = dict(r)
            try:
                r_dict["steps"] = json.loads(r_dict.get("steps_json", "[]"))
            except (json.JSONDecodeError, TypeError):
                r_dict["steps"] = []
            routines.append(r_dict)
        return routines

    @staticmethod
    def get_routine_by_id(routine_id):
        """Fetch a single routine by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routines WHERE id = ?;", (routine_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        r_dict = dict(row)
        try:
            r_dict["steps"] = json.loads(r_dict.get("steps_json", "[]"))
        except (json.JSONDecodeError, TypeError):
            r_dict["steps"] = []
        return r_dict

    @staticmethod
    def create_routine(student_id, title, category, steps, is_custom=1):
        """Create a new routine for a student."""
        conn = get_db_connection()
        cursor = conn.cursor()

        steps_json = json.dumps(steps) if isinstance(steps, list) else str(steps)

        cursor.execute("""
            INSERT INTO routines (student_id, title, category, steps_json, is_custom)
            VALUES (?, ?, ?, ?, ?);
        """, (student_id, title, category, steps_json, is_custom))
        routine_id = cursor.lastrowid
        conn.commit()

        cursor.execute("SELECT * FROM routines WHERE id = ?;", (routine_id,))
        result = dict(cursor.fetchone())
        result["steps"] = json.loads(result["steps_json"])
        conn.close()
        return result

    @staticmethod
    def update_routine(routine_id, title=None, category=None, steps=None):
        """Update fields or step states of an existing routine."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM routines WHERE id = ?;", (routine_id,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            return None

        new_title = title if title is not None else existing["title"]
        new_category = category if category is not None else existing["category"]
        if steps is not None:
            new_steps_json = json.dumps(steps) if isinstance(steps, list) else str(steps)
        else:
            new_steps_json = existing["steps_json"]

        cursor.execute("""
            UPDATE routines
            SET title = ?, category = ?, steps_json = ?
            WHERE id = ?;
        """, (new_title, new_category, new_steps_json, routine_id))
        conn.commit()

        cursor.execute("SELECT * FROM routines WHERE id = ?;", (routine_id,))
        result = dict(cursor.fetchone())
        result["steps"] = json.loads(result["steps_json"])
        conn.close()
        return result

    @staticmethod
    def delete_routine(routine_id):
        """Delete a routine by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM routines WHERE id = ?;", (routine_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0
