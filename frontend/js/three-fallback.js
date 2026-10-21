/**
 * MindVerse — Inclusive Learning Lab: 2D Canvas Sensory Background Fallback
 * Works smoothly on any device without WebGL or Three.js dependencies.
 * Extremely lightweight, non-distracting, sensory-calming celestial background.
 */

const ThreeFallback = (() => {
  let canvas = null;
  let ctx = null;
  let animId = null;
  let stars = [];
  let isPaused = false;
  let width = 0;
  let height = 0;

  function init(canvasId = 'bgCanvas') {
    canvas = document.getElementById(canvasId);
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = canvasId;
      document.body.prepend(canvas);
    }

    ctx = canvas.getContext('2d');
    if (!ctx) return false;

    resize();
    createStars(45);

    window.addEventListener('resize', onResize);
    document.addEventListener('visibilitychange', onVisibilityChange);

    start();
    return true;
  }

  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    if (canvas) {
      canvas.width = width;
      canvas.height = height;
    }
  }

  function onResize() {
    resize();
  }

  function onVisibilityChange() {
    if (document.hidden) {
      stop();
    } else if (!isPaused) {
      start();
    }
  }

  function createStars(count) {
    stars = [];
    for (let i = 0; i < count; i++) {
      stars.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.8 + 0.8,
        alpha: Math.random() * 0.5 + 0.2,
        speed: Math.random() * 0.005 + 0.002
      });
    }
  }

  function render(time) {
    if (isPaused || !ctx) return;

    // Draw calming background gradient
    const theme = document.documentElement.getAttribute('data-theme') || 'default';
    let grad;

    if (theme === 'high-contrast-dark') {
      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, width, height);
      // Gentle crisp stars
      ctx.fillStyle = '#FFD700';
      for (const s of stars) {
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.radius * 0.9, 0, Math.PI * 2);
        ctx.fill();
      }
      return;
    } else if (theme === 'pastel-calming') {
      grad = ctx.createLinearGradient(0, 0, width, height);
      grad.addColorStop(0, '#FAF7F2');
      grad.addColorStop(1, '#EDE8DF');
    } else if (theme === 'high-contrast-light') {
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, width, height);
      return;
    } else {
      // Default soft sky gradient
      grad = ctx.createLinearGradient(0, 0, width, height);
      grad.addColorStop(0, '#F0F8FF');
      grad.addColorStop(0.5, '#E6F4EA');
      grad.addColorStop(1, '#F8FAFC');
    }

    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, width, height);

    // Draw soft twinkling stars
    for (const s of stars) {
      s.alpha += Math.sin(time * s.speed) * 0.008;
      const displayAlpha = Math.max(0.1, Math.min(0.65, s.alpha));
      ctx.fillStyle = `rgba(58, 134, 200, ${displayAlpha})`;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
      ctx.fill();
    }

    animId = requestAnimationFrame(render);
  }

  function start() {
    if (!animId && !isPaused) {
      animId = requestAnimationFrame(render);
    }
  }

  function stop() {
    if (animId) {
      cancelAnimationFrame(animId);
      animId = null;
    }
  }

  function setPaused(paused) {
    isPaused = !!paused;
    if (isPaused) {
      stop();
    } else {
      start();
    }
  }

  function dispose() {
    stop();
    window.removeEventListener('resize', onResize);
    document.removeEventListener('visibilitychange', onVisibilityChange);
  }

  return {
    init,
    start,
    stop,
    setPaused,
    dispose
  };
})();

window.ThreeFallback = ThreeFallback;
