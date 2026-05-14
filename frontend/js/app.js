'use strict';

// ─── API ──────────────────────────────────────────────────────────────────────
// file:// 로 열 경우 절대 URL, FastAPI에서 서빙 시 상대 URL 사용
const API = window.location.protocol === 'file:'
  ? 'http://localhost:8000/api/tasks'
  : '/api/tasks';

async function apiFetch(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok && res.status !== 204) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `HTTP ${res.status}`);
  }
  return res.status === 204 ? null : res.json();
}

const api = {
  list:   ()         => apiFetch(API),
  get:    (id)       => apiFetch(`${API}/${id}`),
  create: (data)     => apiFetch(API, { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => apiFetch(`${API}/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  remove: (id)       => apiFetch(`${API}/${id}`, { method: 'DELETE' }),
};

// ─── State ────────────────────────────────────────────────────────────────────
let tasks = [];

// ─── Theme ────────────────────────────────────────────────────────────────────
const themeBtn = document.getElementById('themeBtn');

function syncThemeBtn() {
  themeBtn.textContent = document.documentElement.classList.contains('dark') ? '☀️' : '🌙';
}

themeBtn.addEventListener('click', () => {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  syncThemeBtn();
});

syncThemeBtn();

// ─── Utilities ────────────────────────────────────────────────────────────────
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// datetime-local 입력값 ↔ ISO 8601 변환
function toLocalDatetimeStr(isoStr) {
  if (!isoStr) return '';
  const d = new Date(isoStr);
  const pad = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function toISOStr(localStr) {
  if (!localStr) return null;
  return new Date(localStr).toISOString();
}

// D-N HH:MM 포맷 계산
function formatDueAt(isoStr) {
  if (!isoStr) return null;
  const due = new Date(isoStr);
  const now = new Date();
  const diffMs = due - now;
  const diffDays = Math.floor(Math.abs(diffMs) / (1000 * 60 * 60 * 24));
  const hh = String(due.getHours()).padStart(2, '0');
  const mm = String(due.getMinutes()).padStart(2, '0');
  const isOverdue = diffMs < 0;
  const prefix = isOverdue ? `D+${diffDays}` : `D-${diffDays}`;
  return { text: `${prefix} ${hh}:${mm}`, isOverdue };
}

// ─── Render ───────────────────────────────────────────────────────────────────
const STATUS_BADGE = {
  todo:        'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300',
  in_progress: 'bg-blue-100 text-blue-700 dark:bg-blue-900/60 dark:text-blue-300',
  done:        'bg-green-100 text-green-700 dark:bg-green-900/60 dark:text-green-300',
};
const STATUS_LABEL = { todo: 'Todo', in_progress: '진행 중', done: '완료' };

function renderCard(task) {
  const due = formatDueAt(task.due_at);
  const dueHtml = due
    ? `<span class="text-xs font-mono ${due.isOverdue ? 'text-red-500 dark:text-red-400' : 'text-gray-400 dark:text-gray-500'}">${escapeHtml(due.text)}</span>`
    : '';

  return `
    <div
      class="task-card group relative bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-xl shadow-lg p-4 cursor-pointer hover:shadow-xl active:scale-[0.99] transition-all"
      data-id="${task.id}"
    >
      <div class="flex items-start justify-between gap-3">
        <div class="flex-1 min-w-0 space-y-1">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-xs px-2 py-0.5 rounded-full font-medium ${STATUS_BADGE[task.status]}">
              ${STATUS_LABEL[task.status]}
            </span>
            ${dueHtml}
          </div>
          <p class="text-sm font-medium text-gray-800 dark:text-gray-100 truncate">${escapeHtml(task.title)}</p>
        </div>
        <button
          class="delete-btn min-h-[44px] min-w-[44px] -mr-2 flex items-center justify-center rounded-xl text-gray-300 hover:text-red-500 dark:text-gray-600 dark:hover:text-red-400 transition-colors flex-shrink-0"
          data-id="${task.id}"
          title="삭제"
          aria-label="업무 삭제"
        >🗑</button>
      </div>
    </div>`;
}

function renderTasks() {
  const list = document.getElementById('taskList');
  if (tasks.length === 0) {
    list.innerHTML = `
      <p class="text-center text-gray-400 dark:text-gray-500 py-16 text-sm">
        업무가 없습니다. 첫 번째 업무를 추가해보세요.
      </p>`;
    return;
  }
  list.innerHTML = tasks.map(renderCard).join('');
}

// ─── 추가 폼 ──────────────────────────────────────────────────────────────────
const taskForm  = document.getElementById('taskForm');
const newTitle  = document.getElementById('newTitle');
const newDueAt  = document.getElementById('newDueAt');
const newStatus = document.getElementById('newStatus');
const addBtn    = document.getElementById('addBtn');

newTitle.addEventListener('input', () => {
  addBtn.disabled = newTitle.value.trim() === '';
});

taskForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const title = newTitle.value.trim();
  if (!title) return;

  const original = addBtn.textContent;
  addBtn.disabled = true;
  addBtn.textContent = '추가 중…';
  try {
    await api.create({
      title,
      due_at: toISOStr(newDueAt.value),
      status: newStatus.value,
    });
    taskForm.reset();
    addBtn.disabled = true;
    await loadTasks();
  } catch (err) {
    alert(`추가 실패: ${err.message}`);
    addBtn.disabled = false;
  } finally {
    addBtn.textContent = original;
  }
});

// ─── 수정 모달 ────────────────────────────────────────────────────────────────
const modalOverlay    = document.getElementById('modalOverlay');
const editForm        = document.getElementById('editForm');
const editId          = document.getElementById('editId');
const editTitle       = document.getElementById('editTitle');
const editDescription = document.getElementById('editDescription');
const editStatus      = document.getElementById('editStatus');
const editDueAt       = document.getElementById('editDueAt');
const cancelBtn       = document.getElementById('cancelBtn');

function openModal(task) {
  editId.value          = task.id;
  editTitle.value       = task.title;
  editDescription.value = task.description || '';
  editStatus.value      = task.status;
  editDueAt.value       = toLocalDatetimeStr(task.due_at);
  modalOverlay.classList.remove('hidden');
  setTimeout(() => editTitle.focus(), 50);
}

function closeModal() {
  modalOverlay.classList.add('hidden');
  editForm.reset();
}

cancelBtn.addEventListener('click', closeModal);

// 모달 바깥 클릭 시 닫기
modalOverlay.addEventListener('click', (e) => {
  if (e.target === modalOverlay) closeModal();
});

// ESC 키로 닫기
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !modalOverlay.classList.contains('hidden')) closeModal();
});

editForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const title = editTitle.value.trim();
  if (!title) return;

  try {
    await api.update(Number(editId.value), {
      title,
      description: editDescription.value.trim() || null,
      status: editStatus.value,
      due_at: toISOStr(editDueAt.value),
    });
    closeModal();
    await loadTasks();
  } catch (err) {
    alert(`저장 실패: ${err.message}`);
  }
});

// ─── 이벤트 위임: 카드 클릭 / 삭제 ──────────────────────────────────────────
document.getElementById('taskList').addEventListener('click', async (e) => {
  // 삭제 버튼 처리
  const deleteBtn = e.target.closest('.delete-btn');
  if (deleteBtn) {
    e.stopPropagation();
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try {
      await api.remove(Number(deleteBtn.dataset.id));
      await loadTasks();
    } catch (err) {
      alert(`삭제 실패: ${err.message}`);
    }
    return;
  }

  // 카드 클릭 → 수정 모달
  const card = e.target.closest('.task-card');
  if (card) {
    try {
      const task = await api.get(Number(card.dataset.id));
      openModal(task);
    } catch (err) {
      alert(`불러오기 실패: ${err.message}`);
    }
  }
});

// ─── 데이터 로드 & 폴링 ───────────────────────────────────────────────────────
async function loadTasks() {
  try {
    tasks = await api.list();
    renderTasks();
  } catch (err) {
    console.error('목록 로드 실패:', err);
  }
}

loadTasks();
setInterval(loadTasks, 3000);
