/**
 * MindVerse — Inclusive Learning Lab: Visual Daily Routine Engine
 * Manages pictorial schedules, step checkboxes, custom task builder, and backend persistence.
 */

const DailyRoutineManager = (() => {
  let studentId = 1;
  let allRoutines = [];
  let currentCategory = 'morning';

  async function init() {
    studentId = window.AccessibilityManager ? window.AccessibilityManager.getStudentId() : 1;
    await loadRoutines();
    renderCategoryTabs();
    renderCurrentRoutine();
    bindCustomTaskForm();
  }

  async function loadRoutines() {
    if (window.MindVerseAPI) {
      allRoutines = await window.MindVerseAPI.getRoutines(studentId);
    }
    // Fallback if empty or offline
    if (!allRoutines || allRoutines.length === 0) {
      allRoutines = [
        {
          id: 101,
          student_id: studentId,
          title: "Morning Routine",
          category: "morning",
          steps: [
            { id: "m1", title: "Wake up gently", icon: "sun", completed: true, time: "7:00 AM" },
            { id: "m2", title: "Drink a glass of water", icon: "cup", completed: true, time: "7:15 AM" },
            { id: "m3", title: "Brush teeth", icon: "toothbrush", completed: false, time: "7:25 AM" },
            { id: "m4", title: "Get dressed in comfy clothes", icon: "shirt", completed: false, time: "7:35 AM" },
            { id: "m5", title: "Eat healthy breakfast", icon: "apple", completed: false, time: "7:45 AM" }
          ]
        },
        {
          id: 102,
          student_id: studentId,
          title: "Hygiene & Clean Hands",
          category: "hygiene",
          steps: [
            { id: "h1", title: "Wash hands with warm soap", icon: "soap", completed: true, time: "Anytime" },
            { id: "h2", title: "Brush teeth for 2 minutes", icon: "toothbrush", completed: false, time: "Morning/Night" },
            { id: "h3", title: "Comb hair gently", icon: "comb", completed: false, time: "Morning" }
          ]
        },
        {
          id: 103,
          student_id: studentId,
          title: "School Day Schedule",
          category: "school",
          steps: [
            { id: "s1", title: "Pack school bag & water bottle", icon: "backpack", completed: false, time: "8:00 AM" },
            { id: "s2", title: "Put on shoes and jacket", icon: "shoe", completed: false, time: "8:15 AM" },
            { id: "s3", title: "Say hello to teacher & friends", icon: "hand-wave", completed: false, time: "8:45 AM" }
          ]
        },
        {
          id: 104,
          student_id: studentId,
          title: "Peaceful Bedtime",
          category: "bedtime",
          steps: [
            { id: "b1", title: "Put away toys", icon: "box", completed: false, time: "8:00 PM" },
            { id: "b2", title: "Cozy pajamas on", icon: "moon", completed: false, time: "8:15 PM" },
            { id: "b3", title: "Bedtime story time", icon: "book", completed: false, time: "8:30 PM" },
            { id: "b4", title: "Three deep calming breaths", icon: "wind", completed: false, time: "8:45 PM" }
          ]
        }
      ];
    }
  }

  function renderCategoryTabs() {
    const tabsContainer = document.getElementById('routineCategoryTabs');
    if (!tabsContainer) return;

    const categories = [
      { id: 'morning', label: '☀️ Morning' },
      { id: 'hygiene', label: '🧼 Hygiene' },
      { id: 'school', label: '🎒 School' },
      { id: 'bedtime', label: '🌙 Bedtime' },
      { id: 'custom', label: '⭐ Custom' }
    ];

    tabsContainer.innerHTML = categories.map(cat => `
      <button class="btn btn-outline category-tab-btn ${cat.id === currentCategory ? 'active' : ''}" data-cat="${cat.id}" style="min-height: 44px; font-size: 0.95rem;">
        ${cat.label}
      </button>
    `).join('');

    tabsContainer.querySelectorAll('.category-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        tabsContainer.querySelectorAll('.category-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCategory = btn.getAttribute('data-cat');
        if (window.SoundEngine) window.SoundEngine.playClick();
        renderCurrentRoutine();
      });
    });
  }

  function renderCurrentRoutine() {
    const listContainer = document.getElementById('routineListContainer');
    const progressText = document.getElementById('routineProgressSummary');
    if (!listContainer) return;

    // Filter routines for category
    const activeRoutine = allRoutines.find(r => r.category === currentCategory) || allRoutines[0];

    if (!activeRoutine) {
      listContainer.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: 24px;">No routines found for this category yet.</p>';
      return;
    }

    const steps = activeRoutine.steps || [];
    const completedCount = steps.filter(s => s.completed).length;
    const percent = steps.length > 0 ? Math.round((completedCount / steps.length) * 100) : 0;

    if (progressText) {
      progressText.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
          <span style="font-weight: 700;">${activeRoutine.title}</span>
          <span style="font-weight: 800; color: var(--color-primary);">${completedCount} of ${steps.length} completed (${percent}%)</span>
        </div>
        <div style="height: 12px; background: var(--bg-surface); border-radius: var(--radius-full); overflow: hidden;">
          <div style="height: 100%; width: ${percent}%; background: var(--color-secondary); transition: width 0.3s ease;"></div>
        </div>
      `;
    }

    listContainer.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 12px;">
        ${steps.map((s, idx) => `
          <div class="card" style="display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-left: 6px solid ${s.completed ? '#10B981' : 'var(--color-primary)'}; background: ${s.completed ? '#F0FDF4' : 'var(--bg-card)'};">
            <div style="display: flex; align-items: center; gap: 16px;">
              <input type="checkbox" id="stepCheck_${idx}" class="routine-step-checkbox" data-index="${idx}" ${s.completed ? 'checked' : ''} style="width: 24px; height: 24px; accent-color: var(--color-secondary); cursor: pointer;" aria-label="Mark task '${s.title}' complete" />
              <div>
                <label for="stepCheck_${idx}" style="font-size: 1.1rem; font-weight: 700; cursor: pointer; text-decoration: ${s.completed ? 'line-through' : 'none'}; color: ${s.completed ? '#047857' : 'var(--text-main)'};">
                  ${s.title}
                </label>
                ${s.time ? `<div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">⏰ ${s.time}</div>` : ''}
              </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <button class="btn btn-outline speak-step-btn" data-text="${s.title}" style="min-height: 38px; min-width: 38px; padding: 6px 12px; font-size: 0.9rem;" title="Listen to task instruction" aria-label="Listen to step instruction: ${s.title}">
                🔊
              </button>
              <button class="btn btn-outline delete-step-btn" data-index="${idx}" style="min-height: 38px; min-width: 38px; padding: 6px 12px; font-size: 0.9rem; color: #EF4444;" title="Delete this task" aria-label="Delete step ${s.title}">
                🗑️
              </button>
            </div>
          </div>
        `).join('')}
      </div>
    `;

    // Bind checkboxes
    listContainer.querySelectorAll('.routine-step-checkbox').forEach(cb => {
      cb.addEventListener('change', async (e) => {
        const idx = parseInt(cb.getAttribute('data-index'), 10);
        steps[idx].completed = cb.checked;

        if (cb.checked) {
          if (window.SoundEngine) window.SoundEngine.playChime();
          if (window.MiloCompanion) window.MiloCompanion.celebrate(`Good work completing: ${steps[idx].title}!`);
        }

        renderCurrentRoutine();
        saveRoutineChanges(activeRoutine);
      });
    });

    // Bind speech buttons
    listContainer.querySelectorAll('.speak-step-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const text = btn.getAttribute('data-text');
        if (window.MiloCompanion) window.MiloCompanion.speak(text);
      });
    });

    // Bind delete step buttons
    listContainer.querySelectorAll('.delete-step-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.getAttribute('data-index'), 10);
        steps.splice(idx, 1);
        renderCurrentRoutine();
        saveRoutineChanges(activeRoutine);
      });
    });
  }

  async function saveRoutineChanges(routine) {
    if (window.MindVerseAPI && routine.id) {
      await window.MindVerseAPI.updateRoutine(routine.id, {
        title: routine.title,
        category: routine.category,
        steps: routine.steps
      });
    }
  }

  function bindCustomTaskForm() {
    const addBtn = document.getElementById('addRoutineTaskBtn');
    const taskInput = document.getElementById('newRoutineTaskInput');
    const timeInput = document.getElementById('newRoutineTimeInput');

    if (!addBtn || !taskInput) return;

    addBtn.addEventListener('click', async () => {
      const title = taskInput.value.trim();
      if (!title) return;

      const time = timeInput ? timeInput.value.trim() : '';

      let activeRoutine = allRoutines.find(r => r.category === currentCategory);
      if (!activeRoutine) {
        activeRoutine = {
          student_id: studentId,
          title: `${currentCategory.toUpperCase()} Routine`,
          category: currentCategory,
          steps: []
        };
        allRoutines.push(activeRoutine);
      }

      activeRoutine.steps.push({
        id: `custom_${Date.now()}`,
        title: title,
        time: time,
        completed: false
      });

      taskInput.value = '';
      if (timeInput) timeInput.value = '';

      if (window.SoundEngine) window.SoundEngine.playClick();
      renderCurrentRoutine();
      saveRoutineChanges(activeRoutine);
    });
  }

  return {
    init
  };
})();

window.DailyRoutineManager = DailyRoutineManager;
