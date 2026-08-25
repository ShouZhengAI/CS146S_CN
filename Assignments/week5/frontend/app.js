const state = {
  notes: { items: [], total: 0, page: 1, pageSize: 10 },
  actions: { items: [], total: 0, page: 1, pageSize: 10 },
};

async function fetchJSON(url, options = {}) {
  const response = await fetch(url, options);
  let payload;
  try { payload = await response.json(); } catch { throw new Error(`HTTP ${response.status}`); }
  if (!response.ok || !payload.ok) throw new Error(payload.error?.message || `HTTP ${response.status}`);
  return payload.data;
}

function showError(error) {
  const box = document.getElementById('error');
  box.textContent = error.message || String(error);
  box.hidden = false;
}

function apiOptions(method, body) {
  return { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) };
}

function renderNotes() {
  const list = document.getElementById('notes');
  list.replaceChildren();
  for (const note of state.notes.items) {
    const li = document.createElement('li');
    const text = document.createElement('span');
    text.textContent = `${note.title}: ${note.content} `;
    li.appendChild(text);
    for (const tag of note.tags) {
      const badge = document.createElement('button');
      badge.className = 'tag'; badge.textContent = `#${tag.name}`;
      badge.onclick = () => { document.getElementById('tag-filter').value = tag.name; state.notes.page = 1; loadNotes(); };
      li.appendChild(badge);
    }
    const edit = document.createElement('button'); edit.textContent = '编辑';
    edit.onclick = () => editNote(note);
    const extract = document.createElement('button'); extract.textContent = '提取';
    extract.onclick = async () => { try { await fetchJSON(`/notes/${note.id}/extract?apply=true`, { method: 'POST' }); await Promise.all([loadNotes(), loadActions(), loadTags()]); } catch (error) { showError(error); } };
    const remove = document.createElement('button'); remove.textContent = '删除';
    remove.onclick = () => deleteNote(note);
    li.append(edit, extract, remove); list.appendChild(li);
  }
  document.getElementById('note-count').textContent = `共 ${state.notes.total} 条`;
  document.getElementById('notes-page').textContent = `第 ${state.notes.page} 页`;
  document.getElementById('notes-prev').disabled = state.notes.page === 1;
  document.getElementById('notes-next').disabled = state.notes.page * state.notes.pageSize >= state.notes.total;
}

async function loadNotes() {
  try {
    const q = document.getElementById('note-search').value.trim();
    const tag = document.getElementById('tag-filter').value;
    const params = new URLSearchParams({ page: state.notes.page, page_size: state.notes.pageSize });
    let path = '/notes/';
    if (q) { path = '/notes/search'; params.set('q', q); params.set('sort', document.getElementById('note-sort').value); }
    else if (tag) params.set('tag', tag);
    Object.assign(state.notes, await fetchJSON(`${path}?${params}`)); renderNotes();
  } catch (error) { showError(error); }
}

async function editNote(note) {
  const title = window.prompt('新标题', note.title); if (title === null) return;
  const content = window.prompt('新内容', note.content); if (content === null) return;
  const before = { ...note }; Object.assign(note, { title, content }); renderNotes();
  try { Object.assign(note, await fetchJSON(`/notes/${note.id}`, apiOptions('PUT', { title, content }))); }
  catch (error) { Object.assign(note, before); showError(error); }
  renderNotes();
}

async function deleteNote(note) {
  const index = state.notes.items.indexOf(note); state.notes.items.splice(index, 1); state.notes.total -= 1; renderNotes();
  try { await fetchJSON(`/notes/${note.id}`, { method: 'DELETE' }); }
  catch (error) { state.notes.items.splice(index, 0, note); state.notes.total += 1; renderNotes(); showError(error); }
}

function renderActions() {
  const list = document.getElementById('actions'); list.replaceChildren();
  for (const item of state.actions.items) {
    const li = document.createElement('li');
    const checkbox = document.createElement('input'); checkbox.type = 'checkbox'; checkbox.className = 'bulk-id'; checkbox.value = item.id; checkbox.disabled = item.completed;
    const text = document.createElement('span'); text.textContent = `${item.description} [${item.completed ? '完成' : '未完成'}]`;
    li.append(checkbox, text);
    if (!item.completed) {
      const button = document.createElement('button'); button.textContent = '完成';
      button.onclick = async () => { const before = item.completed; item.completed = true; renderActions(); try { Object.assign(item, await fetchJSON(`/action-items/${item.id}/complete`, { method: 'PUT' })); } catch (error) { item.completed = before; showError(error); } renderActions(); };
      li.appendChild(button);
    }
    list.appendChild(li);
  }
  document.getElementById('action-count').textContent = `共 ${state.actions.total} 条`;
  document.getElementById('actions-page').textContent = `第 ${state.actions.page} 页`;
  document.getElementById('actions-prev').disabled = state.actions.page === 1;
  document.getElementById('actions-next').disabled = state.actions.page * state.actions.pageSize >= state.actions.total;
}

async function loadActions() {
  try {
    const params = new URLSearchParams({ page: state.actions.page, page_size: state.actions.pageSize });
    const completed = document.getElementById('action-filter').value; if (completed) params.set('completed', completed);
    Object.assign(state.actions, await fetchJSON(`/action-items/?${params}`)); renderActions();
  } catch (error) { showError(error); }
}

async function loadTags() {
  try {
    const data = await fetchJSON('/tags/'); const select = document.getElementById('tag-filter'); const current = select.value;
    select.replaceChildren(new Option('全部标签', ''));
    data.items.forEach(tag => select.add(new Option(`#${tag.name}`, tag.name))); select.value = current;
  } catch (error) { showError(error); }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').onsubmit = async event => { event.preventDefault(); try { await fetchJSON('/notes/', apiOptions('POST', { title: document.getElementById('note-title').value, content: document.getElementById('note-content').value })); event.target.reset(); state.notes.page = 1; await loadNotes(); } catch (error) { showError(error); } };
  document.getElementById('action-form').onsubmit = async event => { event.preventDefault(); try { await fetchJSON('/action-items/', apiOptions('POST', { description: document.getElementById('action-desc').value })); event.target.reset(); state.actions.page = 1; await loadActions(); } catch (error) { showError(error); } };
  document.getElementById('note-search-button').onclick = () => { state.notes.page = 1; loadNotes(); };
  document.getElementById('tag-filter').onchange = () => { document.getElementById('note-search').value = ''; state.notes.page = 1; loadNotes(); };
  document.getElementById('action-filter').onchange = () => { state.actions.page = 1; loadActions(); };
  document.getElementById('notes-prev').onclick = () => { state.notes.page -= 1; loadNotes(); };
  document.getElementById('notes-next').onclick = () => { state.notes.page += 1; loadNotes(); };
  document.getElementById('actions-prev').onclick = () => { state.actions.page -= 1; loadActions(); };
  document.getElementById('actions-next').onclick = () => { state.actions.page += 1; loadActions(); };
  document.getElementById('bulk-complete').onclick = async () => { const ids = [...document.querySelectorAll('.bulk-id:checked')].map(input => Number(input.value)); if (!ids.length) return; const before = state.actions.items.map(item => ({ item, completed: item.completed })); state.actions.items.filter(item => ids.includes(item.id)).forEach(item => { item.completed = true; }); renderActions(); try { await fetchJSON('/action-items/bulk-complete', apiOptions('POST', { ids })); } catch (error) { before.forEach(entry => { entry.item.completed = entry.completed; }); renderActions(); showError(error); } };
  Promise.all([loadNotes(), loadActions(), loadTags()]);
});
