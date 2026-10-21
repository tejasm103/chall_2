/**
 * MindVerse — Inclusive Learning Lab: Centralized API Client Module
 * Communicates with the Flask REST API backend with offline fallbacks.
 */

const MindVerseAPI = (() => {
  // Determine API base URL dynamically
  function getBaseUrl() {
    if (window.MINDVERSE_API_URL) {
      return window.MINDVERSE_API_URL.replace(/\/+$/, '');
    }
    const stored = localStorage.getItem('mindverse_api_url');
    if (stored) {
      return stored.replace(/\/+$/, '');
    }
    // If running directly on the unified live server (port 5000)
    if (window.location.port === '5000') {
      return '/api';
    }
    // Default local Flask backend when running separate frontend server
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://127.0.0.1:5000/api';
    }
    // Production deployment relative URL or configured domain
    return '/api';
  }

  async function request(endpoint, options = {}) {
    const url = `${getBaseUrl()}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...(options.headers || {})
      }
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.error || `Request failed with status ${response.status}`);
      }
      return data;
    } catch (err) {
      console.warn(`[MindVerseAPI] Error communicating with ${url}:`, err.message);
      // Graceful offline fallback return
      return {
        success: false,
        offline: true,
        error: err.message
      };
    }
  }

  return {
    getBaseUrl,

    // Health
    async checkHealth() {
      return request('/health');
    },

    // Students
    async getStudents() {
      const res = await request('/students');
      if (res.success) return res.students;
      // Offline fallback
      return [
        { id: 1, name: "Alex (Local)", avatar: "robot-milo", learning_level: 1, preferred_theme: "default", font_size: "standard", voice_enabled: 1, sound_enabled: 1, reduced_motion: 0 }
      ];
    },

    async getStudent(id) {
      const res = await request(`/students/${id}`);
      if (res.success) return res.student;
      return { id, name: "Alex (Local)", learning_level: 1, preferred_theme: "default" };
    },

    async createStudent(studentData) {
      return request('/students', {
        method: 'POST',
        body: JSON.stringify(studentData)
      });
    },

    async updateStudent(id, studentData) {
      return request(`/students/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(studentData)
      });
    },

    // Preferences
    async getPreferences(studentId) {
      const res = await request(`/preferences/${studentId}`);
      if (res.success) return res.preferences;
      // Local fallback
      return {
        student_id: studentId,
        preferred_theme: localStorage.getItem('mindverse_theme') || 'default',
        font_size: localStorage.getItem('mindverse_font_size') || 'standard',
        voice_enabled: localStorage.getItem('mindverse_voice') !== '0' ? 1 : 0,
        sound_enabled: localStorage.getItem('mindverse_sound') !== '0' ? 1 : 0,
        reduced_motion: localStorage.getItem('mindverse_motion') === '1' ? 1 : 0
      };
    },

    async savePreferences(studentId, prefs) {
      // Always store locally first for instant offline readiness
      if (prefs.preferred_theme) localStorage.setItem('mindverse_theme', prefs.preferred_theme);
      if (prefs.font_size) localStorage.setItem('mindverse_font_size', prefs.font_size);
      if (prefs.voice_enabled !== undefined) localStorage.setItem('mindverse_voice', prefs.voice_enabled ? '1' : '0');
      if (prefs.sound_enabled !== undefined) localStorage.setItem('mindverse_sound', prefs.sound_enabled ? '1' : '0');
      if (prefs.reduced_motion !== undefined) localStorage.setItem('mindverse_motion', prefs.reduced_motion ? '1' : '0');

      return request(`/preferences/${studentId}`, {
        method: 'PUT',
        body: JSON.stringify(prefs)
      });
    },

    // Lessons
    async getLessons(level = null, subject = null) {
      let query = '';
      const params = [];
      if (level) params.push(`level=${encodeURIComponent(level)}`);
      if (subject) params.push(`subject=${encodeURIComponent(subject)}`);
      if (params.length > 0) query = `?${params.join('&')}`;

      const res = await request(`/lessons${query}`);
      if (res.success) return res.lessons;
      return [];
    },

    async getLessonDetail(slug) {
      const res = await request(`/lessons/${encodeURIComponent(slug)}`);
      if (res.success) return res.lesson;
      return null;
    },

    // Progress
    async getProgress(studentId) {
      const res = await request(`/progress/${studentId}`);
      if (res.success) return res.progress;
      return [];
    },

    async saveProgress(progressData) {
      return request('/progress', {
        method: 'POST',
        body: JSON.stringify(progressData)
      });
    },

    // Games
    async getGames() {
      const res = await request('/games');
      if (res.success) return res.games;
      return [];
    },

    async saveGameScore(scoreData) {
      return request('/game-scores', {
        method: 'POST',
        body: JSON.stringify(scoreData)
      });
    },

    // Routines
    async getRoutines(studentId) {
      const res = await request(`/routines/${studentId}`);
      if (res.success) return res.routines;
      return [];
    },

    async createRoutine(routineData) {
      return request('/routines', {
        method: 'POST',
        body: JSON.stringify(routineData)
      });
    },

    async updateRoutine(routineId, routineData) {
      return request(`/routines/${routineId}`, {
        method: 'PATCH',
        body: JSON.stringify(routineData)
      });
    },

    async deleteRoutine(routineId) {
      return request(`/routines/${routineId}`, {
        method: 'DELETE'
      });
    },

    // Videos
    async getVideos(category = null) {
      const query = category ? `?category=${encodeURIComponent(category)}` : '';
      const res = await request(`/videos${query}`);
      if (res.success) return res.videos;
      return [];
    },

    async getVideoDetail(videoId) {
      const res = await request(`/videos/${videoId}`);
      if (res.success) return res.video;
      return null;
    },

    async trackVideoPlay(videoId) {
      return request(`/videos/${videoId}/play`, { method: 'POST' });
    },

    // Computer Skills
    async getComputerSkillsActivities() {
      const res = await request('/computer-skills/activities');
      if (res.success) return res.activities;
      return [];
    },

    async saveComputerSkillProgress(data) {
      return request('/computer-skills/progress', {
        method: 'POST',
        body: JSON.stringify(data)
      });
    },

    // Caregiver
    async getCaregiverStats(studentId) {
      const res = await request(`/caregiver/stats/${studentId}`);
      if (res.success) return res.stats;
      return null;
    },

    async resetStudentProgress(studentId) {
      return request(`/caregiver/reset/${studentId}`, {
        method: 'POST',
        body: JSON.stringify({ confirm: true })
      });
    },

    async loginCaregiver(pin, password) {
      return request('/caregiver/login', {
        method: 'POST',
        body: JSON.stringify({ pin, password })
      });
    }
  };
})();

window.MindVerseAPI = MindVerseAPI;
