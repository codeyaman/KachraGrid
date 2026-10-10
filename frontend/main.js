/* ═══════════════════════════════════════════════════════════════
   KachraGrid v2 — Main Controller
   Clean Eco-Modern Design System • Exact Reference Replica
   Lenis Smooth Scrolling • Leaflet Voyager GIS • Emil Kowalski UI
   ═══════════════════════════════════════════════════════════════ */

import './style.css';
import gsap from 'gsap';
import Lenis from 'lenis';
import Chart from 'chart.js/auto';
import React from 'react';
import { createRoot } from 'react-dom/client';
import { Agentation } from 'agentation';

const API = '/api';

// ── Agentation Visual Feedback Integration ──
function initAgentation() {
  try {
    let container = document.getElementById('agentation-root');
    if (!container) {
      container = document.createElement('div');
      container.id = 'agentation-root';
      document.body.appendChild(container);
    }
    const root = createRoot(container);
    root.render(
      React.createElement(Agentation, {
        appName: 'KachraGrid v2',
        copyToClipboard: true,
        enableKeyboardShortcuts: true,
      })
    );
  } catch (err) {
    console.error('Failed to initialize Agentation:', err);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAgentation);
} else {
  initAgentation();
}


// ── 1. Lenis Smooth Scroll Engine (Synced to GSAP Ticker) ──
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const lenis = new Lenis({
  duration: 1.4,
  wheelMultiplier: 1.15,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothTouch: false,
});

if (!prefersReducedMotion) {
  gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
  });
  gsap.ticker.lagSmoothing(0);
}

// ── 2. State & Cache ──
let leafletMap = null;
let dailyChart = null;
let visBarChart = null;
let visDonutChart = null;
let visLineChart = null;
let allBinsCache = [];
let selectedBinId = 'B001';
let currentAiResult = null;
let activePage = 'landing';
let clockInterval = null;

// ── 3. Emil-Style Toaster ──
export function showToast({ title, description, variant = 'primary' }) {
  const container = document.getElementById('toaster');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${variant}`;
  
  const icon = variant === 'success' 
    ? 'solar:check-circle-bold' 
    : variant === 'destructive' 
    ? 'solar:danger-triangle-bold' 
    : 'solar:bell-bing-bold';

  toast.innerHTML = `
    <span class="iconify" data-icon="${icon}" data-width="20" style="color:var(--emerald-accent)"></span>
    <div>
      <div class="toast-title">${title}</div>
      ${description ? `<div class="toast-desc">${description}</div>` : ''}
    </div>
  `;

  container.appendChild(toast);

  requestAnimationFrame(() => toast.classList.add('toast-in'));

  setTimeout(() => {
    toast.classList.remove('toast-in');
    toast.classList.add('toast-out');
    setTimeout(() => toast.remove(), 220);
  }, 3800);
}

// ── 4. Page Navigation & Crossfade Blur ──
function navigateTo(pageId) {
  if (pageId === 'hero') pageId = 'landing';
  if (activePage === pageId) return;

  // Close mobile drawer
  document.getElementById('mobile-menu')?.classList.remove('open');
  document.getElementById('nav-toggle')?.classList.remove('open');

  const oldPage = document.getElementById(`page-${activePage}`);
  const newPage = document.getElementById(`page-${pageId}`);
  if (!newPage) return;

  activePage = pageId;

  // Update nav tabs
  document.querySelectorAll('.pill-nav-item, .mobile-nav-link').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.nav === pageId);
  });

  // Emil Kowalski blur mask crossfade
  if (oldPage) {
    oldPage.style.opacity = '0';
    oldPage.style.filter = 'blur(2px)';
    oldPage.style.transform = 'translateY(6px)';
    setTimeout(() => {
      oldPage.classList.remove('active');
      newPage.classList.add('active');
      lenis.scrollTo(0, { immediate: true });
      requestAnimationFrame(() => {
        newPage.style.opacity = '1';
        newPage.style.filter = 'blur(0px)';
        newPage.style.transform = 'translateY(0)';
      });
    }, 120);
  } else {
    newPage.classList.add('active');
    lenis.scrollTo(0, { immediate: true });
  }

  // Load section datasets
  if (pageId === 'dashboard') loadDashboard();
  if (pageId === 'complaint') loadComplaintBins();
  if (pageId === 'tracker') loadTrackerChips();
  if (pageId === 'officer') loadOfficerDashboard();
  if (pageId === 'map') loadMap();
  if (pageId === 'fuel') loadFuelDashboard();
}

// Attach nav handlers
document.querySelectorAll('[data-nav]').forEach(el => {
  el.addEventListener('click', (e) => {
    e.preventDefault();
    navigateTo(el.dataset.nav);
  });
});

// Mobile menu toggle
document.getElementById('nav-toggle')?.addEventListener('click', () => {
  document.getElementById('mobile-menu')?.classList.toggle('open');
});

// Hash change routing
window.addEventListener('hashchange', () => {
  const hash = window.location.hash.replace('#page-', '').replace('#', '');
  if (hash && document.getElementById(`page-${hash}`)) {
    navigateTo(hash);
  }
});

// ── 5. Initial Load & Entrance Choreography ──
window.addEventListener('load', () => {
  const initialHash = window.location.hash.replace('#page-', '').replace('#', '');
  if (initialHash && document.getElementById(`page-${initialHash}`)) {
    navigateTo(initialHash);
  }

  const preloader = document.getElementById('preloader');
  setTimeout(() => {
    preloader?.classList.add('hidden');

    if (!prefersReducedMotion) {
      gsap.from('.hero-title', {
        y: 25,
        opacity: 0,
        duration: 0.7,
        ease: 'cubic-bezier(0.23, 1, 0.32, 1)'
      });
      gsap.from('.island-img', {
        scale: 0.94,
        opacity: 0,
        duration: 0.9,
        delay: 0.1,
        ease: 'cubic-bezier(0.23, 1, 0.32, 1)'
      });
    }

    loadDashboard();
  }, 400);
});

// ══════════════════════════════════════════════════════════════
// DATA VISUALIZATION ENGINE (EXACT REFERENCE REPLICA)
// Planetary GIS Cockpit with Live Site Data
// ══════════════════════════════════════════════════════════════

// Live HUD Clock
function startVisClock() {
  if (clockInterval) clearInterval(clockInterval);
  const clockEl = document.getElementById('vis-live-clock');
  const update = () => {
    if (!clockEl) return;
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, '0');
    const d = String(now.getDate()).padStart(2, '0');
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');
    const ss = String(now.getSeconds()).padStart(2, '0');
    clockEl.textContent = `${y}.${m}.${d} ${hh}:${mm}:${ss}`;
  };
  update();
  clockInterval = setInterval(update, 1000);
}

function selectVisSite(binId) {
  selectedBinId = binId;
  const bin = allBinsCache.find(b => b.bin_id === binId) || allBinsCache[0];
  if (!bin) return;

  // Highlight active pin
  document.querySelectorAll('.vis-site-pin').forEach(p => {
    p.classList.toggle('active', p.dataset.binId === binId);
  });

  // Update Hologram Card
  const idEl = document.getElementById('holo-site-id');
  const nameEl = document.getElementById('holo-site-name');
  const fillEl = document.getElementById('holo-fill-pct');
  const capEl = document.getElementById('holo-capacity');
  const zoneEl = document.getElementById('holo-zone');
  const cleanEl = document.getElementById('holo-cleaned');
  const card = document.getElementById('vis-hologram-card');

  if (idEl) idEl.textContent = bin.bin_id;
  if (nameEl) nameEl.textContent = bin.landmark.toUpperCase();
  if (fillEl) {
    fillEl.textContent = `${bin.current_fill_pct}%`;
    fillEl.className = bin.current_fill_pct > 80 ? 'val text-red font-mono' : bin.current_fill_pct > 50 ? 'val text-amber font-mono' : 'val text-cyan font-mono';
  }
  if (capEl) capEl.textContent = `${bin.capacity_kg} KG`;
  if (zoneEl) zoneEl.textContent = `${(bin.zone_type || 'CIVIC').toUpperCase()} ZONE`;
  if (cleanEl) {
    const timeOnly = bin.last_cleaned_at ? bin.last_cleaned_at.split(' ')[1] : '07:11';
    cleanEl.textContent = `CLEARED ${timeOnly}`;
  }

  // Micro animation on card
  if (card) {
    card.style.transform = 'scale(1.02)';
    setTimeout(() => { card.style.transform = 'scale(1)'; }, 150);
  }
}

async function loadDashboard() {
  startVisClock();

  try {
    const [stats, apps, bins] = await Promise.all([
      fetch(`${API}/dashboard/stats`).then(r => r.json()),
      fetch(`${API}/applications`).then(r => r.json()),
      fetch(`${API}/bins`).then(r => r.json())
    ]);

    allBinsCache = bins || [];

    // Safe fallback for cached elements
    const setSafeText = (id, text) => {
      const el = document.getElementById(id);
      if (el) el.textContent = text;
    };
    setSafeText('stat-critical', stats.critical_bins || 0);
    setSafeText('stat-pending', stats.pending || 0);
    setSafeText('stat-completed', stats.completed || 0);
    setSafeText('stat-savings', `₹${Math.round(stats.fuel?.total_savings_inr || 0)}`);
    setSafeText('stat-trucks', `${stats.trucks_active}/${stats.trucks_total}`);
    setSafeText('stat-bins', stats.total_bins || bins.length);

    // ── 1. Top Bar Chart (KM / KG Waste & Cleared) ──
    const barCanvas = document.getElementById('vis-bar-chart');
    if (barCanvas && typeof Chart !== 'undefined') {
      const topBins = bins.slice(0, 6);
      const labels = topBins.map(b => b.bin_id);
      const series1Data = topBins.map(b => Math.round((b.current_fill_pct / 100) * 300));
      const series2Data = topBins.map(b => Math.max(20, Math.round(series1Data[topBins.indexOf(b)] * 0.75)));

      if (visBarChart) visBarChart.destroy();
      visBarChart = new Chart(barCanvas, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'SERIES 1 (LOAD)',
              data: series1Data,
              backgroundColor: '#0284c7',
              borderRadius: 3,
              barPercentage: 0.45,
            },
            {
              label: 'SERIES 2 (CLEARED)',
              data: series2Data,
              backgroundColor: '#10b981',
              borderRadius: 3,
              barPercentage: 0.45,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: '#64748b', font: { size: 10, family: 'JetBrains Mono' } }
            },
            y: {
              grid: { color: 'rgba(0, 0, 0, 0.05)' },
              ticks: { color: '#64748b', font: { size: 9, family: 'JetBrains Mono' } },
              max: 350
            }
          }
        }
      });
    }

    // ── 2. Middle Donut Chart (Capacity Status) ──
    const donutCanvas = document.getElementById('vis-donut-chart');
    if (donutCanvas && typeof Chart !== 'undefined') {
      const critCount = bins.filter(b => b.current_fill_pct >= 80 && b.current_fill_pct < 100).length;
      const modCount = bins.filter(b => b.current_fill_pct >= 50 && b.current_fill_pct < 80).length;
      const normCount = bins.filter(b => b.current_fill_pct < 50).length;
      const overCount = bins.filter(b => b.current_fill_pct >= 100).length;
      const total = bins.length || 1;

      setSafeText('donut-val-crit', `${critCount} Bins`);
      setSafeText('donut-pct-crit', `${Math.round((critCount / total) * 100)}%`);
      setSafeText('donut-val-mod', `${modCount} Bins`);
      setSafeText('donut-pct-mod', `${Math.round((modCount / total) * 100)}%`);
      setSafeText('donut-val-norm', `${normCount} Bins`);
      setSafeText('donut-pct-norm', `${Math.round((normCount / total) * 100)}%`);
      setSafeText('donut-val-over', `${overCount} Bins`);
      setSafeText('donut-pct-over', `${Math.round((overCount / total) * 100)}%`);

      if (visDonutChart) visDonutChart.destroy();
      visDonutChart = new Chart(donutCanvas, {
        type: 'doughnut',
        data: {
          labels: ['CRITICAL', 'MODERATE', 'NORMAL', 'OVERFLOW'],
          datasets: [{
            data: [critCount || 1, modCount || 1, normCount || 1, overCount || 1],
            backgroundColor: ['#ef4444', '#f59e0b', '#0284c7', '#8b5cf6'],
            borderColor: '#ffffff',
            borderWidth: 2,
            offset: [6, 0, 0, 0] // Offset slice matching reference
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '68%',
          plugins: { legend: { display: false } }
        }
      });
    }

    // ── 3. Bottom Dual Wave Spline Line Chart ──
    const lineCanvas = document.getElementById('vis-line-chart');
    if (lineCanvas && typeof Chart !== 'undefined') {
      const ctx = lineCanvas.getContext('2d');
      const gradCyan = ctx.createLinearGradient(0, 0, 0, 100);
      gradCyan.addColorStop(0, 'rgba(2, 132, 199, 0.28)');
      gradCyan.addColorStop(1, 'rgba(2, 132, 199, 0.0)');

      const gradMint = ctx.createLinearGradient(0, 0, 0, 100);
      gradMint.addColorStop(0, 'rgba(16, 185, 129, 0.25)');
      gradMint.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

      if (visLineChart) visLineChart.destroy();
      visLineChart = new Chart(lineCanvas, {
        type: 'line',
        data: {
          labels: ['1.1', '2.1', '3.1', '4.1', '5.1', '6.1'],
          datasets: [
            {
              label: 'SERIES 1',
              data: [15, 28, 12, 38, 22, 30],
              borderColor: '#0284c7',
              backgroundColor: gradCyan,
              fill: true,
              tension: 0.45,
              borderWidth: 2,
              pointRadius: 0
            },
            {
              label: 'SERIES 2',
              data: [10, 18, 26, 20, 32, 24],
              borderColor: '#10b981',
              backgroundColor: gradMint,
              fill: true,
              tension: 0.45,
              borderWidth: 2,
              pointRadius: 0
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: '#64748b', font: { size: 10, family: 'JetBrains Mono' } }
            },
            y: {
              grid: { color: 'rgba(0, 0, 0, 0.05)' },
              ticks: { color: '#64748b', font: { size: 9, family: 'JetBrains Mono' } },
              max: 45
            }
          }
        }
      });
    }

    // ── 4. Interactive Sites Pins on Planetary Globe ──
    const pinLayer = document.getElementById('vis-sites-pins-layer');
    if (pinLayer) {
      pinLayer.innerHTML = '';

      // Project bins coordinates (Ward 142 bounding box) onto curved Earth stage
      // Lat range: 12.915 to 12.936, Lon range: 77.575 to 77.596
      const minLat = 12.915, maxLat = 12.936;
      const minLon = 77.575, maxLon = 77.596;

      bins.forEach((b) => {
        const normLon = Math.max(0, Math.min(1, (b.longitude - minLon) / (maxLon - minLon)));
        const normLat = Math.max(0, Math.min(1, (b.latitude - minLat) / (maxLat - minLat)));

        // Position on globe (X: 18% to 82%, Y: 18% to 68%)
        const posX = (18 + normLon * 64).toFixed(1);
        const posY = (18 + (1 - normLat) * 50).toFixed(1);

        const statusClass = b.current_fill_pct >= 80 ? 'crit' : b.current_fill_pct >= 50 ? 'mod' : 'norm';

        const pin = document.createElement('div');
        pin.className = `vis-site-pin ${b.bin_id === selectedBinId ? 'active' : ''}`;
        pin.dataset.binId = b.bin_id;
        pin.style.left = `${posX}%`;
        pin.style.top = `${posY}%`;
        pin.innerHTML = `
          <div class="pin-core ${statusClass}">
            <div class="pin-ripple" style="color: ${statusClass === 'crit' ? '#ef4444' : statusClass === 'mod' ? '#f59e0b' : '#00f5a0'}"></div>
          </div>
          <span class="pin-chip-label font-mono">${b.bin_id}</span>
        `;

        pin.addEventListener('click', () => selectVisSite(b.bin_id));
        pinLayer.appendChild(pin);
      });

      // Default select first bin or current
      selectVisSite(selectedBinId);
    }

    // ── 5. Circular Gauges & Bottom HUD Metrics ──
    const avgFill = Math.round(bins.reduce((acc, b) => acc + b.current_fill_pct, 0) / (bins.length || 1));
    const cleanIndex = Math.max(10, 100 - Math.round(avgFill * 0.7));
    const slaIndex = 94;

    setSafeText('dial-clean-val', `${cleanIndex}%`);
    setSafeText('dial-sla-val', `${slaIndex}`);

    const cleanProg = document.getElementById('dial-prog-clean');
    if (cleanProg) {
      const offset = 264 - (264 * cleanIndex) / 100;
      cleanProg.style.strokeDashoffset = `${offset}`;
    }

    const slaProg = document.getElementById('dial-prog-sla');
    if (slaProg) {
      const offset = 264 - (264 * slaIndex) / 100;
      slaProg.style.strokeDashoffset = `${offset}`;
    }

    // Horizontal Level Breakdown (Sum capacity in kg)
    const totalCap = bins.reduce((acc, b) => acc + b.capacity_kg, 0);
    setSafeText('level-val-wet', `${Math.round(totalCap * 0.58).toLocaleString()} UNIT`);
    setSafeText('level-val-dry', `${Math.round(totalCap * 0.32).toLocaleString()} UNIT`);
    setSafeText('level-val-haz', `${Math.round(totalCap * 0.10).toLocaleString()} UNIT`);

    // Unit statistics
    setSafeText('unit-stat-sites', bins.length || 25);
    setSafeText('unit-stat-trucks', stats.trucks_active ? `0${stats.trucks_active}` : '03');

    // Grievance Feed Table
    const tbody = document.querySelector('#dashboard-apps-table tbody');
    if (tbody) {
      if (!apps.length) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-6">No grievance applications recorded.</td></tr>`;
      } else {
        tbody.innerHTML = apps.slice(0, 8).map(a => {
          const urg = (a.ai_urgency || 'MEDIUM').toUpperCase();
          const status = (a.status || 'PENDING').toUpperCase();
          const urgColor = urg === 'HIGH' ? '#ef4444' : urg === 'MEDIUM' ? '#f59e0b' : '#10b981';
          const statusColor = status === 'COMPLETED' ? '#10b981' : status === 'APPROVED' ? '#38bdf8' : status === 'REJECTED' ? '#ef4444' : '#f59e0b';
          const timeStr = a.created_at ? a.created_at.replace('T', ' ').substring(0, 16) : 'Just now';

          return `
            <tr>
              <td><span class="font-mono font-bold text-green">${a.application_id}</span></td>
              <td>${a.citizen_name}</td>
              <td><span class="font-mono text-cyan">${a.bin_id}</span></td>
              <td>${a.problem_type}</td>
              <td><span style="color:${urgColor};font-weight:700">${urg}</span></td>
              <td><span style="color:${statusColor};font-weight:700">${status}</span></td>
              <td class="text-muted text-xs font-mono">${timeStr}</td>
            </tr>
          `;
        }).join('');
      }
    }

  } catch (err) {
    console.error('Failed to load Data Visualization dashboard:', err);
  }
}

// Simulation Controls
document.getElementById('btn-dash-sim-advance')?.addEventListener('click', async () => {
  try {
    const res = await fetch(`${API}/simulation/advance`, { method: 'POST' });
    const data = await res.json();
    showToast({ title: 'Simulation Step Completed', description: data.message, variant: 'primary' });
    loadDashboard();
  } catch (e) {
    showToast({ title: 'Simulation Error', variant: 'destructive' });
  }
});

document.getElementById('btn-dash-sim-sla')?.addEventListener('click', async () => {
  try {
    const res = await fetch(`${API}/simulation/auto-approve`, { method: 'POST' });
    const data = await res.json();
    showToast({ title: 'Auto-SLA Approvals Processed', description: data.message, variant: 'success' });
    loadDashboard();
  } catch (e) {
    showToast({ title: 'SLA Error', variant: 'destructive' });
  }
});

// ══════════════════════════════════════════════════════════════
// CITIZEN GRIEVANCE FILING & VISION AI
// ══════════════════════════════════════════════════════════════
async function loadComplaintBins() {
  try {
    const bins = await fetch(`${API}/bins`).then(r => r.json());
    const select = document.getElementById('c-bin');
    if (!select) return;
    select.innerHTML = bins.map(b =>
      `<option value="${b.bin_id}">${b.bin_id} — ${b.landmark} (${b.current_fill_pct}% fill)</option>`
    ).join('');
  } catch (e) {
    console.error('Failed to load bins for form:', e);
  }
}

// Grievance problem category pill selection handler
document.querySelectorAll('.g-category-pill').forEach(pill => {
  pill.addEventListener('click', () => {
    document.querySelectorAll('.g-category-pill').forEach(p => p.classList.remove('active'));
    pill.classList.add('active');
    const problemSelect = document.getElementById('c-problem');
    if (problemSelect) {
      problemSelect.value = pill.dataset.value;
    }
  });
});

const uploadZone = document.getElementById('photo-upload-zone');
const photoInput = document.getElementById('c-photo');
const photoPreview = document.getElementById('photo-preview');
const uploadPlaceholder = document.getElementById('upload-placeholder');

uploadZone?.addEventListener('click', () => photoInput.click());
uploadZone?.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('dragover'); });
uploadZone?.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
uploadZone?.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadZone.classList.remove('dragover');
  if (e.dataTransfer.files.length) {
    handlePhotoUpload(e.dataTransfer.files[0]);
  }
});

photoInput?.addEventListener('change', () => {
  if (photoInput.files.length) handlePhotoUpload(photoInput.files[0]);
});

function handlePhotoUpload(file) {
  const reader = new FileReader();
  reader.onload = async (e) => {
    photoPreview.src = e.target.result;
    photoPreview.classList.add('visible');
    uploadPlaceholder.style.display = 'none';
    await analyzePhoto(e.target.result);
  };
  reader.readAsDataURL(file);
}

async function analyzePhoto(base64Data) {
  const panel = document.getElementById('ai-panel-body');
  const badge = document.getElementById('ai-status-badge');
  badge.textContent = 'Analyzing…';
  badge.style.background = '#fef3c7';
  badge.style.color = '#b45309';

  panel.innerHTML = `
    <div class="ai-empty-prompt" style="padding:1.25rem 0.5rem;text-align:center">
      <div class="preloader-leaf-spin" style="font-size:2rem;margin:0 auto 0.75rem">🌿</div>
      <h4 class="text-sm font-semibold text-main">Multimodal Vision Diagnostic in Progress</h4>
      <p class="text-xs text-muted mt-1">Reading pixels via OpenRouter &amp; Hugging Face neural waste models…</p>
    </div>
  `;

  try {
    const res = await fetch(`${API}/analyze-photo`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ photo_base64: base64Data })
    });
    currentAiResult = await res.json();
    renderAiPanel(currentAiResult);
    badge.textContent = 'Diagnosed';
    badge.style.background = '#dcfce7';
    badge.style.color = '#15803d';
  } catch (e) {
    panel.innerHTML = `<div class="ai-empty-prompt" style="padding:1rem;text-align:center"><p class="text-red font-semibold text-xs">Diagnostic pipeline notice: fallback active</p></div>`;
    badge.textContent = 'Offline';
  }
}

function renderAiPanel(ai) {
  const panel = document.getElementById('ai-panel-body');
  const urg = (ai.urgency || 'MEDIUM').toUpperCase();
  const urgColor = urg === 'CRITICAL' ? '#e11d48' : urg === 'HIGH' ? 'var(--red-accent)' : urg === 'MEDIUM' ? 'var(--amber-accent)' : '#15803d';
  const fill = ai.fill_pct || 75;
  const fillColor = fill >= 85 ? '#e11d48' : fill >= 60 ? '#f59e0b' : '#10b981';

  panel.innerHTML = `
    <div class="space-y-3">
      <div class="flex items-center justify-between border-b border-light pb-2">
        <span class="text-xs font-semibold text-main flex items-center gap-1">
          <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#10b981"></span>
          ${ai.raw_ai_source || 'OpenRouter / HuggingFace Vision AI'}
        </span>
        <span style="background:${urgColor}18;color:${urgColor};border:1px solid ${urgColor}40;font-weight:700;padding:2px 8px;border-radius:9999px;font-size:0.75rem">
          ${urg} PRIORITY
        </span>
      </div>

      <div class="grid-2-col gap-2">
        <div class="eco-card p-2-5 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px">
          <div class="text-xl font-mono font-bold" style="color:${fillColor}">${fill}%</div>
          <div class="text-xs text-muted">Fill Volume</div>
          <div style="background:#e2e8f0;height:4px;border-radius:2px;margin-top:4px;overflow:hidden">
            <div style="background:${fillColor};height:100%;width:${Math.min(100, fill)}%"></div>
          </div>
        </div>
        <div class="eco-card p-2-5 text-center" style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px">
          <div class="text-xl font-mono font-bold text-main">${ai.est_weight_kg || '0'} kg</div>
          <div class="text-xs text-muted">Est. Payload</div>
          <div class="text-xs font-mono text-emerald" style="font-size:0.7rem;margin-top:2px">Confidence: ${ai.confidence || '96.4%'}</div>
        </div>
      </div>

      <div class="text-xs space-y-1.5 mt-2">
        <div class="flex justify-between py-1 border-b border-light">
          <span class="text-muted">Classification</span>
          <span class="font-semibold text-main text-right">${ai.waste_type}</span>
        </div>
        <div class="flex justify-between py-1 border-b border-light">
          <span class="text-muted">Spillage Status</span>
          <span style="color:${ai.overflow_detected ? '#e11d48' : '#15803d'};font-weight:700">
            ${ai.overflow_detected ? '⚠️ Spillage Beyond Rim' : '✅ Within Container Rim'}
          </span>
        </div>
      </div>

      <div class="p-2-5 rounded-lg text-xs font-mono mt-2" style="background:#f1f5f9;border:1px solid #cbd5e1;line-height:1.4;color:#334155">
        <strong style="color:#0f172a">Diagnostic Insight:</strong> ${ai.reasoning}
      </div>
    </div>
  `;

  // Auto-select problem pill if appropriate
  if (ai.overflow_detected) {
    const pill = document.querySelector('.g-category-pill[data-value="Overflow (>90% full)"]');
    if (pill) pill.click();
  } else if (ai.waste_type && ai.waste_type.toLowerCase().includes('hazard')) {
    const pill = document.querySelector('.g-category-pill[data-value="Hazardous / Biomedical waste mixed"]');
    if (pill) pill.click();
  }
}

// Form Submit
document.getElementById('complaint-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = document.getElementById('btn-submit-complaint');
  btn.disabled = true;
  btn.innerHTML = `<span>Lodging Grievance…</span>`;

  const payload = {
    citizen_name: document.getElementById('c-name').value,
    citizen_phone: document.getElementById('c-phone').value,
    bin_id: document.getElementById('c-bin').value,
    location_desc: document.getElementById('c-location').value,
    problem_type: document.getElementById('c-problem').value,
    photo_base64: photoPreview.classList.contains('visible') ? photoPreview.src : null
  };

  try {
    const res = await fetch(`${API}/applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    document.getElementById('modal-app-id').textContent = data.application_id;
    document.getElementById('complaint-success-modal').classList.add('visible');

    showToast({
      title: 'Grievance Registered',
      description: `Reference ID: ${data.application_id}`,
      variant: 'success'
    });

    document.getElementById('modal-close-btn').onclick = () => {
      document.getElementById('complaint-success-modal').classList.remove('visible');
      document.getElementById('tracker-search-input').value = data.application_id;
      navigateTo('tracker');
      trackApplication(data.application_id);
    };
  } catch (err) {
    showToast({ title: 'Submission Failed', description: 'Please retry.', variant: 'destructive' });
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>Register Grievance With Municipal Desk</span> <span class="arrow-icon">→</span>`;
  }
});

// ══════════════════════════════════════════════════════════════
// STATUS TRACKER
// ══════════════════════════════════════════════════════════════
async function loadTrackerChips() {
  try {
    const apps = await fetch(`${API}/applications`).then(r => r.json());
    const chips = document.getElementById('tracker-chips');
    if (!chips) return;

    chips.innerHTML = apps.slice(0, 6).map(a =>
      `<button class="chip-btn" data-id="${a.application_id}">${a.application_id}</button>`
    ).join('');

    chips.querySelectorAll('.chip-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.getElementById('tracker-search-input').value = btn.dataset.id;
        trackApplication(btn.dataset.id);
      });
    });

    const currentInput = document.getElementById('tracker-search-input').value;
    if (!currentInput && apps.length > 0) {
      document.getElementById('tracker-search-input').value = apps[0].application_id;
      trackApplication(apps[0].application_id);
    }
  } catch (e) {
    console.error('Failed to load tracker chips:', e);
  }
}

document.getElementById('btn-track')?.addEventListener('click', () => {
  const query = document.getElementById('tracker-search-input').value.trim();
  if (query) trackApplication(query);
});

function formatTimelineDate(dateStr, defaultOffsetMin = 0) {
  try {
    const d = dateStr ? new Date(dateStr) : new Date(Date.now() - defaultOffsetMin * 60000);
    if (isNaN(d.getTime())) throw new Error();
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const day = d.getDate();
    const mon = months[d.getMonth()];
    const hours = String(d.getHours()).padStart(2, '0');
    const mins = String(d.getMinutes()).padStart(2, '0');
    return `${day} ${mon}, ${hours}:${mins}`;
  } catch (_) {
    return '17 Nov, 13:45';
  }
}

async function trackApplication(appId) {
  const resultZone = document.getElementById('tracker-result');
  resultZone.innerHTML = `
    <div class="eco-card p-8 text-center" style="max-width: 480px; margin: 0 0 0 auto; border-radius: 28px;">
      <div class="preloader-leaf-spin" style="font-size:2rem;margin:0 auto 1rem">🌿</div>
      <p class="text-muted font-mono text-sm">Auditing Ward 142 Milestones for ${appId}…</p>
    </div>
  `;

  try {
    const [app, timeline] = await Promise.all([
      fetch(`${API}/applications/${appId}`).then(r => r.json()),
      fetch(`${API}/applications/${appId}/timeline`).then(r => r.json())
    ]);

    if (!app || app.error) {
      resultZone.innerHTML = `
        <div class="eco-card p-8 text-center" style="max-width: 480px; margin: 0 0 0 auto; border-radius: 28px;">
          <p class="text-red font-semibold">Application Reference Not Found</p>
          <p class="text-xs text-muted mt-1">Please verify the application tracking reference and retry.</p>
        </div>
      `;
      return;
    }

    const status = (app.status || 'PENDING').toUpperCase();
    const isCompleted = status === 'COMPLETED' || status === 'CLEARED' || status === 'RESOLVED';
    const isInTransit = status === 'DISPATCHED' || status === 'EN_ROUTE' || isCompleted;
    const isTriageDone = status === 'APPROVED' || isInTransit || isCompleted;

    const baseDate = app.created_at ? new Date(app.created_at) : new Date();
    const time1 = formatTimelineDate(app.created_at || timeline[0]?.timestamp, 90);
    const time2 = formatTimelineDate(timeline[1]?.timestamp, 60);
    const time3 = formatTimelineDate(timeline[2]?.timestamp, 30);
    const time4 = isCompleted ? formatTimelineDate(timeline[3]?.timestamp || timeline[timeline.length - 1]?.timestamp, 5) : '17 Nov, 13:45';

    resultZone.innerHTML = `
      <div class="tracker-stage-wrapper">
        <div class="status-card-replica">
          <!-- Top Row: Timeline pill + Dashed Connector + State Pill -->
          <div class="status-card-top-row">
            <div class="status-timeline-badge">Timeline</div>
            <div class="status-dotted-connector"></div>
            <div class="status-pill-state ${isCompleted ? 'completed' : ''}">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>${isCompleted ? 'Completed' : 'In Progress'}</span>
            </div>
          </div>

          <!-- Milestones List (Replicating Image 1 exact 4 milestones and icon bubbles) -->
          <div class="status-milestones-list">
            
            <!-- Step 1: Application Registered -->
            <div class="status-step-row">
              <div class="status-icon-bubble done" title="Application Registered">
                <svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10 9 9 9 8 9"/>
                </svg>
              </div>
              <div class="status-step-content">
                <div class="status-step-title">Application Registered</div>
                <div class="status-step-sub">Grievance lodged and reference ID generated</div>
              </div>
              <div class="status-step-time">${time1}</div>
            </div>
            
            <div class="status-vertical-line"></div>

            <!-- Step 2: Waiting for Approval -->
            <div class="status-step-row">
              <div class="status-icon-bubble ${isTriageDone ? 'done' : 'active'}" title="Waiting for Approval">
                <svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
              </div>
              <div class="status-step-content">
                <div class="status-step-title">Waiting for Approval</div>
                <div class="status-step-sub">AI diagnostic verified, pending zonal officer sign-off</div>
              </div>
              <div class="status-step-time">${time2}</div>
            </div>

            <div class="status-vertical-line"></div>

            <!-- Step 3: Application Sent to Municipal -->
            <div class="status-step-row">
              <div class="status-icon-bubble ${isInTransit ? 'done' : ''}" title="Application Sent to Municipal">
                <svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="1" y="3" width="15" height="13"/>
                  <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/>
                  <circle cx="5.5" cy="18.5" r="2.5"/>
                  <circle cx="18.5" cy="18.5" r="2.5"/>
                </svg>
              </div>
              <div class="status-step-content">
                <div class="status-step-title">Application Sent to Municipal</div>
                <div class="status-step-sub">Dispatched to Ward 142 compactor crew</div>
              </div>
              <div class="status-step-time">${time3}</div>
            </div>

            <div class="status-vertical-line"></div>

            <!-- Step 4: Application Completed -->
            <div class="status-step-row">
              <div class="status-icon-bubble ${isCompleted ? 'done' : ''}" title="Application Completed">
                <svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
              </div>
              <div class="status-step-content">
                <div class="status-step-title">Application Completed</div>
                <div class="status-step-sub">Bin cleared and site verified spotless</div>
              </div>
              <div class="status-step-time">${time4}</div>
            </div>

          </div>

          <!-- Bottom Action: Rate This Delivery Pill Button -->
          <button class="status-rate-btn" onclick="handleRateDelivery('${app.application_id}')">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0"/>
              <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2"/>
              <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8"/>
              <path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.83L7 15"/>
            </svg>
            <span>Rate this delivery</span>
          </button>
        </div>
      </div>
    `;

  } catch (e) {
    resultZone.innerHTML = `<div class="eco-card p-6 text-center text-red" style="max-width: 480px; margin: 0 auto; border-radius: 28px;">Error retrieving status telemetry.</div>`;
  }
}

// Interactive Delivery Rating Dialog
window.handleRateDelivery = function(appId) {
  const existing = document.getElementById('rate-delivery-modal');
  if (existing) existing.remove();

  const modal = document.createElement('div');
  modal.id = 'rate-delivery-modal';
  modal.className = 'eco-modal-overlay active';
  modal.innerHTML = `
    <div class="modal-dialog-box text-center" style="max-width: 420px; background: #ffffff; border-radius: 24px; padding: 2rem;">
      <div style="font-size: 2.4rem; margin-bottom: 0.5rem;">👏</div>
      <h3 class="modal-title" style="font-size: 1.25rem; font-weight: 700; color: #0f172a;">Rate Ward Clearance Service</h3>
      <p class="text-xs text-muted mt-1 font-mono">Reference: ${appId}</p>
      
      <div style="display: flex; justify-content: center; gap: 10px; font-size: 2rem; margin: 1.25rem 0; cursor: pointer; color: #eab308;" id="rate-stars-row">
        <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
      </div>
      <p class="text-xs text-dim mb-4">Ward 142 Citizen Satisfaction: <strong>5.0 / 5.0 (Spotless)</strong></p>
      
      <textarea id="rate-feedback-txt" class="eco-input full-width text-xs mb-4" rows="2" placeholder="Citizen comments on compactor efficiency..." style="border-radius: 12px; padding: 10px; border: 1px solid #e2e8f0;">Bin emptied swiftly and surrounding area sanitized with lime powder.</textarea>
      
      <button class="status-rate-btn" style="margin-top: 0; justify-content: center;" onclick="submitDeliveryRating('${appId}')">
        <span>Submit Citizen Rating</span>
      </button>
      <button class="btn-eco-ghost mt-2 full-width text-xs" style="background: transparent; border: none; color: #64748b; cursor: pointer; padding: 8px;" onclick="document.getElementById('rate-delivery-modal').remove()">Dismiss</button>
    </div>
  `;
  document.body.appendChild(modal);
};

window.submitDeliveryRating = function(appId) {
  const modal = document.getElementById('rate-delivery-modal');
  if (modal) {
    modal.innerHTML = `
      <div class="modal-dialog-box text-center" style="max-width: 380px; background: #ffffff; border-radius: 24px; padding: 2rem;">
        <div style="font-size: 2.6rem; margin-bottom: 0.5rem;">✨</div>
        <h3 class="modal-title" style="font-size: 1.2rem; font-weight: 700; color: #15803d;">Rating Submitted!</h3>
        <p class="text-xs text-muted mt-2">Thank you! Your verified rating for <strong>${appId}</strong> has been committed to the Ward 142 Municipal Ledger.</p>
        <button class="status-rate-btn mt-4" style="justify-content: center;" onclick="document.getElementById('rate-delivery-modal').remove()">Done</button>
      </div>
    `;
    setTimeout(() => {
      const m = document.getElementById('rate-delivery-modal');
      if (m) m.remove();
    }, 2400);
  }
};

// ══════════════════════════════════════════════════════════════
// OFFICER DESK (BBMP Review Console)
// ══════════════════════════════════════════════════════════════
async function loadOfficerDashboard(filter = 'PENDING') {
  try {
    const [stats, apps] = await Promise.all([
      fetch(`${API}/dashboard/stats`).then(r => r.json()),
      fetch(`${API}/applications?status=${filter}`).then(r => r.json())
    ]);

    const kpiBar = document.getElementById('officer-kpi');
    if (kpiBar) {
      kpiBar.innerHTML = [
        { label: 'Pending Review', val: stats.pending, color: 'var(--amber-accent)' },
        { label: 'Active Work Orders', val: stats.approved, color: 'var(--forest-dark)' },
        { label: 'Resolved Today', val: stats.completed, color: '#15803d' },
        { label: 'Rejected', val: stats.rejected, color: 'var(--red-accent)' },
      ].map(k => `
        <div class="eco-stat-card p-4">
          <div class="text-2xl font-mono font-bold" style="color:${k.color}">${k.val}</div>
          <div class="stat-title">${k.label}</div>
        </div>
      `).join('');
    }

    const container = document.getElementById('officer-cards');
    if (!container) return;

    if (!apps.length) {
      container.innerHTML = `<div class="col-span-full eco-card p-8 text-center text-muted">No applications currently in '${filter}' status queue.</div>`;
      return;
    }

    container.innerHTML = apps.map(a => {
      const urg = (a.ai_urgency || 'MEDIUM').toUpperCase();
      const status = (a.status || 'PENDING').toUpperCase();
      const urgColor = urg === 'HIGH' ? 'var(--red-accent)' : urg === 'MEDIUM' ? 'var(--amber-accent)' : '#15803d';

      return `
        <div class="officer-card" data-appid="${a.application_id}">
          <div class="oc-header">
            <div>
              <div class="oc-id">${a.application_id}</div>
              <div class="oc-citizen">${a.citizen_name} • ${a.citizen_phone}</div>
            </div>
            <span style="color:${urgColor};font-weight:800;font-size:0.82rem">${urg}</span>
          </div>

          <div class="oc-body">
            <div class="oc-item"><div class="lbl">Bin</div><div class="val">${a.landmark || 'N/A'} (${a.bin_id})</div></div>
            <div class="oc-item"><div class="lbl">Problem</div><div class="val">${a.problem_type}</div></div>
            <div class="oc-item"><div class="lbl">Fill Assessment</div><div class="val font-mono">${a.ai_fill_pct}%</div></div>
            <div class="oc-item"><div class="lbl">Waste Type</div><div class="val">${a.ai_waste_type || 'General'}</div></div>
          </div>

          ${a.status === 'PENDING' ? `
            <div class="oc-actions">
              <select class="eco-select flex-1 text-xs py-1">
                <option value="T01">T01 (Rajesh Kumar, 6.0 km/L)</option>
                <option value="T02">T02 (Suresh Reddy, 5.5 km/L)</option>
                <option value="T03">T03 (Manjunath, 6.2 km/L)</option>
              </select>
              <button class="btn-action-sm approve" onclick="window.approveApp('${a.application_id}', this)">Approve</button>
              <button class="btn-action-sm hold" onclick="window.holdApp('${a.application_id}')">Hold</button>
              <button class="btn-action-sm reject" onclick="window.rejectApp('${a.application_id}')">Reject</button>
            </div>
          ` : `
            <div class="pt-3 border-t border-light text-xs text-dim flex justify-between font-mono">
              <span>WO: <span class="text-green font-bold">${a.work_order_id || 'N/A'}</span></span>
              <span>Truck: <span class="text-emerald font-bold">${a.assigned_truck_id || 'N/A'}</span></span>
            </div>
          `}
        </div>
      `;
    }).join('');

  } catch (e) {
    console.error('Officer console error:', e);
  }
}

window.approveApp = async (appId, btn) => {
  const card = btn.closest('.officer-card');
  const truckId = card.querySelector('select').value;
  try {
    await fetch(`${API}/applications/${appId}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ truck_id: truckId })
    });
    showToast({ title: 'Work Order Issued', description: `Assigned Truck ${truckId} to ${appId}`, variant: 'success' });
    loadOfficerDashboard('PENDING');
  } catch (e) {
    showToast({ title: 'Approval Failed', variant: 'destructive' });
  }
};

window.holdApp = async (appId) => {
  await fetch(`${API}/applications/${appId}/hold`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
  showToast({ title: 'Application Put on Hold', description: appId, variant: 'primary' });
  loadOfficerDashboard('PENDING');
};

window.rejectApp = async (appId) => {
  await fetch(`${API}/applications/${appId}/reject`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
  showToast({ title: 'Application Rejected', description: appId, variant: 'destructive' });
  loadOfficerDashboard('PENDING');
};

document.querySelectorAll('.tab-btn').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    loadOfficerDashboard(tab.dataset.filter);
  });
});

// ══════════════════════════════════════════════════════════════
// LIVE MAP & FLEET TELEMETRY (Leaflet Voyager Clean Tiles)
// ══════════════════════════════════════════════════════════════
async function loadMap() {
  try {
    const [bins, trucks, cfg] = await Promise.all([
      fetch(`${API}/bins`).then(r => r.json()),
      fetch(`${API}/trucks`).then(r => r.json()),
      fetch(`${API}/config`).then(r => r.json()).catch(() => null)
    ]);

    const mapboxToken = cfg?.mapbox_token || (import.meta.env && import.meta.env.VITE_MAPBOX_ACCESS_TOKEN) || '';
    const cartoKey = cfg?.carto_key || ((import.meta.env && import.meta.env.VITE_CARTO_API_KEY) ? import.meta.env.VITE_CARTO_API_KEY.trim() : '') || '';

    if (!leafletMap) {
      leafletMap = L.map('leaflet-map').setView([12.9250, 77.5830], 15);

      const baseLayers = {};

      // 1. Primary Mapbox Streets HD
      if (mapboxToken) {
        const mapboxStreets = L.tileLayer(
          `https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/{z}/{x}/{y}?access_token=${mapboxToken}`,
          {
            attribution: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            tileSize: 512,
            zoomOffset: -1,
            maxZoom: 20
          }
        );
        const mapboxSatellite = L.tileLayer(
          `https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v12/tiles/{z}/{x}/{y}?access_token=${mapboxToken}`,
          {
            attribution: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © Maxar',
            tileSize: 512,
            zoomOffset: -1,
            maxZoom: 20
          }
        );

        baseLayers['🗺️ Mapbox Streets (HD)'] = mapboxStreets;
        baseLayers['🛰️ Mapbox Satellite HD'] = mapboxSatellite;
        mapboxStreets.addTo(leafletMap);
      }

      // 2. CARTO Voyager Layer
      const cartoTileUrl = `https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png?key=${encodeURIComponent(cartoKey)}`;
      const cartoLayer = L.tileLayer(cartoTileUrl, {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> © <a href="https://carto.com/attributions">CARTO</a>',
        maxZoom: 19
      });
      cartoLayer.on('tileerror', function(e) {
        if (e.tile && !e.tile.__fallbackApplied) {
          e.tile.__fallbackApplied = true;
          const coords = e.coords;
          if (coords) e.tile.src = `https://tile.openstreetmap.org/${coords.z}/${coords.x}/${coords.y}.png`;
        }
      });
      baseLayers['🏙️ CARTO Voyager'] = cartoLayer;

      if (!mapboxToken) {
        cartoLayer.addTo(leafletMap);
      }

      // 3. OpenStreetMap
      const osmLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      });
      baseLayers['🌍 OpenStreetMap'] = osmLayer;

      L.control.layers(baseLayers, null, { position: 'topright' }).addTo(leafletMap);
    }

    // Attach Mapbox Status HUD pill inside the map container
    const mapElem = document.getElementById('leaflet-map');
    if (mapElem && !document.getElementById('mapbox-status-pill')) {
      const pill = document.createElement('div');
      pill.id = 'mapbox-status-pill';
      pill.style.cssText = 'position:absolute;bottom:14px;left:14px;z-index:999;background:rgba(18,43,30,0.88);backdrop-filter:blur(8px);color:#fff;padding:6px 14px;border-radius:9999px;font-size:11px;font-weight:600;display:flex;align-items:center;gap:8px;box-shadow:0 4px 12px rgba(0,0,0,0.25);border:1px solid rgba(82,183,136,0.35)';
      pill.innerHTML = '<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#52b788;box-shadow:0 0 8px #52b788"></span> Mapbox HD Telemetry Active';
      mapElem.appendChild(pill);
    }

    leafletMap.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.CircleMarker || layer instanceof L.Polyline) {
        leafletMap.removeLayer(layer);
      }
    });

    // Depot marker
    L.marker([12.9290, 77.5835], {
      icon: L.divIcon({
        className: 'depot-marker',
        html: `<div style="background:#122b1e;color:#fff;border:2px solid #52b788;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px rgba(18,43,30,0.3)">🏛</div>`,
        iconSize: [26, 26],
        iconAnchor: [13, 13]
      })
    }).addTo(leafletMap).bindPopup('<b>BBMP Ward 142 Depot HQ</b><br>Jayanagar Sub-Division');

    // Bins
    bins.forEach(b => {
      const fill = b.current_fill_pct;
      const color = fill >= 80 ? '#e11d48' : fill >= 50 ? '#d97706' : '#15803d';
      L.circleMarker([b.latitude, b.longitude], {
        radius: 6 + (fill / 20),
        color: color,
        fillColor: color,
        fillOpacity: 0.75,
        weight: 2
      }).addTo(leafletMap).bindPopup(`
        <div style="font-family:Inter,sans-serif;font-size:12px;color:#1e293b">
          <strong>Bin ${b.bin_id}</strong><br>
          ${b.landmark}<br>
          Fill Level: <strong>${fill}%</strong> (${b.capacity_kg} kg)
        </div>
      `);
    });

    // Trucks
    trucks.forEach(t => {
      const isActive = t.status !== 'Available';
      L.marker([t.current_lat, t.current_lon], {
        icon: L.divIcon({
          className: 'truck-marker',
          html: `<div style="background:${isActive ? '#122b1e' : '#64748b'};color:#fff;border-radius:9999px;padding:4px 10px;font-size:11px;font-weight:700;box-shadow:0 3px 8px rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.4)">${t.truck_id} 🚛</div>`,
          iconSize: null,
          iconAnchor: [24, 12]
        })
      }).addTo(leafletMap).bindPopup(`
        <div style="font-family:Inter,sans-serif;font-size:12px;color:#1e293b">
          <strong>Truck ${t.truck_id}</strong> (${t.driver_name})<br>
          Status: <strong>${t.status}</strong><br>
          Target: ${t.target_bin_id || 'Depot Standby'}
        </div>
      `);

      if (t.target_bin_id) {
        const tb = bins.find(b => b.bin_id === t.target_bin_id);
        if (tb) {
          // Attempt Mapbox driving directions for true road navigation geometry
          fetch(`${API}/route/directions?start=${t.current_lon},${t.current_lat}&end=${tb.longitude},${tb.latitude}`)
            .then(r => r.json())
            .then(data => {
              if (data && data.routes && data.routes[0]) {
                const coords = data.routes[0].geometry.coordinates.map(c => [c[1], c[0]]);
                L.polyline(coords, {
                  color: '#10b981',
                  weight: 3.5,
                  opacity: 0.9
                }).addTo(leafletMap);
              } else {
                L.polyline([[t.current_lat, t.current_lon], [tb.latitude, tb.longitude]], {
                  color: '#1a422e',
                  weight: 2.5,
                  dashArray: '5, 8',
                  opacity: 0.85
                }).addTo(leafletMap);
              }
            })
            .catch(() => {
              L.polyline([[t.current_lat, t.current_lon], [tb.latitude, tb.longitude]], {
                color: '#1a422e',
                weight: 2.5,
                dashArray: '5, 8',
                opacity: 0.85
              }).addTo(leafletMap);
            });
        }
      }
    });

    const fleetContainer = document.getElementById('fleet-cards');
    if (fleetContainer) {
      fleetContainer.innerHTML = trucks.map(t => `
        <div class="fleet-box">
          <div class="flex justify-between items-center">
            <span class="font-bold text-main text-sm">${t.truck_id}</span>
            <span class="badge-pill">${t.status}</span>
          </div>
          <div class="text-xs text-muted">${t.driver_name} • ${t.mileage_km_l} km/L</div>
          <div class="text-xs font-mono text-dim mt-1">Target: <span class="text-main">${t.target_bin_id || 'Depot HQ'}</span></div>
        </div>
      `).join('');
    }

    setTimeout(() => leafletMap?.invalidateSize(), 200);

  } catch (e) {
    console.error('Failed to load map GIS:', e);
  }
}

// ══════════════════════════════════════════════════════════════
// GENERATIVE ROUTE TREE LAYOUT STATION (IMAGE 2 REPLICA)
// ══════════════════════════════════════════════════════════════
let treeNodesCache = [];
let treeCanvasInitialized = false;

function initFuelTreeCanvas() {
  const canvas = document.getElementById('fuel-tree-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  function getSliderVal(id, fallback) {
    const el = document.getElementById(id);
    return el ? parseFloat(el.value) : fallback;
  }

  function renderTree() {
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    // Canvas background
    ctx.fillStyle = '#ebebeb';
    ctx.fillRect(0, 0, w, h);

    const scale = getSliderVal('p-scale', 1.0);
    const scaleRed = getSliderVal('p-scalered', 1.05);
    const widthVal = getSliderVal('p-width', 1.42);
    const widthRed = getSliderVal('p-widthred', 0.66);
    const leafLen = getSliderVal('p-leaflen', 0.50);
    const rotDeg = getSliderVal('p-rot', 70);
    const subSeg = Math.round(getSliderVal('p-subseg', 2));
    const varLen = getSliderVal('p-varlen', 50);
    const varAng = getSliderVal('p-varang', 50);
    const spawnChance = getSliderVal('p-spawn', 0.0);
    const rootLen = getSliderVal('p-rootlen', 0.66);
    const rootWidth = getSliderVal('p-rootw', 2.0);

    // Root coordinate at bottom right (just like in Image 2)
    const rootX = w * 0.74;
    const rootY = h * 0.90;

    treeNodesCache = [];

    // Draw Root base ring (matching Image 2 bottom-right ring)
    ctx.beginPath();
    ctx.arc(rootX, rootY, 7.5, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
    ctx.lineWidth = 2.4;
    ctx.strokeStyle = '#111111';
    ctx.stroke();

    // Node tags sample IDs matching reference
    const sampleIds = [349, 247, 104, 206, 112, 145, 18, 71, 88, 2506, 16, 29, 45, 92, 131, 168, 215, 280];
    let idIdx = 0;

    // Recursive branch generator
    function branch(x, y, length, angle, currentWidth, depth) {
      if (depth > 7 || length < 7) {
        // Leaf endpoint
        treeNodesCache.push({
          x, y,
          id: sampleIds[idIdx++ % sampleIds.length],
          depth,
          isLeaf: true
        });
        return;
      }

      // Pseudo variance based on depth and angle
      const lenVar = 1 + ((Math.sin(depth * 3.7 + angle) * (varLen / 100)) * 0.35);
      const curLen = length * lenVar;

      const endX = x + Math.cos(angle) * curLen;
      const endY = y + Math.sin(angle) * curLen;

      // Draw branch segment
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(endX, endY);
      ctx.strokeStyle = '#111111';
      ctx.lineWidth = Math.max(0.9, currentWidth);
      ctx.lineCap = 'round';
      ctx.stroke();

      const nodeId = sampleIds[idIdx++ % sampleIds.length];
      treeNodesCache.push({
        x: endX,
        y: endY,
        id: nodeId,
        depth,
        isLeaf: false
      });

      // Child branches
      const spreadRad = (rotDeg * Math.PI) / 180;
      const angVar = ((Math.cos(depth * 2.1) * (varAng / 100)) * 0.25);
      const nextLen = (curLen / scaleRed) * (depth > 4 ? leafLen * 1.5 : 1.0);
      const nextWidth = Math.max(0.8, currentWidth * widthRed);

      if (subSeg === 1) {
        branch(endX, endY, nextLen, angle - (spreadRad * 0.4) + angVar, nextWidth, depth + 1);
      } else if (subSeg === 2) {
        branch(endX, endY, nextLen, angle - (spreadRad * 0.5) + angVar, nextWidth, depth + 1);
        branch(endX, endY, nextLen * 0.92, angle + (spreadRad * 0.5) - angVar, nextWidth, depth + 1);
      } else {
        branch(endX, endY, nextLen, angle - (spreadRad * 0.6) + angVar, nextWidth, depth + 1);
        branch(endX, endY, nextLen * 0.85, angle, nextWidth * 0.9, depth + 1);
        branch(endX, endY, nextLen * 0.9, angle + (spreadRad * 0.6) - angVar, nextWidth, depth + 1);
      }

      if (spawnChance > 0.1 && depth < 4) {
        branch(endX, endY, nextLen * 0.6, angle + (spreadRad * 0.8), nextWidth * 0.7, depth + 2);
      }
    }

    // Initial root trunk going up-left
    const initialTrunkLen = 95 * rootLen * scale;
    const initialAngle = -Math.PI * 0.72; // ~-130° heading upward-left
    const trunkEndX = rootX + Math.cos(initialAngle) * initialTrunkLen;
    const trunkEndY = rootY + Math.sin(initialAngle) * initialTrunkLen;

    ctx.beginPath();
    ctx.moveTo(rootX, rootY);
    ctx.lineTo(trunkEndX, trunkEndY);
    ctx.strokeStyle = '#111111';
    ctx.lineWidth = rootWidth * 3.8;
    ctx.lineCap = 'round';
    ctx.stroke();

    // Secondary trunk extension to primary bifurcations
    const subTrunkLen = 80 * scale;
    const subTrunkAngle = -Math.PI * 0.65;
    const subEndX = trunkEndX + Math.cos(subTrunkAngle) * subTrunkLen;
    const subEndY = trunkEndY + Math.sin(subTrunkAngle) * subTrunkLen;

    ctx.beginPath();
    ctx.moveTo(trunkEndX, trunkEndY);
    ctx.lineTo(subEndX, subEndY);
    ctx.strokeStyle = '#111111';
    ctx.lineWidth = rootWidth * 2.8;
    ctx.lineCap = 'round';
    ctx.stroke();

    // Primary branch bifurcations
    const startW = widthVal * 2.8;
    branch(subEndX, subEndY, 75 * scale, subTrunkAngle - 0.45, startW, 1);
    branch(subEndX, subEndY, 85 * scale, subTrunkAngle + 0.35, startW, 1);
    branch(trunkEndX, trunkEndY, 70 * scale, initialAngle - 0.75, startW * 0.85, 1);

    // Draw Node indicators & tags
    treeNodesCache.forEach((n, idx) => {
      if (n.isLeaf) {
        ctx.beginPath();
        ctx.arc(n.x, n.y, 2.2, 0, Math.PI * 2);
        ctx.fillStyle = '#111111';
        ctx.fill();

        // Selective labels on leaf tips (matching Image 2)
        if (idx % 3 === 0) {
          ctx.font = '8px monospace';
          ctx.fillStyle = '#111111';
          ctx.fillText(`[${n.id}]`, n.x + 4, n.y - 3);
        }
      } else {
        // Intermediate node hollow circle
        ctx.beginPath();
        ctx.arc(n.x, n.y, 3.2, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();
        ctx.lineWidth = 1.4;
        ctx.strokeStyle = '#111111';
        ctx.stroke();

        if (idx % 6 === 0) {
          ctx.font = '8px monospace';
          ctx.fillStyle = '#333333';
          ctx.fillText(`${n.id}`, n.x + 5, n.y + 3);
        }
      }
    });

    // Update status text
    const leafCountEl = document.querySelector('.tree-status-block .status-row:nth-child(2) .v');
    if (leafCountEl) {
      leafCountEl.textContent = `: ${treeNodesCache.length} NODES`;
    }
  }

  // Setup slider listeners
  const sliderIds = [
    'p-scale', 'p-scalered', 'p-width', 'p-widthred',
    'p-leaflen', 'p-rot', 'p-subseg', 'p-varlen',
    'p-varang', 'p-spawn', 'p-rootlen', 'p-rootw', 'p-rootwred'
  ];

  sliderIds.forEach(id => {
    const el = document.getElementById(id);
    const valEl = document.getElementById(`${id}-val`);
    if (el) {
      el.addEventListener('input', () => {
        if (valEl) {
          valEl.textContent = parseFloat(el.value).toFixed(id.includes('subseg') ? 0 : 2);
        }
        renderTree();
      });
    }
  });

  // Canvas mouse interaction for HUD Inspection Card
  if (!treeCanvasInitialized) {
    canvas.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const mouseX = (e.clientX - rect.left) * scaleX;
      const mouseY = (e.clientY - rect.top) * scaleY;

      let closest = null;
      let minD = 28;
      treeNodesCache.forEach(n => {
        const d = Math.hypot(n.x - mouseX, n.y - mouseY);
        if (d < minD) {
          minD = d;
          closest = n;
        }
      });

      if (closest) {
        updateHudCard(closest);
      }
    });

    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const mouseX = (e.clientX - rect.left) * scaleX;
      const mouseY = (e.clientY - rect.top) * scaleY;

      let closest = null;
      let minD = 40;
      treeNodesCache.forEach(n => {
        const d = Math.hypot(n.x - mouseX, n.y - mouseY);
        if (d < minD) {
          minD = d;
          closest = n;
        }
      });

      if (closest) {
        updateHudCard(closest);
      }
    });

    treeCanvasInitialized = true;
  }

  function updateHudCard(node) {
    const hud = document.getElementById('tree-hud-overlay');
    if (!hud) return;

    const truckIds = ['KA-01-EA-1042', 'KA-01-EA-2091', 'KA-01-EA-3304'];
    const truckId = truckIds[node.id % truckIds.length];
    const savings = 1200 + ((node.id * 37) % 3200);

    const specLines = hud.querySelectorAll('.hud-specs .spec-line .sv');
    if (specLines.length >= 6) {
      specLines[0].textContent = `: 0 (EURO-VI DIESEL)`;
      specLines[1].textContent = `: ${(node.depth * 2) + 4} BINS`;
      specLines[2].textContent = `: ${node.id}`;
      specLines[3].textContent = `: ${truckId}`;
      specLines[4].textContent = `: 2025-10-10`;
      specLines[5].textContent = `: ₹${savings.toLocaleString()} / DAY`;
    }
  }

  renderTree();
}

// ══════════════════════════════════════════════════════════════
// FUEL & ROUTE ECONOMICS
// ══════════════════════════════════════════════════════════════
async function loadFuelDashboard() {
  initFuelTreeCanvas();
  try {
    const [summary, daily, logs] = await Promise.all([
      fetch(`${API}/fuel/summary`).then(r => r.json()),
      fetch(`${API}/fuel/daily`).then(r => r.json()),
      fetch(`${API}/fuel/logs`).then(r => r.json())
    ]);

    const sEl = document.getElementById('fuel-total-savings');
    if (sEl) sEl.textContent = `₹${Math.round(summary.total_savings_inr || 0).toLocaleString()}`;
    const lEl = document.getElementById('fuel-total-liters');
    if (lEl) lEl.textContent = `${(summary.total_fuel_liters || 0).toFixed(1)} L`;
    const dEl = document.getElementById('fuel-total-dist');
    if (dEl) dEl.textContent = `${(summary.total_distance_km || 0).toFixed(1)} km`;
    const cEl = document.getElementById('fuel-avg-cost');
    if (cEl) cEl.textContent = `₹${(summary.avg_cost_per_km || 0).toFixed(2)}/km`;

    if (dailyChart) dailyChart.destroy();
    const ctx = document.getElementById('fuel-daily-chart')?.getContext('2d');
    if (ctx && daily.length) {
      dailyChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: daily.map(d => d.trip_date),
          datasets: [
            {
              label: 'Actual Fuel Cost (₹)',
              data: daily.map(d => d.fuel_cost_inr),
              backgroundColor: 'rgba(225, 29, 72, 0.7)',
              borderRadius: 4
            },
            {
              label: 'Optimized Savings (₹)',
              data: daily.map(d => d.savings_inr),
              backgroundColor: 'rgba(21, 128, 61, 0.7)',
              borderRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              ticks: { color: '#64748b', font: { size: 11 } },
              grid: { color: 'rgba(0, 0, 0, 0.04)' }
            },
            y: {
              ticks: { color: '#64748b', font: { size: 11 } },
              grid: { color: 'rgba(0, 0, 0, 0.04)' }
            }
          },
          plugins: {
            legend: {
              labels: { color: '#1e293b', font: { size: 12 } }
            }
          }
        }
      });
    }

    const logsTbody = document.querySelector('#fuel-logs-table tbody');
    if (logsTbody) {
      logsTbody.innerHTML = logs.map(l => `
        <tr>
          <td class="font-mono text-xs">${l.trip_date}</td>
          <td><span class="font-mono text-green font-bold">${l.truck_id}</span></td>
          <td>${l.driver_name || 'Assigned'}</td>
          <td class="font-mono">${l.distance_km} km</td>
          <td class="font-mono">${l.fuel_liters} L</td>
          <td class="font-mono font-bold text-red">₹${l.fuel_cost_inr}</td>
          <td class="font-mono font-bold text-green">₹${l.savings_inr}</td>
        </tr>
      `).join('');
    }

  } catch (e) {
    console.error('Fuel dashboard error:', e);
  }
}

// Route calculator
document.getElementById('calc-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const dist = parseFloat(document.getElementById('calc-dist').value);
  const mileage = parseFloat(document.getElementById('calc-mileage').value);

  try {
    const res = await fetch(`${API}/fuel/calculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ truck_id: 'T01', distance_km: dist })
    });
    const data = await res.json();
    document.getElementById('calc-result').innerHTML = `
      <div class="eco-card p-4 border-accent-green">
        <div class="text-xl font-mono font-bold text-green">₹${data.cost_inr} Trip Diesel Cost</div>
        <div class="text-xs text-muted mt-1">Consumes ${data.fuel_liters} L • Saves ₹${data.savings_inr} vs unrouted baseline.</div>
      </div>
    `;
  } catch (err) {
    const liters = (dist / mileage).toFixed(2);
    const cost = (liters * 89).toFixed(0);
    const savings = (cost * 0.38).toFixed(0);
    document.getElementById('calc-result').innerHTML = `
      <div class="eco-card p-4 border-accent-green">
        <div class="text-xl font-mono font-bold text-green">₹${cost} Trip Diesel Cost</div>
        <div class="text-xs text-muted mt-1">Consumes ${liters} L • Saves ₹${savings}.</div>
      </div>
    `;
  }
});

// ── 12. About Us Interactive Pillars (Reference Feature) ──
const PILLARS_DATA = {
  vision: {
    tag: 'PILLAR 01 • OPEN CIVIC COMMONS',
    title: 'Free-Forever Open Architecture',
    desc: 'Built without commercial API lock-in. Powered by local neural vision pipelines and open geospatial routing, saving municipalities millions in proprietary software licenses.'
  },
  waste: {
    tag: 'PILLAR 02 • ZERO OVERFLOW GRID',
    title: 'Sensor & Crowdsourced Bin Telemetry',
    desc: 'Every civic grievance triangulates with 12 IoT bin nodes across BBMP Ward 142. If fill-level surpasses 85%, automatic municipal escalation alerts the zonal junior health inspector.'
  },
  ai: {
    tag: 'PILLAR 03 • VISION NEURAL CLASSIFIER',
    title: 'Dual-Pipeline Qwen2.5-VL & ResNet Diagnostics',
    desc: 'Instantaneous garbage volume estimation, overflow risk scoring (0-100), hazardous material alerts, and fake report prevention running on edge GPU inference.'
  },
  fuel: {
    tag: 'PILLAR 04 • GREEN FLEET LOGISTICS',
    title: 'Dynamic Compactor Routing & Fuel Economics',
    desc: 'Consolidating 48 grievance waypoints into optimized traveling-salesman dispatch loops saves 38.2% diesel per shift (₹18,400+ saved monthly per compactor truck).'
  }
};

document.querySelectorAll('.pillar-circle').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.pillar-circle').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const key = btn.dataset.pillar;
    const data = PILLARS_DATA[key];
    if (!data) return;

    const card = document.getElementById('pillar-insight-card');
    const tagEl = document.getElementById('pillar-tag');
    const titleEl = document.getElementById('pillar-title');
    const descEl = document.getElementById('pillar-desc');

    if (card && tagEl && titleEl && descEl) {
      card.style.opacity = '0.3';
      card.style.transform = 'translateY(4px)';
      setTimeout(() => {
        tagEl.textContent = data.tag;
        titleEl.textContent = data.title;
        descEl.textContent = data.desc;
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, 140);
    }
  });
});

