# 🌟 MindVerse — Inclusive Learning Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.x](https://img.shields.io/badge/Flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![WCAG 2.2 AA Aligned](https://img.shields.io/badge/WCAG-2.2%20AA-purple.svg)](https://www.w3.org/WAI/standards-guidelines/wcag/)

> **MindVerse — Inclusive Learning Lab** is a calm, predictable, accessible, and interactive educational platform engineered specifically for children who benefit from additional learning support, including learners with **autism spectrum disorder (ASD)**, **ADHD**, **Down syndrome**, **dyslexia**, and **sensory processing differences**.

Rather than displaying passive flashcards, MindVerse actively teaches through **tactile visual demonstrations**, **errorless learning cues**, **gentle Web Audio chimes**, **Milo the digital teaching companion**, and **structured progress tracking**.

---

## 📑 Table of Contents
1. [Problem Statement & Educational Approach](#-problem-statement--educational-approach)
2. [Target Learners & Neurodivergent UX Principles](#-target-learners--neurodivergent-ux-principles)
3. [Key Features Overview](#-key-features-overview)
4. [System Architecture](#-system-architecture)
5. [Repository Structure](#-repository-structure)
6. [Technology Stack](#-technology-stack)
7. [Local Quick Start (Windows PowerShell & VS Code)](#-local-quick-start-windows-powershell--vs-code)
8. [Environment Variables](#-environment-variables)
9. [REST API Documentation](#-rest-api-documentation)
10. [Automated Testing Suite](#-automated-testing-suite)
11. [Independent Cloud Deployment Guide](#-independent-cloud-deployment-guide)
12. [Troubleshooting & Limitations](#-troubleshooting--limitations)

---

## 🎯 Problem Statement & Educational Approach

Traditional educational software frequently overwhelms neurodivergent children with:
- Flashing confetti, high-frequency loud noises, and ticking timer countdowns that trigger sensory overload.
- Punitive red "X" marks and buzzer sounds that induce anxiety and learned helplessness.
- Rigid progression locks that force learners into activities based on chronological age rather than developmental readiness.
- Dense walls of text without multi-sensory or visual demonstration fallbacks.

### The MindVerse Solution
MindVerse applies **Universal Design for Learning (UDL)** and **Errorless Learning** methodology:
- **Demonstration First**: Learners see the concept modeled visually before being invited to try.
- **Supportive Hints**: If a learner is unsure, gentle visual hints appear without judgment.
- **Predictable Routine**: Calm, consistent layouts with Milo docked reliably in the bottom-right.
- **Sensory Safe**: Volume-limited Web Audio envelopes, no autoplaying surprise audio, and zero flashing animations.
- **Flexible Mastery**: Caregivers and teachers can configure levels freely (Levels 1 to 6).

---

## 🧩 Target Learners & Neurodivergent UX Principles

| Learner Profile | Tailored Feature in MindVerse |
| :--- | :--- |
| **Autism Spectrum Disorder (ASD)** | Predictable layouts, pictorial visual schedules, emotion cue explanations, calm colors. |
| **ADHD** | Bite-sized single-task steps, no distracting background clutter, immediate positive reinforcement. |
| **Dyslexia** | One-click Dyslexia-friendly font toggle, extra letter spacing, dual text + audio pronunciations. |
| **Sensory Processing Differences** | 4 visual themes (including High Contrast Dark & Pastel Calming), Reduce Motion toggle, volume control. |
| **Fine Motor Challenges** | Large 48px+ touch targets, single-click alternatives for double-clicking, keyboard equivalents for drag-and-drop. |

---

## 🚀 Key Features Overview

### 1. 🤖 Milo — Digital Teaching Companion
- Interactive SVG robot docked in the bottom-right corner.
- 4 emotional states: `idle` (gentle breathing), `speaking` (mouth flutter + antenna glow), `celebrating` (star shimmer), `encouraging` (warm smile).
- Native Web Speech API integration (~0.85 rate, warm pitch) with visual speech bubble, "Hear again" button, and minimize option.

### 2. 🔤 Alphabet & Phonics Wall (`/pages/alphabet.html`)
- Complete A to Z interactive learning wall.
- Each card features uppercase/lowercase letters, phonetic sound cues (e.g. `/æ/`), simple words, and original SVG illustrations.
- Interactive audio pronunciation and errorless recognition challenge.

### 3. 📚 Structured 6-Level Curriculum (`/pages/lessons.html` & `/pages/lesson-detail.html`)
- **Level 1**: Discovering the World (Colors, Shapes, Everyday Objects)
- **Level 2**: Foundational Phonics and Counting (Sounds, Quantities 1-5)
- **Level 3**: Early Academic Skills and Emotions (Feelings, Word Families)
- **Level 4**: Primary Skills and Problem Solving (Sequencing, Visual Math)
- **Level 5**: Middle Skills and Logic (Pattern Detective, Categorization)
- **Level 6**: Everyday Independence (Step-by-Step Handwashing, Communication)
- Real validation, hints, attempt tracking, and 3-star scoring saved to SQLite.

### 4. 🎮 Educational Games Hub (`/pages/games.html`)
- **Color Matcher**: Match colors using large cards with text labels and patterns.
- **Emotion Recognizer**: Identify smiling, calm, surprised, and sad faces with empathetic context.
- **Object Counter**: One-to-one counting of apples, stars, and fish.
- **Picture–Word Pairing**: Sight-word and picture association.

### 5. 🖱️ Computer & Motor Skills (`/pages/computer-skills.html`)
- **Gentle Path Navigator**: Wide, forgiving celestial cursor tracking.
- **Calm Bubble Pop**: Hover or tap floating musical bubbles.
- **Friendly Target Practice**: Unpressured targeting of clear bullseyes.
- **Treasure Chest Unlock**: Double-click practice with accessible single-click helper.
- **Shape Sorting Box**: Drag-and-drop sorting with keyboard (1-3) and tap buttons.

### 6. 📅 Visual Daily Routine (`/pages/daily-routine.html`)
- Pictorial schedules for **Morning**, **Hygiene**, **School**, and **Bedtime**.
- Interactive checkboxes, step audio reader, progress bar, and custom task creator.

### 7. 🎬 Accessible Video Library (`/pages/videos.html`)
- Local demonstration visualizer (no broken external links).
- Synchronized WebVTT captions, interactive clickable transcripts, 0.5x/0.75x/1.0x speed control, and Normal/Dim/Warm contrast filters.

### 8. 🛡️ Caregiver & Teacher Portal (`/pages/caregiver.html`)
- Student profile creation and level configuration.
- Real-time statistics from SQLite (stars, hints used, attempts, completion rates).
- Activity audit timeline and progress reset with confirmation safety.

---

## 🏛️ System Architecture

```
                                  [ Browser Client ]
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
          [ Static Frontend ]                            [ Flask REST API ]
       Vanilla HTML5 / CSS3 / ES6                       Python 3.10+ / Gunicorn
                    │                                             │
      ┌─────────────┼─────────────┐                  ┌────────────┼────────────┐
      ▼             ▼             ▼                  ▼            ▼            ▼
[ ThreeWorld /  [ SoundEngine  [ Milo Companion   [ Blueprints ] [ Services ] [ SQLite DB ]
  2D Fallback ]   Web Audio ]    Web Speech ]     - api_bp       - lesson     (WAL Mode)
                                                  - lessons_bp   - progress   - students
                                                  - games_bp     - routine    - lessons
                                                  - routines_bp               - progress
                                                  - videos_bp                 - game_scores
                                                  - computer_bp               - routines
```

---

## 📂 Repository Structure

```
d:/chall_2/
├── frontend/
│   ├── index.html                  # Landing page
│   ├── pages/
│   │   ├── dashboard.html          # Learner dashboard
│   │   ├── alphabet.html           # A-Z Phonics wall
│   │   ├── lessons.html            # Curriculum level catalog
│   │   ├── lesson-detail.html      # Interactive lesson player
│   │   ├── videos.html             # Video player & transcripts
│   │   ├── games.html              # Educational mini-games
│   │   ├── computer-skills.html    # Motor skills practice
│   │   ├── daily-routine.html      # Visual daily schedule
│   │   └── caregiver.html          # Educator/Caregiver portal
│   ├── assets/
│   │   ├── icons/                  # MindVerse logo, emotion icons, shapes
│   │   └── images/                 # Milo SVG mascot, 26 alphabet SVGs, video posters
│   ├── css/
│   │   ├── main.css                # Design tokens & layouts
│   │   ├── accessibility.css       # Themes, fonts & sensory filters
│   │   ├── animations.css          # Motion controls & gentle transitions
│   │   ├── games.css               # Game boards & choices
│   │   ├── video-player.css        # Video UI & transcripts
│   │   └── responsive.css          # Mobile breakpoints & Milo dock
│   ├── js/
│   │   ├── api.js                  # Centralized REST client with offline fallback
│   │   ├── main.js                 # Global application bootstrap
│   │   ├── accessibility.js        # Persistent toolbar controller
│   │   ├── sound-engine.js         # Procedural Web Audio synthesizer
│   │   ├── character.js            # Milo companion & speech synthesis
│   │   ├── three-world.js          # Safe WebGL 3D background
│   │   ├── three-fallback.js       # 2D canvas background fallback
│   │   ├── learning-games.js       # 4 Educational mini-games
│   │   ├── computer-skills.js      # 5 Motor skills activities
│   │   └── daily-routine.js        # Schedule checklist engine
│   ├── package.json
│   └── README.md
├── backend/
│   ├── app.py                      # Flask factory & CORS configuration
│   ├── config.py                   # Config profiles & DB resolution
│   ├── requirements.txt            # Python dependencies
│   ├── wsgi.py                     # Production entrypoint
│   ├── conftest.py                 # Pytest path configuration
│   ├── database/
│   │   ├── schema.sql              # SQLite DDL with FK constraints
│   │   └── init_db.py              # Auto-initialization & idempotent seeding
│   ├── blueprints/
│   │   ├── api.py                  # Students, prefs, health, caregiver auth
│   │   ├── lessons.py              # Lessons & progress recording
│   │   ├── videos.py               # Video metadata & tracking
│   │   ├── games.py                # Mini-games & scores
│   │   ├── computer_skills.py      # Motor skills logging
│   │   ├── daily_routine.py        # Routine CRUD & toggles
│   │   └── pages.py                # Combined mode landing
│   ├── services/
│   │   ├── lesson_service.py       # Lesson querying & step formatting
│   │   ├── progress_service.py     # Aggregated stats & progress calculation
│   │   └── routine_service.py      # Routine checklist persistence
│   └── tests/
│       ├── test_database.py        # Schema & idempotency tests
│       ├── test_api.py             # Endpoint & CORS tests
│       └── test_learning_flow.py   # End-to-end integration test
├── deployment/
│   ├── render.yaml                 # Render backend deployment blueprint
│   ├── netlify.toml                # Netlify frontend deployment config
│   └── nginx.conf                  # Production reverse proxy config
├── .env.example                    # Environment variable template
├── .gitignore                      # Git exclusion rules
├── README.md                       # Master project documentation
└── LICENSE                         # MIT License
```

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, ES6+ JavaScript (Vanilla, no framework bloat).
- **Audio Synthesis**: Web Audio API (Sine/Triangle oscillators, ADSR envelopes).
- **Speech**: Web Speech API (`SpeechSynthesisUtterance` at 0.85 rate).
- **3D / 2D Canvas**: Three.js r128 with automatic 2D Canvas fallback (`three-fallback.js`).
- **Backend**: Python 3.10+, Flask 3.1+, Flask-CORS, Werkzeug.
- **Database**: SQLite 3 with Foreign Keys, WAL Journaling, and 5000ms busy timeout.
- **Testing**: Pytest 9.x.
- **Production Server**: Gunicorn WSGI.

---

## 💻 Local Quick Start (Windows PowerShell & VS Code)

### Prerequisites
- Python 3.10 or newer (`python --version`)
- Visual Studio Code or any modern web browser

### 1. Start the Flask Backend Server
Open a Windows PowerShell terminal in the repository root:

```powershell
# Navigate into backend directory
cd backend

# Create virtual environment (optional if Python packages already installed)
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Start the Flask API server
python app.py
```
> The backend will initialize the SQLite database automatically and serve at **http://127.0.0.1:5000**.
> Verify health by opening [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health).

### 2. Start the Static Frontend Server
Open a second Windows PowerShell terminal:

```powershell
# Navigate into frontend directory
cd frontend

# Start lightweight static development server
python -m http.server 3000
```
> Open your browser to **http://localhost:3000** to explore MindVerse!
> (Alternatively, right-click `frontend/index.html` in VS Code and select **Open with Live Server**).

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` if custom overrides are needed:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `FLASK_ENV` | `development` | Environment mode (`development`, `production`, `testing`). |
| `SECRET_KEY` | `mindverse-dev-...` | Session secret key (Set to a secure 32+ char secret in production). |
| `DATABASE` | `database/mindverse.db` | Path to SQLite database file. |
| `PORT` | `5000` | Port for Flask backend server. |
| `FRONTEND_ORIGIN` | `http://localhost:3000,...` | Allowed CORS origins for browser security. |
| `CAREGIVER_DEFAULT_PIN` | `1234` | Default PIN for demo caregiver access. |

---

## 📡 REST API Documentation

### Application Health
- `GET /api/health`: Returns service health status and database connectivity.

### Students & Preferences
- `GET /api/students`: List all learners.
- `POST /api/students`: Create a new learner profile.
- `GET /api/students/<id>`: Retrieve single learner details.
- `PATCH /api/students/<id>`: Update learner level, avatar, or settings.
- `GET /api/preferences/<student_id>`: Get accessibility preferences.
- `PUT /api/preferences/<student_id>`: Save accessibility preferences (theme, font, motion).

### Lessons & Progress
- `GET /api/lessons`: Retrieve all curriculum lessons (`?level=1..6`, `?subject=...`).
- `GET /api/lessons/<slug>`: Retrieve step-by-step lesson details by slug.
- `GET /api/progress/<student_id>`: Retrieve all progress records for a student.
- `POST /api/progress`: Record lesson step completion, hints used, attempts, and stars.

### Games & Motor Skills
- `GET /api/games`: List educational games catalog and scoring criteria.
- `POST /api/game-scores`: Record completed game score, stars (1-3), and accuracy.
- `GET /api/computer-skills/activities`: List accessible motor skills activities.
- `POST /api/computer-skills/progress`: Log fine-motor activity completion.

### Daily Routines
- `GET /api/routines/<student_id>`: Get all pictorial schedules for a student.
- `POST /api/routines`: Create a new custom routine schedule.
- `PATCH /api/routines/<routine_id>`: Update routine steps or task completion checkboxes.
- `DELETE /api/routines/<routine_id>`: Delete a custom routine.

### Videos & Caregiver Tools
- `GET /api/videos`: List all accessible educational videos.
- `GET /api/videos/<id>`: Get video detail with transcript and captions.
- `POST /api/videos/<id>/play`: Increment video view counter.
- `GET /api/caregiver/stats/<student_id>`: Get aggregated learning statistics.
- `POST /api/caregiver/reset/<student_id>`: Reset student progress (`{"confirm": true}`).
- `POST /api/caregiver/login`: Verify caregiver PIN (`1234`) or password.

---

## 🧪 Automated Testing Suite

MindVerse includes an extensive automated test suite covering database schema creation, seed idempotency, foreign key enforcement, all API endpoints, and end-to-end learning flows.

To run the tests from the project root:

```powershell
python -m pytest backend/tests -v
```

### Actual Test Execution Output:
```
backend/tests/test_api.py::test_health_check PASSED                      [  7%]
backend/tests/test_api.py::test_students_api PASSED                      [ 15%]
backend/tests/test_api.py::test_preferences_api PASSED                   [ 23%]
backend/tests/test_api.py::test_lessons_api PASSED                       [ 30%]
backend/tests/test_api.py::test_progress_api PASSED                      [ 38%]
backend/tests/test_api.py::test_games_api PASSED                         [ 46%]
backend/tests/test_api.py::test_daily_routine_api PASSED                 [ 53%]
backend/tests/test_api.py::test_video_api PASSED                         [ 61%]
backend/tests/test_api.py::test_caregiver_api_and_reset PASSED           [ 69%]
backend/tests/test_database.py::test_init_db_creates_tables PASSED       [ 76%]
backend/tests/test_database.py::test_init_db_idempotency PASSED          [ 84%]
backend/tests/test_database.py::test_foreign_key_enforcement PASSED      [ 92%]
backend/tests/test_learning_flow.py::test_complete_inclusive_learning_journey PASSED [100%]

============================= 13 passed in 4.67s ==============================
```

---

## ☁️ Independent Cloud Deployment Guide

The frontend and backend are completely decoupled and independently deployable.

### 1. Deploy the Backend to Render
1. Create a new Web Service on [Render](https://render.com).
2. Connect your GitHub repository (`https://github.com/tejasm103/chall_2.git`).
3. Set **Root Directory** to `backend`.
4. Set **Build Command** to: `pip install -r requirements.txt`.
5. Set **Start Command** to: `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 4`.
6. Add Environment Variables:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: `(generate secure random 32+ string)`
   - `DATABASE`: `/var/data/mindverse.db`
   - `FRONTEND_ORIGIN`: `https://your-frontend-site.netlify.app`
7. In the **Disks** section, attach a 1 GB persistent disk mounted at `/var/data` to ensure the SQLite database persists across redeployments.

### 2. Deploy the Static Frontend to Netlify
1. Connect your repository to [Netlify](https://netlify.com).
2. Set **Publish directory** to `frontend`.
3. Set **Build command** to empty (None required for vanilla static files).
4. Configure your backend API URL by either:
   - Setting the redirect in `deployment/netlify.toml` to point `/api/*` to your Render backend URL.
   - Or injecting `window.MINDVERSE_API_URL = "https://your-backend.onrender.com/api";` into `frontend/index.html`.

---

## 🔍 Troubleshooting & Limitations

- **Browser Audio Gestures**: In modern browsers (Chrome, Edge, Safari), audio playback is paused until the user interacts with the page (click or tap). MindVerse automatically unlocks audio upon the first user gesture.
- **WebGL Fallback**: If running on low-power devices, virtual machines, or browsers with disabled WebGL, MindVerse seamlessly falls back to the HTML5 2D canvas (`three-fallback.js`) without error.
- **Ephemeral Storage on Free Cloud Tiers**: Free hosting tiers (like standard free Render or Heroku) use ephemeral file systems. In production, attach a persistent storage disk or configure a hosted database URL so student records persist across restarts.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
