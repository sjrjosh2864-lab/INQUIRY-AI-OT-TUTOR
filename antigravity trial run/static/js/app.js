/**
 * INQUIRY OT Tutor - Main Client Application Logic
 * Implements 6 Learning Modes, OT Reasoning Pathway, Socratic Guidance,
 * MGRU Syllabus Tree, Weakness Tracking & RAG Document Management.
 */

// Application State
const state = {
  currentMode: 'inquiry',
  activeCaseId: 'cva_mca_case_1',
  currentCaseStep: 1,
  examMarks: 5,
  isLoading: false,
  studentProfile: null,
  syllabusData: null,
  pathwayStep: 1
};

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const btnSend = document.getElementById('btnSend');
const btnRequestHint = document.getElementById('btnRequestHint');
const modeTabs = document.querySelectorAll('.mode-tab');
const modeBanner = document.getElementById('modeBanner');
const bannerBadge = document.getElementById('bannerBadge');
const bannerDescription = document.getElementById('bannerDescription');
const modeToolbar = document.getElementById('modeToolbar');
const pathwayTicker = document.getElementById('pathwayTicker');
const engineBadgeText = document.getElementById('engineBadgeText');

// Modals
const modalSettings = document.getElementById('modalSettings');
const modalRAG = document.getElementById('modalRAG');
const modalAnalytics = document.getElementById('modalAnalytics');

// Initialize on Load
document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  loadConfig();
  loadSyllabus();
  loadCases();
  loadStudentDashboard();
  updateModeUI(state.currentMode);
});

// Event Listeners Setup
function setupEventListeners() {
  // Mode switcher tabs
  modeTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const mode = tab.dataset.mode;
      switchMode(mode);
    });
  });

  // Chat submit form
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage();
  });

  // Textarea auto-resize & keyboard shortcuts
  userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 140) + 'px';
  });

  // Hint button
  btnRequestHint.addEventListener('click', () => {
    quickAsk("Please give me a progressive clinical hint for this condition.");
  });

  // Top nav modal buttons
  document.getElementById('btnOpenSettings').addEventListener('click', () => openModal('modalSettings'));
  document.getElementById('btnOpenRAG').addEventListener('click', () => {
    openModal('modalRAG');
    loadRAGSources();
  });
  document.getElementById('btnOpenAnalytics').addEventListener('click', () => {
    openModal('modalAnalytics');
    renderFullAnalyticsModal();
  });

  // Settings form submission
  document.getElementById('settingsForm').addEventListener('submit', handleSettingsSubmit);

  // Provider dropdown change
  const apiProviderSelect = document.getElementById('apiProvider');
  if (apiProviderSelect) {
    apiProviderSelect.addEventListener('change', (e) => {
      toggleProviderFields(e.target.value);
    });
  }

  // Test AI Connection button
  const btnTestConn = document.getElementById('btnTestConnection');
  if (btnTestConn) {
    btnTestConn.addEventListener('click', handleTestConnection);
  }

  // Toggle API key visibility
  const btnToggleVis = document.getElementById('btnToggleKeyVis');
  if (btnToggleVis) {
    btnToggleVis.addEventListener('click', () => {
      const keyInput = document.getElementById('apiKey');
      if (keyInput.type === 'password') {
        keyInput.type = 'text';
        btnToggleVis.textContent = '🔒';
      } else {
        keyInput.type = 'password';
        btnToggleVis.textContent = '👁️';
      }
    });
  }

  // RAG custom notes upload form
  document.getElementById('uploadNotesForm').addEventListener('submit', handleNotesUpload);

  // Syllabus search input
  document.getElementById('syllabusSearch').addEventListener('input', handleSyllabusSearch);

  // Sidebar tab switcher
  document.querySelectorAll('.sidebar-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.sidebar-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.sidebar-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      const panelId = tab.dataset.tab === 'syllabus' ? 'tabSyllabus' :
                      tab.dataset.tab === 'cases' ? 'tabCases' : 'tabWeakness';
      document.getElementById(panelId).classList.add('active');
    });
  });

  // Launch revision quiz button
  document.getElementById('btnLaunchRevisionQuiz').addEventListener('click', () => {
    switchMode('revision');
    quickAsk("Generate a targeted diagnostic revision quiz based on my weak areas.");
  });
}

// ==========================================================================
// Mode Switching & Toolbars
// ==========================================================================
function switchMode(mode) {
  state.currentMode = mode;

  // Update tabs
  modeTabs.forEach(t => {
    t.classList.toggle('active', t.dataset.mode === mode);
  });

  updateModeUI(mode);
}

function updateModeUI(mode) {
  const configs = {
    inquiry: {
      badge: '🧠 INQUIRY MODE ACTIVE',
      color: '#7c3aed',
      desc: 'The tutor teaches through leading questions and guided clinical reasoning. It identifies your gaps and offers hints.',
      toolbar: `
        <button class="toolbar-pill active" onclick="quickAsk('Give me an inquiry question on this topic.')">New Question</button>
        <button class="toolbar-pill" onclick="quickAsk('Give me a hint on this.')">💡 Request Hint</button>
        <button class="toolbar-pill" onclick="quickAsk('Explain the underlying biomechanical mechanism.')">Explain Mechanism</button>
      `
    },
    tutor: {
      badge: '📚 TUTOR MODE ACTIVE',
      color: '#059669',
      desc: 'Direct, comprehensive academic explanations structured with anatomy, assessments, interventions, and textbook pearls.',
      toolbar: `
        <button class="toolbar-pill active" onclick="quickAsk('Explain this concept in full academic detail.')">Academic Breakdown</button>
        <button class="toolbar-pill" onclick="quickAsk('Show clinical pearls and precautions for this.')">Clinical Pearls</button>
        <button class="toolbar-pill" onclick="quickAsk('Summarize the primary Frames of Reference.')">Frames of Reference</button>
      `
    },
    exam: {
      badge: '📝 EXAM MODE (TNMGRU MARK SCHEMES)',
      color: '#d97706',
      desc: 'Prepares university-standard answers formatted for 2/3 marks (Short), 5 marks (Brief), and 10/15 marks (Long Essay).',
      toolbar: `
        <button class="toolbar-pill ${state.examMarks === 2 ? 'active' : ''}" onclick="setExamMarks(2)">2 Marks (Short)</button>
        <button class="toolbar-pill ${state.examMarks === 5 ? 'active' : ''}" onclick="setExamMarks(5)">5 Marks (Brief)</button>
        <button class="toolbar-pill ${state.examMarks === 10 ? 'active' : ''}" onclick="setExamMarks(10)">10 Marks (Essay)</button>
        <button class="toolbar-pill" onclick="promptAnswerSubmission()">Grade My Answer</button>
      `
    },
    viva: {
      badge: '🎓 VIVA VOCE ORAL EXAM SIMULATION',
      color: '#0284c7',
      desc: 'Simulates a university external examiner asking rapid clinical oral questions. Evaluates your oral answers out of 10.',
      toolbar: `
        <button class="toolbar-pill active" onclick="quickAsk('Start a new Viva Voce examination.')">Start Viva</button>
        <button class="toolbar-pill" onclick="quickAsk('Ask me the next rapid viva question.')">Next Question</button>
        <button class="toolbar-pill" onclick="quickAsk('What are the critical red flags and safety contraindications?')">Red Flags</button>
      `
    },
    clinical_reasoning: {
      badge: '🩺 CLINICAL REASONING CASE SIMULATOR',
      color: '#0d9488',
      desc: 'Walks through authentic patient cases along the strict 8-step OT Reasoning Pathway from Condition to Justification.',
      toolbar: `
        <button class="toolbar-pill active" onclick="loadSelectedCase('cva_mca_case_1')">Case 1: CVA Stroke</button>
        <button class="toolbar-pill" onclick="loadSelectedCase('radial_nerve_case_2')">Case 2: Radial Nerve</button>
        <button class="toolbar-pill" onclick="loadSelectedCase('pediatric_cp_case_3')">Case 3: Paediatric CP</button>
        <button class="toolbar-pill" onclick="advanceCaseStep()">Next Pathway Stage →</button>
      `
    },
    revision: {
      badge: '🔄 REVISION & WEAK-AREA DIAGNOSTIC',
      color: '#e11d48',
      desc: 'Analyzes your recorded mistakes and low-scoring areas. Generates targeted clinical drills to ensure mastery.',
      toolbar: `
        <button class="toolbar-pill active" onclick="quickAsk('Run a diagnostic quiz on my weak areas.')">Diagnostic Quiz</button>
        <button class="toolbar-pill" onclick="quickAsk('Review my recurring misconceptions.')">Review Mistakes</button>
        <button class="toolbar-pill" onclick="quickAsk('High-yield clinical flashcards.')">Flashcards</button>
      `
    }
  };

  const cfg = configs[mode] || configs.inquiry;
  bannerBadge.textContent = cfg.badge;
  bannerBadge.style.color = cfg.color;
  bannerDescription.textContent = cfg.desc;
  modeToolbar.innerHTML = cfg.toolbar;
}

function setExamMarks(marks) {
  state.examMarks = marks;
  updateModeUI('exam');
  showToast(`Exam format set to ${marks} Marks.`);
}

function promptAnswerSubmission() {
  userInput.value = "Evaluate my answer for 10 marks: ";
  userInput.focus();
}

// ==========================================================================
// OT Reasoning Pathway Stepper
// ==========================================================================
function setPathwayStep(stepNumber) {
  state.pathwayStep = Math.max(1, Math.min(8, stepNumber));
  const steps = pathwayTicker.querySelectorAll('.pathway-step');
  steps.forEach(stepEl => {
    const s = parseInt(stepEl.dataset.step);
    stepEl.classList.remove('active', 'completed');
    if (s === state.pathwayStep) {
      stepEl.classList.add('active');
    } else if (s < state.pathwayStep) {
      stepEl.classList.add('completed');
    }
  });
}

function advanceCaseStep() {
  state.currentCaseStep = (state.currentCaseStep % 5) + 1;
  setPathwayStep(state.currentCaseStep * 1.6);
  quickAsk(`Advance to Stage ${state.currentCaseStep} of the OT Reasoning Pathway for this case.`);
}

// ==========================================================================
// Chat Messaging & Communication
// ==========================================================================
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text || state.isLoading) return;

  // Append user message to chat UI
  appendMessage({
    sender: 'user',
    name: state.studentProfile ? state.studentProfile.student_name : 'You',
    text: text
  });

  userInput.value = '';
  userInput.style.height = 'auto';

  // Show typing indicator
  const typingIndicator = showTypingIndicator();
  state.isLoading = true;
  btnSend.disabled = true;

  try {
    const payload = {
      message: text,
      mode: state.currentMode,
      context_data: {
        marks: state.examMarks,
        case_id: state.activeCaseId,
        step: state.currentCaseStep
      }
    };

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    typingIndicator.remove();

    if (data.error) {
      appendMessage({
        sender: 'assistant',
        name: 'INQUIRY OT Tutor',
        text: `⚠️ Error: ${data.error}`
      });
    } else {
      appendMessage({
        sender: 'assistant',
        name: 'INQUIRY OT Tutor',
        text: data.response,
        mode: data.mode,
        engine: data.engine,
        ai_error: data.ai_error,
        citations: data.citations || [],
        snippets: data.rag_snippets || []
      });

      if (data.ai_error) {
        showToast('Live AI notice: Using Built-in Academic Engine');
      }

      // Advance pathway step if in clinical reasoning
      if (state.currentMode === 'clinical_reasoning') {
        state.pathwayStep = Math.min(8, state.pathwayStep + 1);
        setPathwayStep(state.pathwayStep);
      }

      // Refresh student stats
      loadStudentDashboard();
    }
  } catch (err) {
    typingIndicator.remove();
    appendMessage({
      sender: 'assistant',
      name: 'INQUIRY OT Tutor',
      text: `⚠️ Network error: Could not reach the tutor server. Please ensure the app is running.`
    });
  } finally {
    state.isLoading = false;
    btnSend.disabled = false;
    userInput.focus();
  }
}

function quickAsk(promptText) {
  userInput.value = promptText;
  sendMessage();
}

function appendMessage(msg) {
  const isUser = msg.sender === 'user';
  const msgEl = document.createElement('div');
  msgEl.className = `message ${isUser ? 'user' : 'assistant'}`;

  const avatar = isUser ? '👤' : '🌿';
  const modeTag = msg.mode ? `<span class="mode-tag">${formatModeName(msg.mode)}</span>` : '';
  const sourceTag = !isUser ? `<span class="source-tag">Grounded OT Literature</span>` : '';

  let aiAlertHtml = '';
  if (msg.ai_error) {
    aiAlertHtml = `
      <div style="background:#fffbeb; border:1px solid #fde68a; border-left:4px solid #f59e0b; padding:10px 14px; border-radius:8px; margin-bottom:12px; font-size:12.5px; color:#92400e; line-height:1.45;">
        <strong>⚠️ AI Engine Notice:</strong> ${escapeHtml(msg.ai_error)}
        <div style="margin-top:6px;">
          <button onclick="openModal('modalSettings')" style="background:#fef3c7; border:1px solid #f59e0b; padding:4px 10px; border-radius:4px; font-size:11px; font-weight:700; color:#b45309; cursor:pointer;">⚙️ Open Settings to switch to Free Google Gemini</button>
        </div>
      </div>
    `;
  }

  let citationsHtml = '';
  if (msg.citations && msg.citations.length > 0) {
    citationsHtml = `
      <div class="citation-box">
        <div class="citation-header">📚 Grounded Academic Citations:</div>
        <div>${msg.citations.map(c => `• ${escapeHtml(c)}`).join('<br>')}</div>
      </div>
    `;
  }

  msgEl.innerHTML = `
    <div class="message-avatar">${avatar}</div>
    <div class="message-body">
      <div class="message-meta">
        <span class="sender-name">${escapeHtml(msg.name)}</span>
        ${modeTag}
        ${sourceTag}
      </div>
      <div class="message-text">
        ${aiAlertHtml}
        ${renderMarkdown(msg.text)}
        ${citationsHtml}
      </div>
    </div>
  `;

  chatMessages.appendChild(msgEl);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
  const el = document.createElement('div');
  el.className = 'message assistant';
  el.id = 'typingIndicator';
  el.innerHTML = `
    <div class="message-avatar">🌿</div>
    <div class="message-body">
      <div class="message-meta">
        <span class="sender-name">INQUIRY OT Tutor</span>
        <span class="mode-tag">Reasoning...</span>
      </div>
      <div class="message-text">
        <span class="loading-spinner">Analyzing clinical scenario & referencing academic literature...</span>
      </div>
    </div>
  `;
  chatMessages.appendChild(el);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return el;
}

// ==========================================================================
// Syllabus Explorer (MGRU Aligned)
// ==========================================================================
async function loadSyllabus() {
  const treeContainer = document.getElementById('syllabusTree');
  try {
    const res = await fetch('/api/syllabus');
    const data = await res.json();
    state.syllabusData = data.subjects || [];
    renderSyllabusTree(state.syllabusData);
  } catch (err) {
    treeContainer.innerHTML = `<div class="loading-spinner">Error loading syllabus.</div>`;
  }
}

function renderSyllabusTree(subjects) {
  const treeContainer = document.getElementById('syllabusTree');
  treeContainer.innerHTML = '';

  subjects.forEach(subject => {
    const subjEl = document.createElement('div');
    subjEl.className = 'subject-item';

    const header = document.createElement('div');
    header.className = 'subject-header';
    header.innerHTML = `
      <span>${escapeHtml(subject.short_name || subject.name)}</span>
      <span class="badge">${subject.units ? subject.units.length : 0} Units</span>
    `;

    const unitList = document.createElement('div');
    unitList.className = 'unit-list';
    unitList.style.display = 'none';

    (subject.units || []).forEach(unit => {
      const unitEl = document.createElement('div');
      unitEl.className = 'unit-item';
      unitEl.innerHTML = `<div class="unit-title">${escapeHtml(unit.unit_name)}</div>`;

      const topicList = document.createElement('div');
      topicList.className = 'topic-list';

      (unit.topics || []).forEach(topic => {
        const topicPill = document.createElement('div');
        topicPill.className = 'topic-pill';
        topicPill.innerHTML = `
          <span>${escapeHtml(topic.title)}</span>
          <span style="font-size: 10px; color: var(--text-muted);">▶</span>
        `;
        topicPill.addEventListener('click', () => {
          quickAsk(`Let's investigate the topic: "${topic.title}" from ${subject.name}.`);
        });
        topicList.appendChild(topicPill);
      });

      unitEl.appendChild(topicList);
      unitList.appendChild(unitEl);
    });

    header.addEventListener('click', () => {
      const isOpen = unitList.style.display === 'flex';
      unitList.style.display = isOpen ? 'none' : 'flex';
    });

    subjEl.appendChild(header);
    subjEl.appendChild(unitList);
    treeContainer.appendChild(subjEl);
  });
}

function handleSyllabusSearch(e) {
  const q = e.target.value.toLowerCase().trim();
  if (!q) {
    renderSyllabusTree(state.syllabusData);
    return;
  }

  const filtered = [];
  (state.syllabusData || []).forEach(subj => {
    const matchedUnits = [];
    (subj.units || []).forEach(u => {
      const matchedTopics = (u.topics || []).filter(t => 
        t.title.toLowerCase().includes(q) ||
        (t.key_terms && t.key_terms.some(k => k.toLowerCase().includes(q))) ||
        (t.subtopics && t.subtopics.some(s => s.toLowerCase().includes(q)))
      );
      if (matchedTopics.length > 0) {
        matchedUnits.push({ ...u, topics: matchedTopics });
      }
    });
    if (matchedUnits.length > 0) {
      filtered.push({ ...subj, units: matchedUnits });
    }
  });

  renderSyllabusTree(filtered);
  // Auto-expand search results
  document.querySelectorAll('.unit-list').forEach(u => u.style.display = 'flex');
}

// ==========================================================================
// Clinical Case Simulator
// ==========================================================================
async function loadCases() {
  const listEl = document.getElementById('casesList');
  try {
    const res = await fetch('/api/cases');
    const data = await res.json();
    const cases = data.cases || [];
    renderCasesList(cases);
  } catch (err) {
    listEl.innerHTML = `<div class="loading-spinner">Error loading clinical cases.</div>`;
  }
}

function renderCasesList(cases) {
  const listEl = document.getElementById('casesList');
  listEl.innerHTML = '';

  cases.forEach((c, idx) => {
    const card = document.createElement('div');
    card.className = `case-card ${idx === 0 ? 'active' : ''}`;
    card.innerHTML = `
      <div class="case-title">${escapeHtml(c.title)}</div>
      <div class="case-meta">
        <span>${escapeHtml(c.subject.toUpperCase())}</span>
        <span>${c.steps_count || 5} Pathway Steps</span>
      </div>
    `;
    card.addEventListener('click', () => {
      document.querySelectorAll('.case-card').forEach(el => el.classList.remove('active'));
      card.classList.add('active');
      loadSelectedCase(c.case_id);
    });
    listEl.appendChild(card);
  });
}

function loadSelectedCase(caseId) {
  state.activeCaseId = caseId;
  state.currentCaseStep = 1;
  setPathwayStep(1);
  switchMode('clinical_reasoning');
  quickAsk(`Begin clinical case simulation for: ${caseId}`);
}

// ==========================================================================
// Student Progress, Weak Areas & Recurring Mistakes
// ==========================================================================
async function loadStudentDashboard() {
  try {
    const res = await fetch('/api/student/dashboard');
    const data = await res.json();
    state.studentProfile = data;

    // Update metrics
    document.getElementById('statAccuracy').textContent = `${data.accuracy_percent || 0}%`;
    document.getElementById('statAttempted').textContent = data.stats ? data.stats.total_questions_attempted : 0;
    document.getElementById('statMastery').textContent = `${data.overall_mastery || 70}%`;

    // Render weak areas list
    const weakList = document.getElementById('weakTopicsList');
    weakList.innerHTML = '';
    const weaks = data.weak_areas || [];
    if (weaks.length === 0) {
      weakList.innerHTML = `<span style="font-size:12px; color: var(--text-muted);">No critical weak areas logged yet. Excellent!</span>`;
    } else {
      weaks.forEach(w => {
        const tag = document.createElement('span');
        tag.className = 'weak-tag';
        tag.textContent = w;
        tag.style.cursor = 'pointer';
        tag.title = 'Click to practice this weak area';
        tag.addEventListener('click', () => {
          switchMode('revision');
          quickAsk(`Let's revise my weak area: ${w}`);
        });
        weakList.appendChild(tag);
      });
    }

    // Render recurring mistakes
    const mistakeList = document.getElementById('recurringMistakesList');
    mistakeList.innerHTML = '';
    const mistakes = data.recurring_mistakes || [];
    mistakes.slice(0, 3).forEach(m => {
      const mCard = document.createElement('div');
      mCard.className = 'mistake-card';
      mCard.innerHTML = `
        <div class="mistake-topic">⚠️ ${escapeHtml(m.topic)}</div>
        <div class="mistake-correction"><strong>Correction:</strong> ${escapeHtml(m.correction)}</div>
      `;
      mistakeList.appendChild(mCard);
    });
  } catch (err) {
    console.error('Error fetching dashboard:', err);
  }
}

function renderFullAnalyticsModal() {
  const container = document.getElementById('analyticsModalContent');
  if (!state.studentProfile) {
    container.innerHTML = '<div class="loading-spinner">Loading analytics...</div>';
    return;
  }

  const p = state.studentProfile;
  const subjs = p.subject_mastery || {};

  container.innerHTML = `
    <div style="margin-bottom: 16px;">
      <h4 style="font-size: 16px; font-weight: 800;">${escapeHtml(p.student_name)}</h4>
      <p style="font-size: 12px; color: var(--text-muted);">${escapeHtml(p.study_level)} · ${escapeHtml(p.target_university)}</p>
    </div>

    <div class="analytics-card" style="margin-bottom: 20px;">
      <div class="metric-row">
        <div class="metric-item">
          <span class="metric-val">${p.accuracy_percent}%</span>
          <span class="metric-lbl">Accuracy</span>
        </div>
        <div class="metric-item">
          <span class="metric-val">${p.stats.cases_completed || 0}</span>
          <span class="metric-lbl">Cases Mastered</span>
        </div>
        <div class="metric-item">
          <span class="metric-val">${p.stats.viva_sessions || 0}</span>
          <span class="metric-lbl">Viva Exams</span>
        </div>
      </div>
    </div>

    <h5 style="font-size: 13px; font-weight: 700; margin-bottom: 10px;">Subject Mastery Breakdown</h5>
    <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px;">
      ${Object.entries(subjs).map(([k, v]) => `
        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 12.5px;">
          <span style="font-weight: 600; text-transform: capitalize;">${k.replace('_', ' ')}</span>
          <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 140px; height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
              <div style="width: ${v.mastery_score}%; height: 100%; background: var(--primary);"></div>
            </div>
            <span style="font-weight: 700; font-size: 12px; width: 35px;">${v.mastery_score}%</span>
          </div>
        </div>
      `).join('')}
    </div>

    <h5 style="font-size: 13px; font-weight: 700; margin-bottom: 10px;">Recent Study Activity</h5>
    <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12px;">
      ${(p.recent_activities || []).slice(0, 5).map(act => `
        <div style="padding: 6px 10px; background: #f8fafc; border: 1px solid var(--border-light); border-radius: 6px; display: flex; justify-content: space-between;">
          <span><strong>${act.topic}</strong> (${act.mode})</span>
          <span style="color: var(--text-muted);">${act.timestamp}</span>
        </div>
      `).join('')}
    </div>
  `;
}

// ==========================================================================
// RAG Knowledge Base & Notes Uploader
// ==========================================================================
async function loadRAGSources() {
  const list = document.getElementById('ragSourcesList');
  list.innerHTML = '<div class="loading-spinner">Loading knowledge sources...</div>';

  try {
    const res = await fetch('/api/rag/sources');
    const data = await res.json();
    list.innerHTML = '';

    (data.sources || []).forEach(s => {
      const item = document.createElement('div');
      item.className = 'source-item';
      item.innerHTML = `
        <div class="source-title">📖 ${escapeHtml(s.source)}</div>
        <div class="source-meta">${s.sections_count} Indexed Clinical Sections · Topics: ${(s.topics || []).slice(0, 4).join(', ')}</div>
      `;
      list.appendChild(item);
    });
  } catch (err) {
    list.innerHTML = '<div class="loading-spinner">Error loading sources.</div>';
  }
}

async function handleNotesUpload(e) {
  e.preventDefault();
  const title = document.getElementById('noteTitle').value.trim();
  const source = document.getElementById('noteSource').value.trim();
  const content = document.getElementById('noteContent').value.trim();

  if (!title || !content) return;

  try {
    const res = await fetch('/api/rag/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, source, content })
    });
    const data = await res.json();
    if (data.success) {
      showToast('Document indexed successfully into RAG knowledge base!');
      document.getElementById('uploadNotesForm').reset();
      loadRAGSources();
    } else {
      showToast('Failed to upload document.');
    }
  } catch (err) {
    showToast('Error uploading document.');
  }
}

// ==========================================================================
// Settings Configuration & API Key Management
// ==========================================================================
async function loadConfig() {
  try {
    const res = await fetch('/api/config');
    const conf = await res.json();

    document.getElementById('studentName').value = conf.student_name || 'OT Scholar';
    document.getElementById('studyLevel').value = conf.study_level || '3rd Year BOT (Clinical Phase)';
    
    const provider = conf.api_provider || 'gemini';
    const providerSelect = document.getElementById('apiProvider');
    if (providerSelect) {
      providerSelect.value = provider;
      toggleProviderFields(provider);
    }

    if (document.getElementById('geminiModel')) {
      const gModel = conf.gemini_model || 'gemini-3.5-flash-lite';
      document.getElementById('geminiModel').value = (gModel.includes('1.5') || gModel.includes('2.5')) ? 'gemini-3.5-flash-lite' : gModel;
    }
    if (document.getElementById('openaiModel')) {
      document.getElementById('openaiModel').value = conf.openai_model || 'gpt-4o-mini';
    }

    const apiKeyInput = document.getElementById('apiKey');
    if (conf.api_key_masked && !conf.api_key_masked.startsWith('Not set')) {
      if (provider === 'gemini') {
        engineBadgeText.textContent = '✨ Live Gemini AI';
      } else {
        engineBadgeText.textContent = '✨ Live OpenAI';
      }
      apiKeyInput.placeholder = conf.api_key_masked;
    } else {
      engineBadgeText.textContent = '🌿 Built-in OT AI';
    }
  } catch (err) {
    console.error('Error loading config:', err);
  }
}

function toggleProviderFields(provider) {
  const geminiGroup = document.getElementById('geminiModelGroup');
  const openaiGroup = document.getElementById('openaiModelGroup');
  const apiKeyInput = document.getElementById('apiKey');
  const apiKeyHelpText = document.getElementById('apiKeyHelpText');

  if (provider === 'openai') {
    if (geminiGroup) geminiGroup.style.display = 'none';
    if (openaiGroup) openaiGroup.style.display = 'block';
    if (apiKeyInput) apiKeyInput.placeholder = 'sk-... (requires active billing balance)';
    if (apiKeyHelpText) apiKeyHelpText.textContent = 'Note: OpenAI requires pre-purchased credits. Accounts with $0 credit balance will return error 429.';
  } else {
    if (geminiGroup) geminiGroup.style.display = 'block';
    if (openaiGroup) openaiGroup.style.display = 'none';
    if (apiKeyInput) apiKeyInput.placeholder = 'AIzaSy... (Get free key at aistudio.google.com)';
    if (apiKeyHelpText) apiKeyHelpText.innerHTML = 'Google Gemini offers a <strong>100% free tier</strong> with no credit card required!';
  }
}

async function handleTestConnection() {
  const provider = document.getElementById('apiProvider').value;
  const apiKey = document.getElementById('apiKey').value.trim();
  const model = provider === 'gemini' 
    ? document.getElementById('geminiModel').value 
    : document.getElementById('openaiModel').value;

  const resultBox = document.getElementById('connectionTestResult');
  resultBox.style.display = 'block';
  resultBox.style.background = '#f8fafc';
  resultBox.style.border = '1px solid #cbd5e1';
  resultBox.style.color = '#334155';
  resultBox.innerHTML = `<strong>⏳ Testing connection to ${provider.toUpperCase()}...</strong> Please wait a moment.`;

  try {
    const res = await fetch('/api/test-connection', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_provider: provider, api_key: apiKey, model: model })
    });
    const data = await res.json();

    if (data.success) {
      resultBox.style.background = '#ecfdf5';
      resultBox.style.border = '1px solid #6ee7b7';
      resultBox.style.color = '#065f46';
      resultBox.innerHTML = `<strong>✅ Success!</strong> ${escapeHtml(data.message)}`;
      showToast('AI Connection Verified!');
    } else {
      resultBox.style.background = '#fff1f2';
      resultBox.style.border = '1px solid #fecdd3';
      resultBox.style.color = '#9f1239';
      resultBox.innerHTML = `<strong>⚠️ Connection Failed:</strong><br>${escapeHtml(data.message)}`;
    }
  } catch (err) {
    resultBox.style.background = '#fff1f2';
    resultBox.style.border = '1px solid #fecdd3';
    resultBox.style.color = '#9f1239';
    resultBox.innerHTML = `<strong>⚠️ Test Error:</strong> Could not connect to the local tutor server.`;
  }
}

async function handleSettingsSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('studentName').value.trim();
  const level = document.getElementById('studyLevel').value;
  const provider = document.getElementById('apiProvider').value;
  const apiKey = document.getElementById('apiKey').value.trim();
  const geminiModel = document.getElementById('geminiModel').value;
  const openaiModel = document.getElementById('openaiModel') ? document.getElementById('openaiModel').value : 'gpt-4o-mini';

  const payload = {
    student_name: name,
    study_level: level,
    api_provider: provider,
    gemini_model: geminiModel,
    openai_model: openaiModel
  };

  if (apiKey) {
    payload.api_key = apiKey;
  }

  try {
    const res = await fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      showToast('Settings saved successfully!');
      closeModal('modalSettings');
      loadConfig();
      // Update student profile name in tracker
      await fetch('/api/student/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_name: name, study_level: level })
      });
      loadStudentDashboard();
    }
  } catch (err) {
    showToast('Failed to save settings.');
  }
}

// ==========================================================================
// Modal & UI Utilities
// ==========================================================================
function openModal(modalId) {
  const el = document.getElementById(modalId);
  if (el) el.classList.add('active');
}

function closeModal(modalId) {
  const el = document.getElementById(modalId);
  if (el) el.classList.remove('active');
}

function showToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3200);
}

function formatModeName(mode) {
  const map = {
    inquiry: 'Inquiry Mode',
    tutor: 'Tutor Mode',
    exam: 'Exam Mode',
    viva: 'Viva Mode',
    clinical_reasoning: 'Clinical Reasoning',
    revision: 'Revision Mode'
  };
  return map[mode] || mode;
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
}

function renderMarkdown(text) {
  if (!text) return '';
  let html = escapeHtml(text);

  // Bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Italics
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  // Horizontal rule
  html = html.replace(/---/g, '<hr>');

  // Split into paragraphs & lists
  const lines = html.split('\n');
  let inList = false;
  let result = [];

  lines.forEach(line => {
    const trimmed = line.trim();
    if (trimmed.startsWith('• ') || trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      if (!inList) {
        result.push('<ul>');
        inList = true;
      }
      result.push(`<li>${trimmed.substring(2)}</li>`);
    } else {
      if (inList) {
        result.push('</ul>');
        inList = false;
      }
      if (trimmed.length > 0) {
        result.push(`<p>${line}</p>`);
      }
    }
  });

  if (inList) {
    result.push('</ul>');
  }

  return result.join('');
}
