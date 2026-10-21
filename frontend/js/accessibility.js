/**
 * MindVerse — Inclusive Learning Lab: Accessibility Controller Module
 * Manages persistent toolbar controls, theme switching, font scaling,
 * dyslexia typography, sensory overrides, and backend preference synchronization.
 */

const AccessibilityManager = (() => {
  let currentStudentId = 1;
  let activeTheme = 'default';
  let activeFontSize = 'standard';
  let isDyslexiaFont = false;
  let isReducedMotion = false;
  let is3DPaused = false;
  let isSoundEnabled = true;
  let isVoiceEnabled = true;
  let isCaptionsEnabled = false;
  let activeVideoFilter = 'normal';

  async function init(studentId = 1) {
    currentStudentId = studentId;

    // 1. Detect OS reduced motion preference
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      isReducedMotion = true;
    }

    // 2. Load preferences from LocalStorage or Backend API
    loadLocalPreferences();
    await loadBackendPreferences();

    // 3. Apply settings to DOM
    applyTheme(activeTheme);
    applyFontSize(activeFontSize);
    applyDyslexiaFont(isDyslexiaFont);
    applyReducedMotion(isReducedMotion);
    applySound(isSoundEnabled);
    applyVoice(isVoiceEnabled);
    applyCaptions(isCaptionsEnabled);

    // 4. Render persistent toolbar in HTML if element exists
    renderToolbar();
  }

  function loadLocalPreferences() {
    activeTheme = localStorage.getItem('mindverse_theme') || activeTheme;
    activeFontSize = localStorage.getItem('mindverse_font_size') || activeFontSize;
    isDyslexiaFont = localStorage.getItem('mindverse_dyslexia') === '1';
    isSoundEnabled = localStorage.getItem('mindverse_sound') !== '0';
    isVoiceEnabled = localStorage.getItem('mindverse_voice') !== '0';
    isCaptionsEnabled = localStorage.getItem('mindverse_captions') === '1';
    is3DPaused = localStorage.getItem('mindverse_pause_3d') === '1';
    if (localStorage.getItem('mindverse_motion') !== null) {
      isReducedMotion = localStorage.getItem('mindverse_motion') === '1';
    }
  }

  async function loadBackendPreferences() {
    if (window.MindVerseAPI) {
      try {
        const prefs = await window.MindVerseAPI.getPreferences(currentStudentId);
        if (prefs && !prefs.is_fallback) {
          if (prefs.preferred_theme) activeTheme = prefs.preferred_theme;
          if (prefs.font_size) activeFontSize = prefs.font_size;
          if (prefs.sound_enabled !== undefined) isSoundEnabled = !!prefs.sound_enabled;
          if (prefs.voice_enabled !== undefined) isVoiceEnabled = !!prefs.voice_enabled;
          if (prefs.reduced_motion !== undefined) isReducedMotion = !!prefs.reduced_motion;
        }
      } catch (err) {
        console.warn('[AccessibilityManager] Error loading backend prefs:', err);
      }
    }
  }

  async function persistPreferences() {
    // 1. LocalStorage
    localStorage.setItem('mindverse_theme', activeTheme);
    localStorage.setItem('mindverse_font_size', activeFontSize);
    localStorage.setItem('mindverse_dyslexia', isDyslexiaFont ? '1' : '0');
    localStorage.setItem('mindverse_sound', isSoundEnabled ? '1' : '0');
    localStorage.setItem('mindverse_voice', isVoiceEnabled ? '1' : '0');
    localStorage.setItem('mindverse_captions', isCaptionsEnabled ? '1' : '0');
    localStorage.setItem('mindverse_motion', isReducedMotion ? '1' : '0');
    localStorage.setItem('mindverse_pause_3d', is3DPaused ? '1' : '0');

    // 2. Backend API
    if (window.MindVerseAPI) {
      await window.MindVerseAPI.savePreferences(currentStudentId, {
        preferred_theme: activeTheme,
        font_size: activeFontSize,
        sound_enabled: isSoundEnabled ? 1 : 0,
        voice_enabled: isVoiceEnabled ? 1 : 0,
        reduced_motion: isReducedMotion ? 1 : 0
      });
    }
  }

  // ----------------- DOM Applicators -----------------

  function applyTheme(themeName) {
    activeTheme = themeName;
    document.documentElement.setAttribute('data-theme', themeName);
    if (window.ThreeWorld && window.ThreeWorld.updateTheme) {
      window.ThreeWorld.updateTheme(themeName);
    }
    updateToolbarActiveStates();
  }

  function applyFontSize(size) {
    activeFontSize = size;
    document.documentElement.setAttribute('data-font-size', size);
    updateToolbarActiveStates();
  }

  function applyDyslexiaFont(enabled) {
    isDyslexiaFont = !!enabled;
    document.documentElement.setAttribute('data-dyslexia-font', isDyslexiaFont ? 'true' : 'false');
    updateToolbarActiveStates();
  }

  function applyReducedMotion(enabled) {
    isReducedMotion = !!enabled;
    document.documentElement.setAttribute('data-reduced-motion', isReducedMotion ? 'true' : 'false');
    if (window.ThreeWorld && window.ThreeWorld.setReducedMotion) {
      window.ThreeWorld.setReducedMotion(isReducedMotion);
    }
    updateToolbarActiveStates();
  }

  function applySound(enabled) {
    isSoundEnabled = !!enabled;
    if (window.SoundEngine) window.SoundEngine.setEnabled(isSoundEnabled);
    updateToolbarActiveStates();
  }

  function applyVoice(enabled) {
    isVoiceEnabled = !!enabled;
    if (window.MiloCompanion) window.MiloCompanion.setVoiceEnabled(isVoiceEnabled);
    updateToolbarActiveStates();
  }

  function applyCaptions(enabled) {
    isCaptionsEnabled = !!enabled;
    const overlay = document.getElementById('speechCaptionOverlay');
    if (overlay) {
      if (isCaptionsEnabled) overlay.classList.add('active');
      else overlay.classList.remove('active');
    }
    updateToolbarActiveStates();
  }

  function apply3DPause(paused) {
    is3DPaused = !!paused;
    if (window.ThreeWorld) window.ThreeWorld.setPaused(is3DPaused || isReducedMotion);
    updateToolbarActiveStates();
  }

  function applyVideoFilter(filterName) {
    activeVideoFilter = filterName;
    const containers = document.querySelectorAll('.video-container');
    containers.forEach(c => {
      c.classList.remove('filter-normal', 'filter-dim', 'filter-warm');
      c.classList.add(`filter-${filterName}`);
    });
  }

  // ----------------- UI Toolbar Rendering -----------------

  function renderToolbar() {
    const container = document.getElementById('accessibilityToolbar');
    if (!container) return;

    container.innerHTML = `
      <div class="toolbar-inner" role="toolbar" aria-label="Accessibility & Sensory Controls">
        <!-- Theme Controls -->
        <div class="toolbar-group" role="group" aria-label="Visual Theme Options">
          <span class="toolbar-label">Theme:</span>
          <button id="themeDefaultBtn" class="toolbar-btn ${activeTheme === 'default' ? 'active' : ''}" aria-pressed="${activeTheme === 'default'}" title="Soft Daylight Theme">Daylight</button>
          <button id="themePastelBtn" class="toolbar-btn ${activeTheme === 'pastel-calming' ? 'active' : ''}" aria-pressed="${activeTheme === 'pastel-calming'}" title="Pastel Calming Theme">Pastel</button>
          <button id="themeHCDarkBtn" class="toolbar-btn ${activeTheme === 'high-contrast-dark' ? 'active' : ''}" aria-pressed="${activeTheme === 'high-contrast-dark'}" title="High Contrast Dark Theme">High Contrast Dark</button>
          <button id="themeHCLightBtn" class="toolbar-btn ${activeTheme === 'high-contrast-light' ? 'active' : ''}" aria-pressed="${activeTheme === 'high-contrast-light'}" title="High Contrast Light Theme">High Contrast Light</button>
        </div>

        <!-- Typography Controls -->
        <div class="toolbar-group" role="group" aria-label="Text Sizing and Font Options">
          <span class="toolbar-label">Text:</span>
          <button id="fontStandardBtn" class="toolbar-btn ${activeFontSize === 'standard' ? 'active' : ''}" aria-pressed="${activeFontSize === 'standard'}" title="Standard 16px font">Standard</button>
          <button id="fontLargeBtn" class="toolbar-btn ${activeFontSize === 'large' ? 'active' : ''}" aria-pressed="${activeFontSize === 'large'}" title="Large 18px font">Large</button>
          <button id="fontXLargeBtn" class="toolbar-btn ${activeFontSize === 'xlarge' ? 'active' : ''}" aria-pressed="${activeFontSize === 'xlarge'}" title="Extra Large 22px font">XL</button>
          <button id="fontDyslexiaBtn" class="toolbar-btn ${isDyslexiaFont ? 'active' : ''}" aria-pressed="${isDyslexiaFont}" title="Toggle Dyslexia-Friendly Letter Spacing">Dyslexia Font</button>
        </div>

        <!-- Sensory & Audio Controls -->
        <div class="toolbar-group" role="group" aria-label="Sensory and Audio Options">
          <span class="toolbar-label">Sensory:</span>
          <button id="motionToggleBtn" class="toolbar-btn ${isReducedMotion ? 'active' : ''}" aria-pressed="${isReducedMotion}" title="Reduce on-screen animations">
            ${isReducedMotion ? 'Motion: Off' : 'Motion: On'}
          </button>
          <button id="bgPauseBtn" class="toolbar-btn ${is3DPaused ? 'active' : ''}" aria-pressed="${is3DPaused}" title="Pause 3D Background">
            ${is3DPaused ? '3D: Paused' : '3D: Active'}
          </button>
          <button id="soundToggleBtn" class="toolbar-btn ${isSoundEnabled ? 'active' : ''}" aria-pressed="${isSoundEnabled}" title="Mute or Unmute Sound Effects">
            ${isSoundEnabled ? '🔊 Sound: On' : '🔇 Sound: Off'}
          </button>
          <button id="voiceToggleBtn" class="toolbar-btn ${isVoiceEnabled ? 'active' : ''}" aria-pressed="${isVoiceEnabled}" title="Milo Voice Guidance">
            ${isVoiceEnabled ? '🗣️ Voice: On' : '🤫 Voice: Off'}
          </button>
          <button id="captionsToggleBtn" class="toolbar-btn ${isCaptionsEnabled ? 'active' : ''}" aria-pressed="${isCaptionsEnabled}" title="Toggle Spoken Captions Box">
            ${isCaptionsEnabled ? '💬 Captions: On' : 'Captions: Off'}
          </button>
        </div>
      </div>
    `;

    bindToolbarEvents();
  }

  function bindToolbarEvents() {
    // Theme buttons
    document.getElementById('themeDefaultBtn')?.addEventListener('click', () => {
      applyTheme('default');
      persistPreferences();
    });
    document.getElementById('themePastelBtn')?.addEventListener('click', () => {
      applyTheme('pastel-calming');
      persistPreferences();
    });
    document.getElementById('themeHCDarkBtn')?.addEventListener('click', () => {
      applyTheme('high-contrast-dark');
      persistPreferences();
    });
    document.getElementById('themeHCLightBtn')?.addEventListener('click', () => {
      applyTheme('high-contrast-light');
      persistPreferences();
    });

    // Font buttons
    document.getElementById('fontStandardBtn')?.addEventListener('click', () => {
      applyFontSize('standard');
      persistPreferences();
    });
    document.getElementById('fontLargeBtn')?.addEventListener('click', () => {
      applyFontSize('large');
      persistPreferences();
    });
    document.getElementById('fontXLargeBtn')?.addEventListener('click', () => {
      applyFontSize('xlarge');
      persistPreferences();
    });
    document.getElementById('fontDyslexiaBtn')?.addEventListener('click', () => {
      applyDyslexiaFont(!isDyslexiaFont);
      persistPreferences();
    });

    // Sensory buttons
    document.getElementById('motionToggleBtn')?.addEventListener('click', () => {
      applyReducedMotion(!isReducedMotion);
      persistPreferences();
    });
    document.getElementById('bgPauseBtn')?.addEventListener('click', () => {
      apply3DPause(!is3DPaused);
      persistPreferences();
    });
    document.getElementById('soundToggleBtn')?.addEventListener('click', () => {
      applySound(!isSoundEnabled);
      persistPreferences();
    });
    document.getElementById('voiceToggleBtn')?.addEventListener('click', () => {
      applyVoice(!isVoiceEnabled);
      persistPreferences();
    });
    document.getElementById('captionsToggleBtn')?.addEventListener('click', () => {
      applyCaptions(!isCaptionsEnabled);
      persistPreferences();
    });
  }

  function updateToolbarActiveStates() {
    // Update theme button active states
    ['Default', 'Pastel', 'HCDark', 'HCLight'].forEach(t => {
      const btn = document.getElementById(`theme${t}Btn`);
      if (btn) {
        const isAct = (t === 'Default' && activeTheme === 'default') ||
                      (t === 'Pastel' && activeTheme === 'pastel-calming') ||
                      (t === 'HCDark' && activeTheme === 'high-contrast-dark') ||
                      (t === 'HCLight' && activeTheme === 'high-contrast-light');
        btn.classList.toggle('active', isAct);
        btn.setAttribute('aria-pressed', isAct ? 'true' : 'false');
      }
    });

    // Update text size active states
    ['Standard', 'Large', 'XLarge'].forEach(s => {
      const btn = document.getElementById(`font${s}Btn`);
      if (btn) {
        const isAct = (s.toLowerCase() === activeFontSize);
        btn.classList.toggle('active', isAct);
        btn.setAttribute('aria-pressed', isAct ? 'true' : 'false');
      }
    });

    const dyslexiaBtn = document.getElementById('fontDyslexiaBtn');
    if (dyslexiaBtn) {
      dyslexiaBtn.classList.toggle('active', isDyslexiaFont);
      dyslexiaBtn.setAttribute('aria-pressed', isDyslexiaFont ? 'true' : 'false');
    }

    const motionBtn = document.getElementById('motionToggleBtn');
    if (motionBtn) {
      motionBtn.classList.toggle('active', isReducedMotion);
      motionBtn.textContent = isReducedMotion ? 'Motion: Off' : 'Motion: On';
      motionBtn.setAttribute('aria-pressed', isReducedMotion ? 'true' : 'false');
    }

    const bgBtn = document.getElementById('bgPauseBtn');
    if (bgBtn) {
      bgBtn.classList.toggle('active', is3DPaused);
      bgBtn.textContent = is3DPaused ? '3D: Paused' : '3D: Active';
      bgBtn.setAttribute('aria-pressed', is3DPaused ? 'true' : 'false');
    }

    const soundBtn = document.getElementById('soundToggleBtn');
    if (soundBtn) {
      soundBtn.classList.toggle('active', isSoundEnabled);
      soundBtn.textContent = isSoundEnabled ? '🔊 Sound: On' : '🔇 Sound: Off';
      soundBtn.setAttribute('aria-pressed', isSoundEnabled ? 'true' : 'false');
    }

    const voiceBtn = document.getElementById('voiceToggleBtn');
    if (voiceBtn) {
      voiceBtn.classList.toggle('active', isVoiceEnabled);
      voiceBtn.textContent = isVoiceEnabled ? '🗣️ Voice: On' : '🤫 Voice: Off';
      voiceBtn.setAttribute('aria-pressed', isVoiceEnabled ? 'true' : 'false');
    }

    const captionsBtn = document.getElementById('captionsToggleBtn');
    if (captionsBtn) {
      captionsBtn.classList.toggle('active', isCaptionsEnabled);
      captionsBtn.textContent = isCaptionsEnabled ? '💬 Captions: On' : 'Captions: Off';
      captionsBtn.setAttribute('aria-pressed', isCaptionsEnabled ? 'true' : 'false');
    }
  }

  return {
    init,
    applyTheme,
    applyFontSize,
    applyDyslexiaFont,
    applyReducedMotion,
    applySound,
    applyVoice,
    applyCaptions,
    apply3DPause,
    applyVideoFilter,
    getStudentId: () => currentStudentId
  };
})();

window.AccessibilityManager = AccessibilityManager;
