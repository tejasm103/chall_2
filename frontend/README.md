# MindVerse Frontend — Inclusive Learning Lab

This directory houses the static, framework-free frontend application for **MindVerse — Inclusive Learning Lab**.

## Architecture & Technology
- **Pure Web Standards**: HTML5, CSS3, Vanilla ES6+ JavaScript.
- **Zero Framework Bloat**: No React, Vue, Angular, Vite, Webpack, or Tailwind required.
- **Centralized API**: Uses `js/api.js` to connect to the Flask REST backend (`/api` or configured base URL).
- **Graceful Fallbacks**: Fully operational even if the backend is temporarily offline, providing cached data and smooth feedback without crashing.
- **Sensory & Accessibility First**:
  - 4 visual themes: Default Daylight, Pastel Calming, High Contrast Dark, High Contrast Light.
  - 3 typography scale levels (16px, 18px, 22px).
  - Dyslexia-friendly letter and word spacing.
  - Reduced-motion support respecting both OS setting and user toggle.
  - Procedural Web Audio API sound synthesizer with sensory-safe volume ceiling.
  - Native Web Speech API voice companion (Milo) with text transcripts and "Hear again" button.

## Directory Structure
```
frontend/
├── index.html                   # Interactive landing page & quick start
├── pages/
│   ├── dashboard.html           # Student dashboard & level progression
│   ├── alphabet.html            # Tactile A to Z phonics wall
│   ├── lessons.html             # Structured 6-level curriculum catalog
│   ├── lesson-detail.html       # Interactive lesson player with errorless hints
│   ├── videos.html              # Accessible video player with transcripts & captions
│   ├── games.html               # 4 Educational mini-games (Color, Emotion, Counting, Words)
│   ├── computer-skills.html     # 5 Motor skills activities (Path, Bubbles, Targets, Chest, Sorting)
│   ├── daily-routine.html       # Visual pictorial schedules & checklist manager
│   └── caregiver.html           # Caregiver dashboard, metrics & profile settings
├── assets/
│   ├── icons/                   # MindVerse SVG logo, shapes, emotion icons
│   └── images/                  # Milo SVG companion, 26 alphabet illustrations, video posters
├── css/
│   ├── main.css                 # Core design tokens, layouts, buttons, header/footer
│   ├── accessibility.css        # Themes, typography scaling, video filters, captions
│   ├── animations.css           # Gentle transitions and sensory motion controls
│   ├── games.css                # Mini-game boards and interactive cards
│   ├── video-player.css         # Custom player styling & interactive transcript box
│   └── responsive.css           # Mobile, tablet, desktop breakpoints and Milo docking
├── js/
│   ├── api.js                   # Centralized REST API client with offline fallback
│   ├── sound-engine.js          # Procedural Web Audio API synthesizer
│   ├── character.js             # Milo digital companion controller & speech synthesis
│   ├── three-world.js           # Safe Three.js 3D background with WebGL context recovery
│   ├── three-fallback.js        # 2D canvas background fallback
│   ├── accessibility.js         # Persistent accessibility toolbar & preferences
│   ├── learning-games.js        # Game logic for all 4 mini-games
│   ├── computer-skills.js       # Motor skills activity logic
│   ├── daily-routine.js         # Routine checklist & custom task manager
│   └── main.js                  # Global application bootstrapping
├── package.json                 # Static development server helper script
└── README.md                    # Frontend documentation
```

## Running Locally

### Option A: Using Python built-in HTTP server (No Node.js needed!)
From the `frontend` folder:
```powershell
python -m http.server 3000
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### Option B: Using VS Code Live Server
Right-click `frontend/index.html` and select **Open with Live Server**.

### Option C: Using Node.js npx serve
```powershell
npx -y serve -l 3000 .
```

## API Configuration for Production
In production, point the frontend to your deployed Flask backend by either:
1. Setting `window.MINDVERSE_API_URL = "https://your-backend.onrender.com/api";` in a script tag or environment configuration.
2. Saving the base URL in the browser's localStorage:
   ```javascript
   localStorage.setItem('mindverse_api_url', 'https://your-backend.onrender.com/api');
   ```
If running on the same domain or behind an Nginx reverse proxy, the default `/api` relative URL path works out of the box!
