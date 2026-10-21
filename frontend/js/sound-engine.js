/**
 * MindVerse — Inclusive Learning Lab: Sound Engine
 * Self-contained procedural Web Audio API synthesizer.
 * Does not require external sound files. Sensory-calming and non-abrupt.
 */

const SoundEngine = (() => {
  let audioCtx = null;
  let isSoundEnabled = true;

  // Master gentle volume ceiling (sensory-friendly)
  const MASTER_VOLUME = 0.22;

  function initAudioContext() {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        audioCtx = new AudioContextClass();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume().catch(() => {});
    }
  }

  function setSoundEnabled(enabled) {
    isSoundEnabled = !!enabled;
  }

  function getSoundEnabled() {
    return isSoundEnabled;
  }

  /**
   * Play a clean, gentle tone using sine or triangle wave with smooth attack/decay envelope.
   */
  function playTone(frequency, duration = 0.3, type = 'sine', delay = 0, peakGain = MASTER_VOLUME) {
    if (!isSoundEnabled) return;
    initAudioContext();
    if (!audioCtx) return;

    try {
      const startTime = audioCtx.currentTime + delay;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = type;
      osc.frequency.setValueAtTime(frequency, startTime);

      // Smooth attack, sustain, decay envelope to avoid speaker clicks
      gain.gain.setValueAtTime(0.0001, startTime);
      gain.gain.exponentialRampToValueAtTime(peakGain, startTime + 0.04);
      gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start(startTime);
      osc.stop(startTime + duration + 0.05);

      // Clean up nodes after playback
      osc.onended = () => {
        try {
          osc.disconnect();
          gain.disconnect();
        } catch (e) {}
      };
    } catch (err) {
      console.warn('[SoundEngine] Play tone error:', err);
    }
  }

  return {
    init: initAudioContext,
    setEnabled: setSoundEnabled,
    isEnabled: getSoundEnabled,

    /**
     * Gentle C5-to-E5 two-note chime
     */
    playChime() {
      if (!isSoundEnabled) return;
      playTone(523.25, 0.28, 'sine', 0, MASTER_VOLUME * 0.9);      // C5
      playTone(659.25, 0.40, 'sine', 0.18, MASTER_VOLUME * 0.9);   // E5
    },

    /**
     * Short C-E-G-C celebratory sequence
     */
    playSuccess() {
      if (!isSoundEnabled) return;
      const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
      notes.forEach((freq, idx) => {
        playTone(freq, 0.22, 'sine', idx * 0.12, MASTER_VOLUME * 0.85);
      });
    },

    /**
     * Soft, short triangle-wave click
     */
    playClick() {
      if (!isSoundEnabled) return;
      playTone(440, 0.05, 'triangle', 0, MASTER_VOLUME * 0.4);
    },

    /**
     * Low-volume, gentle harmonic tone for errorless re-try
     */
    playGentleTryAgain() {
      if (!isSoundEnabled) return;
      playTone(392.00, 0.35, 'sine', 0, MASTER_VOLUME * 0.5); // G4
      playTone(349.23, 0.45, 'sine', 0.2, MASTER_VOLUME * 0.45); // F4
    }
  };
})();

window.SoundEngine = SoundEngine;
