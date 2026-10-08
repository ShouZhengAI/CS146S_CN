import { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const empty = { title: '', notes: '', completed: false }

export default function App() {
  const [tasks, setTasks] = useState([])
  const [form, setForm] = useState(empty)
  const [editing, setEditing] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function request(path = '', options = {}) {
    const response = await fetch(`${API}/tasks${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    })
    if (!response.ok) {
      const body = await response.json().catch(() => ({}))
      throw new Error(body.detail || '请求失败，请稍后重试')
    }
    return response.status === 204 ? null : response.json()
  }

  async function load() {
    try {
      setTasks(await request())
      setError('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  async function submit(event) {
    event.preventDefault()
    if (!form.title.trim()) return setError('标题不能为空')
    try {
      const method = editing ? 'PUT' : 'POST'
      await request(editing ? `/${editing}` : '', { method, body: JSON.stringify(form) })
      setForm(empty)
      setEditing(null)
      await load()
    } catch (err) { setError(err.message) }
  }

  function edit(task) {
    setEditing(task.id)
    setForm({ title: task.title, notes: task.notes, completed: task.completed })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  async function toggle(task) {
    try {
      await request(`/${task.id}`, { method: 'PUT', body: JSON.stringify({ ...task, completed: !task.completed }) })
      await load()
    } catch (err) { setError(err.message) }
  }

  async function remove(id) {
    if (!window.confirm('确定删除这条任务吗？')) return
    try {
      await request(`/${id}`, { method: 'DELETE' })
      if (editing === id) { setEditing(null); setForm(empty) }
      await load()
    } catch (err) { setError(err.message) }
  }

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-12 text-slate-100">
      <div className="mx-auto max-w-4xl">
        <header className="mb-8">
          <p className="mb-2 text-sm font-bold uppercase tracking-[.25em] text-cyan-400">Bolt-style productivity</p>
          <h1 className="text-4xl font-black sm:text-5xl">Focus Notes</h1>
          <p className="mt-3 text-slate-400">把任务和备注放在一起，专注完成下一件事。</p>
        </header>

        <form onSubmit={submit} className="mb-8 grid gap-4 rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-2xl sm:p-7">
          <h2 className="text-xl font-bold">{editing ? '编辑任务' : '新建任务'}</h2>
          <input aria-label="任务标题" maxLength="120" required placeholder="任务标题" value={form.title}
            onChange={e => setForm({ ...form, title: e.target.value })}
            className="rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-cyan-400" />
          <textarea aria-label="任务备注" maxLength="2000" rows="4" placeholder="补充备注（可选）" value={form.notes}
            onChange={e => setForm({ ...form, notes: e.target.value })}
            className="resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-cyan-400" />
          <label className="flex items-center gap-3 text-sm text-slate-300">
            <input type="checkbox" checked={form.completed} onChange={e => setForm({ ...form, completed: e.target.checked })} /> 已完成
          </label>
          <div className="flex gap-3">
            <button className="rounded-xl bg-cyan-400 px-5 py-3 font-bold text-slate-950 hover:bg-cyan-300">{editing ? '保存修改' : '添加任务'}</button>
            {editing && <button type="button" onClick={() => { setEditing(null); setForm(empty) }} className="rounded-xl border border-slate-700 px-5 py-3">取消</button>}
          </div>
        </form>

        {error && <p role="alert" className="mb-5 rounded-xl border border-red-800 bg-red-950/60 p-4 text-red-200">{error}</p>}
        {loading ? <p className="text-slate-400">正在加载…</p> : tasks.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-700 p-10 text-center text-slate-400">还没有任务，从上方创建第一条。</div>
        ) : (
          <section className="grid gap-4" aria-label="任务列表">
            {tasks.map(task => (
              <article key={task.id} className="flex gap-4 rounded-2xl border border-slate-800 bg-slate-900 p-5">
                <button aria-label={task.completed ? '标记未完成' : '标记完成'} onClick={() => toggle(task)}
                  className={`mt-1 h-6 w-6 shrink-0 rounded-full border-2 ${task.completed ? 'border-emerald-400 bg-emerald-400' : 'border-slate-600'}`} />
                <div className="min-w-0 flex-1">
                  <h3 className={`text-lg font-bold ${task.completed ? 'text-slate-500 line-through' : ''}`}>{task.title}</h3>
                  {task.notes && <p className="mt-2 whitespace-pre-wrap text-sm text-slate-400">{task.notes}</p>}
                  <div className="mt-4 flex gap-4 text-sm">
                    <button onClick={() => edit(task)} className="text-cyan-400 hover:text-cyan-300">编辑</button>
                    <button onClick={() => remove(task.id)} className="text-red-400 hover:text-red-300">删除</button>
                  </div>
                </div>
              </article>
            ))}
          </section>
        )}
      </div>
    </main>
  )
}
