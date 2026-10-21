/**
 * MindVerse — Inclusive Learning Lab: Main Application Controller
 * Bootstraps accessibility, 3D/2D background, Milo companion, and global user interactions.
 */

document.addEventListener('DOMContentLoaded', async () => {
  console.info('🚀 [MindVerse] Initializing Inclusive Learning Lab frontend...');

  // 1. Accessibility Toolbar & Theme Bootstrapping
  if (window.AccessibilityManager) {
    await window.AccessibilityManager.init(1);
  }

  // 2. Background Canvas Initialization (Three.js with 2D Canvas Fallback)
  if (window.ThreeWorld) {
    window.ThreeWorld.init('bgCanvas');
  } else if (window.ThreeFallback) {
    window.ThreeFallback.init('bgCanvas');
  }

  // 3. Digital Teaching Companion Milo
  if (window.MiloCompanion) {
    window.MiloCompanion.init();
  }

  // 4. Highlight Active Navigation Link
  highlightActiveNav();

  // 5. User Gesture Audio & Speech Synthesis Unlocking
  const unlockAudio = () => {
    if (window.SoundEngine) {
      window.SoundEngine.init();
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.resume();
    }
    window.removeEventListener('click', unlockAudio);
    window.removeEventListener('keydown', unlockAudio);
    window.removeEventListener('touchstart', unlockAudio);
  };
  window.addEventListener('click', unlockAudio);
  window.addEventListener('keydown', unlockAudio);
  window.addEventListener('touchstart', unlockAudio);

  // 6. Global Sound on Button Clicks
  document.querySelectorAll('button:not(.silent), a.btn:not(.silent)').forEach(btn => {
    btn.addEventListener('click', () => {
      if (window.SoundEngine) window.SoundEngine.playClick();
    });
  });
});

function highlightActiveNav() {
  const currentPath = window.location.pathname.toLowerCase();
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    const cleanHref = href.toLowerCase();

    if (currentPath.endsWith(cleanHref) || 
       (cleanHref.includes('index.html') && (currentPath.endsWith('/') || currentPath.endsWith('/index.html')))) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}
