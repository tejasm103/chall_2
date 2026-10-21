import os
import json
import pytest
from pathlib import Path
from app import create_app
from database.init_db import init_db

TEST_DB_PATH = Path(__file__).resolve().parent / "test_api.db"

@pytest.fixture
def client():
    """Create test client with clean isolated test database."""
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

def test_health_check(client):
    """Test /api/health returns 200 with healthy database status."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

def test_students_api(client):
    """Test student listing, creation, retrieval, and patch."""
    # List students
    res = client.get("/api/students")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["students"]) >= 3

    # Create new student
    new_student = {
        "name": "Sammy",
        "avatar": "curious-cat",
        "learning_level": 2,
        "preferred_theme": "pastel-calming",
        "font_size": "large"
    }
    res_post = client.post("/api/students", json=new_student)
    assert res_post.status_code == 201
    created = res_post.get_json()["student"]
    assert created["name"] == "Sammy"
    student_id = created["id"]

    # Get single student
    res_get = client.get(f"/api/students/{student_id}")
    assert res_get.status_code == 200
    assert res_get.get_json()["student"]["name"] == "Sammy"

    # Patch student
    res_patch = client.patch(f"/api/students/{student_id}", json={"learning_level": 3})
    assert res_patch.status_code == 200
    assert res_patch.get_json()["student"]["learning_level"] == 3

def test_preferences_api(client):
    """Test accessibility preferences retrieval and update."""
    # Alex is student ID 1
    res = client.get("/api/preferences/1")
    assert res.status_code == 200
    prefs = res.get_json()["preferences"]
    assert "preferred_theme" in prefs

    # Update preferences
    update_data = {
        "preferred_theme": "high-contrast-dark",
        "font_size": "xlarge",
        "reduced_motion": 1
    }
    res_put = client.put("/api/preferences/1", json=update_data)
    assert res_put.status_code == 200
    updated_prefs = res_put.get_json()["preferences"]
    assert updated_prefs["preferred_theme"] == "high-contrast-dark"
    assert updated_prefs["font_size"] == "xlarge"
    assert updated_prefs["reduced_motion"] == 1

def test_lessons_api(client):
    """Test lessons listing, filtering by level, and detail view."""
    # All lessons
    res = client.get("/api/lessons")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] >= 10

    # Filter level 1
    res_l1 = client.get("/api/lessons?level=1")
    assert res_l1.status_code == 200
    l1_data = res_l1.get_json()
    assert all(l["level"] == 1 for l in l1_data["lessons"])

    # Detail by slug
    res_slug = client.get("/api/lessons/wonderful-colors")
    assert res_slug.status_code == 200
    lesson = res_slug.get_json()["lesson"]
    assert lesson["slug"] == "wonderful-colors"
    assert len(lesson["steps"]) > 0

    # 404 for unknown slug
    res_404 = client.get("/api/lessons/nonexistent-lesson")
    assert res_404.status_code == 404

def test_progress_api(client):
    """Test saving and retrieving lesson progress."""
    # Save progress for student 1, lesson 1
    progress_payload = {
        "student_id": 1,
        "lesson_id": 1,
        "status": "completed",
        "score": 100,
        "hints_used": 1,
        "attempts": 2,
        "stars": 3
    }
    res = client.post("/api/progress", json=progress_payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["progress"]["stars"] == 3

    # Get student progress
    res_get = client.get("/api/progress/1")
    assert res_get.status_code == 200
    assert len(res_get.get_json()["progress"]) > 0

def test_games_api(client):
    """Test games catalogue and game score recording."""
    res_list = client.get("/api/games")
    assert res_list.status_code == 200
    games = res_list.get_json()["games"]
    assert len(games) == 4

    # Record score
    score_payload = {
        "student_id": 1,
        "game_name": "Color Matcher",
        "difficulty": "easy",
        "score": 100,
        "stars": 3,
        "accuracy": 100.0
    }
    res_score = client.post("/api/game-scores", json=score_payload)
    assert res_score.status_code == 201
    assert res_score.get_json()["game_score"]["stars"] == 3

def test_daily_routine_api(client):
    """Test routine retrieval, creation, patch, and deletion."""
    # Get routines for student 1
    res = client.get("/api/routines/1")
    assert res.status_code == 200
    routines = res.get_json()["routines"]
    assert len(routines) >= 4

    # Create custom routine
    new_routine = {
        "student_id": 1,
        "title": "Sensory Calming Space",
        "category": "custom",
        "steps": [
            {"id": "c1", "title": "Dim lights", "completed": True},
            {"id": "c2", "title": "Put on weighted blanket", "completed": False}
        ]
    }
    res_post = client.post("/api/routines", json=new_routine)
    assert res_post.status_code == 201
    created_routine = res_post.get_json()["routine"]
    routine_id = created_routine["id"]

    # Patch routine
    res_patch = client.patch(f"/api/routines/{routine_id}", json={"title": "Updated Sensory Space"})
    assert res_patch.status_code == 200
    assert res_patch.get_json()["routine"]["title"] == "Updated Sensory Space"

    # Delete routine
    res_del = client.delete(f"/api/routines/{routine_id}")
    assert res_del.status_code == 200

def test_video_api(client):
    """Test educational video catalogue and play counter."""
    res = client.get("/api/videos")
    assert res.status_code == 200
    videos = res.get_json()["videos"]
    assert len(videos) >= 5

    # Play video
    vid_id = videos[0]["id"]
    res_play = client.post(f"/api/videos/{vid_id}/play")
    assert res_play.status_code == 200
    assert res_play.get_json()["plays_count"] > 0

def test_caregiver_api_and_reset(client):
    """Test caregiver stats calculation and progress reset."""
    res_stats = client.get("/api/caregiver/stats/1")
    assert res_stats.status_code == 200
    stats = res_stats.get_json()["stats"]
    assert "curriculum" in stats
    assert "games" in stats

    # Reset progress without confirm -> 400
    res_bad_reset = client.post("/api/caregiver/reset/1", json={"confirm": False})
    assert res_bad_reset.status_code == 400

    # Reset progress with confirm -> 200
    res_reset = client.post("/api/caregiver/reset/1", json={"confirm": True})
    assert res_reset.status_code == 200

    # Check stats after reset
    res_stats2 = client.get("/api/caregiver/stats/1")
    stats2 = res_stats2.get_json()["stats"]
    assert stats2["curriculum"]["completed_lessons"] == 0
