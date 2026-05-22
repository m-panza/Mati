import { useState, useEffect } from 'react';
import { Users, Layers, Cpu } from 'lucide-react';
import { api, authFetch } from '../api/client';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

// ── Attribute stat cards ──────────────────────────────────────────────────────

const CHART_COLORS = ['#4f9cf9', '#4caf7d', '#c084fc', '#ffcc00', '#f472b6', '#22d3ee', '#fb923c'];
const NO_DATA_COLOR = '#2a2a2a';
const YES_COLOR = '#4caf7d';
const NO_COLOR = '#3a1a1a';

function BoolPieCard({ attr, summary }) {
  const yes = summary.filter(s => s.app_attributes?.[attr.name] === 'true').length;
  const no  = summary.filter(s => s.app_attributes?.[attr.name] === 'false').length;
  const none = summary.length - yes - no;
  const data = [
    { name: 'Sí',       value: yes,  color: YES_COLOR },
    { name: 'No',       value: no,   color: '#8b1a1a' },
    { name: 'Sin dato', value: none, color: NO_DATA_COLOR },
  ].filter(d => d.value > 0);

  const pct = summary.length > 0 ? Math.round(yes * 100 / summary.length) : 0;

  return (
    <div className="home-card" style={{ minWidth: 180 }}>
      <div className="home-card-title">{attr.name}</div>
      <div style={{ fontSize: 11, color: 'var(--text-2)', marginBottom: 8 }}>{attr.category}</div>
      <ResponsiveContainer width="100%" height={90}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={25} outerRadius={40} dataKey="value" strokeWidth={0}>
            {data.map((entry, i) => <Cell key={i} fill={entry.color} />)}
          </Pie>
          <Tooltip formatter={(v, n) => [v, n]} contentStyle={{ background: 'var(--bg-2)', border: '1px solid var(--border)', fontSize: 11 }} />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ textAlign: 'center', fontSize: 20, fontWeight: 700, color: 'var(--text)', marginTop: 4 }}>{pct}%</div>
      <div style={{ textAlign: 'center', fontSize: 11, color: 'var(--text-2)' }}>{yes}/{summary.length} apps</div>
    </div>
  );
}

function SelectPieCard({ attr, summary }) {
  const counts = {};
  let noData = 0;
  summary.forEach(s => {
    const val = s.app_attributes?.[attr.name];
    if (val) counts[val] = (counts[val] || 0) + 1;
    else noData++;
  });

  const realData = Object.entries(counts).map(([name, value], i) => ({
    name, value, color: CHART_COLORS[i % CHART_COLORS.length],
  }));
  const data = noData > 0
    ? [...realData, { name: '(sin dato)', value: noData, color: NO_DATA_COLOR }]
    : realData;

  const total = summary.length;

  return (
    <div className="home-card" style={{ minWidth: 180 }}>
      <div className="home-card-title">{attr.name}</div>
      <div style={{ fontSize: 11, color: 'var(--text-2)', marginBottom: 8 }}>{attr.category}</div>
      <ResponsiveContainer width="100%" height={90}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={25} outerRadius={40} dataKey="value" strokeWidth={0}>
            {data.map((entry, i) => <Cell key={i} fill={entry.color} />)}
          </Pie>
          <Tooltip
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;
              const d = payload[0].payload;
              return (
                <div style={{ background: 'var(--bg-2)', border: '1px solid var(--border)', borderRadius: 4, padding: '4px 8px', fontSize: 11 }}>
                  <span style={{ color: d.color }}>{d.name}</span>: {d.value}
                </div>
              );
            }}
          />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 6, justifyContent: 'center' }}>
        {realData.map((d, i) => (
          <span key={i} style={{ fontSize: 10, color: d.color, display: 'flex', alignItems: 'center', gap: 3 }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: d.color, display: 'inline-block' }} />
            {d.name} ({d.value})
          </span>
        ))}
      </div>
    </div>
  );
}

function TextCompletionCard({ attr, summary }) {
  const withValue = summary.filter(s => s.app_attributes?.[attr.name]).length;
  const pct = summary.length > 0 ? Math.round(withValue * 100 / summary.length) : 0;
  const data = [
    { name: 'Con valor', value: withValue, color: '#4f9cf9' },
    { name: 'Sin dato',  value: summary.length - withValue, color: NO_DATA_COLOR },
  ];

  return (
    <div className="home-card" style={{ minWidth: 180 }}>
      <div className="home-card-title">{attr.name}</div>
      <div style={{ fontSize: 11, color: 'var(--text-2)', marginBottom: 8 }}>{attr.category}</div>
      <ResponsiveContainer width="100%" height={90}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={25} outerRadius={40} dataKey="value" strokeWidth={0}>
            {data.map((entry, i) => <Cell key={i} fill={entry.color} />)}
          </Pie>
          <Tooltip formatter={(v, n) => [v, n]} contentStyle={{ background: 'var(--bg-2)', border: '1px solid var(--border)', fontSize: 11 }} />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ textAlign: 'center', fontSize: 20, fontWeight: 700, color: 'var(--text)', marginTop: 4 }}>{pct}%</div>
      <div style={{ textAlign: 'center', fontSize: 11, color: 'var(--text-2)' }}>{withValue}/{summary.length} apps</div>
    </div>
  );
}

function SvcBoolPieCard({ attr, summary }) {
  let yes = 0, no = 0, none = 0, total = 0;
  summary.forEach(s => {
    const data = s.service_attributes?.[attr.name];
    if (!data) return;
    yes  += data.count;
    no   += data.total - data.count;
    total += data.total;
  });
  none = 0; // ya contamos todos
  const pct = total > 0 ? Math.round(yes * 100 / total) : 0;
  const data = [
    { name: 'Sí',  value: yes, color: YES_COLOR },
    { name: 'No',  value: no,  color: '#8b1a1a' },
  ].filter(d => d.value > 0);

  return (
    <div className="home-card" style={{ minWidth: 180 }}>
      <div className="home-card-title">{attr.name}</div>
      <div style={{ fontSize: 11, color: 'var(--text-2)', marginBottom: 8 }}>{attr.category}</div>
      <ResponsiveContainer width="100%" height={90}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={25} outerRadius={40} dataKey="value" strokeWidth={0}>
            {data.map((entry, i) => <Cell key={i} fill={entry.color} />)}
          </Pie>
          <Tooltip formatter={(v, n) => [v, n]} contentStyle={{ background: 'var(--bg-2)', border: '1px solid var(--border)', fontSize: 11 }} />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ textAlign: 'center', fontSize: 20, fontWeight: 700, color: 'var(--text)', marginTop: 4 }}>{pct}%</div>
      <div style={{ textAlign: 'center', fontSize: 11, color: 'var(--text-2)' }}>{yes}/{total} servicios</div>
    </div>
  );
}

function AttributeStatsCards({ attributes, summary }) {
  const appAttrs = attributes.filter(a => a.scope === 'app' && a.active && a.show_in_summary);
  const svcAttrs = attributes.filter(a => a.scope === 'service' && a.active && a.show_in_summary);

  if (appAttrs.length === 0 && svcAttrs.length === 0) return null;

  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16, marginBottom: 24 }}>
      {appAttrs.map(attr => {
        if (attr.input_type === 'boolean') return <BoolPieCard key={attr.id} attr={attr} summary={summary} />;
        if (attr.input_type === 'select')  return <SelectPieCard key={attr.id} attr={attr} summary={summary} />;
        return <TextCompletionCard key={attr.id} attr={attr} summary={summary} />;
      })}
      {svcAttrs.map(attr => (
        attr.input_type === 'boolean'
          ? <SvcBoolPieCard key={attr.id} attr={attr} summary={summary} />
          : null
      ))}
    </div>
  );
}

function appStatus(app) {
  if (app.total === 0) return 'pending';
  if (app.with_data === app.total) return 'measuring';
  if (app.with_data === 0) return 'pending';
  return 'partial';
}

const DORA_DOT = {
  measuring: { bg: '#4caf7d', title: 'measuring' },
  partial:   { bg: '#ffcc00', title: 'partial' },
  pending:   { bg: 'var(--bg-3)', title: 'pending', border: '1px solid var(--border-2)' },
};

const TAG_COLORS = [
  { bg: '#1a2a3a', color: '#4f9cf9' },
  { bg: '#1a3a2a', color: '#4caf7d' },
  { bg: '#3a2a3a', color: '#c084fc' },
  { bg: '#3a3a1a', color: '#ffcc00' },
  { bg: '#2a1a3a', color: '#f472b6' },
  { bg: '#1a3a3a', color: '#22d3ee' },
  { bg: '#3a2a1a', color: '#fb923c' },
];
const tagColorCache = {};
function getTagColor(value) {
  if (!tagColorCache[value]) {
    // hash djb2 para mejor distribución
    let hash = 5381;
    for (let i = 0; i < value.length; i++) {
      hash = ((hash << 5) + hash) + value.charCodeAt(i);
      hash = hash & hash; // convert to 32bit int
    }
    const idx = Math.abs(hash) % TAG_COLORS.length;
    tagColorCache[value] = TAG_COLORS[idx];
  }
  return tagColorCache[value];
}

function TextTag({ value }) {
  if (!value) return <span style={{ color: 'var(--text-2)', fontSize: 12 }}>—</span>;
  const { bg, color } = getTagColor(value);
  return (
    <span style={{ background: bg, color, padding: '2px 8px', borderRadius: 4, fontSize: 11, fontWeight: 500 }}>
      {value}
    </span>
  );
}

function BoolBadge({ value }) {
  if (!value) return (
    <span style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: 16, height: 16, borderRadius: '50%', background: 'var(--bg-3)', border: '1px solid var(--border-2)', fontSize: 9, color: 'var(--text-2)', fontWeight: 700 }}>—</span>
  );
  const isTrue = value === 'true';
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: 16, height: 16, borderRadius: '50%', background: isTrue ? '#4caf7d' : 'var(--bg-3)', border: isTrue ? 'none' : '1px solid var(--border-2)', fontSize: 9, color: isTrue ? '#fff' : 'var(--text-2)', fontWeight: 700 }}>
      {isTrue ? '✓' : '—'}
    </span>
  );
}

function PctBadge({ count, total }) {
  if (total === 0) return <span style={{ color: 'var(--text-2)', fontSize: 12 }}>—</span>;
  const pct = Math.round(count * 100 / total);
  const color = pct >= 80 ? '#4caf7d' : pct >= 40 ? '#ffcc00' : pct > 0 ? '#ff8800' : 'var(--border-2)';
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
      <span style={{ fontSize: 11, color: 'var(--text-2)', fontFamily: 'var(--font-mono)', minWidth: 32 }}>{count}/{total}</span>
      <div style={{ width: 48, height: 4, background: 'var(--bg-3)', borderRadius: 2, overflow: 'hidden' }}>
        <div style={{ width: `${pct}%`, height: '100%', background: color, borderRadius: 2 }} />
      </div>
    </div>
  );
}

function AppRow({ app, treeApp, appAttrs, svcAttrs, tableAttrs, serviceFilter }) {
  const [expanded, setExpanded] = useState(false);
  const [svcValues, setSvcValues] = useState({});
  const status = appStatus(treeApp || { total: 0, with_data: 0 });
  const dot = DORA_DOT[status];

  const visibleServices = serviceFilter
    ? treeApp?.services?.filter(s => s.name === serviceFilter)
    : treeApp?.services;

  const handleExpand = async () => {
    const next = !expanded;
    setExpanded(next);
    if (next && svcAttrs.length > 0 && treeApp?.services?.length > 0) {
      const missing = treeApp.services.filter(s => !svcValues[s.id]);
      if (missing.length > 0) {
        const results = await Promise.all(
          missing.map(s =>
            api.getAttributeValues({ service_id: s.id })
              .then(vals => {
                const map = {};
                vals.forEach(v => { map[v.name] = v.value; });
                return [s.id, map];
              })
          )
        );
        setSvcValues(prev => {
          const next = { ...prev };
          results.forEach(([id, map]) => { next[id] = map; });
          return next;
        });
      }
    }
  };

  return (
    <>
      <tr>
        <td style={{ paddingLeft: 12 }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            {treeApp?.services?.length > 0 ? (
              <button className="btn-expand" onClick={handleExpand} style={{ flexShrink: 0 }}>
                {expanded ? '▾' : '▸'}
              </button>
            ) : (
              <span style={{ width: 20, flexShrink: 0 }} />
            )}
            <Layers size={13} strokeWidth={1.5} style={{ color: 'var(--text-2)', flexShrink: 0 }} />
            {app?.app_name || treeApp?.name}
          </span>
        </td>
        <td>
          <span title={dot.title} style={{ display: 'inline-block', width: 12, height: 12, borderRadius: '50%', background: dot.bg, border: dot.border || 'none' }} />
        </td>
        {tableAttrs.map(attr => (
          <td key={attr.name}>
            {attr.scope === 'app'
              ? attr.input_type === 'boolean'
                ? <BoolBadge value={app?.app_attributes?.[attr.name]} />
                : <TextTag value={app?.app_attributes?.[attr.name]} />
              : app
                ? <PctBadge count={app.service_attributes?.[attr.name]?.count || 0} total={app.service_attributes?.[attr.name]?.total || 0} />
                : <span style={{ color: 'var(--text-2)', fontSize: 12 }}>—</span>}
          </td>
        ))}
      </tr>
      {expanded && visibleServices?.map(svc => (
        <tr key={svc.id} style={{ background: 'var(--bg-3)' }}>
          <td style={{ paddingLeft: 44 }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--text-2)' }}>
              <Cpu size={11} strokeWidth={1.5} style={{ flexShrink: 0 }} />
              {svc.name}
            </span>
          </td>
          <td>
            <span title={svc.has_data ? 'measuring' : 'pending'} style={{ display: 'inline-block', width: 12, height: 12, borderRadius: '50%', background: svc.has_data ? '#4caf7d' : 'var(--bg-3)', border: svc.has_data ? 'none' : '1px solid var(--border-2)' }} />
          </td>
          {tableAttrs.map(attr => (
            <td key={attr.name}>
              {attr.scope === 'app'
                ? attr.input_type === 'boolean'
                  ? <BoolBadge value={app?.app_attributes?.[attr.name]} />
                  : <TextTag value={app?.app_attributes?.[attr.name]} />
                : attr.input_type === 'boolean'
                  ? <BoolBadge value={svcValues[svc.id]?.[attr.name]} />
                  : <TextTag value={svcValues[svc.id]?.[attr.name]} />}
            </td>
          ))}
        </tr>
      ))}
    </>
  );
}

async function exportToCSV(filteredTree, summaryByApp, tableAttrs) {
  const svcScopeAttrs = tableAttrs.filter(a => a.scope === 'service');

  // Fetch individual service attribute values for all visible services
  const svcValues = {};
  if (svcScopeAttrs.length > 0) {
    const allServices = filteredTree.flatMap(team =>
      team.apps.flatMap(a => a.services || [])
    );
    await Promise.all(
      allServices.map(svc =>
        api.getAttributeValues({ service_id: svc.id }).then(vals => {
          const map = {};
          vals.forEach(v => { map[v.name] = v.value; });
          svcValues[svc.id] = map;
        })
      )
    );
  }

  const headers = ['Team', 'App', 'Service', 'DORA', ...tableAttrs.map(a => a.name)];
  const rows = [];

  filteredTree.forEach(team => {
    team.apps.forEach(treeApp => {
      const app = summaryByApp[treeApp.id];
      const status = appStatus(treeApp || { total: 0, with_data: 0 });

      // App-level row
      const appCols = tableAttrs.map(attr => {
        if (attr.scope === 'app') return app?.app_attributes?.[attr.name] ?? '';
        const count = app?.service_attributes?.[attr.name]?.count;
        const total = app?.service_attributes?.[attr.name]?.total;
        return count != null ? `${count}/${total}` : '';
      });
      rows.push([team.name, treeApp.name, '', status, ...appCols]);

      // Service-level rows
      (treeApp.services || []).forEach(svc => {
        const svcStatus = svc.has_data ? 'measuring' : 'pending';
        const svcCols = tableAttrs.map(attr => {
          if (attr.scope === 'app') return app?.app_attributes?.[attr.name] ?? '';
          return svcValues[svc.id]?.[attr.name] ?? '';
        });
        rows.push([team.name, treeApp.name, svc.name, svcStatus, ...svcCols]);
      });
    });
  });

  const escape = cell => `"${String(cell).replace(/"/g, '""')}"`;
  const csv = [headers, ...rows].map(row => row.map(escape).join(',')).join('\n');

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `applications_${new Date().toISOString().slice(0, 10)}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

export default function ApplicationsPage() {
  const [coverage, setCoverage] = useState(null);
  const [tree, setTree] = useState([]);
  const [summary, setSummary] = useState([]);
  const [attributes, setAttributes] = useState([]);
  const [loading, setLoading] = useState(true);

  const [teamFilter, setTeamFilter] = useState('');
  const [appFilter, setAppFilter] = useState('');
  const [serviceFilter, setServiceFilter] = useState('');

  const [refreshKey, setRefreshKey] = useState(0);
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      authFetch('/metrics/coverage').then(r => r.json()),
      authFetch('/metrics/coverage-tree').then(r => r.json()),
      api.getAttributesSummary(),
      api.listAttributes({ active: true }),
    ]).then(([cov, tr, sum, attrs]) => {
      setCoverage(cov);
      setTree(tr);
      setSummary(sum);
      setAttributes(attrs);
    }).finally(() => setLoading(false));
  }, [refreshKey]);

  if (loading) return <div className="page"><div className="metrics-loading">Loading...</div></div>;
  if (!coverage) return <div className="page"><div className="metrics-loading">Error loading data.</div></div>;

  const appAttrs = attributes.filter(a => a.scope === 'app').sort((a, b) => a.order_idx - b.order_idx);
  const svcAttrs = attributes.filter(a => a.scope === 'service').sort((a, b) => a.order_idx - b.order_idx);
  // Columnas de la tabla ordenadas globalmente por order_idx
  const tableAttrs = [...attributes].sort((a, b) => a.order_idx - b.order_idx);
  const summaryByApp = Object.fromEntries(summary.map(s => [s.app_id, s]));

  // Opciones encadenadas
  const teams = [...new Set(tree.map(t => t.name))];
  const selectedTeam = tree.find(t => t.name === teamFilter);
  const apps = selectedTeam ? selectedTeam.apps : tree.flatMap(t => t.apps);
  const selectedApp = apps.find(a => a.name === appFilter);
  const services = selectedApp ? selectedApp.services : apps.flatMap(a => a.services || []);

  // Filtrado de tree
  const filteredTree = tree
    .filter(team => !teamFilter || team.name === teamFilter)
    .map(team => ({
      ...team,
      apps: team.apps
        .filter(app => !appFilter || app.name === appFilter)
        .filter(app => !serviceFilter || app.services?.some(s => s.name === serviceFilter)),
    }))
    .filter(team => team.apps.length > 0);

  const colCount = 2 + tableAttrs.length;

  return (
    <div className="page">
      <div className="page-header">
        <h2>Applications</h2>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-secondary" disabled={exporting} onClick={async () => { setExporting(true); try { await exportToCSV(filteredTree, summaryByApp, tableAttrs); } finally { setExporting(false); } }}>{exporting ? 'Exportando...' : '↓ Export CSV'}</button>
          <button className="btn btn-secondary" onClick={() => setRefreshKey(k => k + 1)}>↻ Refresh</button>
        </div>
      </div>

      <AttributeStatsCards attributes={attributes} summary={summary} />

      <div className="toolbar" style={{ marginTop: 16 }}>
        <select value={teamFilter} onChange={e => { setTeamFilter(e.target.value); setAppFilter(''); setServiceFilter(''); }}>
          <option value="">All teams</option>
          {teams.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
        <select value={appFilter} onChange={e => { setAppFilter(e.target.value); setServiceFilter(''); }} disabled={!teamFilter}>
          <option value="">All apps</option>
          {apps.map(a => <option key={a.id} value={a.name}>{a.name}</option>)}
        </select>
        <select value={serviceFilter} onChange={e => setServiceFilter(e.target.value)} disabled={!appFilter}>
          <option value="">All services</option>
          {services.map(s => <option key={s.id} value={s.name}>{s.name}</option>)}
        </select>
      </div>

      <div style={{ marginTop: 16, overflowY: 'auto', maxHeight: 'calc(100vh - 280px)', borderRadius: 8, border: '1px solid var(--border)' }}>
        <table className="home-coverage-table" style={{ borderRadius: 0 }}>
          <thead>
            <tr>
              <th>App</th>
              <th>DORA</th>
              {tableAttrs.map(attr => <th key={attr.name}>{attr.name}</th>)}
            </tr>
          </thead>
          <tbody>
            {filteredTree.map(team => (
              <>
                <tr key={`team-${team.id}`}>
                  <td colSpan={colCount} style={{
                    fontFamily: 'var(--font-mono)', fontSize: 11,
                    letterSpacing: '0.08em', textTransform: 'uppercase',
                    color: 'var(--text-2)', padding: '12px 12px 6px',
                    background: 'var(--bg-2)', borderTop: '1px solid var(--border)',
                  }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                      <Users size={12} strokeWidth={1.5} />
                      {team.name}
                    </span>
                  </td>
                </tr>
                {team.apps.map(treeApp => (
                  <AppRow
                    key={treeApp.id}
                    app={summaryByApp[treeApp.id]}
                    treeApp={treeApp}
                    appAttrs={appAttrs}
                    svcAttrs={svcAttrs}
                    tableAttrs={tableAttrs}
                    serviceFilter={serviceFilter}
                  />
                ))}
              </>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
