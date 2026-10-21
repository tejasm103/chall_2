/**
 * MindVerse — Inclusive Learning Lab: 3D Celestial Web World
 * Powered by Three.js with interactive camera parallax, floating geometry,
 * interactive click sparkles, and dynamic theme synchronization.
 */

const ThreeWorld = (() => {
  let scene = null;
  let camera = null;
  let renderer = null;
  let animId = null;

  // 3D Objects
  let starsMesh = null;
  let floatingGroup = null;
  let icosahedronMesh = null;
  let torusMesh = null;
  let dodecahedronMesh = null;
  let particleRibbonMesh = null;
  let clickParticles = [];

  // Interaction State
  let mouseX = 0;
  let mouseY = 0;
  let targetCamX = 0;
  let targetCamY = 0;
  let isPaused = false;
  let isReducedMotion = false;
  let contextLost = false;
  let currentTheme = 'default';

  // Theme Color Configurations
  const THEME_COLORS = {
    'default': {
      bg: 0xEEF6FC,
      stars: 0x3A86C8,
      ico: 0x2A9D8F,
      torus: 0x48CAE4,
      dodec: 0xFFD166,
      ribbon: 0x3A86C8
    },
    'high-contrast-dark': {
      bg: 0x05070A,
      stars: 0xFFD700,
      ico: 0x00E5FF,
      torus: 0xFFD700,
      dodec: 0x00E5FF,
      ribbon: 0xFFD700
    },
    'high-contrast-light': {
      bg: 0xF4F7FA,
      stars: 0x002D62,
      ico: 0x004080,
      torus: 0x002D62,
      dodec: 0x004080,
      ribbon: 0x002D62
    },
    'pastel-calming': {
      bg: 0xF7F4EE,
      stars: 0x78998D,
      ico: 0x9D97B5,
      torus: 0xA7C4BC,
      dodec: 0xE9C46A,
      ribbon: 0x9D97B5
    }
  };

  function isWebGLAvailable() {
    try {
      const testCanvas = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl')));
    } catch (e) {
      return false;
    }
  }

  function init(canvasId = 'bgCanvas') {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return false;

    // Check if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const reducedMotionSetting = document.documentElement.getAttribute('data-reduced-motion') === 'true';
    isReducedMotion = prefersReducedMotion || reducedMotionSetting;

    // Ensure THREE.js is loaded
    if (typeof THREE === 'undefined') {
      console.warn('[ThreeWorld] THREE library not loaded. Checking 2D fallback.');
      if (window.ThreeFallback) return window.ThreeFallback.init(canvasId);
      return false;
    }

    if (!isWebGLAvailable()) {
      console.warn('[ThreeWorld] WebGL unavailable. Checking 2D fallback.');
      if (window.ThreeFallback) return window.ThreeFallback.init(canvasId);
      return false;
    }

    try {
      // 1. Scene & Camera
      scene = new THREE.Scene();
      const themeConfig = THEME_COLORS[currentTheme] || THEME_COLORS['default'];
      scene.background = new THREE.Color(themeConfig.bg);

      camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 24;

      // 2. High-performance WebGL Renderer
      renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: false,
        antialias: true,
        powerPreference: 'default'
      });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));

      // 3. WebGL Context Loss Handler
      canvas.addEventListener('webglcontextlost', (e) => {
        e.preventDefault();
        contextLost = true;
        stop();
        console.warn('[ThreeWorld] WebGL context lost.');
      }, false);

      canvas.addEventListener('webglcontextrestored', () => {
        contextLost = false;
        init(canvasId);
      }, false);

      // 4. Layer 1: Multi-depth 3D Starfield
      const starsCount = 280;
      const starsGeometry = new THREE.BufferGeometry();
      const positions = new Float32Array(starsCount * 3);
      const scales = new Float32Array(starsCount);

      for (let i = 0; i < starsCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 80;
        positions[i + 1] = (Math.random() - 0.5) * 55;
        positions[i + 2] = (Math.random() - 0.5) * 45;
        scales[i / 3] = Math.random() * 0.8 + 0.4;
      }
      starsGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      starsGeometry.setAttribute('scale', new THREE.BufferAttribute(scales, 1));

      const starsMaterial = new THREE.PointsMaterial({
        color: themeConfig.stars,
        size: 0.9,
        transparent: true,
        opacity: 0.55
      });
      starsMesh = new THREE.Points(starsGeometry, starsMaterial);
      scene.add(starsMesh);

      // 5. Layer 2: Floating 3D Geometric Group
      floatingGroup = new THREE.Group();

      // Object A: Soft Wireframe Icosahedron (Top-Right)
      const icoGeo = new THREE.IcosahedronGeometry(3.2, 0);
      const icoMat = new THREE.MeshBasicMaterial({
        color: themeConfig.ico,
        wireframe: true,
        transparent: true,
        opacity: 0.28
      });
      icosahedronMesh = new THREE.Mesh(icoGeo, icoMat);
      icosahedronMesh.position.set(16, 7, -6);
      floatingGroup.add(icosahedronMesh);

      // Object B: Gentle Glowing Torus Ring (Bottom-Left)
      const torusGeo = new THREE.TorusGeometry(3.8, 0.35, 12, 36);
      const torusMat = new THREE.MeshBasicMaterial({
        color: themeConfig.torus,
        wireframe: true,
        transparent: true,
        opacity: 0.22
      });
      torusMesh = new THREE.Mesh(torusGeo, torusMat);
      torusMesh.position.set(-15, -7, -4);
      floatingGroup.add(torusMesh);

      // Object C: Floating Dodecahedron (Center-Right Floating Orb)
      const dodecGeo = new THREE.DodecahedronGeometry(2.0);
      const dodecMat = new THREE.MeshBasicMaterial({
        color: themeConfig.dodec,
        wireframe: true,
        transparent: true,
        opacity: 0.25
      });
      dodecahedronMesh = new THREE.Mesh(dodecGeo, dodecMat);
      dodecahedronMesh.position.set(12, -8, -2);
      floatingGroup.add(dodecahedronMesh);

      // Object D: Gentle Orbiting Particle Ring / Ribbon
      const ribbonCount = 120;
      const ribbonGeo = new THREE.BufferGeometry();
      const ribbonPos = new Float32Array(ribbonCount * 3);
      for (let i = 0; i < ribbonCount; i++) {
        const theta = (i / ribbonCount) * Math.PI * 2;
        const rad = 18 + Math.sin(theta * 3) * 1.5;
        ribbonPos[i * 3] = Math.cos(theta) * rad;
        ribbonPos[i * 3 + 1] = Math.sin(theta) * rad * 0.45;
        ribbonPos[i * 3 + 2] = Math.sin(theta * 2) * 5;
      }
      ribbonGeo.setAttribute('position', new THREE.BufferAttribute(ribbonPos, 3));
      const ribbonMat = new THREE.PointsMaterial({
        color: themeConfig.ribbon,
        size: 0.75,
        transparent: true,
        opacity: 0.35
      });
      particleRibbonMesh = new THREE.Points(ribbonGeo, ribbonMat);
      floatingGroup.add(particleRibbonMesh);

      scene.add(floatingGroup);

      // 6. Interactive Event Listeners
      window.addEventListener('resize', onResize);
      window.addEventListener('mousemove', onMouseMove, { passive: true });
      window.addEventListener('pointerdown', onPointerDown, { passive: true });
      document.addEventListener('visibilitychange', onVisibilityChange);

      // Detect active HTML theme attribute if set
      const docTheme = document.documentElement.getAttribute('data-theme');
      if (docTheme) updateTheme(docTheme);

      start();
      console.info('✨ [ThreeWorld] 3D Website initialized successfully with Three.js.');
      return true;
    } catch (err) {
      console.warn('[ThreeWorld] 3D Initialization error:', err);
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

  function onMouseMove(e) {
    if (isReducedMotion) return;
    mouseX = (e.clientX / window.innerWidth) * 2 - 1;
    mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    targetCamX = mouseX * 2.5;
    targetCamY = mouseY * 1.8;
  }

  function onPointerDown(e) {
    if (!scene || isReducedMotion) return;

    // Create a burst of 3D sparkle particles in space
    const count = 10;
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(count * 3);
    const vels = [];

    // Map screen x, y roughly to world coordinates at z = 0
    const normX = (e.clientX / window.innerWidth) * 2 - 1;
    const normY = -(e.clientY / window.innerHeight) * 2 + 1;
    const originX = normX * 18;
    const originY = normY * 11;

    for (let i = 0; i < count; i++) {
      pos[i * 3] = originX;
      pos[i * 3 + 1] = originY;
      pos[i * 3 + 2] = 2;

      vels.push({
        vx: (Math.random() - 0.5) * 0.12,
        vy: (Math.random() - 0.5) * 0.12,
        vz: (Math.random() - 0.5) * 0.08,
        life: 1.0
      });
    }

    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    const mat = new THREE.PointsMaterial({
      color: 0xFFD166,
      size: 1.1,
      transparent: true,
      opacity: 0.9
    });

    const mesh = new THREE.Points(geo, mat);
    scene.add(mesh);
    clickParticles.push({ mesh, vels, geo, mat });
  }

  function updateClickParticles() {
    for (let i = clickParticles.length - 1; i >= 0; i--) {
      const p = clickParticles[i];
      const positions = p.geo.attributes.position.array;
      let allDead = true;

      for (let j = 0; j < p.vels.length; j++) {
        const vel = p.vels[j];
        if (vel.life > 0) {
          allDead = false;
          positions[j * 3] += vel.vx;
          positions[j * 3 + 1] += vel.vy;
          positions[j * 3 + 2] += vel.vz;
          vel.life -= 0.025;
        }
      }
      p.geo.attributes.position.needsUpdate = true;
      p.mat.opacity = Math.max(0, p.mat.opacity - 0.025);

      if (allDead || p.mat.opacity <= 0.05) {
        scene.remove(p.mesh);
        p.geo.dispose();
        p.mat.dispose();
        clickParticles.splice(i, 1);
      }
    }
  }

  function onVisibilityChange() {
    if (document.hidden) {
      stop();
    } else if (!isPaused && !contextLost) {
      start();
    }
  }

  function updateTheme(themeName) {
    currentTheme = themeName;
    const config = THEME_COLORS[themeName] || THEME_COLORS['default'];
    if (scene) {
      scene.background = new THREE.Color(config.bg);
    }
    if (starsMesh && starsMesh.material) {
      starsMesh.material.color.setHex(config.stars);
    }
    if (icosahedronMesh && icosahedronMesh.material) {
      icosahedronMesh.material.color.setHex(config.ico);
    }
    if (torusMesh && torusMesh.material) {
      torusMesh.material.color.setHex(config.torus);
    }
    if (dodecahedronMesh && dodecahedronMesh.material) {
      dodecahedronMesh.material.color.setHex(config.dodec);
    }
    if (particleRibbonMesh && particleRibbonMesh.material) {
      particleRibbonMesh.material.color.setHex(config.ribbon);
    }
  }

  function render() {
    if (isPaused || contextLost || !renderer || !scene || !camera) return;

    // Smooth Camera Parallax Damping
    if (!isReducedMotion) {
      camera.position.x += (targetCamX - camera.position.x) * 0.04;
      camera.position.y += (targetCamY - camera.position.y) * 0.04;
      camera.lookAt(0, 0, 0);

      // Subtle ambient 3D rotations
      if (starsMesh) {
        starsMesh.rotation.y += 0.0003;
        starsMesh.rotation.x += 0.0001;
      }
      if (icosahedronMesh) {
        icosahedronMesh.rotation.y += 0.003;
        icosahedronMesh.rotation.x += 0.002;
      }
      if (torusMesh) {
        torusMesh.rotation.x += 0.004;
        torusMesh.rotation.y += 0.002;
      }
      if (dodecahedronMesh) {
        dodecahedronMesh.rotation.y += 0.0025;
        dodecahedronMesh.rotation.z += 0.0015;
      }
      if (particleRibbonMesh) {
        particleRibbonMesh.rotation.z += 0.001;
      }
      if (floatingGroup) {
        floatingGroup.rotation.y = Math.sin(Date.now() * 0.0004) * 0.05;
      }
    } else {
      // Ultra-gentle resting pose under reduced motion
      camera.position.set(0, 0, 24);
      camera.lookAt(0, 0, 0);
      if (starsMesh) starsMesh.rotation.y += 0.00005;
    }

    // Update active click particle sparks
    if (clickParticles.length > 0) {
      updateClickParticles();
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
  }

  function setReducedMotion(reduced) {
    isReducedMotion = !!reduced;
  }

  return {
    init,
    start,
    stop,
    setPaused,
    setReducedMotion,
    updateTheme
  };
})();

window.ThreeWorld = ThreeWorld;
