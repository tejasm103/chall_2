/**
 * MindVerse — Inclusive Learning Lab: Milo Digital Teaching Companion
 * Manages Milo's docked avatar, states, speech bubble, and Web Speech API synthesis.
 */

const MiloCompanion = (() => {
  let isVoiceEnabled = true;
  let currentMessage = "Hello friend! I'm Milo, your learning companion.";
  let synth = null;
  let currentUtterance = null;
  let isMinimized = false;

  // Initialize Speech Synthesis
  if ('speechSynthesis' in window) {
    synth = window.speechSynthesis;
  }

  function setVoiceEnabled(enabled) {
    isVoiceEnabled = !!enabled;
    if (!isVoiceEnabled && synth) {
      synth.cancel();
    }
  }

  function setState(state) {
    const characterGroup = document.getElementById('miloCharacter');
    if (!characterGroup) return;

    // Reset state classes
    characterGroup.classList.remove('milo-idle', 'milo-speaking', 'milo-celebrating', 'milo-encouraging');
    characterGroup.classList.add(`milo-${state}`);

    // Manage mouth SVGs
    const normalMouth = document.getElementById('miloMouthSmile');
    const speakMouth = document.getElementById('miloMouthSpeaking');
    const celebMouth = document.getElementById('miloMouthCelebrating');

    if (normalMouth) normalMouth.style.display = (state === 'idle' || state === 'encouraging') ? 'block' : 'none';
    if (speakMouth) speakMouth.style.display = (state === 'speaking') ? 'block' : 'none';
    if (celebMouth) celebMouth.style.display = (state === 'celebrating') ? 'block' : 'none';
  }

  function speak(text, options = {}) {
    currentMessage = text;
    updateBubbleText(text);

    // Announce to aria-live screen readers
    const liveAnnouncer = document.getElementById('ariaLiveRegion');
    if (liveAnnouncer) {
      liveAnnouncer.textContent = text;
    }

    // Also update speech captions overlay if active
    const captionOverlay = document.getElementById('speechCaptionOverlay');
    if (captionOverlay && captionOverlay.classList.contains('active')) {
      captionOverlay.textContent = text;
    }

    if (!isVoiceEnabled || !synth) {
      setState('encouraging');
      setTimeout(() => setState('idle'), 2500);
      return;
    }

    try {
      synth.cancel();
      currentUtterance = new SpeechSynthesisUtterance(text);
      // Gentle, clear speech pacing for neurodivergent learners
      currentUtterance.rate = 0.85;
      currentUtterance.pitch = 1.05;

      currentUtterance.onstart = () => {
        setState('speaking');
      };

      currentUtterance.onend = () => {
        setState('idle');
      };

      currentUtterance.onerror = () => {
        setState('idle');
      };

      synth.speak(currentUtterance);
    } catch (err) {
      console.warn('[MiloCompanion] Speech synthesis error:', err);
      setState('idle');
    }
  }

  function repeatLastMessage() {
    if (window.SoundEngine) window.SoundEngine.playClick();
    speak(currentMessage);
  }

  function updateBubbleText(text) {
    const bubbleTextElem = document.getElementById('miloDialogueText');
    if (bubbleTextElem) {
      bubbleTextElem.textContent = text;
    }
    const bubbleWrap = document.getElementById('miloBubbleWrap');
    if (bubbleWrap && isMinimized) {
      bubbleWrap.style.display = 'block';
      isMinimized = false;
    }
  }

  function toggleMinimize() {
    const bubbleWrap = document.getElementById('miloBubbleWrap');
    if (!bubbleWrap) return;
    isMinimized = !isMinimized;
    bubbleWrap.style.display = isMinimized ? 'none' : 'block';
    if (window.SoundEngine) window.SoundEngine.playClick();
  }

  function celebrate(customMessage = "Great work! You did it!") {
    if (window.SoundEngine) window.SoundEngine.playSuccess();
    setState('celebrating');
    speak(customMessage);
    setTimeout(() => {
      setState('idle');
    }, 4000);
  }

  function encourage(customMessage = "You can take your time and try again!") {
    if (window.SoundEngine) window.SoundEngine.playGentleTryAgain();
    setState('encouraging');
    speak(customMessage);
    setTimeout(() => {
      setState('idle');
    }, 3000);
  }

  function renderDock() {
    // Check if dock already exists
    if (document.getElementById('miloDock')) return;

    const dock = document.createElement('aside');
    dock.id = 'miloDock';
    dock.className = 'milo-dock';
    dock.setAttribute('aria-label', 'Milo Learning Companion');

    const assetPrefix = window.location.pathname.includes('/pages/') ? '../assets/' : './assets/';

    dock.innerHTML = `
      <div id="miloBubbleWrap" class="milo-bubble-wrap" role="region" aria-live="polite">
        <p id="miloDialogueText" class="milo-dialogue-text">${currentMessage}</p>
        <div class="milo-bubble-actions">
          <button id="miloHearAgainBtn" class="milo-btn-small" title="Hear Milo speak again" aria-label="Hear instruction again">
            🔊 Hear again
          </button>
          <button id="miloDismissBtn" class="milo-btn-small" title="Minimize speech bubble" aria-label="Minimize Milo instructions">
            Hide
          </button>
        </div>
      </div>
      <button id="miloAvatarBtn" class="milo-avatar-btn" title="Click to talk with Milo" aria-label="Milo Teaching Companion">
        <object id="miloSvgObject" type="image/svg+xml" data="${assetPrefix}images/milo-robot.svg" width="90" height="112" aria-hidden="true"></object>
      </button>
    `;

    document.body.appendChild(dock);

    // Event listeners
    document.getElementById('miloHearAgainBtn')?.addEventListener('click', () => repeatLastMessage());
    document.getElementById('miloDismissBtn')?.addEventListener('click', () => toggleMinimize());
    document.getElementById('miloAvatarBtn')?.addEventListener('click', () => {
      if (isMinimized) {
        toggleMinimize();
      }
      repeatLastMessage();
    });
  }

  return {
    init: renderDock,
    speak,
    celebrate,
    encourage,
    setState,
    setVoiceEnabled,
    repeat: repeatLastMessage,
    toggleMinimize
  };
})();

window.MiloCompanion = MiloCompanion;
