import os
from pathlib import Path

OUT_DIR = Path(r"d:\chall_2\frontend\assets\images\alphabet")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SVG_DEFS = {
    "apple": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <path d="M 50 25 C 48 15 54 8 62 6 C 60 14 54 22 50 25 Z" fill="#4CAF50" />
  <path d="M 50 24 Q 52 14 58 10" stroke="#795548" stroke-width="3" stroke-linecap="round" fill="none" />
  <path d="M 50 30 C 35 25 15 35 15 60 C 15 82 35 95 50 92 C 65 95 85 82 85 60 C 85 35 65 25 50 30 Z" fill="#E53935" />
  <path d="M 30 40 Q 25 50 30 65" stroke="#FFCDD2" stroke-width="4" stroke-linecap="round" fill="none" opacity="0.6" />
</svg>""",

    "ball": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle cx="50" cy="50" r="42" fill="#1E88E5" />
  <path d="M 12 50 A 42 42 0 0 1 88 50" fill="#E53935" />
  <rect x="8" y="44" width="84" height="12" rx="4" fill="#FDD835" />
  <circle cx="50" cy="50" r="10" fill="#FFFFFF" />
  <path d="M 30 25 A 35 35 0 0 1 70 25" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.5" />
</svg>""",

    "cat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Ears -->
  <polygon points="25,45 35,15 50,35" fill="#FB8C00" />
  <polygon points="30,40 37,22 47,35" fill="#FFCC80" />
  <polygon points="75,45 65,15 50,35" fill="#FB8C00" />
  <polygon points="70,40 63,22 53,35" fill="#FFCC80" />
  <!-- Head -->
  <ellipse cx="50" cy="55" rx="35" ry="30" fill="#FFA726" />
  <!-- Eyes -->
  <circle cx="38" cy="50" r="5" fill="#2E7D32" />
  <circle cx="62" cy="50" r="5" fill="#2E7D32" />
  <circle cx="39" cy="48" r="1.5" fill="#FFFFFF" />
  <circle cx="63" cy="48" r="1.5" fill="#FFFFFF" />
  <!-- Nose & Mouth -->
  <polygon points="47,60 53,60 50,64" fill="#D81B60" />
  <path d="M 45 66 Q 50 70 50 64 Q 50 70 55 66" stroke="#5D4037" stroke-width="2" stroke-linecap="round" fill="none" />
  <!-- Whiskers -->
  <line x1="20" y1="56" x2="32" y2="58" stroke="#5D4037" stroke-width="1.8" stroke-linecap="round" />
  <line x1="18" y1="64" x2="32" y2="62" stroke="#5D4037" stroke-width="1.8" stroke-linecap="round" />
  <line x1="80" y1="56" x2="68" y2="58" stroke="#5D4037" stroke-width="1.8" stroke-linecap="round" />
  <line x1="82" y1="64" x2="68" y2="62" stroke="#5D4037" stroke-width="1.8" stroke-linecap="round" />
</svg>""",

    "duck": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Body -->
  <path d="M 25 55 C 15 55 10 70 25 80 C 45 92 75 90 85 75 C 90 65 75 55 60 55 Z" fill="#FDD835" />
  <!-- Wing -->
  <path d="M 35 62 Q 55 60 65 72 Q 45 80 35 62 Z" fill="#FBC02D" />
  <!-- Head -->
  <circle cx="68" cy="40" r="18" fill="#FDD835" />
  <!-- Eye -->
  <circle cx="72" cy="36" r="3" fill="#212121" />
  <circle cx="73" cy="35" r="1" fill="#FFFFFF" />
  <!-- Beak -->
  <path d="M 82 38 Q 96 42 82 48 Z" fill="#FB8C00" />
  <!-- Water Waves -->
  <path d="M 10 88 Q 25 82 40 88 Q 55 94 70 88 Q 85 82 95 88" stroke="#42A5F5" stroke-width="3" stroke-linecap="round" fill="none" />
</svg>""",

    "elephant": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Body -->
  <ellipse cx="45" cy="58" rx="30" ry="24" fill="#90A4AE" />
  <!-- Legs -->
  <rect x="25" y="70" width="10" height="20" rx="3" fill="#78909C" />
  <rect x="42" y="70" width="10" height="20" rx="3" fill="#78909C" />
  <!-- Head & Trunk -->
  <circle cx="70" cy="45" r="16" fill="#90A4AE" />
  <path d="M 80 48 Q 92 56 86 70 Q 82 78 78 72 Q 82 62 76 56" fill="#90A4AE" />
  <!-- Eye -->
  <circle cx="72" cy="40" r="2.5" fill="#263238" />
  <!-- Large Ear -->
  <ellipse cx="60" cy="46" rx="12" ry="16" fill="#B0BEC5" stroke="#78909C" stroke-width="2" />
  <path d="M 76 56 Q 84 56 82 60" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" fill="none" />
</svg>""",

    "fish": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Tail Fin -->
  <polygon points="15,25 35,50 15,75" fill="#FF7043" />
  <!-- Body -->
  <ellipse cx="55" cy="50" rx="32" ry="22" fill="#FFA726" />
  <!-- Stripes -->
  <path d="M 50 30 Q 56 50 50 70" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none" />
  <path d="M 64 32 Q 68 50 64 68" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none" />
  <!-- Eye -->
  <circle cx="74" cy="44" r="4" fill="#212121" />
  <circle cx="75" cy="43" r="1.5" fill="#FFFFFF" />
  <!-- Fin -->
  <polygon points="45,46 56,50 48,58" fill="#FF7043" />
</svg>""",

    "giraffe": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Neck & Body -->
  <path d="M 30 75 Q 40 70 55 75 L 55 90 L 45 90 L 45 80 L 35 90 L 25 90 Z" fill="#FDD835" />
  <path d="M 46 72 L 56 25 L 68 25 L 58 72 Z" fill="#FDD835" />
  <!-- Spots -->
  <circle cx="54" cy="45" r="4" fill="#D87A16" />
  <circle cx="58" cy="60" r="5" fill="#D87A16" />
  <circle cx="42" cy="76" r="4" fill="#D87A16" />
  <!-- Head -->
  <ellipse cx="68" cy="22" rx="10" ry="7" fill="#FDD835" />
  <!-- Horns -->
  <line x1="64" y1="16" x2="63" y2="10" stroke="#795548" stroke-width="2" />
  <circle cx="63" cy="9" r="2" fill="#795548" />
  <line x1="68" y1="16" x2="69" y2="10" stroke="#795548" stroke-width="2" />
  <circle cx="69" cy="9" r="2" fill="#795548" />
  <!-- Eye -->
  <circle cx="70" cy="20" r="2" fill="#3E2723" />
</svg>""",

    "house": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Roof -->
  <polygon points="50,15 15,45 85,45" fill="#E53935" />
  <rect x="68" y="20" width="8" height="16" fill="#B71C1C" />
  <!-- Walls -->
  <rect x="22" y="45" width="56" height="45" rx="3" fill="#FFF9C4" stroke="#FBC02D" stroke-width="2" />
  <!-- Door -->
  <rect x="42" y="60" width="16" height="30" rx="3" fill="#795548" />
  <circle cx="46" cy="76" r="2" fill="#FFD54F" />
  <!-- Window -->
  <rect x="28" y="52" width="12" height="12" rx="2" fill="#81D4FA" stroke="#0288D1" stroke-width="1.5" />
  <rect x="60" y="52" width="12" height="12" rx="2" fill="#81D4FA" stroke="#0288D1" stroke-width="1.5" />
</svg>""",

    "igloo": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Dome -->
  <path d="M 15 80 A 35 35 0 0 1 85 80 Z" fill="#E0F7FA" stroke="#80DEEA" stroke-width="3" />
  <!-- Blocks -->
  <path d="M 22 65 Q 50 60 78 65" stroke="#B2EBF2" stroke-width="2" fill="none" />
  <path d="M 32 50 Q 50 46 68 50" stroke="#B2EBF2" stroke-width="2" fill="none" />
  <!-- Entrance -->
  <path d="M 40 80 A 15 15 0 0 1 60 80 Z" fill="#006064" />
  <ellipse cx="50" cy="80" rx="10" ry="14" fill="#00838F" />
  <ellipse cx="50" cy="80" rx="7" ry="10" fill="#004D40" />
</svg>""",

    "jellyfish": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Dome Body -->
  <path d="M 20 48 C 20 22 80 22 80 48 Q 50 56 20 48 Z" fill="#BA68C8" />
  <!-- Cute Eyes -->
  <circle cx="40" cy="40" r="3" fill="#FFFFFF" />
  <circle cx="41" cy="40" r="1.5" fill="#4A148C" />
  <circle cx="60" cy="40" r="3" fill="#FFFFFF" />
  <circle cx="61" cy="40" r="1.5" fill="#4A148C" />
  <path d="M 47 45 Q 50 48 53 45" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" fill="none" />
  <!-- Tentacles -->
  <path d="M 30 52 Q 25 68 32 85" stroke="#CE93D8" stroke-width="3" stroke-linecap="round" fill="none" />
  <path d="M 42 52 Q 48 70 40 88" stroke="#BA68C8" stroke-width="3" stroke-linecap="round" fill="none" />
  <path d="M 58 52 Q 52 70 60 88" stroke="#BA68C8" stroke-width="3" stroke-linecap="round" fill="none" />
  <path d="M 70 52 Q 75 68 68 85" stroke="#CE93D8" stroke-width="3" stroke-linecap="round" fill="none" />
</svg>""",

    "kite": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Diamond -->
  <polygon points="50,10 80,45 50,75 20,45" fill="#FF4081" />
  <polygon points="50,10 50,75 20,45" fill="#7C4DFF" />
  <!-- Cross Struts -->
  <line x1="50" y1="10" x2="50" y2="75" stroke="#FFFFFF" stroke-width="2" />
  <line x1="20" y1="45" x2="80" y2="45" stroke="#FFFFFF" stroke-width="2" />
  <!-- Tail -->
  <path d="M 50 75 Q 40 82 52 90 Q 60 94 48 98" stroke="#FFD700" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <!-- Bows on Tail -->
  <polygon points="46,84 54,84 50,86" fill="#00E676" />
  <polygon points="52,92 60,92 56,94" fill="#00B0FF" />
</svg>""",

    "lion": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Mane -->
  <circle cx="50" cy="50" r="38" fill="#E65100" />
  <!-- Head -->
  <circle cx="50" cy="52" r="26" fill="#FFB74D" />
  <!-- Ears -->
  <circle cx="32" cy="34" r="8" fill="#FFB74D" />
  <circle cx="32" cy="34" r="4" fill="#E65100" />
  <circle cx="68" cy="34" r="8" fill="#FFB74D" />
  <circle cx="68" cy="34" r="4" fill="#E65100" />
  <!-- Eyes -->
  <circle cx="41" cy="48" r="3.5" fill="#3E2723" />
  <circle cx="59" cy="48" r="3.5" fill="#3E2723" />
  <!-- Snout & Nose -->
  <ellipse cx="50" cy="58" rx="8" ry="6" fill="#FFE0B2" />
  <polygon points="47,56 53,56 50,60" fill="#3E2723" />
  <path d="M 47 62 Q 50 64 53 62" stroke="#3E2723" stroke-width="1.5" stroke-linecap="round" fill="none" />
</svg>""",

    "moon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <path d="M 60 15 A 35 35 0 1 0 85 65 A 35 35 0 0 1 60 15 Z" fill="#FDD835" />
  <!-- Gentle sleeping face -->
  <path d="M 45 42 Q 50 46 55 42" stroke="#F57F17" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <path d="M 48 56 Q 52 58 56 56" stroke="#F57F17" stroke-width="2" stroke-linecap="round" fill="none" />
  <!-- Small Star -->
  <polygon points="76,22 78,28 84,28 79,32 81,38 76,34 71,38 73,32 68,28 74,28" fill="#FFF59D" />
</svg>""",

    "nest": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Eggs -->
  <ellipse cx="40" cy="45" rx="8" ry="11" fill="#80DEEA" />
  <ellipse cx="60" cy="45" rx="8" ry="11" fill="#80DEEA" />
  <ellipse cx="50" cy="42" rx="8" ry="11" fill="#B2EBF2" />
  <!-- Twig Nest Base -->
  <path d="M 15 55 Q 50 45 85 55 Q 88 80 50 82 Q 12 80 15 55 Z" fill="#8D6E63" />
  <path d="M 18 60 Q 50 68 82 60" stroke="#5D4037" stroke-width="3" stroke-linecap="round" fill="none" />
  <path d="M 22 70 Q 50 76 78 70" stroke="#6D4C41" stroke-width="2.5" stroke-linecap="round" fill="none" />
</svg>""",

    "owl": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Body -->
  <ellipse cx="50" cy="55" rx="28" ry="32" fill="#795548" />
  <!-- Belly -->
  <ellipse cx="50" cy="62" rx="16" ry="20" fill="#D7CCC8" />
  <!-- Ear Tufts -->
  <polygon points="30,32 38,18 45,30" fill="#5D4037" />
  <polygon points="70,32 62,18 55,30" fill="#5D4037" />
  <!-- Big Eyes -->
  <circle cx="38" cy="42" r="10" fill="#FFF9C4" stroke="#5D4037" stroke-width="2" />
  <circle cx="38" cy="42" r="5" fill="#212121" />
  <circle cx="62" cy="42" r="10" fill="#FFF9C4" stroke="#5D4037" stroke-width="2" />
  <circle cx="62" cy="42" r="5" fill="#212121" />
  <!-- Beak -->
  <polygon points="47,48 53,48 50,56" fill="#FFA000" />
</svg>""",

    "penguin": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Body -->
  <ellipse cx="50" cy="55" rx="26" ry="34" fill="#263238" />
  <!-- White Belly -->
  <ellipse cx="50" cy="60" rx="18" ry="26" fill="#ECEFF1" />
  <!-- Flippers -->
  <ellipse cx="23" cy="58" rx="6" ry="18" fill="#37474F" transform="rotate(15 23 58)" />
  <ellipse cx="77" cy="58" rx="6" ry="18" fill="#37474F" transform="rotate(-15 77 58)" />
  <!-- Eyes -->
  <circle cx="42" cy="38" r="3" fill="#212121" />
  <circle cx="58" cy="38" r="3" fill="#212121" />
  <!-- Beak -->
  <polygon points="46,42 54,42 50,49" fill="#FF9800" />
  <!-- Feet -->
  <ellipse cx="40" cy="88" rx="8" ry="4" fill="#FFA726" />
  <ellipse cx="60" cy="88" rx="8" ry="4" fill="#FFA726" />
</svg>""",

    "queen": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Hair -->
  <ellipse cx="50" cy="52" rx="26" ry="24" fill="#6D4C41" />
  <!-- Crown -->
  <polygon points="30,30 35,16 50,24 65,16 70,30" fill="#FFD700" stroke="#FFA000" stroke-width="2" />
  <circle cx="35" cy="16" r="3" fill="#E91E63" />
  <circle cx="50" cy="24" r="3" fill="#00E676" />
  <circle cx="65" cy="16" r="3" fill="#2979FF" />
  <!-- Face -->
  <circle cx="50" cy="54" r="18" fill="#FFE0B2" />
  <circle cx="44" cy="50" r="2.5" fill="#3E2723" />
  <circle cx="56" cy="50" r="2.5" fill="#3E2723" />
  <path d="M 46 60 Q 50 64 54 60" stroke="#E91E63" stroke-width="2" stroke-linecap="round" fill="none" />
  <!-- Royal Gown collar -->
  <path d="M 32 76 Q 50 68 68 76 L 74 95 L 26 95 Z" fill="#7B1FA2" />
</svg>""",

    "rainbow": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Rainbow Arcs -->
  <ellipse cx="50" cy="75" rx="42" ry="42" fill="none" stroke="#E53935" stroke-width="6" />
  <ellipse cx="50" cy="75" rx="36" ry="36" fill="none" stroke="#FB8C00" stroke-width="6" />
  <ellipse cx="50" cy="75" rx="30" ry="30" fill="none" stroke="#FDD835" stroke-width="6" />
  <ellipse cx="50" cy="75" rx="24" ry="24" fill="none" stroke="#43A047" stroke-width="6" />
  <ellipse cx="50" cy="75" rx="18" ry="18" fill="none" stroke="#1E88E5" stroke-width="6" />
  <ellipse cx="50" cy="75" rx="12" ry="12" fill="none" stroke="#8E24AA" stroke-width="6" />
  <!-- Clouds -->
  <circle cx="20" cy="75" r="14" fill="#FFFFFF" opacity="0.9" />
  <circle cx="30" cy="72" r="10" fill="#FFFFFF" opacity="0.9" />
  <circle cx="80" cy="75" r="14" fill="#FFFFFF" opacity="0.9" />
  <circle cx="70" cy="72" r="10" fill="#FFFFFF" opacity="0.9" />
</svg>""",

    "sun": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Rays -->
  <g stroke="#FFA000" stroke-width="4" stroke-linecap="round">
    <line x1="50" y1="10" x2="50" y2="20" />
    <line x1="50" y1="80" x2="50" y2="90" />
    <line x1="10" y1="50" x2="20" y2="50" />
    <line x1="80" y1="50" x2="90" y2="50" />
    <line x1="22" y1="22" x2="30" y2="30" />
    <line x1="70" y1="70" x2="78" y2="78" />
    <line x1="22" y1="78" x2="30" y2="70" />
    <line x1="70" y1="30" x2="78" y2="22" />
  </g>
  <!-- Sun Disk -->
  <circle cx="50" cy="50" r="26" fill="#FFD54F" />
  <!-- Smile -->
  <circle cx="42" cy="46" r="3" fill="#E65100" />
  <circle cx="58" cy="46" r="3" fill="#E65100" />
  <path d="M 42 54 Q 50 62 58 54" stroke="#E65100" stroke-width="2.5" stroke-linecap="round" fill="none" />
</svg>""",

    "tree": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Trunk -->
  <rect x="44" y="60" width="12" height="30" rx="3" fill="#6D4C41" />
  <!-- Leaves Foliage -->
  <circle cx="50" cy="35" r="24" fill="#388E3C" />
  <circle cx="35" cy="48" r="18" fill="#43A047" />
  <circle cx="65" cy="48" r="18" fill="#43A047" />
  <circle cx="50" cy="50" r="20" fill="#2E7D32" />
  <!-- Apple accents on tree -->
  <circle cx="42" cy="36" r="3" fill="#E53935" />
  <circle cx="58" cy="42" r="3" fill="#E53935" />
</svg>""",

    "umbrella": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Top Handle -->
  <line x1="50" y1="14" x2="50" y2="22" stroke="#455A64" stroke-width="3" stroke-linecap="round" />
  <!-- Canopy -->
  <path d="M 15 55 C 15 28 85 28 85 55 Q 68 50 50 55 Q 32 50 15 55 Z" fill="#00BCD4" />
  <path d="M 50 24 Q 40 40 32 53" stroke="#80DEEA" stroke-width="2" fill="none" />
  <path d="M 50 24 Q 60 40 68 53" stroke="#80DEEA" stroke-width="2" fill="none" />
  <!-- Shaft -->
  <line x1="50" y1="52" x2="50" y2="80" stroke="#455A64" stroke-width="3.5" />
  <!-- Hook Handle -->
  <path d="M 50 80 Q 50 88 42 88 Q 34 88 34 82" stroke="#455A64" stroke-width="3.5" stroke-linecap="round" fill="none" />
</svg>""",

    "volcano": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Mountain -->
  <polygon points="50,38 18,88 82,88" fill="#4E342E" />
  <!-- Lava Crater -->
  <polygon points="40,38 60,38 56,44 44,44" fill="#FF5722" />
  <!-- Lava flow -->
  <path d="M 48 44 Q 44 60 40 70" stroke="#FF9800" stroke-width="3.5" stroke-linecap="round" fill="none" />
  <path d="M 54 44 Q 58 55 56 68" stroke="#FF5722" stroke-width="3" stroke-linecap="round" fill="none" />
  <!-- Smoke / sparks -->
  <circle cx="50" cy="24" r="5" fill="#B0BEC5" opacity="0.7" />
  <circle cx="56" cy="16" r="4" fill="#CFD8DC" opacity="0.6" />
  <circle cx="44" cy="18" r="3" fill="#FFA726" />
</svg>""",

    "whale": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Water Spout -->
  <path d="M 38 34 Q 32 20 28 18" stroke="#4FC3F7" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <path d="M 40 34 Q 44 18 52 18" stroke="#4FC3F7" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <!-- Body -->
  <path d="M 15 55 C 15 35 60 38 75 50 Q 88 44 92 38 Q 88 56 75 62 C 60 75 25 75 15 55 Z" fill="#0288D1" />
  <!-- White Underbelly -->
  <path d="M 22 62 Q 45 74 65 65 Q 45 68 22 62 Z" fill="#E1F5FE" />
  <!-- Eye -->
  <circle cx="30" cy="50" r="2.5" fill="#FFFFFF" />
  <circle cx="31" cy="50" r="1.5" fill="#01579B" />
</svg>""",

    "xylophone": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Wooden base -->
  <polygon points="18,28 82,36 78,80 22,76" fill="#8D6E63" />
  <!-- Colorful bars -->
  <rect x="22" y="32" width="10" height="42" rx="2" fill="#E53935" />
  <rect x="34" y="34" width="10" height="38" rx="2" fill="#FB8C00" />
  <rect x="46" y="36" width="10" height="34" rx="2" fill="#FDD835" />
  <rect x="58" y="38" width="10" height="30" rx="2" fill="#43A047" />
  <rect x="70" y="40" width="10" height="26" rx="2" fill="#1E88E5" />
  <!-- Mallet -->
  <line x1="84" y1="20" x2="60" y2="50" stroke="#D7CCC8" stroke-width="3" stroke-linecap="round" />
  <circle cx="84" cy="20" r="5" fill="#FF5252" />
</svg>""",

    "yacht": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Hull -->
  <polygon points="15,68 85,68 75,82 25,82" fill="#0288D1" />
  <!-- Mast -->
  <line x1="48" y1="20" x2="48" y2="68" stroke="#5D4037" stroke-width="3" />
  <!-- Big Sail -->
  <polygon points="46,24 18,64 46,64" fill="#FFFFFF" stroke="#B0BEC5" stroke-width="1.5" />
  <!-- Small Sail -->
  <polygon points="50,28 78,64 50,64" fill="#FF7043" />
  <!-- Waves -->
  <path d="M 8 84 Q 25 80 45 84 Q 65 88 85 84" stroke="#4FC3F7" stroke-width="3" stroke-linecap="round" fill="none" />
</svg>""",

    "zebra": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <!-- Head & Mane -->
  <ellipse cx="50" cy="54" rx="24" ry="28" fill="#F5F5F5" stroke="#424242" stroke-width="2" />
  <!-- Ears -->
  <polygon points="34,32 40,16 48,28" fill="#424242" />
  <polygon points="66,32 60,16 52,28" fill="#424242" />
  <!-- Stripes -->
  <path d="M 30 46 L 44 48" stroke="#212121" stroke-width="3.5" stroke-linecap="round" />
  <path d="M 70 46 L 56 48" stroke="#212121" stroke-width="3.5" stroke-linecap="round" />
  <path d="M 28 58 L 42 59" stroke="#212121" stroke-width="3.5" stroke-linecap="round" />
  <path d="M 72 58 L 58 59" stroke="#212121" stroke-width="3.5" stroke-linecap="round" />
  <!-- Eyes -->
  <circle cx="40" cy="48" r="3.5" fill="#212121" />
  <circle cx="60" cy="48" r="3.5" fill="#212121" />
  <!-- Muzzle -->
  <ellipse cx="50" cy="68" rx="14" ry="10" fill="#424242" />
  <circle cx="45" cy="68" r="1.5" fill="#BDBDBD" />
  <circle cx="55" cy="68" r="1.5" fill="#BDBDBD" />
</svg>"""
}

for name, svg_content in SVG_DEFS.items():
    file_path = OUT_DIR / f"{name}.svg"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

print(f"Generated {len(SVG_DEFS)} alphabet SVGs in {OUT_DIR}")
