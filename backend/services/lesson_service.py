import json
from database.init_db import get_db_connection

class LessonService:
    @staticmethod
    def get_all_lessons(level=None, subject=None, is_active=1):
        """Fetch all active lessons with optional filtering by level and subject."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM lessons WHERE is_active = ?"
        params = [is_active]
        
        if level is not None:
            query += " AND level = ?"
            params.append(level)
            
        if subject is not None:
            query += " AND subject = ?"
            params.append(subject)
            
        query += " ORDER BY level ASC, id ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        lessons = []
        for row in rows:
            lesson_dict = dict(row)
            try:
                lesson_dict["steps"] = json.loads(lesson_dict.get("steps_json", "[]"))
            except (json.JSONDecodeError, TypeError):
                lesson_dict["steps"] = []
            lessons.append(lesson_dict)
            
        return lessons

    @staticmethod
    def get_lesson_by_slug(slug):
        """Retrieve a single lesson by its URL-friendly slug."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lessons WHERE slug = ? AND is_active = 1 LIMIT 1;", (slug,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
            
        lesson = dict(row)
        try:
            lesson["steps"] = json.loads(lesson.get("steps_json", "[]"))
        except (json.JSONDecodeError, TypeError):
            lesson["steps"] = []
        return lesson

    @staticmethod
    def get_lesson_by_id(lesson_id):
        """Retrieve a single lesson by primary key."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lessons WHERE id = ? LIMIT 1;", (lesson_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
            
        lesson = dict(row)
        try:
            lesson["steps"] = json.loads(lesson.get("steps_json", "[]"))
        except (json.JSONDecodeError, TypeError):
            lesson["steps"] = []
        return lesson
