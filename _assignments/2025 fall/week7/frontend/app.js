async function fetchJSON(url, options) {
  const error = document.getElementById('error');
  const res = await fetch(url, options);
  if (!res.ok) {
    const payload = await res.json().catch(() => null);
    const message = payload?.error?.message || `Request failed (${res.status})`;
    if (error) error.textContent = message;
    throw new Error(message);
  }
  if (error) error.textContent = '';
  return res.status === 204 ? null : res.json();
}

async function loadNotes(params = {}) {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  const notes = await fetchJSON('/notes/?' + query.toString());
  for (const n of notes) {
    const tags = n.tags.map((tag) => `#${tag.name}`).join(' ');
    const text = document.createElement('span');
    text.textContent = `${n.title}: ${n.content}${tags ? ` — ${tags}` : ''} `;
    const button = document.createElement('button');
    button.textContent = 'Delete';
    button.onclick = async () => {
      await fetchJSON(`/notes/${n.id}`, { method: 'DELETE' });
      await loadNotes(params);
    };
    li.append(text, button);
    list.appendChild(li);
  }
}

async function loadActions(params = {}) {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  const items = await fetchJSON('/action-items/?' + query.toString());
  for (const a of items) {
    const li = document.createElement('li');
    li.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = async () => {
      await fetchJSON(`/action-items/${a.id}`, { method: 'DELETE' });
      await loadActions(params);
    };
    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions(params);
      };
      li.appendChild(btn);
    } else {
      const btn = document.createElement('button');
      btn.textContent = 'Reopen';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ completed: false }),
        });
        loadActions(params);
      };
      li.appendChild(btn);
    }
    li.appendChild(deleteButton);
    list.appendChild(li);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    const tags = document
      .getElementById('note-tags')
      .value.split(',')
      .map((tag) => tag.trim())
      .filter(Boolean);
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content, tags }),
    });
    e.target.reset();
    loadNotes();
  });

  document.getElementById('note-search-btn').addEventListener('click', async () => {
    const q = document.getElementById('note-search').value;
    loadNotes({ q });
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  document.getElementById('filter-completed').addEventListener('change', (e) => {
    const checked = e.target.checked;
    loadActions({ completed: checked });
  });

  loadNotes();
  loadActions();
});


