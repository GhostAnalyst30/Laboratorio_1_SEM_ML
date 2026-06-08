'use client'

import { useSelectionStore } from '@/stores/selectionStore'
import { useUIStore } from '@/stores/uiStore'
import { useApartmentRealtime, useForecast, useAnomalies, useRecommendations } from '@/hooks/useSimulation'
import { X, Zap, Droplets, Flame, Wifi, Thermometer, Leaf } from 'lucide-react'

const ACTIVITY_LABELS: Record<string, string> = {
  sleeping: 'Sleeping', waking: 'Waking', morning_routine: 'Morning Routine',
  away: 'Away', working: 'Working', studying: 'Studying', cooking: 'Cooking',
  eating: 'Eating', leisure: 'Leisure', cleaning: 'Cleaning',
  night_routine: 'Night Routine', entertainment: 'Entertainment',
}

export default function SidePanel() {
  const selectedApartment = useSelectionStore((s) => s.selectedApartment)
  const sidebarOpen = useUIStore((s) => s.sidebarOpen)
  const activePanel = useUIStore((s) => s.activePanel)
  const setActivePanel = useUIStore((s) => s.setActivePanel)
  const setSidebarOpen = useUIStore((s) => s.setSidebarOpen)
  const clearSelection = useSelectionStore((s) => s.clearSelection)

  const { data: realtime } = useApartmentRealtime(selectedApartment || '')
  const { data: forecast } = useForecast(selectedApartment || '')
  const { data: anomalies } = useAnomalies(selectedApartment || '')
  const { data: recs } = useRecommendations(selectedApartment || '')

  if (!selectedApartment || !sidebarOpen) return null

  const s = realtime?.state

  return (
    <div className="fixed right-0 top-12 bottom-0 w-[340px] bg-[#0c0e1a]/90 backdrop-blur-md border-l border-white/[0.04] z-40 overflow-y-auto">
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <div>
            <div className="text-sm font-bold font-mono text-white/90 tracking-wider">{selectedApartment}</div>
            <div className="text-[10px] font-mono text-white/30 tracking-wide">
              TOWER {selectedApartment[0]} · FLOOR {selectedApartment[1]}
            </div>
          </div>
          <button onClick={() => { clearSelection(); setSidebarOpen(false) }}
            className="p-1 hover:bg-white/[0.04] rounded transition-colors"
          >
            <X size={14} className="text-white/30" />
          </button>
        </div>

        {s && (
          <>
            <div className="bg-white/[0.03] border border-white/[0.04] rounded-lg p-3 mb-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-xs font-mono text-white/70 capitalize">
                    {ACTIVITY_LABELS[s.activity_type] || s.activity_type.replace(/_/g, ' ')}
                  </div>
                  <div className="text-[10px] font-mono text-white/30 mt-0.5">
                    {s.num_people_present} present · {s.occupancy_state}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-[10px] font-mono text-white/30">Comfort</div>
                  <div className="text-sm font-bold font-mono text-indigo-300">
                    {(s.comfort_score * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2 mb-4">
              <StatCard icon={<Zap size={12} />} label="Electricity" value={`${s.electricity_wh.toFixed(1)}`} unit="Wh" color="#818cf8" />
              <StatCard icon={<Droplets size={12} />} label="Water" value={`${s.water_liters.toFixed(1)}`} unit="L" color="#22d3ee" />
              <StatCard icon={<Flame size={12} />} label="Gas" value={`${s.gas_m3.toFixed(3)}`} unit="m³" color="#f59e0b" />
              <StatCard icon={<Wifi size={12} />} label="Internet" value={`${s.internet_gb.toFixed(3)}`} unit="GB" color="#a855f7" />
            </div>

            <div className="flex gap-1 mb-4 bg-white/[0.03] border border-white/[0.04] rounded-lg p-0.5">
              {(['info', 'charts', 'analytics'] as const).map((tab) => (
                <button key={tab} onClick={() => setActivePanel(tab)}
                  className={`flex-1 px-2.5 py-1.5 text-[10px] font-mono rounded transition-all uppercase tracking-wider ${
                    activePanel === tab ? 'bg-indigo-500/20 text-indigo-300' : 'text-white/30 hover:text-white/60'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>

            {activePanel === 'info' && (
              <div className="space-y-2 text-[11px] font-mono">
                <div className="bg-white/[0.03] border border-white/[0.04] rounded-lg p-3">
                  <div className="text-[10px] text-white/30 mb-2 uppercase tracking-wider">Environment</div>
                  {[
                    ['Temperature', `${s.temperature}°C`],
                    ['Humidity', `${s.humidity}%`],
                    ['Solar', `${s.solar_radiation.toFixed(0)} W/m²`],
                    ['Air Quality', `${s.air_quality.toFixed(0)}`],
                  ].map(([label, val]) => (
                    <div key={label} className="flex justify-between py-0.5">
                      <span className="text-white/30">{label}</span>
                      <span className="text-white/70">{val}</span>
                    </div>
                  ))}
                </div>
                <div className="bg-white/[0.03] border border-white/[0.04] rounded-lg p-3">
                  <div className="text-[10px] text-white/30 mb-2 uppercase tracking-wider">Scores</div>
                  {[
                    ['Comfort', `${(s.comfort_score * 100).toFixed(0)}%`],
                    ['Sustainability', `${(s.sustainability_score * 100).toFixed(0)}%`],
                  ].map(([label, val]) => (
                    <div key={label} className="flex justify-between py-0.5">
                      <span className="text-white/30">{label}</span>
                      <span className="text-white/70">{val}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activePanel === 'charts' && (
              <div className="space-y-3">
                <ForecastChart data={forecast?.forecasts || []} />
              </div>
            )}

            {activePanel === 'analytics' && (
              <div className="space-y-3">
                {anomalies?.anomalies?.length > 0 && (
                  <div className="bg-white/[0.03] border border-white/[0.04] rounded-lg p-3">
                    <div className="text-[10px] font-mono text-red-400/70 mb-2 uppercase tracking-wider">Anomalies</div>
                    {anomalies.anomalies.slice(0, 3).map((a: any, i: number) => (
                      <div key={i} className="text-[10px] text-white/40 mb-1 font-mono">
                        <span className="text-white/70">t={a.timestamp}</span> {a.description}
                      </div>
                    ))}
                  </div>
                )}
                {recs?.recommendations?.length > 0 && (
                  <div className="bg-white/[0.03] border border-white/[0.04] rounded-lg p-3">
                    <div className="text-[10px] font-mono text-green-400/70 mb-2 uppercase tracking-wider">Recommendations</div>
                    {recs.recommendations.slice(0, 3).map((r: any, i: number) => (
                      <div key={i} className="mb-2 last:mb-0">
                        <div className="flex items-center gap-1.5 mb-0.5">
                          <span className={`text-[9px] uppercase tracking-wider px-1 py-0.5 rounded font-mono ${
                            r.priority === 'high' ? 'bg-red-500/10 text-red-400' :
                            r.priority === 'medium' ? 'bg-yellow-500/10 text-yellow-400' :
                            'bg-indigo-500/10 text-indigo-400'
                          }`}>{r.priority}</span>
                          <span className="text-[11px] text-white/70 font-medium">{r.title}</span>
                        </div>
                        <p className="text-[10px] text-white/40">{r.description}</p>
                      </div>
                    ))}
                  </div>
                )}
                {forecast && (
                  <div className="bg-white/[0.03] border border-white/[0.04] rounded-lg p-3">
                    <div className="text-[10px] font-mono text-indigo-400/70 mb-2 uppercase tracking-wider">Forecast</div>
                    {forecast.forecasts.slice(0, 5).map((f: any, i: number) => (
                      <div key={i} className="flex justify-between text-[10px] font-mono text-white/40 py-0.5">
                        <span>t+{i + 1}</span>
                        <span className="text-white/70">{f.predicted_value.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </>
        )}

        {!s && (
          <div className="text-center py-8">
            <div className="text-[11px] font-mono text-white/20">Start the simulation to see live data</div>
          </div>
        )}
      </div>
    </div>
  )
}

function StatCard({ icon, label, value, unit, color }: {
  icon: React.ReactNode; label: string; value: string; unit: string; color: string
}) {
  return (
    <div className="bg-white/[0.03] border border-white/[0.04] rounded-lg p-2.5">
      <div className="flex items-center gap-1.5 mb-1">
        <span style={{ color }}>{icon}</span>
        <span className="text-[9px] font-mono text-white/30 uppercase tracking-wider">{label}</span>
      </div>
      <div className="text-sm font-bold font-mono text-white/90">{value}</div>
      <div className="text-[9px] font-mono text-white/20">{unit}</div>
    </div>
  )
}

function ForecastChart({ data }: { data: any[] }) {
  if (data.length === 0) return null
  const max = Math.max(...data.map(d => d.upper_bound), 1)
  const min = Math.min(...data.map(d => d.lower_bound), 0)
  const range = max - min || 1
  const w = 290
  const h = 120
  const pad = { top: 10, right: 10, bottom: 20, left: 30 }
  const pw = w - pad.left - pad.right
  const ph = h - pad.top - pad.bottom

  const line = data.map((d, i) => {
    const x = pad.left + (i / (data.length - 1)) * pw
    const y = pad.top + ph - ((d.predicted_value - min) / range) * ph
    return `${x},${y}`
  }).join(' ')

  const upper = data.map((d, i) => {
    const x = pad.left + (i / (data.length - 1)) * pw
    const y = pad.top + ph - ((d.upper_bound - min) / range) * ph
    return `${x},${y}`
  }).join(' ')
  const lower = data.map((d, i) => {
    const x = pad.left + (i / (data.length - 1)) * pw
    const y = pad.top + ph - ((d.lower_bound - min) / range) * ph
    return `${x},${y}`
  }).reverse().join(' ')

  return (
    <div className="bg-white/[0.03] border border-white/[0.04] rounded-lg p-3">
      <div className="text-[10px] font-mono text-white/30 mb-2 uppercase tracking-wider">Forecast</div>
      <svg width={w} height={h} className="w-full">
        {[0, 0.25, 0.5, 0.75, 1].map(f => {
          const y = pad.top + ph * (1 - f)
          return (
            <g key={f}>
              <line x1={pad.left} y1={y} x2={pad.left + pw} y2={y} stroke="rgba(255,255,255,0.04)" strokeWidth={1} />
              <text x={pad.left - 4} y={y + 3} textAnchor="end" fill="rgba(255,255,255,0.2)" fontSize={8} fontFamily="monospace">
                {(min + range * f).toFixed(0)}
              </text>
            </g>
          )
        })}
        <polygon points={upper + ' ' + lower} fill="rgba(99,102,241,0.08)" />
        <polyline points={line} fill="none" stroke="rgba(99,102,241,0.6)" strokeWidth={1.5} />
      </svg>
      <div className="text-[9px] font-mono text-white/20 text-center mt-1">polynomial trend · 72-step horizon</div>
    </div>
  )
}
