/**
 * MindVerse — Inclusive Learning Lab: Accessible Computer & Motor Skills Engine
 * Implements 5 activities:
 * 1. Gentle Path Mouse Tracking
 * 2. Bubble Pop
 * 3. Target Practice
 * 4. Treasure Chest (Double-click with accessible single-click toggle)
 * 5. Shape Sorting (Drag-and-drop with accessible tap/keyboard buttons)
 */

const ComputerSkills = (() => {
  let activeActivity = null;
  let studentId = 1;

  function init(activityId = 'mouse-tracking') {
    activeActivity = activityId;
    studentId = window.AccessibilityManager ? window.AccessibilityManager.getStudentId() : 1;

    const container = document.getElementById('skillsActiveArena');
    if (!container) return;

    if (window.SoundEngine) window.SoundEngine.playClick();

    switch (activityId) {
      case 'mouse-tracking':
        renderMouseTracking(container);
        break;
      case 'bubble-pop':
        renderBubblePop(container);
        break;
      case 'target-practice':
        renderTargetPractice(container);
        break;
      case 'treasure-chest':
        renderTreasureChest(container);
        break;
      case 'shape-sorting':
        renderShapeSorting(container);
        break;
      default:
        renderMouseTracking(container);
    }
  }

  // ---------------- 1. MOUSE TRACKING ----------------
  function renderMouseTracking(container) {
    if (window.MiloCompanion) {
      window.MiloCompanion.speak("Follow the wide celestial path from the friendly star to the goal!");
    }

    container.innerHTML = `
      <div style="text-align: center; margin-bottom: 16px;">
        <h3 style="font-size: 1.5rem; font-weight: 800;">Gentle Path Navigator</h3>
        <p style="color: var(--text-muted);">Guide your pointer or touch along the blue starry road.</p>
      </div>

      <div id="pathArenaBox" style="position: relative; width: 100%; max-width: 700px; height: 320px; background: #0F172A; border-radius: var(--radius-lg); margin: 0 auto; overflow: hidden; touch-action: none; cursor: crosshair;">
        <!-- Wide SVG Path -->
        <svg viewBox="0 0 700 320" width="100%" height="100%">
          <path d="M 60 160 Q 200 40 350 160 T 640 160" fill="none" stroke="#1E293B" stroke-width="84" stroke-linecap="round" />
          <path id="guidePath" d="M 60 160 Q 200 40 350 160 T 640 160" fill="none" stroke="#3A86C8" stroke-width="64" stroke-linecap="round" stroke-dasharray="8 8" />
          <!-- Start Indicator -->
          <circle cx="60" cy="160" r="28" fill="#2A9D8F" />
          <text x="60" y="166" font-size="20" fill="#FFFFFF" text-anchor="middle">★</text>
          <!-- Finish Goal -->
          <circle id="trackingGoal" cx="640" cy="160" r="32" fill="#FFD166" />
          <text x="640" y="166" font-size="24" fill="#000000" text-anchor="middle">🏁</text>
        </svg>

        <div id="trackingCursorFriend" style="position: absolute; top: 136px; left: 36px; width: 48px; height: 48px; border-radius: 50%; background: #48CAE4; border: 3px solid #FFFFFF; box-shadow: 0 0 16px #48CAE4; display: flex; align-items: center; justify-content: center; pointer-events: none; transition: transform 0.05s ease;">
          ⭐
        </div>
      </div>

      <div style="text-align: center; margin-top: 16px;">
        <button id="keyboardSteerBtn" class="btn btn-outline" style="min-height: 40px; font-size: 0.9rem;">
          ⌨️ Keyboard/Tap Assist: Guide to finish
        </button>
      </div>
    `;

    const arena = document.getElementById('pathArenaBox');
    const friend = document.getElementById('trackingCursorFriend');
    const goal = document.getElementById('trackingGoal');
    let completed = false;

    function moveFriend(x, y) {
      if (completed) return;
      const rect = arena.getBoundingClientRect();
      const relX = Math.max(0, Math.min(rect.width - 48, x - rect.left - 24));
      const relY = Math.max(0, Math.min(rect.height - 48, y - rect.top - 24));
      friend.style.left = `${relX}px`;
      friend.style.top = `${relY}px`;

      // Check distance to goal (near right edge)
      if (relX > rect.width - 100) {
        completed = true;
        finishSkillActivity("mouse-tracking", "Wonderful steering! You reached the goal!");
      }
    }

    arena.addEventListener('mousemove', (e) => moveFriend(e.clientX, e.clientY));
    arena.addEventListener('touchmove', (e) => {
      if (e.touches.length > 0) {
        moveFriend(e.touches[0].clientX, e.touches[0].clientY);
      }
    });

    document.getElementById('keyboardSteerBtn')?.addEventListener('click', () => {
      completed = true;
      friend.style.left = '85%';
      finishSkillActivity("mouse-tracking", "Great job using the keyboard helper!");
    });
  }

  // ---------------- 2. BUBBLE POP ----------------
  function renderBubblePop(container) {
    if (window.MiloCompanion) {
      window.MiloCompanion.speak("Hover over or tap the colorful bubbles to gently pop them!");
    }

    let poppedCount = 0;
    const targetPops = 6;

    container.innerHTML = `
      <div style="text-align: center; margin-bottom: 16px;">
        <h3 style="font-size: 1.5rem; font-weight: 800;">Calm Bubble Pop</h3>
        <p style="color: var(--text-muted);">Popped: <strong id="bubbleCountText">0 of ${targetPops}</strong> bubbles</p>
      </div>

      <div id="bubbleField" style="position: relative; width: 100%; max-width: 680px; height: 320px; background: #EBF8FF; border: 2px solid #BAE6FD; border-radius: var(--radius-lg); margin: 0 auto; overflow: hidden;">
        <!-- Bubbles injected below -->
      </div>
    `;

    const field = document.getElementById('bubbleField');
    const bubbleColors = ['#38BDF8', '#818CF8', '#34D399', '#F472B6', '#FBBF24', '#A78BFA'];

    for (let i = 0; i < targetPops; i++) {
      const bubble = document.createElement('button');
      bubble.className = 'bubble-floating';
      bubble.setAttribute('aria-label', `Bubble number ${i + 1}`);
      const size = Math.floor(Math.random() * 25) + 65; // 65px - 90px
      const left = Math.floor(Math.random() * 75) + 10;
      const top = Math.floor(Math.random() * 65) + 10;
      const color = bubbleColors[i % bubbleColors.length];

      bubble.style.cssText = `
        position: absolute;
        left: ${left}%;
        top: ${top}%;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #FFFFFF, ${color});
        opacity: 0.85;
        border: 2px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        cursor: pointer;
      `;

      function popBubble() {
        if (bubble.dataset.popped === 'true') return;
        bubble.dataset.popped = 'true';
        if (window.SoundEngine) window.SoundEngine.playChime();

        bubble.style.transform = 'scale(1.4)';
        bubble.style.opacity = '0';
        bubble.style.transition = 'all 0.25s ease';

        poppedCount++;
        const countText = document.getElementById('bubbleCountText');
        if (countText) countText.textContent = `${poppedCount} of ${targetPops}`;

        setTimeout(() => bubble.remove(), 260);

        if (poppedCount >= targetPops) {
          finishSkillActivity('bubble-pop', 'Pop! All bubbles popped gently!');
        }
      }

      bubble.addEventListener('mouseenter', popBubble);
      bubble.addEventListener('click', popBubble);
      bubble.addEventListener('touchstart', (e) => {
        e.preventDefault();
        popBubble();
      });

      field.appendChild(bubble);
    }
  }

  // ---------------- 3. TARGET PRACTICE ----------------
  function renderTargetPractice(container) {
    if (window.MiloCompanion) {
      window.MiloCompanion.speak("Click or tap the friendly glowing target! Take all the time you need.");
    }

    let clicks = 0;
    const requiredClicks = 4;

    container.innerHTML = `
      <div style="text-align: center; margin-bottom: 16px;">
        <h3 style="font-size: 1.5rem; font-weight: 800;">Friendly Target Practice</h3>
        <p style="color: var(--text-muted);">Hits: <strong id="targetHitsText">0 of ${requiredClicks}</strong></p>
      </div>

      <div id="targetPlayArea" style="position: relative; width: 100%; max-width: 680px; height: 320px; background: var(--bg-surface); border: 2px solid var(--border-light); border-radius: var(--radius-lg); margin: 0 auto; overflow: hidden;">
        <button id="activeSkillTarget" aria-label="Large friendly bullseye target" style="position: absolute; top: 110px; left: 290px; width: 96px; height: 96px; border-radius: 50%; background: #EF4444; border: 8px solid #FFFFFF; box-shadow: 0 4px 16px rgba(0,0,0,0.15); cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 2rem; color: #FFFFFF; transition: all 0.2s ease;">
          🎯
        </button>
      </div>
    `;

    const targetBtn = document.getElementById('activeSkillTarget');
    const playArea = document.getElementById('targetPlayArea');

    function hitTarget() {
      clicks++;
      if (window.SoundEngine) window.SoundEngine.playSuccess();

      const hitsText = document.getElementById('targetHitsText');
      if (hitsText) hitsText.textContent = `${clicks} of ${requiredClicks}`;

      if (clicks >= requiredClicks) {
        finishSkillActivity('target-practice', 'Bullseye! You hit all targets with great accuracy!');
        return;
      }

      // Reposition to a new predictable zone
      const rect = playArea.getBoundingClientRect();
      const maxX = rect.width - 120;
      const maxY = rect.height - 120;
      const newX = Math.max(20, Math.floor(Math.random() * maxX));
      const newY = Math.max(20, Math.floor(Math.random() * maxY));

      targetBtn.style.left = `${newX}px`;
      targetBtn.style.top = `${newY}px`;
    }

    targetBtn.addEventListener('click', hitTarget);
  }

  // ---------------- 4. TREASURE CHEST ----------------
  function renderTreasureChest(container) {
    if (window.MiloCompanion) {
      window.MiloCompanion.speak("Double-click the treasure chest to unlock it, or use the accessible one-click button!");
    }

    container.innerHTML = `
      <div style="text-align: center; margin-bottom: 16px;">
        <h3 style="font-size: 1.5rem; font-weight: 800;">Treasure Chest Unlock</h3>
        <p style="color: var(--text-muted);">Practice double-clicking or use the accessible single-click helper.</p>
      </div>

      <div style="max-width: 500px; margin: 0 auto; background: var(--bg-surface); padding: 36px; border-radius: var(--radius-lg); text-align: center; border: 2px solid var(--border-light);">
        <div id="chestVisual" style="font-size: 5.5rem; margin-bottom: 16px; cursor: pointer; user-select: none;" title="Double-click to open!">
          🎁
        </div>
        <p id="chestStatusText" style="font-weight: 700; margin-bottom: 20px; color: var(--text-main);">
          Locked: Double-click me!
        </p>

        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
          <button id="accessibleSingleClickBtn" class="btn btn-secondary">
            ✨ Open with Single-Click
          </button>
        </div>
      </div>
    `;

    const chest = document.getElementById('chestVisual');
    const statusText = document.getElementById('chestStatusText');
    const singleBtn = document.getElementById('accessibleSingleClickBtn');
    let opened = false;

    function openChest() {
      if (opened) return;
      opened = true;
      if (window.SoundEngine) window.SoundEngine.playSuccess();

      chest.textContent = '🌟';
      chest.style.transform = 'scale(1.2)';
      chest.style.transition = 'transform 0.3s ease';
      statusText.innerHTML = '<span style="color: #03543F;">Unlocked! You found the golden learning stars!</span>';

      finishSkillActivity('treasure-chest', 'Hooray! The treasure chest is open!');
    }

    chest.addEventListener('dblclick', openChest);
    singleBtn.addEventListener('click', openChest);
  }

  // ---------------- 5. SHAPE SORTING ----------------
  function renderShapeSorting(container) {
    if (window.MiloCompanion) {
      window.MiloCompanion.speak("Put each shape into its matching container! You can drag, tap, or press numbers 1, 2, or 3.");
    }

    container.innerHTML = `
      <div style="text-align: center; margin-bottom: 16px;">
        <h3 style="font-size: 1.5rem; font-weight: 800;">Shape Sorting Box</h3>
        <p style="color: var(--text-muted);">Match the Circle, Square, and Triangle to their labeled bins.</p>
      </div>

      <div style="max-width: 700px; margin: 0 auto;">
        <!-- Shape to sort -->
        <div style="text-align: center; margin-bottom: 24px;">
          <span style="font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 8px;">Active Shape:</span>
          <div id="shapeToPlace" style="display: inline-flex; align-items: center; justify-content: center; width: 88px; height: 88px; border-radius: var(--radius-md); background: #3A86C8; color: #FFFFFF; font-size: 2.5rem; box-shadow: var(--shadow-md); cursor: grab;" draggable="true" title="Drag me to matching bin">
            ⚪
          </div>
          <p id="shapeLabelPrompt" style="margin-top: 8px; font-weight: 800; font-size: 1.1rem;">It's a Circle!</p>
        </div>

        <!-- 3 Target Bins -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px;">
          <div class="sorting-bin" data-shape="circle" style="background: var(--bg-surface); border: 3px dashed #3A86C8; border-radius: var(--radius-md); padding: 20px 10px; text-align: center; cursor: pointer;">
            <div style="font-size: 2rem;">⚪</div>
            <strong style="display: block; margin-top: 6px;">1. Circle Bin</strong>
            <button class="btn btn-outline tap-bin-btn" data-shape="circle" style="margin-top: 8px; width: 100%; min-height: 38px; font-size: 0.85rem;">Place Here</button>
          </div>
          <div class="sorting-bin" data-shape="square" style="background: var(--bg-surface); border: 3px dashed #43A047; border-radius: var(--radius-md); padding: 20px 10px; text-align: center; cursor: pointer;">
            <div style="font-size: 2rem;">🟩</div>
            <strong style="display: block; margin-top: 6px;">2. Square Bin</strong>
            <button class="btn btn-outline tap-bin-btn" data-shape="square" style="margin-top: 8px; width: 100%; min-height: 38px; font-size: 0.85rem;">Place Here</button>
          </div>
          <div class="sorting-bin" data-shape="triangle" style="background: var(--bg-surface); border: 3px dashed #FB8C00; border-radius: var(--radius-md); padding: 20px 10px; text-align: center; cursor: pointer;">
            <div style="font-size: 2rem;">🔺</div>
            <strong style="display: block; margin-top: 6px;">3. Triangle Bin</strong>
            <button class="btn btn-outline tap-bin-btn" data-shape="triangle" style="margin-top: 8px; width: 100%; min-height: 38px; font-size: 0.85rem;">Place Here</button>
          </div>
        </div>
      </div>
    `;

    const currentTarget = 'circle';

    function handleBinChoice(chosen) {
      if (chosen === currentTarget) {
        if (window.SoundEngine) window.SoundEngine.playSuccess();
        finishSkillActivity('shape-sorting', 'Perfect! The circle fits right in the circle bin!');
      } else {
        if (window.SoundEngine) window.SoundEngine.playGentleTryAgain();
        if (window.MiloCompanion) window.MiloCompanion.encourage("Circles are round all the way around. Try the circle bin!");
      }
    }

    container.querySelectorAll('.tap-bin-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        handleBinChoice(btn.getAttribute('data-shape'));
      });
    });

    container.querySelectorAll('.sorting-bin').forEach(bin => {
      bin.addEventListener('click', () => {
        handleBinChoice(bin.getAttribute('data-shape'));
      });
      bin.addEventListener('dragover', (e) => e.preventDefault());
      bin.addEventListener('drop', (e) => {
        e.preventDefault();
        handleBinChoice(bin.getAttribute('data-shape'));
      });
    });

    // Keyboard support: 1, 2, 3
    window.addEventListener('keydown', function keyHandler(e) {
      if (e.key === '1') handleBinChoice('circle');
      if (e.key === '2') handleBinChoice('square');
      if (e.key === '3') handleBinChoice('triangle');
    }, { once: true });
  }

  // ---------------- ACTIVITY COMPLETION ----------------
  async function finishSkillActivity(activityId, message) {
    if (window.MiloCompanion) {
      window.MiloCompanion.celebrate(message);
    }

    // Save completion to backend
    if (window.MindVerseAPI) {
      await window.MindVerseAPI.saveComputerSkillProgress({
        student_id: studentId,
        activity_id: activityId,
        stars: 3,
        accuracy: 100.0
      });
    }

    const container = document.getElementById('skillsActiveArena');
    if (!container) return;

    setTimeout(() => {
      container.innerHTML = `
        <div style="background: #DEF7EC; border: 2px solid #BCF0DA; border-radius: var(--radius-lg); padding: 36px 20px; text-align: center;">
          <div style="font-size: 3rem; margin-bottom: 8px;">🌟 ★ ★ ★ 🌟</div>
          <h2 style="color: #03543F; font-size: 1.8rem; font-weight: 800; margin-bottom: 8px;">Wonderful Job!</h2>
          <p style="color: #046C4E; font-size: 1.1rem; margin-bottom: 24px;">${message}</p>
          <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            <button class="btn btn-primary" onclick="ComputerSkills.init('${activityId}')">
              🔄 Practice Again
            </button>
            <a href="/pages/dashboard.html" class="btn btn-secondary">
              ⭐ Return to Dashboard
            </a>
          </div>
        </div>
      `;
    }, 1200);
  }

  return {
    init
  };
})();

window.ComputerSkills = ComputerSkills;
