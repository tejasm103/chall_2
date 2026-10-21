/**
 * MindVerse — Inclusive Learning Lab: Educational Games Engine
 * Implements Color Matcher, Emotion Recognizer, Object Counter, and Picture-Word Pairing.
 * Adheres to errorless learning, positive reinforcement, and SQLite score persistence.
 */

const LearningGames = (() => {
  let currentGame = null;
  let currentDifficulty = 'easy';
  let studentId = 1;

  let currentRound = 0;
  let totalRounds = 5;
  let correctCount = 0;
  let attemptsCount = 0;

  const assetPrefix = window.location.pathname.includes('/pages/') ? '../assets/' : './assets/';

  // 1. COLOR MATCHER DATA
  const COLOR_DATA = [
    { name: "Red", hex: "#E53935", pattern: "dots", prompt: "Can you find the warm Red card?" },
    { name: "Blue", hex: "#1E88E5", pattern: "stripes", prompt: "Which card is calm Blue like the ocean?" },
    { name: "Yellow", hex: "#FDD835", pattern: "sun", prompt: "Find sunny Yellow like bright daylight!" },
    { name: "Green", hex: "#43A047", pattern: "leaves", prompt: "Touch the gentle Green card like fresh leaves." },
    { name: "Purple", hex: "#8E24AA", pattern: "stars", prompt: "Can you tap the peaceful Purple card?" },
    { name: "Orange", hex: "#FB8C00", pattern: "waves", prompt: "Find the cheerful Orange card!" }
  ];

  // 2. EMOTION RECOGNIZER DATA
  const EMOTION_DATA = [
    {
      emotion: "Happy",
      icon: `${assetPrefix}icons/happy-face.svg`,
      description: "A warm smile that curls gently upward at the corners.",
      context: "Friends often smile when doing something fun, but everyone shows joy in their own way."
    },
    {
      emotion: "Calm",
      icon: `${assetPrefix}icons/calm-face.svg`,
      description: "Soft, relaxed eyes and peaceful breathing.",
      context: "Feeling calm helps our body rest and recharge quietly."
    },
    {
      emotion: "Surprised",
      icon: `${assetPrefix}icons/surprised-face.svg`,
      description: "Round, wide-open eyes and an open mouth.",
      context: "We might feel surprised when something unexpected happens!"
    },
    {
      emotion: "Sad",
      icon: `${assetPrefix}icons/sad-face.svg`,
      description: "Gently lowered eyebrows and mouth curving downward.",
      context: "It is natural to feel sad sometimes; taking a quiet break or talking with a friend can help."
    },
    {
      emotion: "Angry",
      icon: `${assetPrefix}icons/angry-face.svg`,
      description: "Focused eyebrows and a firm expression.",
      context: "When someone feels angry, deep breaths and quiet space help feelings settle."
    }
  ];

  // 3. OBJECT COUNTER DATA
  const COUNT_OBJECTS = [
    { name: "Apple", icon: `${assetPrefix}images/alphabet/apple.svg` },
    { name: "Star", icon: `${assetPrefix}icons/star.svg` },
    { name: "Fish", icon: `${assetPrefix}images/alphabet/fish.svg` },
    { name: "Duck", icon: `${assetPrefix}images/alphabet/duck.svg` },
    { name: "Ball", icon: `${assetPrefix}images/alphabet/ball.svg` }
  ];

  // 4. PICTURE-WORD DATA
  const PAIR_DATA = [
    { word: "Apple", icon: `${assetPrefix}images/alphabet/apple.svg` },
    { word: "Cat", icon: `${assetPrefix}images/alphabet/cat.svg` },
    { word: "Sun", icon: `${assetPrefix}images/alphabet/sun.svg` },
    { word: "Tree", icon: `${assetPrefix}images/alphabet/tree.svg` },
    { word: "Whale", icon: `${assetPrefix}images/alphabet/whale.svg` },
    { word: "Owl", icon: `${assetPrefix}images/alphabet/owl.svg` }
  ];

  function start(gameId, difficulty = 'easy') {
    currentGame = gameId;
    currentDifficulty = difficulty;
    currentRound = 0;
    correctCount = 0;
    attemptsCount = 0;

    studentId = window.AccessibilityManager ? window.AccessibilityManager.getStudentId() : 1;

    const arena = document.getElementById('gameArena');
    if (!arena) return;

    arena.style.display = 'block';
    arena.scrollIntoView({ behavior: 'smooth' });

    if (window.SoundEngine) window.SoundEngine.playClick();

    nextRound();
  }

  function nextRound() {
    currentRound++;
    if (currentRound > totalRounds) {
      finishGame();
      return;
    }

    updateScoreBar();

    if (currentGame === 'color-matcher') {
      renderColorMatcherRound();
    } else if (currentGame === 'emotion-recognizer') {
      renderEmotionRound();
    } else if (currentGame === 'object-counter') {
      renderCounterRound();
    } else if (currentGame === 'picture-word-pairing') {
      renderPairingRound();
    }
  }

  function updateScoreBar() {
    const roundElem = document.getElementById('gameRoundText');
    const scoreElem = document.getElementById('gameScoreText');
    const starsElem = document.getElementById('gameStarsDisplay');

    if (roundElem) roundElem.textContent = `Round ${currentRound} of ${totalRounds}`;
    if (scoreElem) scoreElem.textContent = `Score: ${correctCount * 20}`;

    if (starsElem) {
      const currentAccuracy = attemptsCount > 0 ? (correctCount / attemptsCount) : 1;
      let stars = 1;
      if (currentAccuracy >= 0.9) stars = 3;
      else if (currentAccuracy >= 0.7) stars = 2;

      starsElem.innerHTML = `
        <span class="${stars >= 1 ? 'star-filled' : ''}">★</span>
        <span class="${stars >= 2 ? 'star-filled' : ''}">★</span>
        <span class="${stars >= 3 ? 'star-filled' : ''}">★</span>
      `;
    }
  }

  // ---------------- COLOR MATCHER ROUND ----------------
  function renderColorMatcherRound() {
    const arenaBody = document.getElementById('gameArenaBody');
    if (!arenaBody) return;

    // Pick target color
    const shuffled = [...COLOR_DATA].sort(() => 0.5 - Math.random());
    const target = shuffled[0];
    const options = shuffled.slice(0, currentDifficulty === 'hard' ? 4 : 3).sort(() => 0.5 - Math.random());

    if (window.MiloCompanion) {
      window.MiloCompanion.speak(target.prompt);
    }

    arenaBody.innerHTML = `
      <h3 style="font-size: 1.4rem; margin-bottom: 8px;">Target Color: <strong style="color: ${target.hex}">${target.name}</strong></h3>
      <p style="color: var(--text-muted); margin-bottom: 20px;">Pattern clue: ${target.pattern} | ${target.prompt}</p>

      <div class="color-options-grid" role="group" aria-label="Color Choice Options">
        ${options.map(c => `
          <button class="color-card-btn" style="background-color: ${c.hex};" data-name="${c.name}" aria-label="Color ${c.name} with ${c.pattern} pattern">
            <span>${c.name}</span>
            <small style="font-size: 0.75rem; opacity: 0.85;">(${c.pattern})</small>
          </button>
        `).join('')}
      </div>
      <div id="gameRoundFeedback" class="feedback-banner" role="status"></div>
    `;

    arenaBody.querySelectorAll('.color-card-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const chosen = btn.getAttribute('data-name');
        handleChoice(chosen === target.name, `Yes! That is ${target.name}!`, `That's ${chosen}. Take your time and find ${target.name}!`);
      });
    });
  }

  // ---------------- EMOTION RECOGNIZER ROUND ----------------
  function renderEmotionRound() {
    const arenaBody = document.getElementById('gameArenaBody');
    if (!arenaBody) return;

    const shuffled = [...EMOTION_DATA].sort(() => 0.5 - Math.random());
    const target = shuffled[0];
    const options = shuffled.slice(0, 3).sort(() => 0.5 - Math.random());

    if (window.MiloCompanion) {
      window.MiloCompanion.speak(`Can you find the ${target.emotion} expression? ${target.description}`);
    }

    arenaBody.innerHTML = `
      <h3 style="font-size: 1.4rem; margin-bottom: 8px;">Find the Face: <strong>${target.emotion}</strong></h3>
      <p style="color: var(--text-muted); margin-bottom: 12px;">${target.description}</p>
      <div style="background: var(--bg-surface); padding: 10px 16px; border-radius: var(--radius-sm); max-width: 600px; margin: 0 auto 20px; font-size: 0.9rem;">
        💡 <em>Reminder: Facial expressions differ from person to person. No single expression proves how someone feels inside!</em>
      </div>

      <div class="emotion-options-grid" role="group" aria-label="Emotion Facial Expressions">
        ${options.map(e => `
          <button class="emotion-card-btn" data-emotion="${e.emotion}" aria-label="Expression showing ${e.emotion}">
            <img src="${e.icon}" alt="${e.emotion} facial cue" />
            <span style="font-weight: 700; font-size: 1.05rem;">${e.emotion}</span>
          </button>
        `).join('')}
      </div>
      <div id="gameRoundFeedback" class="feedback-banner" role="status"></div>
    `;

    arenaBody.querySelectorAll('.emotion-card-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const chosen = btn.getAttribute('data-emotion');
        handleChoice(chosen === target.emotion, `Great observation! That shows ${target.emotion}.`, `That expression looks like ${chosen}. Look for ${target.emotion}!`);
      });
    });
  }

  // ---------------- OBJECT COUNTER ROUND ----------------
  function renderCounterRound() {
    const arenaBody = document.getElementById('gameArenaBody');
    if (!arenaBody) return;

    const maxCount = currentDifficulty === 'hard' ? 8 : (currentDifficulty === 'medium' ? 5 : 4);
    const targetCount = Math.floor(Math.random() * (maxCount - 1)) + 2; // 2 to maxCount
    const objectType = COUNT_OBJECTS[Math.floor(Math.random() * COUNT_OBJECTS.length)];

    const options = [targetCount];
    while (options.length < 3) {
      const rand = Math.floor(Math.random() * maxCount) + 1;
      if (!options.includes(rand)) options.push(rand);
    }
    options.sort((a, b) => a - b);

    if (window.MiloCompanion) {
      window.MiloCompanion.speak(`Let's count together! How many ${objectType.name}s do you see?`);
    }

    arenaBody.innerHTML = `
      <h3 style="font-size: 1.4rem; margin-bottom: 8px;">Count the <strong>${objectType.name}s</strong></h3>
      <p style="color: var(--text-muted); margin-bottom: 16px;">Touch each item as you count: 1, 2, 3...</p>

      <div class="counting-display-area" role="region" aria-label="Objects to count">
        ${Array.from({ length: targetCount }).map((_, i) => `
          <div class="count-object-item" title="${objectType.name} number ${i + 1}">
            <img src="${objectType.icon}" alt="${objectType.name}" />
          </div>
        `).join('')}
      </div>

      <div style="display: flex; justify-content: center; gap: 16px; margin: 20px 0;">
        ${options.map(num => `
          <button class="number-choice-btn" data-number="${num}" aria-label="Select number ${num}">
            ${num}
          </button>
        `).join('')}
      </div>
      <div id="gameRoundFeedback" class="feedback-banner" role="status"></div>
    `;

    arenaBody.querySelectorAll('.number-choice-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const chosen = parseInt(btn.getAttribute('data-number'), 10);
        handleChoice(chosen === targetCount, `Hooray! There are ${targetCount} ${objectType.name}s!`, `You counted ${chosen}. Let's count them one by one to find ${targetCount}!`);
      });
    });
  }

  // ---------------- PICTURE-WORD PAIRING ROUND ----------------
  function renderPairingRound() {
    const arenaBody = document.getElementById('gameArenaBody');
    if (!arenaBody) return;

    const shuffled = [...PAIR_DATA].sort(() => 0.5 - Math.random()).slice(0, 3);
    const pictures = [...shuffled].sort(() => 0.5 - Math.random());
    const words = [...shuffled].sort(() => 0.5 - Math.random());

    let selectedPic = null;
    let selectedWord = null;

    if (window.MiloCompanion) {
      window.MiloCompanion.speak("Match each friendly picture with its written word card!");
    }

    arenaBody.innerHTML = `
      <h3 style="font-size: 1.4rem; margin-bottom: 8px;">Picture–Word Pairing</h3>
      <p style="color: var(--text-muted); margin-bottom: 16px;">Select a picture on the left, then select its matching word on the right.</p>

      <div class="word-pair-container">
        <div class="pair-slot-column" id="pairPicsColumn">
          ${pictures.map(p => `
            <button class="pair-card-item pic-card" data-word="${p.word}" aria-label="Picture card of ${p.word}">
              <img src="${p.icon}" alt="${p.word}" width="48" height="48" />
              <span style="font-weight: 700;">Picture</span>
            </button>
          `).join('')}
        </div>
        <div class="pair-slot-column" id="pairWordsColumn">
          ${words.map(w => `
            <button class="pair-card-item word-card" data-word="${w.word}" aria-label="Word card for ${w.word}">
              <span style="font-size: 1.2rem; font-weight: 800; color: var(--color-primary);">${w.word}</span>
            </button>
          `).join('')}
        </div>
      </div>
      <div id="gameRoundFeedback" class="feedback-banner" role="status"></div>
    `;

    arenaBody.querySelectorAll('.pic-card').forEach(btn => {
      btn.addEventListener('click', () => {
        arenaBody.querySelectorAll('.pic-card').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedPic = btn.getAttribute('data-word');
        checkPairSelection();
      });
    });

    arenaBody.querySelectorAll('.word-card').forEach(btn => {
      btn.addEventListener('click', () => {
        arenaBody.querySelectorAll('.word-card').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedWord = btn.getAttribute('data-word');
        checkPairSelection();
      });
    });

    function checkPairSelection() {
      if (selectedPic && selectedWord) {
        if (selectedPic === selectedWord) {
          handleChoice(true, `Wonderful match! ${selectedPic} pairs with ${selectedWord}!`, "");
        } else {
          handleChoice(false, "", `That picture is ${selectedPic}, but the word is ${selectedWord}. Try matching them again!`);
        }
      }
    }
  }

  // ---------------- ROUND RESULT HANDLER ----------------
  function handleChoice(isCorrect, successMsg, tryAgainMsg) {
    attemptsCount++;
    const feedback = document.getElementById('gameRoundFeedback');

    if (isCorrect) {
      correctCount++;
      if (feedback) {
        feedback.className = 'feedback-banner success';
        feedback.textContent = `✨ ${successMsg}`;
      }
      if (window.MiloCompanion) window.MiloCompanion.celebrate(successMsg);

      setTimeout(() => {
        nextRound();
      }, 1800);
    } else {
      if (feedback) {
        feedback.className = 'feedback-banner try-again';
        feedback.textContent = `🌱 ${tryAgainMsg}`;
      }
      if (window.MiloCompanion) window.MiloCompanion.encourage(tryAgainMsg);
    }
  }

  // ---------------- GAME COMPLETION & DATABASE SAVE ----------------
  async function finishGame() {
    const arenaBody = document.getElementById('gameArenaBody');
    if (!arenaBody) return;

    const accuracy = attemptsCount > 0 ? Math.round((correctCount / attemptsCount) * 100) : 100;
    const finalScore = correctCount * 20;

    let stars = 1;
    if (accuracy >= 90) stars = 3;
    else if (accuracy >= 70) stars = 2;

    const starsHtml = '★'.repeat(stars) + '☆'.repeat(3 - stars);

    // Save score to SQLite via API
    let savedNotice = '';
    if (window.MindVerseAPI) {
      const res = await window.MindVerseAPI.saveGameScore({
        student_id: studentId,
        game_name: getGameTitle(currentGame),
        difficulty: currentDifficulty,
        score: finalScore,
        stars: stars,
        accuracy: accuracy
      });
      if (res.success) {
        savedNotice = '💾 Score saved to your profile!';
      }
    }

    if (window.MiloCompanion) {
      window.MiloCompanion.celebrate(`Fantastic work! You earned ${stars} stars with ${accuracy}% accuracy!`);
    }

    arenaBody.innerHTML = `
      <div style="padding: 32px 16px; text-align: center;">
        <div style="font-size: 3.5rem; color: #FFD166; margin-bottom: 12px;">${starsHtml}</div>
        <h2 style="font-size: 2rem; font-weight: 800; margin-bottom: 8px;">Activity Completed!</h2>
        <p style="font-size: 1.15rem; color: var(--text-muted); margin-bottom: 16px;">
          Score: <strong>${finalScore}</strong> | Accuracy: <strong>${accuracy}%</strong>
        </p>
        <p style="color: var(--color-secondary); font-weight: 700; margin-bottom: 24px;">${savedNotice}</p>

        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
          <button class="btn btn-primary" onclick="LearningGames.start('${currentGame}', '${currentDifficulty}')">
            🔄 Play Again
          </button>
          <a href="/pages/dashboard.html" class="btn btn-secondary">
            🌟 Back to Dashboard
          </a>
        </div>
      </div>
    `;
  }

  function getGameTitle(id) {
    switch (id) {
      case 'color-matcher': return 'Color Matcher';
      case 'emotion-recognizer': return 'Emotion Recognizer';
      case 'object-counter': return 'Object Counter';
      case 'picture-word-pairing': return 'Picture-Word Pairing';
      default: return 'Educational Game';
    }
  }

  return {
    start
  };
})();

window.LearningGames = LearningGames;
