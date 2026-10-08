const $ = selector => document.querySelector(selector)
const form = $('#task-form')
const elements = { id: $('#task-id'), title: $('#title'), notes: $('#notes'), completed: $('#completed') }
let tasks = []

async function api(path = '', options = {}) {
  const response = await fetch(`/api/tasks${path}`, { headers: { 'Content-Type': 'application/json' }, ...options })
  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new Error(data.error || '请求失败，请稍后重试')
  }
  return response.status === 204 ? null : response.json()
}

function showError(message = '') {
  $('#error').textContent = message
  $('#error').hidden = !message
}

function resetForm() {
  form.reset()
  elements.id.value = ''
  $('#save').textContent = '添加任务'
  $('#cancel').hidden = true
}

function startEdit(task) {
  elements.id.value = task.id
  elements.title.value = task.title
  elements.notes.value = task.notes
  elements.completed.checked = task.completed
  $('#save').textContent = '保存修改'
  $('#cancel').hidden = false
  elements.title.focus()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function render() {
  const container = $('#tasks')
  const filter = $('#filter').value
  const visible = tasks.filter(task => filter === 'all' || (filter === 'done' ? task.completed : !task.completed))
  container.replaceChildren()
  $('#count').textContent = `${tasks.filter(task => !task.completed).length} 项待完成`
  if (!visible.length) {
    const empty = document.createElement('div')
    empty.className = 'empty'
    empty.textContent = tasks.length ? '此筛选条件下没有任务。' : '还没有任务，从上方添加第一条。'
    container.append(empty)
    return
  }
  visible.forEach(task => {
    const node = $('#task-template').content.firstElementChild.cloneNode(true)
    node.classList.toggle('done', task.completed)
    node.querySelector('h3').textContent = task.title
    const notes = node.querySelector('.body p')
    notes.textContent = task.notes
    notes.hidden = !task.notes
    node.querySelector('.meta').textContent = `更新于 ${new Date(`${task.updated_at}Z`).toLocaleString()}`
    node.querySelector('.toggle').addEventListener('click', () => update(task, { ...task, completed: !task.completed }))
    node.querySelector('.edit').addEventListener('click', () => startEdit(task))
    node.querySelector('.delete').addEventListener('click', () => remove(task))
    container.append(node)
  })
}

async function load() {
  try { tasks = await api(); showError(); render() } catch (error) { showError(error.message) }
}

async function update(task, values) {
  try {
    await api(`/${task.id}`, { method: 'PUT', body: JSON.stringify(values) })
    await load()
  } catch (error) { showError(error.message) }
}

async function remove(task) {
  if (!confirm(`确定删除“${task.title}”吗？`)) return
  try {
    await api(`/${task.id}`, { method: 'DELETE' })
    if (String(task.id) === elements.id.value) resetForm()
    await load()
  } catch (error) { showError(error.message) }
}

form.addEventListener('submit', async event => {
  event.preventDefault()
  const values = { title: elements.title.value, notes: elements.notes.value, completed: elements.completed.checked }
  const id = elements.id.value
  try {
    await api(id ? `/${id}` : '', { method: id ? 'PUT' : 'POST', body: JSON.stringify(values) })
    resetForm()
    await load()
  } catch (error) { showError(error.message) }
})

$('#cancel').addEventListener('click', resetForm)
$('#filter').addEventListener('change', render)
load()
