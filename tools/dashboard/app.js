// Agent Army Mission Control & Command Cockpit Logic
document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "";

  // Elements
  const tabs = document.querySelectorAll(".nav-tab");
  const panels = document.querySelectorAll(".tab-panel");
  const heroMissionTitle = document.getElementById("hero-mission-title");
  const heroWorkflowBadge = document.getElementById("hero-workflow-badge");
  const heroStatusPill = document.getElementById("hero-status-pill");
  const heroAgentPill = document.getElementById("hero-agent-pill");
  const pipelineDag = document.getElementById("pipeline-dag");
  const eventsFeed = document.getElementById("events-feed");
  const locksTbody = document.getElementById("locks-tbody");
  const rosterGrid = document.getElementById("roster-grid");
  const rosterFilters = document.getElementById("roster-filters");
  const memoriesGrid = document.getElementById("memories-grid");
  const memorySearchInput = document.getElementById("memory-search-input");
  const btnMemorySearch = document.getElementById("btn-memory-search");
  const memoryQuickTags = document.getElementById("memory-quick-tags");
  const terminalBody = document.getElementById("terminal-body");
  const terminalTitle = document.getElementById("terminal-title");
  const dispatchForm = document.getElementById("dispatch-form");
  const ignitionBox = document.getElementById("ignition-box");
  const ignitionPromptText = document.getElementById("ignition-prompt-text");
  const btnCopyPrompt = document.getElementById("btn-copy-prompt");
  const toastContainer = document.getElementById("toast-container");

  let allAgents = [];
  let pollInterval = null;

  // --- 1. Tab Navigation ---
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      panels.forEach(p => p.classList.remove("active"));
      tab.classList.add("active");
      const targetPanel = document.getElementById(`panel-${tab.dataset.tab}`);
      if (targetPanel) targetPanel.classList.add("active");

      // Load specific tab data on demand
      if (tab.dataset.tab === "roster" && allAgents.length === 0) {
        loadAgents();
      } else if (tab.dataset.tab === "memory") {
        loadMemories();
      } else if (tab.dataset.tab === "settings") {
        loadSettings();
      }
    });
  });

  // --- 2. Live Telemetry & Status Polling ---
  async function fetchStatus() {
    try {
      const res = await fetch(`${API_BASE}/api/status`);
      if (!res.ok) return;
      const data = await res.json();
      renderStatus(data);
    } catch (err) {
      console.warn("Telemetry fetch error:", err);
    }
  }

  function renderStatus(data) {
    const state = data.state || {};
    if (state.active_mission) heroMissionTitle.textContent = state.active_mission;
    if (state.active_workflow) heroWorkflowBadge.textContent = state.active_workflow;
    if (state.status) {
      heroStatusPill.className = `status-pill status-${state.status.toLowerCase().replace(/_/g, '-')}`;
      heroStatusPill.innerHTML = `<span class="pulse-ring"></span> ${state.status}`;
    }
    if (state.active_agent) {
      heroAgentPill.innerHTML = `Active: <strong>${state.active_agent}</strong>`;
    }

    // Render Pipeline DAG
    if (state.pipeline && state.pipeline.length > 0) {
      pipelineDag.innerHTML = "";
      state.pipeline.forEach((stage, idx) => {
        const node = document.createElement("div");
        const statusClass = (stage.status || "pending").toLowerCase().replace(/_/g, "-");
        node.className = `dag-node ${statusClass}`;
        
        let icon = "○";
        if (statusClass === "completed") icon = "✓";
        else if (statusClass === "in-progress") icon = "⚡";

        node.innerHTML = `
          <div class="dag-node-header">
            <span class="dag-node-step">STAGE ${idx + 1}</span>
            <span class="dag-node-icon">${icon}</span>
          </div>
          <div class="dag-node-title" title="${stage.name}">${stage.name}</div>
          <div class="dag-node-agent">${stage.agent || "unassigned"}</div>
        `;
        pipelineDag.appendChild(node);

        if (idx < state.pipeline.length - 1) {
          const arrow = document.createElement("div");
          arrow.className = "dag-arrow";
          arrow.textContent = "➔";
          pipelineDag.appendChild(arrow);
        }
      });
    }

    // Render Events Feed
    if (state.recent_events && state.recent_events.length > 0) {
      eventsFeed.innerHTML = "";
      state.recent_events.forEach(ev => {
        const card = document.createElement("div");
        card.className = "event-card";
        const timeShort = ev.timestamp ? ev.timestamp.split("T")[1].replace("Z", "") : "";
        card.innerHTML = `
          <div class="event-meta">
            <span class="event-agent">${ev.agent}</span>
            <span class="event-type">${ev.type}</span>
          </div>
          <div class="event-msg">${escapeHtml(ev.message)}</div>
          <div class="event-time">${timeShort} UTC</div>
        `;
        eventsFeed.appendChild(card);
      });
    }

    // Render File Locks
    const locks = data.locks || [];
    locksTbody.innerHTML = "";
    if (locks.length === 0) {
      locksTbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color: var(--text-dim); padding: 20px;">Zero active locks. Workspace available for concurrent execution.</td></tr>`;
    } else {
      locks.forEach(l => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><code>${escapeHtml(l.file)}</code></td>
          <td><span class="agent-tag">${escapeHtml(l.holder)}</span></td>
          <td><span class="badge badge-accent">${escapeHtml(l.mode)}</span></td>
          <td style="color: var(--text-dim);">${escapeHtml(l.expires_at || "N/A")}</td>
        `;
        locksTbody.appendChild(tr);
      });
    }
  }

  // --- 3. Mission Dispatcher ---
  dispatchForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const project = document.getElementById("dispatch-project").value.trim();
    const workflow = document.getElementById("dispatch-workflow").value;
    const goal = document.getElementById("dispatch-goal").value.trim();

    if (!goal) {
      showToast("Please enter a mission directive or goal description.", "warning");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/api/dispatch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project, workflow, goal })
      });
      const data = await res.json();
      if (res.ok) {
        ignitionPromptText.textContent = data.ide_prompt;
        ignitionBox.style.display = "block";
        showToast("Mission dispatched to .agent/inbox.json!", "success");
        fetchStatus();
      } else {
        showToast(data.error || "Failed to dispatch mission", "danger");
      }
    } catch (err) {
      showToast("Dispatch error: " + err.message, "danger");
    }
  });

  btnCopyPrompt.addEventListener("click", () => {
    const text = ignitionPromptText.textContent;
    navigator.clipboard.writeText(text).then(() => {
      showToast("Copied Orchestrator ignition prompt to clipboard!", "success");
    });
  });

  // --- 4. Canonical Agent Roster ---
  async function loadAgents() {
    try {
      const res = await fetch(`${API_BASE}/api/agents`);
      if (!res.ok) return;
      const data = await res.json();
      allAgents = data.agents || [];
      document.getElementById("roster-count").textContent = allAgents.length;
      renderAgents(allAgents);
    } catch (err) {
      console.warn("Agents load error:", err);
    }
  }

  function renderAgents(agentsList) {
    rosterGrid.innerHTML = "";
    agentsList.forEach(a => {
      const card = document.createElement("div");
      card.className = "agent-card";
      
      const skillsHtml = (a.skills_required || []).map(s => `<span class="agent-tag">${s}</span>`).join(" ");

      card.innerHTML = `
        <div class="agent-card-header">
          <span class="agent-card-id">${a.id}</span>
          <span class="perm-badge perm-${a.permission_level}">Level ${a.permission_level}</span>
        </div>
        <div class="agent-name">${a.name}</div>
        <div class="agent-battalion">${a.battalion}</div>
        <div class="agent-role">${escapeHtml(a.role)}</div>
        <div class="agent-tags">${skillsHtml}</div>
      `;

      card.addEventListener("click", () => {
        showToast(`${a.name} (${a.id}) - ${a.role}`, "info");
      });

      rosterGrid.appendChild(card);
    });
  }

  rosterFilters.addEventListener("click", (e) => {
    if (!e.target.classList.contains("filter-btn")) return;
    rosterFilters.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    e.target.classList.add("active");
    const filter = e.target.dataset.filter;
    if (filter === "all") {
      renderAgents(allAgents);
    } else {
      const filtered = allAgents.filter(a => a.battalion === filter);
      renderAgents(filtered);
    }
  });

  // --- 5. Memory Vault Explorer ---
  async function loadMemories(query = "") {
    try {
      const url = query ? `${API_BASE}/api/memory/search?q=${encodeURIComponent(query)}` : `${API_BASE}/api/memory/list`;
      const res = await fetch(url);
      if (!res.ok) return;
      const data = await res.json();
      const list = data.results || data.memories || [];
      renderMemories(list);
    } catch (err) {
      console.warn("Memory load error:", err);
    }
  }

  function renderMemories(memories) {
    memoriesGrid.innerHTML = "";
    if (memories.length === 0) {
      memoriesGrid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-dim); padding: 40px;">No memory entries found. Store a memory or adjust search query.</div>`;
      return;
    }

    memories.forEach(m => {
      const card = document.createElement("div");
      card.className = "memory-card";
      const tagsHtml = (m.tags || []).map(t => `<span class="tag-pill">${t}</span>`).join(" ");

      card.innerHTML = `
        <div class="memory-card-header">
          <span class="badge badge-accent">${escapeHtml(m.project)}</span>
          <span style="font-size: 11px; color: var(--text-dim);">${m.date || ""}</span>
        </div>
        <div class="memory-title">${escapeHtml(m.title)}</div>
        <div class="memory-pillar"><strong>What:</strong> ${escapeHtml(m.what_summary || "")}</div>
        <div class="memory-pillar"><strong>Why:</strong> ${escapeHtml(m.why_summary || "")}</div>
        <div class="quick-tags" style="margin-top: auto;">${tagsHtml}</div>
      `;

      card.addEventListener("click", () => openMemoryDetail(m.id));
      memoriesGrid.appendChild(card);
    });
  }

  async function openMemoryDetail(memId) {
    try {
      const res = await fetch(`${API_BASE}/api/memory/get?id=${encodeURIComponent(memId)}`);
      if (!res.ok) return;
      const mem = await res.json();

      document.getElementById("mem-detail-project").textContent = mem.project;
      document.getElementById("mem-detail-title").textContent = mem.title;
      document.getElementById("mem-detail-id").textContent = mem.id;
      document.getElementById("mem-detail-date").textContent = mem.date;
      document.getElementById("mem-detail-file").textContent = mem.relative_path;
      document.getElementById("mem-detail-body").innerHTML = `<pre style="white-space: pre-wrap; font-family: var(--font-sans); color: var(--text-main);">${escapeHtml(mem.content)}</pre>`;

      document.getElementById("modal-memory").style.display = "flex";
    } catch (err) {
      showToast("Failed to load memory detail", "danger");
    }
  }

  document.getElementById("btn-close-mem-modal").addEventListener("click", () => {
    document.getElementById("modal-memory").style.display = "none";
  });

  btnMemorySearch.addEventListener("click", () => {
    loadMemories(memorySearchInput.value.trim());
  });

  memorySearchInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
      loadMemories(memorySearchInput.value.trim());
    }
  });

  memoryQuickTags.addEventListener("click", (e) => {
    if (e.target.classList.contains("tag-pill")) {
      const tag = e.target.dataset.tag;
      memorySearchInput.value = tag;
      loadMemories(tag);
    }
  });

  // --- 6. Diagnostics Tool Runners ---
  async function runDiagnosticTool(toolKey, title) {
    terminalTitle.textContent = `${title} (Running...)`;
    terminalBody.textContent = `[${new Date().toISOString()}] Launching diagnostic tool '${toolKey}'...\n`;

    try {
      const res = await fetch(`${API_BASE}/api/tools/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tool: toolKey })
      });
      const data = await res.json();
      terminalTitle.textContent = `${title} (${data.returncode === 0 ? "PASSED" : "FAILED"} in ${data.duration_seconds}s)`;
      terminalBody.textContent = data.output || "Execution completed with zero output.";
      if (data.returncode === 0) {
        showToast(`${title} passed successfully!`, "success");
      } else {
        showToast(`${title} reported warnings or failures.`, "warning");
      }
    } catch (err) {
      terminalTitle.textContent = `${title} (Error)`;
      terminalBody.textContent = "Execution error: " + err.message;
      showToast("Tool execution failed: " + err.message, "danger");
    }
  }

  document.getElementById("btn-run-tests").addEventListener("click", () => {
    runDiagnosticTool("test", "Automated Test Suite (48 Tests)");
  });

  document.getElementById("btn-run-linter").addEventListener("click", () => {
    runDiagnosticTool("lint", "AST Syntax Linter (14 Languages)");
  });

  document.getElementById("btn-run-scanner").addEventListener("click", () => {
    runDiagnosticTool("scan", "AST Symbol Discovery Scanner");
  });

  document.getElementById("btn-clear-terminal").addEventListener("click", () => {
    terminalBody.textContent = "Console cleared.";
    terminalTitle.textContent = "Execution Console";
  });

  // --- 7. Settings & AI Providers ---
  async function loadSettings() {
    try {
      const res = await fetch(`${API_BASE}/api/settings`);
      if (!res.ok) return;
      const data = await res.json();
      const providers = data.providers || {};
      if (providers.gemini && providers.gemini.api_key) {
        document.getElementById("key-gemini").value = providers.gemini.api_key;
      }
      if (providers.anthropic && providers.anthropic.api_key) {
        document.getElementById("key-anthropic").value = providers.anthropic.api_key;
      }
      if (providers.openai && providers.openai.api_key) {
        document.getElementById("key-openai").value = providers.openai.api_key;
      }
      if (providers.ollama && providers.ollama.base_url) {
        document.getElementById("url-ollama").value = providers.ollama.base_url;
      }
    } catch (err) {
      console.warn("Settings load error:", err);
    }
  }

  document.getElementById("settings-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      default_mode: document.querySelector("input[name='exec-mode']:checked").value,
      providers: {
        gemini: { api_key: document.getElementById("key-gemini").value.trim() },
        anthropic: { api_key: document.getElementById("key-anthropic").value.trim() },
        openai: { api_key: document.getElementById("key-openai").value.trim() },
        ollama: { base_url: document.getElementById("url-ollama").value.trim() }
      }
    };

    try {
      const res = await fetch(`${API_BASE}/api/settings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok) {
        showToast("Provider settings saved to .agent/settings.json!", "success");
      } else {
        showToast(data.error || "Failed to save settings", "danger");
      }
    } catch (err) {
      showToast("Save error: " + err.message, "danger");
    }
  });

  // Mode radio toggle
  document.querySelectorAll("input[name='exec-mode']").forEach(r => {
    r.addEventListener("change", () => {
      document.querySelectorAll(".mode-card").forEach(c => c.classList.remove("active"));
      r.closest(".mode-card").classList.add("active");
    });
  });

  // --- 8. Level 3 Gate Modal ---
  document.getElementById("btn-close-modal").addEventListener("click", () => {
    document.getElementById("modal-approval").style.display = "none";
  });

  document.querySelectorAll(".4-quadrant-gate button").forEach(btn => {
    btn.addEventListener("click", async () => {
      const action = btn.dataset.action;
      const feedback = document.getElementById("gate-feedback").value.trim();
      try {
        await fetch(`${API_BASE}/api/gate/respond`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ action, feedback })
        });
        document.getElementById("modal-approval").style.display = "none";
        showToast(`Gate action [${action.toUpperCase()}] recorded.`, "info");
        fetchStatus();
      } catch (err) {
        showToast("Gate error: " + err.message, "danger");
      }
    });
  });

  // --- 9. Utility Functions ---
  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  function escapeHtml(text) {
    if (!text) return "";
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // --- 10. Initial Boot & Polling ---
  fetchStatus();
  loadAgents();
  loadMemories();
  pollInterval = setInterval(fetchStatus, 3000);
});
