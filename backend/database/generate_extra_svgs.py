import os
from pathlib import Path

ICONS_DIR = Path(r"d:\chall_2\frontend\assets\icons")
IMAGES_DIR = Path(r"d:\chall_2\frontend\assets\images")
ICONS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

EXTRA_SVGS = {
    # Emotion Faces
    ICONS_DIR / "happy-face.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="45" fill="#FFD54F" />
  <circle cx="36" cy="40" r="5" fill="#37474F" />
  <circle cx="64" cy="40" r="5" fill="#37474F" />
  <path d="M 32 55 Q 50 78 68 55" stroke="#37474F" stroke-width="5" stroke-linecap="round" fill="none" />
  <circle cx="28" cy="52" r="5" fill="#FF8A80" opacity="0.6" />
  <circle cx="72" cy="52" r="5" fill="#FF8A80" opacity="0.6" />
</svg>""",

    ICONS_DIR / "calm-face.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="45" fill="#81C784" />
  <!-- Gentle curved closed eyes -->
  <path d="M 28 42 Q 36 36 44 42" stroke="#1B5E20" stroke-width="4" stroke-linecap="round" fill="none" />
  <path d="M 56 42 Q 64 36 72 42" stroke="#1B5E20" stroke-width="4" stroke-linecap="round" fill="none" />
  <path d="M 38 60 Q 50 66 62 60" stroke="#1B5E20" stroke-width="4" stroke-linecap="round" fill="none" />
</svg>""",

    ICONS_DIR / "sad-face.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="45" fill="#90CAF9" />
  <circle cx="36" cy="42" r="5" fill="#1A237E" />
  <circle cx="64" cy="42" r="5" fill="#1A237E" />
  <path d="M 34 66 Q 50 50 66 66" stroke="#1A237E" stroke-width="4.5" stroke-linecap="round" fill="none" />
  <!-- Gentle tear drop -->
  <path d="M 72 48 C 72 44 75 40 75 40 C 75 40 78 44 78 48 C 78 50 75 52 75 52 C 75 52 72 50 72 48 Z" fill="#29B6F6" />
</svg>""",

    ICONS_DIR / "surprised-face.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="45" fill="#FFB74D" />
  <circle cx="35" cy="38" r="6" fill="#3E2723" />
  <circle cx="65" cy="38" r="6" fill="#3E2723" />
  <ellipse cx="50" cy="62" rx="10" ry="14" fill="#3E2723" />
</svg>""",

    ICONS_DIR / "angry-face.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="45" fill="#EF9A9A" />
  <!-- Slanted Eyebrows -->
  <line x1="28" y1="32" x2="44" y2="40" stroke="#B71C1C" stroke-width="4" stroke-linecap="round" />
  <line x1="72" y1="32" x2="56" y2="40" stroke="#B71C1C" stroke-width="4" stroke-linecap="round" />
  <circle cx="36" cy="44" r="5" fill="#B71C1C" />
  <circle cx="64" cy="44" r="5" fill="#B71C1C" />
  <path d="M 36 68 Q 50 56 64 68" stroke="#B71C1C" stroke-width="4" stroke-linecap="round" fill="none" />
</svg>""",

    # Shapes
    ICONS_DIR / "circle.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="42" fill="#42A5F5" stroke="#1E88E5" stroke-width="4" />
</svg>""",

    ICONS_DIR / "square.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect x="12" y="12" width="76" height="76" rx="8" fill="#66BB6A" stroke="#388E3C" stroke-width="4" />
</svg>""",

    ICONS_DIR / "triangle.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <polygon points="50,12 88,86 12,86" fill="#FFA726" stroke="#F57C00" stroke-width="4" stroke-linejoin="round" />
</svg>""",

    ICONS_DIR / "star.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <polygon points="50,10 62,36 90,38 68,58 75,86 50,71 25,86 32,58 10,38 38,36" fill="#FFD54F" stroke="#FFA000" stroke-width="3" stroke-linejoin="round" />
</svg>""",

    # Video Posters
    IMAGES_DIR / "milo-breathing-poster.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 225" width="400" height="225">
  <rect width="400" height="225" fill="#1E293B" />
  <circle cx="200" cy="110" r="55" fill="#2A9D8F" opacity="0.3" />
  <circle cx="200" cy="110" r="40" fill="#2A9D8F" opacity="0.6" />
  <circle cx="200" cy="110" r="28" fill="#48CAE4" />
  <text x="200" y="185" font-family="sans-serif" font-size="16" font-weight="bold" fill="#F8FAFC" text-anchor="middle">Calming Deep Breaths with Milo</text>
  <polygon points="194,100 212,110 194,120" fill="#FFFFFF" />
</svg>""",

    IMAGES_DIR / "phonics-melody-poster.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 225" width="400" height="225">
  <rect width="400" height="225" fill="#3A86C8" />
  <circle cx="200" cy="100" r="45" fill="#FFFFFF" opacity="0.2" />
  <text x="170" y="115" font-family="sans-serif" font-size="42" font-weight="bold" fill="#FFD166">A B C</text>
  <text x="200" y="185" font-family="sans-serif" font-size="16" font-weight="bold" fill="#FFFFFF" text-anchor="middle">The Phonics Melody Song</text>
  <polygon points="194,90 212,100 194,110" fill="#FFFFFF" />
</svg>""",

    IMAGES_DIR / "counting-stars-poster.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 225" width="400" height="225">
  <rect width="400" height="225" fill="#0F172A" />
  <polygon points="200,60 205,75 220,77 208,88 212,103 200,95 188,103 192,88 180,77 195,75" fill="#FFD166" />
  <text x="200" y="145" font-family="sans-serif" font-size="28" font-weight="bold" fill="#64DFDF" text-anchor="middle">1 2 3 4 5</text>
  <text x="200" y="185" font-family="sans-serif" font-size="16" font-weight="bold" fill="#F8FAFC" text-anchor="middle">Counting Playful Stars</text>
</svg>""",

    IMAGES_DIR / "feelings-poster.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 225" width="400" height="225">
  <rect width="400" height="225" fill="#7B1FA2" />
  <circle cx="160" cy="100" r="28" fill="#FFD54F" />
  <circle cx="240" cy="100" r="28" fill="#81C784" />
  <text x="200" y="185" font-family="sans-serif" font-size="16" font-weight="bold" fill="#FFFFFF" text-anchor="middle">Recognizing Feelings with Friends</text>
</svg>""",

    IMAGES_DIR / "handwashing-poster.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 225" width="400" height="225">
  <rect width="400" height="225" fill="#0288D1" />
  <circle cx="200" cy="95" r="38" fill="#80DEEA" opacity="0.4" />
  <text x="200" y="105" font-family="sans-serif" font-size="32" fill="#FFFFFF" text-anchor="middle">🧼 ✨</text>
  <text x="200" y="185" font-family="sans-serif" font-size="16" font-weight="bold" fill="#FFFFFF" text-anchor="middle">Step-by-Step Handwashing Song</text>
</svg>"""
}

for path, content in EXTRA_SVGS.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(EXTRA_SVGS)} extra icons and video posters.")
