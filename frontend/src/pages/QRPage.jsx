import React, { useState, useEffect } from 'react'
import { api } from '../api/client'

const ENTITY_TYPES = [
  { value: 'tacho', label: 'Tacho' },
  { value: 'isla', label: 'Isla' },
  { value: 'nodo', label: 'Nodo' },
]

export default function QRPage() {
  const [entityType, setEntityType] = useState('tacho')
  const [entities, setEntities] = useState([])
  const [selectedId, setSelectedId] = useState('')
  const [qrData, setQrData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    setSelectedId('')
    setQrData(null)
    setEntities([])
    setLoading(true)
    const apiMap = { tacho: api.tachos, isla: api.islas, nodo: api.nodos }
    apiMap[entityType].list({ activo: true, limit: 1000 })
      .then(data => {
        setEntities(Array.isArray(data) ? data : (data.items || []))
      })
      .catch(() => setEntities([]))
      .finally(() => setLoading(false))
  }, [entityType])

  async function handleGenerate() {
    if (!selectedId) return
    setGenerating(true)
    setError('')
    try {
      const data = await api.qr.generar(entityType, selectedId)
      setQrData(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Generador de QR</h1>
      </div>

      <div className="card" style={{ maxWidth: '560px' }}>
        <div className="form-group">
          <label>Tipo de entidad</label>
          <select
            className="form-control"
            value={entityType}
            onChange={e => setEntityType(e.target.value)}
          >
            {ENTITY_TYPES.map(t => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Seleccionar {entityType}</label>
          {loading ? (
            <div style={{ padding: '8px 0' }}><span className="spinner" /></div>
          ) : (
            <select
              className="form-control"
              value={selectedId}
              onChange={e => { setSelectedId(e.target.value); setQrData(null) }}
            >
              <option value="">-- Seleccionar --</option>
              {entities.map(e => (
                <option key={e.id} value={e.id}>{e.codigo} - {e.nombre}</option>
              ))}
            </select>
          )}
        </div>

        {error && (
          <div style={{ color: 'var(--danger)', fontSize: '13px', marginBottom: '12px' }}>{error}</div>
        )}

        <button
          className="btn btn-primary"
          onClick={handleGenerate}
          disabled={!selectedId || generating}
        >
          {generating ? <span className="spinner" /> : 'Generar QR'}
        </button>

        {qrData && (
          <div style={{ marginTop: '24px', textAlign: 'center' }}>
            <div style={{ marginBottom: '12px' }}>
              <span className="mono" style={{ fontSize: '16px', fontWeight: '700' }}>{qrData.codigo_qr}</span>
            </div>
            <img
              src={api.qr.imagenUrl(qrData.codigo_qr)}
              alt={`QR ${qrData.codigo_qr}`}
              style={{
                width: '220px', height: '220px',
                border: '1px solid var(--border-2)',
                borderRadius: '8px',
                background: '#fff',
                display: 'block',
                margin: '0 auto 12px',
              }}
            />
            <div style={{ fontSize: '12px', color: 'var(--text-2)', marginBottom: '12px' }}>
              URL: <a href={qrData.url_qr} target="_blank" rel="noreferrer">{qrData.url_qr}</a>
            </div>
            <a
              href={api.qr.imagenUrl(qrData.codigo_qr)}
              download={`${qrData.codigo_qr}.png`}
              className="btn btn-secondary"
            >
              ↓ Descargar PNG
            </a>
          </div>
        )}
      </div>
    </div>
  )
}
