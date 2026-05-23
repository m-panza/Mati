import React, { useState, useEffect, useCallback } from 'react'
import Modal from './Modal'

/**
 * Generic CRUD table component.
 *
 * Props:
 *   title         - page title
 *   api           - { list, create, update, deactivate }
 *   columns       - [{ key, label, render? }]
 *   fields        - [{ key, label, type?, required?, options? }] for form
 *   exportUrl     - optional URL for CSV export
 *   extraActions  - optional fn(row) => ReactNode
 */
export default function CrudTable({ title, api, columns, fields, exportUrl, extraActions }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [showAll, setShowAll] = useState(false)
  const [modal, setModal] = useState(null) // null | 'create' | 'edit'
  const [editing, setEditing] = useState(null)
  const [formData, setFormData] = useState({})
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const fetchItems = useCallback(async () => {
    setLoading(true)
    try {
      const params = { activo: showAll ? undefined : true }
      if (search) params.search = search
      const data = await api.list(params)
      setItems(Array.isArray(data) ? data : (data.items || []))
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }, [api, search, showAll])

  useEffect(() => { fetchItems() }, [fetchItems])

  function openCreate() {
    setEditing(null)
    const initial = {}
    fields.forEach(f => { initial[f.key] = f.defaultValue ?? '' })
    setFormData(initial)
    setError('')
    setModal('create')
  }

  function openEdit(row) {
    setEditing(row)
    const initial = {}
    fields.forEach(f => { initial[f.key] = row[f.key] ?? '' })
    setFormData(initial)
    setError('')
    setModal('edit')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setError('')
    try {
      // Filter out empty strings for optional fields
      const payload = {}
      fields.forEach(f => {
        const v = formData[f.key]
        if (v !== '' && v !== null && v !== undefined) {
          payload[f.key] = v
        } else if (f.required) {
          payload[f.key] = v
        }
      })

      if (modal === 'create') {
        await api.create(payload)
      } else {
        await api.update(editing.id, payload)
      }
      setModal(null)
      fetchItems()
    } catch (e) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  async function handleDeactivate(row) {
    if (!confirm(`¿Desactivar "${row.nombre || row.codigo || row.id}"?`)) return
    try {
      await api.deactivate(row.id)
      fetchItems()
    } catch (e) {
      alert(e.message)
    }
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">{title}</h1>
        <div className="search-bar">
          <input
            className="search-input"
            placeholder="Buscar..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-2)', fontSize: '13px' }}>
            <input
              type="checkbox"
              checked={showAll}
              onChange={e => setShowAll(e.target.checked)}
            />
            Mostrar inactivos
          </label>
          {exportUrl && (
            <a
              href={exportUrl}
              className="btn btn-secondary"
              style={{ textDecoration: 'none' }}
              download
            >
              ↓ CSV
            </a>
          )}
          <button className="btn btn-primary" onClick={openCreate}>+ Nuevo</button>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <span className="spinner" />
        </div>
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                {columns.map(col => (
                  <th key={col.key}>{col.label}</th>
                ))}
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 ? (
                <tr>
                  <td colSpan={columns.length + 2} style={{ textAlign: 'center', color: 'var(--text-2)', padding: '32px' }}>
                    Sin resultados
                  </td>
                </tr>
              ) : items.map(row => (
                <tr key={row.id}>
                  {columns.map(col => (
                    <td key={col.key}>
                      {col.render ? col.render(row) : (row[col.key] ?? '-')}
                    </td>
                  ))}
                  <td>
                    <span className={`badge ${row.activo ? 'badge-success' : 'badge-danger'}`}>
                      {row.activo ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                      <button className="btn btn-secondary btn-sm" onClick={() => openEdit(row)}>Editar</button>
                      {row.activo && (
                        <button className="btn btn-danger btn-sm" onClick={() => handleDeactivate(row)}>Desactivar</button>
                      )}
                      {extraActions && extraActions(row)}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {modal && (
        <Modal title={modal === 'create' ? `Nuevo ${title}` : `Editar ${title}`} onClose={() => setModal(null)}>
          <form onSubmit={handleSubmit}>
            {fields.map(field => (
              <div className="form-group" key={field.key}>
                <label>{field.label}{field.required && ' *'}</label>
                {field.type === 'select' ? (
                  <select
                    className="form-control"
                    value={formData[field.key] ?? ''}
                    onChange={e => setFormData(p => ({ ...p, [field.key]: e.target.value }))}
                    required={field.required}
                  >
                    <option value="">-- Seleccionar --</option>
                    {field.options?.map(opt => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                ) : field.type === 'textarea' ? (
                  <textarea
                    className="form-control"
                    rows={3}
                    value={formData[field.key] ?? ''}
                    onChange={e => setFormData(p => ({ ...p, [field.key]: e.target.value }))}
                    required={field.required}
                  />
                ) : (
                  <input
                    className="form-control"
                    type={field.type || 'text'}
                    value={formData[field.key] ?? ''}
                    onChange={e => setFormData(p => ({ ...p, [field.key]: e.target.value }))}
                    required={field.required}
                    placeholder={field.placeholder}
                  />
                )}
              </div>
            ))}
            {error && (
              <div style={{ color: 'var(--danger)', marginBottom: '12px', fontSize: '13px' }}>{error}</div>
            )}
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '8px' }}>
              <button type="button" className="btn btn-secondary" onClick={() => setModal(null)}>Cancelar</button>
              <button type="submit" className="btn btn-primary" disabled={saving}>
                {saving ? <span className="spinner" /> : (modal === 'create' ? 'Crear' : 'Guardar')}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  )
}
