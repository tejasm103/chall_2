import os
import sqlite3
import pytest
from pathlib import Path
from database.init_db import init_db, get_db_connection

TEST_DB_PATH = Path(__file__).resolve().parent / "test_scratch.db"

@pytest.fixture(autouse=True)
def cleanup():
    """Ensure clean test database before and after each test."""
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
        except Exception:
            pass
    yield
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
        except Exception:
            pass

def test_init_db_creates_tables():
    """Test that init_db creates all required tables in an empty directory."""
    assert not TEST_DB_PATH.exists()
    init_db(str(TEST_DB_PATH))
    assert TEST_DB_PATH.exists()

    conn = get_db_connection(str(TEST_DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row["name"] for row in cursor.fetchall()]
    conn.close()

    expected = ["students", "lessons", "progress", "game_scores", "routines", "videos", "activity_logs", "caregiver_auth"]
    for table in expected:
        assert table in tables, f"Table '{table}' was not created."

def test_init_db_idempotency():
    """Test that calling init_db multiple times does not create duplicate seed entries."""
    init_db(str(TEST_DB_PATH))
    conn = get_db_connection(str(TEST_DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students;")
    initial_students = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM lessons;")
    initial_lessons = cursor.fetchone()[0]
    conn.close()

    # Re-run init_db
    init_db(str(TEST_DB_PATH))

    conn = get_db_connection(str(TEST_DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students;")
    assert cursor.fetchone()[0] == initial_students
    cursor.execute("SELECT COUNT(*) FROM lessons;")
    assert cursor.fetchone()[0] == initial_lessons
    conn.close()

def test_foreign_key_enforcement():
    """Test that SQLite foreign key constraints are strictly enforced."""
    init_db(str(TEST_DB_PATH))
    conn = get_db_connection(str(TEST_DB_PATH))
    cursor = conn.cursor()

    # Try inserting progress for non-existent student
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO progress (student_id, lesson_id, status, score)
            VALUES (99999, 1, 'completed', 100);
        """)
        conn.commit()

    conn.close()
