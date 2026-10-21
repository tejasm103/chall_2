import os
import json
import pytest
from pathlib import Path
from app import create_app
from database.init_db import init_db

TEST_DB_PATH = Path(__file__).resolve().parent / "test_flow.db"

@pytest.fixture
def client():
    """Create test client with fresh test database."""
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
        except Exception:
            pass

    os.environ["DATABASE"] = str(TEST_DB_PATH)
    os.environ["FLASK_ENV"] = "testing"

    app = create_app("testing")
    app.config["DATABASE"] = str(TEST_DB_PATH)
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db(str(TEST_DB_PATH))
        yield client

    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
        except Exception:
            pass

def test_complete_inclusive_learning_journey(client):
    """
    Test end-to-end flow:
    1. Retrieve student profile and set sensory preferences (large font, reduced motion).
    2. Query structured curriculum for student level.
    3. Complete a lesson with gentle errorless feedback (1 hint used, 1 attempt).
    4. Play a mini-game (Emotion Recognizer) and earn 3 stars.
    5. Check daily routine and mark a morning task completed.
    6. Caregiver views aggregated progress stats reflecting real progress.
    """
    # 1. Fetch student Alex (ID: 1)
    res_student = client.get("/api/students/1")
    assert res_student.status_code == 200
    student = res_student.get_json()["student"]
    assert student["name"] == "Alex"

    # Set accessibility preferences
    res_pref = client.put("/api/preferences/1", json={
        "preferred_theme": "pastel-calming",
        "font_size": "large",
        "reduced_motion": 1,
        "voice_enabled": 1,
        "sound_enabled": 1
    })
    assert res_pref.status_code == 200
    assert res_pref.get_json()["preferences"]["preferred_theme"] == "pastel-calming"

    # 2. Query lessons for Level 1
    res_lessons = client.get("/api/lessons?level=1")
    assert res_lessons.status_code == 200
    lessons = res_lessons.get_json()["lessons"]
    assert len(lessons) >= 2
    first_lesson = lessons[0]

    # 3. Complete lesson
    res_prog = client.post("/api/progress", json={
        "student_id": 1,
        "lesson_id": first_lesson["id"],
        "status": "completed",
        "score": 100,
        "hints_used": 1,
        "attempts": 1,
        "stars": 3
    })
    assert res_prog.status_code == 200
    assert res_prog.get_json()["progress"]["stars"] == 3

    # 4. Play Emotion Recognizer mini-game
    res_game = client.post("/api/game-scores", json={
        "student_id": 1,
        "game_name": "Emotion Recognizer",
        "difficulty": "easy",
        "score": 95,
        "stars": 3,
        "accuracy": 95.0
    })
    assert res_game.status_code == 201
    assert res_game.get_json()["game_score"]["stars"] == 3

    # 5. Routine step update
    res_routines = client.get("/api/routines/1")
    assert res_routines.status_code == 200
    routines = res_routines.get_json()["routines"]
    first_routine = routines[0]
    steps = first_routine["steps"]
    steps[0]["completed"] = True

    res_patch = client.patch(f"/api/routines/{first_routine['id']}", json={"steps": steps})
    assert res_patch.status_code == 200
    assert res_patch.get_json()["routine"]["steps"][0]["completed"] is True

    # 6. Caregiver views stats
    res_stats = client.get("/api/caregiver/stats/1")
    assert res_stats.status_code == 200
    stats = res_stats.get_json()["stats"]
    assert stats["curriculum"]["completed_lessons"] >= 1
    assert stats["games"]["played_count"] >= 1
    assert stats["total_stars"] >= 6
