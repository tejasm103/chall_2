import os
import sqlite3
import json
from pathlib import Path
from werkzeug.security import generate_password_hash

DB_DIR = Path(__file__).resolve().parent
SCHEMA_FILE = DB_DIR / "schema.sql"

def get_db_connection(db_path=None):
    """Create a configured SQLite connection with foreign keys and WAL enabled."""
    if db_path is None:
        try:
            from flask import current_app
            if current_app and current_app.config.get("DATABASE"):
                db_path = current_app.config.get("DATABASE")
        except Exception:
            pass

    if db_path is None:
        try:
            from config import Config
            db_path = Config.DATABASE
        except ImportError:
            import sys
            parent_dir = str(Path(__file__).resolve().parent.parent)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            from config import Config
            db_path = Config.DATABASE

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    conn = sqlite3.connect(db_path, timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn

def init_db(db_path=None, force=False):
    """
    Initialize SQLite database tables using schema.sql and seed sample data.
    Ensures idempotency: never duplicates or deletes existing user data.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    try:
        # Check if tables already exist
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='students';")
        tables_exist = cursor.fetchone()[0] > 0

        if not tables_exist or force:
            with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            cursor.executescript(schema_sql)
            conn.commit()

        # Seed data idempotently
        seed_data(conn)
        conn.commit()
    finally:
        conn.close()

def seed_data(conn):
    """Seed initial students, lessons across 6 levels, routines, videos, and caregiver credentials."""
    cursor = conn.cursor()

    # 1. Seed Students
    cursor.execute("SELECT COUNT(*) FROM students;")
    if cursor.fetchone()[0] == 0:
        students = [
            ("Alex", "robot-milo", 1, "default", "standard", 1, 1, 0),
            ("Maya", "star-buddy", 2, "pastel-calming", "large", 1, 1, 0),
            ("Jordan", "curious-cat", 3, "high-contrast-dark", "xlarge", 1, 1, 1)
        ]
        cursor.executemany("""
            INSERT INTO students (name, avatar, learning_level, preferred_theme, font_size, voice_enabled, sound_enabled, reduced_motion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, students)

    # Fetch default student id
    cursor.execute("SELECT id FROM students WHERE name='Alex' LIMIT 1;")
    alex_row = cursor.fetchone()
    alex_id = alex_row[0] if alex_row else 1

    # 2. Seed Lessons across 6 levels
    cursor.execute("SELECT COUNT(*) FROM lessons;")
    if cursor.fetchone()[0] == 0:
        lessons = [
            # Level 1 — Discovering the World
            (
                1, "Colors & Shapes", "Wonderful Colors", "wonderful-colors",
                "Explore bright primary colors with gentle visual guides and Milo.",
                "Primary Color Recognition", "palette", "gentle",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "Look at the big bright circle. This is Red!",
                        "demonstration": {"type": "color_display", "color": "#E53935", "name": "Red", "item": "Strawberry", "icon": "strawberry"},
                        "question": "Can you touch the Red card?",
                        "options": [
                            {"id": "opt-1", "label": "Red", "color": "#E53935", "is_correct": True},
                            {"id": "opt-2", "label": "Blue", "color": "#1E88E5", "is_correct": False},
                            {"id": "opt-3", "label": "Green", "color": "#43A047", "is_correct": False}
                        ],
                        "hint": "Red looks like a sweet ripe strawberry!",
                        "milo_dialogue": "Let's find the warm Red color together!"
                    },
                    {
                        "step_number": 2,
                        "instruction": "Now look at Blue! Calm and serene like the sky.",
                        "demonstration": {"type": "color_display", "color": "#1E88E5", "name": "Blue", "item": "Blueberry", "icon": "blueberry"},
                        "question": "Which one is Blue?",
                        "options": [
                            {"id": "opt-1", "label": "Yellow", "color": "#FDD835", "is_correct": False},
                            {"id": "opt-2", "label": "Blue", "color": "#1E88E5", "is_correct": True},
                            {"id": "opt-3", "label": "Red", "color": "#E53935", "is_correct": False}
                        ],
                        "hint": "Blue is the color of the clear ocean water.",
                        "milo_dialogue": "You're doing great. Look for the calm blue."
                    },
                    {
                        "step_number": 3,
                        "instruction": "Here comes sunny Yellow! Radiant and joyful.",
                        "demonstration": {"type": "color_display", "color": "#FDD835", "name": "Yellow", "item": "Sun", "icon": "sun"},
                        "question": "Tap the sunny Yellow color!",
                        "options": [
                            {"id": "opt-1", "label": "Blue", "color": "#1E88E5", "is_correct": False},
                            {"id": "opt-2", "label": "Yellow", "color": "#FDD835", "is_correct": True},
                            {"id": "opt-3", "label": "Purple", "color": "#8E24AA", "is_correct": False}
                        ],
                        "hint": "Yellow is bright and cheerful like sunshine.",
                        "milo_dialogue": "Find the happy yellow sun!"
                    }
                ]),
                "multiple_choice", 1
            ),
            (
                1, "Colors & Shapes", "Friendly Shapes", "friendly-shapes",
                "Learn circles, squares, and triangles with predictable tactile shapes.",
                "Shape Identification", "shapes", "gentle",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "A Circle is round and smooth with no sharp corners.",
                        "demonstration": {"type": "shape_display", "shape": "circle", "name": "Circle", "icon": "circle"},
                        "question": "Which shape is round like a clock or wheel?",
                        "options": [
                            {"id": "opt-1", "label": "Circle", "shape": "circle", "is_correct": True},
                            {"id": "opt-2", "label": "Square", "shape": "square", "is_correct": False},
                            {"id": "opt-3", "label": "Triangle", "shape": "triangle", "is_correct": False}
                        ],
                        "hint": "Circles roll smoothly along the ground.",
                        "milo_dialogue": "Circles are round all the way around!"
                    },
                    {
                        "step_number": 2,
                        "instruction": "A Square has 4 straight sides that are all the same length.",
                        "demonstration": {"type": "shape_display", "shape": "square", "name": "Square", "icon": "square"},
                        "question": "Find the Square with 4 equal sides!",
                        "options": [
                            {"id": "opt-1", "label": "Triangle", "shape": "triangle", "is_correct": False},
                            {"id": "opt-2", "label": "Square", "shape": "square", "is_correct": True},
                            {"id": "opt-3", "label": "Circle", "shape": "circle", "is_correct": False}
                        ],
                        "hint": "A square is shaped like a picture block or window.",
                        "milo_dialogue": "Look at the four straight corners."
                    }
                ]),
                "identify_picture", 1
            ),
            (
                1, "Everyday Objects", "Everyday Objects in the House", "everyday-objects",
                "Recognize familiar items we see every day at home.",
                "Everyday Recognition", "home", "gentle",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "We use a Cup when we drink fresh water.",
                        "demonstration": {"type": "object_display", "name": "Cup", "icon": "cup"},
                        "question": "Which picture shows a cup for drinking?",
                        "options": [
                            {"id": "opt-1", "label": "Cup", "icon": "cup", "is_correct": True},
                            {"id": "opt-2", "label": "Shoe", "icon": "shoe", "is_correct": False},
                            {"id": "opt-3", "label": "Hat", "icon": "hat", "is_correct": False}
                        ],
                        "hint": "A cup holds water or milk.",
                        "milo_dialogue": "Let's find the cup we drink with!"
                    }
                ]),
                "identify_picture", 1
            ),

            # Level 2 — Foundational Phonics and Counting
            (
                2, "Phonics", "Letter Sounds A to D", "letter-sounds-a-d",
                "Listen to the starting sounds of letters A, B, C, and D.",
                "Initial Phoneme Identification", "font", "moderate",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "Letter A says /æ/ as in Apple!",
                        "demonstration": {"type": "phonics_display", "letter": "A a", "sound": "ah", "word": "Apple", "icon": "apple"},
                        "question": "Which picture begins with the /æ/ sound for A?",
                        "options": [
                            {"id": "opt-1", "label": "Apple", "icon": "apple", "is_correct": True},
                            {"id": "opt-2", "label": "Ball", "icon": "ball", "is_correct": False},
                            {"id": "opt-3", "label": "Cat", "icon": "cat", "is_correct": False}
                        ],
                        "hint": "/æ/ /æ/ Apple!",
                        "milo_dialogue": "Say 'ah' like when eating a yummy apple!"
                    },
                    {
                        "step_number": 2,
                        "instruction": "Letter B says /b/ as in Bouncing Ball!",
                        "demonstration": {"type": "phonics_display", "letter": "B b", "sound": "buh", "word": "Ball", "icon": "ball"},
                        "question": "Which word starts with the /b/ sound?",
                        "options": [
                            {"id": "opt-1", "label": "Duck", "icon": "duck", "is_correct": False},
                            {"id": "opt-2", "label": "Ball", "icon": "ball", "is_correct": True},
                            {"id": "opt-3", "label": "Apple", "icon": "apple", "is_correct": False}
                        ],
                        "hint": "/b/ /b/ Ball bounces up and down.",
                        "milo_dialogue": "Listen to the bouncy sound: /b/!"
                    }
                ]),
                "multiple_choice", 1
            ),
            (
                2, "Math", "Counting Stars 1 to 5", "counting-stars-1-to-5",
                "Touch each star as we count slowly together: 1, 2, 3, 4, 5.",
                "One-to-One Correspondence", "calculator", "moderate",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "Look at these bright stars. Let's count them: 1, 2, 3!",
                        "demonstration": {"type": "count_display", "count": 3, "items": ["star", "star", "star"]},
                        "question": "How many stars do you see?",
                        "options": [
                            {"id": "opt-1", "label": "2", "is_correct": False},
                            {"id": "opt-2", "label": "3", "is_correct": True},
                            {"id": "opt-3", "label": "4", "is_correct": False}
                        ],
                        "hint": "Count with your finger: one, two, three!",
                        "milo_dialogue": "Point to each star as we count!"
                    }
                ]),
                "multiple_choice", 1
            ),

            # Level 3 — Early Academic Skills and Emotions
            (
                3, "Social-Emotional", "Feelings & Facial Expressions", "feelings-and-emotions",
                "Learn how smiling, resting, and curious faces look. Remember every face is unique!",
                "Emotion Awareness", "smile", "moderate",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "When someone feels happy, their mouth curves up into a warm smile.",
                        "demonstration": {"type": "emotion_display", "emotion": "Happy", "expression": "smile", "icon": "happy-face"},
                        "question": "Which face shows a happy, smiling friend?",
                        "options": [
                            {"id": "opt-1", "label": "Happy", "icon": "happy-face", "is_correct": True},
                            {"id": "opt-2", "label": "Sad", "icon": "sad-face", "is_correct": False},
                            {"id": "opt-3", "label": "Surprised", "icon": "surprised-face", "is_correct": False}
                        ],
                        "hint": "Look for the gentle smile that curls upward.",
                        "milo_dialogue": "A warm smile feels welcoming and friendly."
                    },
                    {
                        "step_number": 2,
                        "instruction": "When feeling calm, the face is relaxed and peaceful.",
                        "demonstration": {"type": "emotion_display", "emotion": "Calm", "expression": "relaxed", "icon": "calm-face"},
                        "question": "Touch the calm and relaxed face.",
                        "options": [
                            {"id": "opt-1", "label": "Angry", "icon": "angry-face", "is_correct": False},
                            {"id": "opt-2", "label": "Calm", "icon": "calm-face", "is_correct": True},
                            {"id": "opt-3", "label": "Sad", "icon": "sad-face", "is_correct": False}
                        ],
                        "hint": "Calm eyes are soft and peaceful.",
                        "milo_dialogue": "Take a gentle breath and feel calm like Milo."
                    }
                ]),
                "identify_picture", 1
            ),
            (
                3, "Reading", "Word Families: The -AT Family", "word-families-at",
                "Combine letters to make words that rhyme: C-AT, H-AT, B-AT.",
                "Rhyming & Word Families", "book", "moderate",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "When we add 'C' to '-AT', we make CAT!",
                        "demonstration": {"type": "word_blend", "prefix": "C", "ending": "AT", "word": "CAT", "icon": "cat"},
                        "question": "Which word rhymes with Hat and Mat?",
                        "options": [
                            {"id": "opt-1", "label": "Cat", "icon": "cat", "is_correct": True},
                            {"id": "opt-2", "label": "Dog", "icon": "dog", "is_correct": False},
                            {"id": "opt-3", "label": "Sun", "icon": "sun", "is_correct": False}
                        ],
                        "hint": "Cat ends with the same '-at' sound as Hat.",
                        "milo_dialogue": "Listen to the rhyme: Hat, Mat, Cat!"
                    }
                ]),
                "matching", 1
            ),

            # Level 4 — Primary Skills and Problem Solving
            (
                4, "Sequencing", "Story Sequencing: Planting a Seed", "story-sequencing-seed",
                "Put events in order: What happens first, next, and last?",
                "Sequential Reasoning", "list-ol", "structured",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "Plants grow in steps: First we plant the seed in soil.",
                        "demonstration": {"type": "sequence_step", "step": "Plant seed in soil", "icon": "seed"},
                        "question": "What is the very first step to grow a plant?",
                        "options": [
                            {"id": "opt-1", "label": "Plant the seed in soil", "icon": "seed", "is_correct": True},
                            {"id": "opt-2", "label": "Pick the full flower", "icon": "flower", "is_correct": False},
                            {"id": "opt-3", "label": "Cut the stems", "icon": "scissors", "is_correct": False}
                        ],
                        "hint": "Before a flower can grow, the little seed needs to go into the soil.",
                        "milo_dialogue": "First comes the seed tucked into the warm earth."
                    },
                    {
                        "step_number": 2,
                        "instruction": "Next, the seed needs gentle water and sunlight to sprout.",
                        "demonstration": {"type": "sequence_step", "step": "Water the soil", "icon": "water-drop"},
                        "question": "What does the seed need next?",
                        "options": [
                            {"id": "opt-1", "label": "Put in the dark fridge", "is_correct": False},
                            {"id": "opt-2", "label": "Water and warm sunlight", "icon": "sun", "is_correct": True},
                            {"id": "opt-3", "label": "Paint it blue", "is_correct": False}
                        ],
                        "hint": "Water and sunshine give the seed energy to grow.",
                        "milo_dialogue": "Water and sunshine help it drink and grow tall!"
                    }
                ]),
                "sequencing", 1
            ),
            (
                4, "Math", "Addition with Visual Blocks", "addition-visual-blocks",
                "Put groups of blocks together to find the total sum.",
                "Basic Addition Concepts", "plus-circle", "structured",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "You have 2 blue blocks and 1 yellow block. Let's combine them!",
                        "demonstration": {"type": "math_blocks", "group_a": 2, "group_b": 1, "total": 3},
                        "question": "2 blocks + 1 block = how many in total?",
                        "options": [
                            {"id": "opt-1", "label": "2", "is_correct": False},
                            {"id": "opt-2", "label": "3", "is_correct": True},
                            {"id": "opt-3", "label": "4", "is_correct": False}
                        ],
                        "hint": "Count all blocks together: 1, 2... and one more makes 3!",
                        "milo_dialogue": "Two plus one equals three blocks!"
                    }
                ]),
                "multiple_choice", 1
            ),

            # Level 5 — Middle Skills and Logic
            (
                5, "Logic & Patterns", "Pattern Detective", "pattern-detective",
                "Notice repeating patterns: Red, Blue, Red, Blue... What comes next?",
                "Pattern Recognition & Extrapolation", "puzzle-piece", "challenging",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "Look at the pattern: Circle, Square, Circle, Square...",
                        "demonstration": {"type": "pattern_display", "pattern": ["circle", "square", "circle", "square"]},
                        "question": "Which shape completes the pattern?",
                        "options": [
                            {"id": "opt-1", "label": "Circle", "icon": "circle", "is_correct": True},
                            {"id": "opt-2", "label": "Star", "icon": "star", "is_correct": False},
                            {"id": "opt-3", "label": "Triangle", "icon": "triangle", "is_correct": False}
                        ],
                        "hint": "After square comes circle, like a steady rhythm.",
                        "milo_dialogue": "Circle, square, circle, square, circle!"
                    }
                ]),
                "multiple_choice", 1
            ),
            (
                5, "Classification", "Sorting & Categorization", "sorting-categorization",
                "Group items by type: Animals, Vehicles, and Yummy Fruits.",
                "Multi-Category Classification", "tags", "challenging",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "Vehicles are machines that help people travel from place to place.",
                        "demonstration": {"type": "category_display", "category": "Vehicles", "examples": ["Car", "Bus", "Bicycle"]},
                        "question": "Which item belongs in the Vehicles category?",
                        "options": [
                            {"id": "opt-1", "label": "Car", "icon": "car", "is_correct": True},
                            {"id": "opt-2", "label": "Banana", "icon": "banana", "is_correct": False},
                            {"id": "opt-3", "label": "Cat", "icon": "cat", "is_correct": False}
                        ],
                        "hint": "A car has wheels and drives on roads.",
                        "milo_dialogue": "A car is a vehicle that drives us places."
                    }
                ]),
                "matching", 1
            ),

            # Level 6 — Everyday Independence
            (
                6, "Life Skills", "Step-by-Step Handwashing", "step-by-step-handwashing",
                "Follow five healthy steps to keep our hands clean and fresh.",
                "Hygiene & Procedural Independence", "hands-wash", "empowering",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "Step 1: Turn on gentle warm water and wet your hands.",
                        "demonstration": {"type": "handwash_step", "step": "Wet hands with water", "icon": "water"},
                        "question": "What is the first step when washing hands?",
                        "options": [
                            {"id": "opt-1", "label": "Wet hands with water", "is_correct": True},
                            {"id": "opt-2", "label": "Dry with towel immediately", "is_correct": False},
                            {"id": "opt-3", "label": "Eat an apple", "is_correct": False}
                        ],
                        "hint": "First make hands wet so soap bubbles can foam.",
                        "milo_dialogue": "Turn on clean water to wet both hands."
                    },
                    {
                        "step_number": 2,
                        "instruction": "Step 2: Add soap and scrub bubbles between fingers and palms for 20 seconds.",
                        "demonstration": {"type": "handwash_step", "step": "Scrub with soap", "icon": "soap"},
                        "question": "What cleans our hands and makes fun bubbles?",
                        "options": [
                            {"id": "opt-1", "label": "Gentle soap", "is_correct": True},
                            {"id": "opt-2", "label": "Sand", "is_correct": False},
                            {"id": "opt-3", "label": "Juice", "is_correct": False}
                        ],
                        "hint": "Soap washes away germs and keeps us healthy.",
                        "milo_dialogue": "Scrub the bubbly soap all over your fingers!"
                    }
                ]),
                "sequencing", 1
            ),
            (
                6, "Communication", "Expressing What I Need", "expressing-what-i-need",
                "Practice clear ways to ask for a break, a drink, or teacher help.",
                "Functional Communication", "comments", "empowering",
                json.dumps([
                    {
                        "step_number": 1,
                        "instruction": "When you feel tired or sensory-overloaded, you can ask for a quiet break.",
                        "demonstration": {"type": "communication_phrase", "phrase": "May I please take a quiet break?", "icon": "pause"},
                        "question": "If you need a quiet moment, what card can you show your teacher?",
                        "options": [
                            {"id": "opt-1", "label": "'I need a quiet break, please'", "icon": "pause", "is_correct": True},
                            {"id": "opt-2", "label": "'Turn the music super loud'", "is_correct": False},
                            {"id": "opt-3", "label": "'Run outside in the rain'", "is_correct": False}
                        ],
                        "hint": "Asking for a quiet break helps your mind rest and recharge.",
                        "milo_dialogue": "It is always okay to ask for a quiet break."
                    }
                ]),
                "identify_picture", 1
            )
        ]

        cursor.executemany("""
            INSERT INTO lessons (level, subject, title, slug, description, concept, icon, difficulty, steps_json, interactive_type, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, lessons)

    # 3. Seed Progress for Alex
    cursor.execute("SELECT COUNT(*) FROM progress WHERE student_id=?;", (alex_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT id FROM lessons WHERE slug='wonderful-colors';")
        l1 = cursor.fetchone()
        if l1:
            cursor.execute("""
                INSERT INTO progress (student_id, lesson_id, status, score, hints_used, attempts, stars)
                VALUES (?, ?, 'completed', 100, 0, 1, 3);
            """, (alex_id, l1[0]))

        cursor.execute("SELECT id FROM lessons WHERE slug='friendly-shapes';")
        l2 = cursor.fetchone()
        if l2:
            cursor.execute("""
                INSERT INTO progress (student_id, lesson_id, status, score, hints_used, attempts, stars)
                VALUES (?, ?, 'in_progress', 50, 1, 2, 2);
            """, (alex_id, l2[0]))

    # 4. Seed Routines
    cursor.execute("SELECT COUNT(*) FROM routines; ")
    if cursor.fetchone()[0] == 0:
        default_routines = [
            (
                alex_id, "Morning Sunshine Routine", "morning",
                json.dumps([
                    {"id": "m1", "title": "Wake up gently", "icon": "sun", "completed": True, "time": "7:00 AM"},
                    {"id": "m2", "title": "Drink a glass of water", "icon": "cup", "completed": True, "time": "7:15 AM"},
                    {"id": "m3", "title": "Brush teeth", "icon": "toothbrush", "completed": False, "time": "7:25 AM"},
                    {"id": "m4", "title": "Get dressed in comfy clothes", "icon": "shirt", "completed": False, "time": "7:35 AM"},
                    {"id": "m5", "title": "Eat healthy breakfast", "icon": "apple", "completed": False, "time": "7:45 AM"}
                ]), 0
            ),
            (
                alex_id, "Fresh & Clean Hygiene", "hygiene",
                json.dumps([
                    {"id": "h1", "title": "Wash hands with warm soap", "icon": "soap", "completed": True, "time": "Anytime"},
                    {"id": "h2", "title": "Brush teeth for 2 minutes", "icon": "toothbrush", "completed": False, "time": "Morning/Night"},
                    {"id": "h3", "title": "Comb or brush hair", "icon": "comb", "completed": False, "time": "Morning"}
                ]), 0
            ),
            (
                alex_id, "Ready for School", "school",
                json.dumps([
                    {"id": "s1", "title": "Pack school bag & water bottle", "icon": "backpack", "completed": False, "time": "8:00 AM"},
                    {"id": "s2", "title": "Put on shoes and jacket", "icon": "shoe", "completed": False, "time": "8:15 AM"},
                    {"id": "s3", "title": "Say hello to teacher & friends", "icon": "hand-wave", "completed": False, "time": "8:45 AM"}
                ]), 0
            ),
            (
                alex_id, "Peaceful Bedtime Routine", "bedtime",
                json.dumps([
                    {"id": "b1", "title": "Put toys away in toy box", "icon": "box", "completed": False, "time": "8:00 PM"},
                    {"id": "b2", "title": "Put on cozy pajamas", "icon": "moon", "completed": False, "time": "8:15 PM"},
                    {"id": "b3", "title": "Listen to a bedtime story", "icon": "book", "completed": False, "time": "8:30 PM"},
                    {"id": "b4", "title": "Three deep calming breaths", "icon": "wind", "completed": False, "time": "8:45 PM"}
                ]), 0
            )
        ]
        cursor.executemany("""
            INSERT INTO routines (student_id, title, category, steps_json, is_custom)
            VALUES (?, ?, ?, ?, ?);
        """, default_routines)

    # 5. Seed Videos
    cursor.execute("SELECT COUNT(*) FROM videos;")
    if cursor.fetchone()[0] == 0:
        videos = [
            (
                "Meeting Milo & Calming Deep Breaths", "calm",
                "Learn how robot Milo takes gentle deep breaths to feel relaxed and ready to learn.",
                "Self-Regulation", "easy",
                "milo-breathing.mp4", "milo-breathing-poster.svg",
                "milo-breathing.vtt", "milo-breathing-transcript.html",
                "2:15", 14
            ),
            (
                "The Phonics Melody: Letters A to Z", "phonics",
                "Sing along to letter sounds with clear lips and visual letter cards.",
                "Language Arts", "easy",
                "phonics-melody.mp4", "phonics-melody-poster.svg",
                "phonics-melody.vtt", "phonics-melody-transcript.html",
                "3:40", 22
            ),
            (
                "Counting Playful Stars 1 to 10", "math",
                "Count bright glowing stars one by one with cheerful visual rhythm.",
                "Mathematics", "easy",
                "counting-stars.mp4", "counting-stars-poster.svg",
                "counting-stars.vtt", "counting-stars-transcript.html",
                "2:50", 18
            ),
            (
                "Recognizing Feelings & Facial Cues", "social",
                "Explore happy, surprised, thinking, and calm expressions with friends.",
                "Social-Emotional", "moderate",
                "recognizing-feelings.mp4", "feelings-poster.svg",
                "feelings.vtt", "feelings-transcript.html",
                "3:15", 9
            ),
            (
                "Step-by-Step Handwashing Song", "independence",
                "A 20-second musical guide to bubbly, clean, germ-free hands.",
                "Life Skills", "easy",
                "handwashing-song.mp4", "handwashing-poster.svg",
                "handwashing.vtt", "handwashing-transcript.html",
                "2:00", 31
            )
        ]
        cursor.executemany("""
            INSERT INTO videos (title, category, description, subject, difficulty, video_file, poster_file, caption_file, transcript_file, duration, plays_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, videos)

    # 6. Seed Game Scores for Alex
    cursor.execute("SELECT COUNT(*) FROM game_scores WHERE student_id=?;", (alex_id,))
    if cursor.fetchone()[0] == 0:
        sample_scores = [
            (alex_id, "Color Matcher", "easy", 100, 3, 100.0),
            (alex_id, "Emotion Recognizer", "easy", 90, 3, 90.0),
            (alex_id, "Object Counter", "easy", 80, 2, 80.0)
        ]
        cursor.executemany("""
            INSERT INTO game_scores (student_id, game_name, difficulty, score, stars, accuracy)
            VALUES (?, ?, ?, ?, ?, ?);
        """, sample_scores)

    # 7. Seed Caregiver Auth
    cursor.execute("SELECT COUNT(*) FROM caregiver_auth;")
    if cursor.fetchone()[0] == 0:
        admin_pass = generate_password_hash("password123")
        cursor.execute("""
            INSERT INTO caregiver_auth (username, password_hash, pin)
            VALUES ('caregiver', ?, '1234');
        """, (admin_pass,))

if __name__ == "__main__":
    init_db()
    print("Database initialized and verified successfully.")
