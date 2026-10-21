-- MindVerse — Inclusive Learning Lab Database Schema
-- Optimized for SQLite 3 with Foreign Keys & WAL support

PRAGMA foreign_keys = ON;

-- 1. Students / Learners Profile Table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    avatar TEXT DEFAULT 'robot-milo',
    learning_level INTEGER DEFAULT 1 CHECK(learning_level BETWEEN 1 AND 6),
    preferred_theme TEXT DEFAULT 'default' CHECK(preferred_theme IN ('default', 'high-contrast-dark', 'high-contrast-light', 'pastel-calming')),
    font_size TEXT DEFAULT 'standard' CHECK(font_size IN ('standard', 'large', 'xlarge')),
    voice_enabled INTEGER DEFAULT 1 CHECK(voice_enabled IN (0, 1)),
    sound_enabled INTEGER DEFAULT 1 CHECK(sound_enabled IN (0, 1)),
    reduced_motion INTEGER DEFAULT 0 CHECK(reduced_motion IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Structured Curriculum Lessons Table
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level INTEGER NOT NULL CHECK(level BETWEEN 1 AND 6),
    subject TEXT NOT NULL,
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT,
    concept TEXT,
    icon TEXT,
    difficulty TEXT DEFAULT 'gentle',
    steps_json TEXT NOT NULL,
    interactive_type TEXT NOT NULL,
    is_active INTEGER DEFAULT 1 CHECK(is_active IN (0, 1))
);

-- 3. Student Progress & Mastery Tracking Table
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    lesson_id INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'in_progress' CHECK(status IN ('not_started', 'in_progress', 'completed')),
    score INTEGER DEFAULT 0,
    hints_used INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 1,
    stars INTEGER DEFAULT 0 CHECK(stars BETWEEN 0 AND 3),
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, lesson_id)
);

-- 4. Educational Game Scores Table
CREATE TABLE IF NOT EXISTS game_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    game_name TEXT NOT NULL,
    difficulty TEXT DEFAULT 'easy',
    score INTEGER DEFAULT 0,
    stars INTEGER DEFAULT 0 CHECK(stars BETWEEN 0 AND 3),
    accuracy REAL DEFAULT 100.0,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Visual Daily Routines & Checklists Table
CREATE TABLE IF NOT EXISTS routines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('morning', 'hygiene', 'school', 'bedtime', 'custom')),
    steps_json TEXT NOT NULL,
    is_custom INTEGER DEFAULT 0 CHECK(is_custom IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Accessible Educational Videos Library Table
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    subject TEXT,
    difficulty TEXT DEFAULT 'easy',
    video_file TEXT,
    poster_file TEXT,
    caption_file TEXT,
    transcript_file TEXT,
    duration TEXT DEFAULT '2:30',
    plays_count INTEGER DEFAULT 0
);

-- 7. Learner Activity Audit Logs Table
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES students(id) ON DELETE SET NULL,
    activity_type TEXT NOT NULL,
    details_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Caregiver / Teacher Authentication Table
CREATE TABLE IF NOT EXISTS caregiver_auth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    pin TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_lessons_level ON lessons(level);
CREATE INDEX IF NOT EXISTS idx_lessons_slug ON lessons(slug);
CREATE INDEX IF NOT EXISTS idx_progress_student ON progress(student_id);
CREATE INDEX IF NOT EXISTS idx_progress_lesson ON progress(lesson_id);
CREATE INDEX IF NOT EXISTS idx_game_scores_student ON game_scores(student_id);
CREATE INDEX IF NOT EXISTS idx_routines_student ON routines(student_id);
CREATE INDEX IF NOT EXISTS idx_routines_category ON routines(category);
CREATE INDEX IF NOT EXISTS idx_videos_category ON videos(category);
CREATE INDEX IF NOT EXISTS idx_activity_logs_student ON activity_logs(student_id);
