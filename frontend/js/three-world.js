/**
 * MindVerse — Inclusive Learning Lab: Safe 3D Celestial Background
 * Uses Three.js r128 with robust WebGL validation and immediate 2D fallback.
 */

const ThreeWorld = (() => {
  let scene = null;
  let camera = null;
  let renderer = null;
  let animId = null;
  let starsMesh = null;
  let planetMesh = null;
  let isPaused = false;
  let contextLost = false;

  function isWebGLAvailable() {
    try {
      const testCanvas = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl')));
    } catch (e) {
      return false;
    }
  }

  function init(canvasId = 'bgCanvas') {
    // Check if user prefers reduced motion or 3D is paused
    const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const reducedMotionSetting = document.documentElement.getAttribute('data-reduced-motion') === 'true';

    if (prefersReducedMotion || reducedMotionSetting) {
      if (window.ThreeFallback) return window.ThreeFallback.init(canvasId);
      return false;
    }

    // Check WebGL and Three.js availability
    if (!isWebGLAvailable() || typeof THREE === 'undefined') {
      console.info('[ThreeWorld] WebGL or THREE.js unavailable. Gracefully switching to 2D canvas fallback.');
      if (window.ThreeFallback) return window.ThreeFallback.init(canvasId);
      return false;
    }

    const canvas = document.getElementById(canvasId);
    if (!canvas) return false;

    try {
      // 1. Scene & Camera
      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 25;

      // 2. Renderer with safety flags
      renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: false,
        powerPreference: 'low-power'
      });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

      // 3. WebGL Context Loss Handler
      canvas.addEventListener('webglcontextlost', (e) => {
        e.preventDefault();
        contextLost = true;
        stop();
        console.warn('[ThreeWorld] WebGL context lost. Switching to 2D fallback.');
        if (window.ThreeFallback) window.ThreeFallback.init(canvasId);
      }, false);

      // 4. Soft Drifting Stars Geometry
      const starsCount = 120;
      const starsGeometry = new THREE.BufferGeometry();
      const positions = new Float32Array(starsCount * 3);
      for (let i = 0; i < starsCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 60;
        positions[i + 1] = (Math.random() - 0.5) * 40;
        positions[i + 2] = (Math.random() - 0.5) * 30;
      }
      starsGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

      const starsMaterial = new THREE.PointsMaterial({
        color: 0x3A86C8,
        size: 0.8,
        transparent: true,
        opacity: 0.4
      });
      starsMesh = new THREE.Points(starsGeometry, starsMaterial);
      scene.add(starsMesh);

      // 5. Gentle Drifting Pastel Celestial Sphere
      const planetGeometry = new THREE.SphereGeometry(3.5, 24, 24);
      const planetMaterial = new THREE.MeshBasicMaterial({
        color: 0x2A9D8F,
        wireframe: true,
        transparent: true,
        opacity: 0.15
      });
      planetMesh = new THREE.Mesh(planetGeometry, planetMaterial);
      planetMesh.position.set(16, -6, -5);
      scene.add(planetMesh);

      // 6. Event listeners
      window.addEventListener('resize', onResize);
      document.addEventListener('visibilitychange', onVisibilityChange);

      start();
      return true;
    } catch (err) {
      console.warn('[ThreeWorld] Failed to initialize 3D scene:', err);
      if (window.ThreeFallback) return window.ThreeFallback.init(canvasId);
      return false;
    }
  }

  function onResize() {
    if (!camera || !renderer) return;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }

  function onVisibilityChange() {
    if (document.hidden) {
      stop();
    } else if (!isPaused && !contextLost) {
      start();
    }
  }

  function render() {
    if (isPaused || contextLost || !renderer || !scene || !camera) return;

    if (starsMesh) {
      starsMesh.rotation.y += 0.0003;
    }
    if (planetMesh) {
      planetMesh.rotation.y += 0.001;
      planetMesh.rotation.x += 0.0005;
    }

    renderer.render(scene, camera);
    animId = requestAnimationFrame(render);
  }

  function start() {
    if (!animId && !isPaused && !contextLost) {
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
    // Sync with fallback if fallback is running
    if (window.ThreeFallback) window.ThreeFallback.setPaused(paused);
  }

  function dispose() {
    stop();
    window.removeEventListener('resize', onResize);
    document.removeEventListener('visibilitychange', onVisibilityChange);
    if (renderer) {
      renderer.dispose();
      renderer = null;
    }
  }

  return {
    init,
    start,
    stop,
    setPaused,
    dispose
  };
})();

window.ThreeWorld = ThreeWorld;
