async function fetchJSON(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${response.status})`);
  }
  return response.status === 204 ? null : response.json();
}

function showError(error) {
  document.getElementById('status').textContent = error.message;
}

async function loadNotes(query = '') {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const url = query ? `/notes/search?q=${encodeURIComponent(query)}` : '/notes/';
  const notes = await fetchJSON(url);
  for (const note of notes) {
    const li = document.createElement('li');
    const text = document.createElement('span');
    text.textContent = `${note.title}: ${note.content} `;
    li.appendChild(text);

    const editButton = document.createElement('button');
    editButton.textContent = 'Edit';
    editButton.onclick = async () => {
      const title = window.prompt('Title', note.title);
      if (title === null) return;
      const content = window.prompt('Content', note.content);
      if (content === null) return;
      try {
        await fetchJSON(`/notes/${note.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, content }),
        });
        await loadNotes();
      } catch (error) {
        showError(error);
      }
    };
    li.appendChild(editButton);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = async () => {
      try {
        await fetchJSON(`/notes/${note.id}`, { method: 'DELETE' });
        await loadNotes();
      } catch (error) {
        showError(error);
      }
    };
    li.appendChild(deleteButton);
    list.appendChild(li);
  }
}

async function loadActions() {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  const items = await fetchJSON('/action-items/');
  for (const item of items) {
    const li = document.createElement('li');
    li.textContent = `${item.description} [${item.completed ? 'done' : 'open'}] `;
    if (!item.completed) {
      const button = document.createElement('button');
      button.textContent = 'Complete';
      button.onclick = async () => {
        try {
          await fetchJSON(`/action-items/${item.id}/complete`, { method: 'PUT' });
          await loadActions();
        } catch (error) {
          showError(error);
        }
      };
      li.appendChild(button);
    }
    list.appendChild(li);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      await fetchJSON('/notes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: document.getElementById('note-title').value,
          content: document.getElementById('note-content').value,
        }),
      });
      event.target.reset();
      await loadNotes();
    } catch (error) {
      showError(error);
    }
  });

  document.getElementById('search-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      await loadNotes(document.getElementById('search-query').value.trim());
    } catch (error) {
      showError(error);
    }
  });

  document.getElementById('action-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      await fetchJSON('/action-items/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          description: document.getElementById('action-desc').value,
        }),
      });
      event.target.reset();
      await loadActions();
    } catch (error) {
      showError(error);
    }
  });

  loadNotes().catch(showError);
  loadActions().catch(showError);
});
