'use client'

import { useParams } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { ACTIVITY_EMOJIS } from '@/lib/constants'

export default function ApartmentPage() {
  const { apartmentId } = useParams()
  const id = apartmentId as string

  const { data: realtime } = useQuery<any>({
    queryKey: ['apartment', id, 'realtime'],
    queryFn: () => api.getApartmentRealtime(id),
    refetchInterval: 5000,
  })

  const { data: insights } = useQuery<any>({
    queryKey: ['insights', id],
    queryFn: () => api.insights(id),
    enabled: !!id,
  })

  const state = realtime?.state as any

  return (
    <div className="min-h-screen bg-[#0f172a] p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold font-mono text-white">{id}</h1>
            <p className="text-sm text-[#94a3b8] font-mono">
              Tower {id[0]} · Floor {id[1]}
            </p>
          </div>
          <a href="/" className="text-sm text-[#6366f1] hover:text-[#818cf8] font-mono">
            ← Back
          </a>
        </div>

        {state && (
          <>
            <div className="bg-[#1e293b] rounded-lg p-4 mb-4">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl">{ACTIVITY_EMOJIS[state.activity_type] || '🏠'}</span>
                <div>
                  <div className="text-white font-medium capitalize">{state.activity_type.replace(/_/g, ' ')}</div>
                  <div className="text-sm text-[#94a3b8]">{state.num_people_present} people · {state.occupancy_state}</div>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  ['Electricity', `${state.electricity_wh.toFixed(1)} Wh`, '#6366f1'],
                  ['Water', `${state.water_liters.toFixed(1)} L`, '#22d3ee'],
                  ['Gas', `${state.gas_m3.toFixed(3)} m³`, '#f59e0b'],
                  ['Internet', `${state.internet_gb.toFixed(3)} GB`, '#a855f7'],
                  ['Comfort', `${(state.comfort_score * 100).toFixed(0)}%`, '#22c55e'],
                  ['Sustainability', `${(state.sustainability_score * 100).toFixed(0)}%`, '#22c55e'],
                  ['Temperature', `${state.temperature}°C`, '#ef4444'],
                  ['Solar', `${state.solar_generation.toFixed(2)} Wh`, '#eab308'],
                ].map(([label, val, color]) => (
                  <div key={label} className="bg-[#0f172a] rounded-lg p-3">
                    <div className="text-xs font-mono" style={{ color }}>{label}</div>
                    <div className="text-lg font-bold font-mono text-white mt-1">{val}</div>
                  </div>
                ))}
              </div>
            </div>

            {insights && (
              <div className="bg-[#1e293b] rounded-lg p-4">
                <h2 className="text-sm font-mono text-[#6366f1] mb-3">AI Insights</h2>
                <p className="text-sm text-[#94a3b8] mb-3">{insights?.summary}</p>
                {insights?.efficiency_grade && (
                  <div className="inline-block px-3 py-1 bg-[#6366f1]/20 text-[#6366f1] text-sm font-mono rounded">
                    Grade: {insights.efficiency_grade}
                  </div>
                )}
                  {insights?.recommendations?.map((r: any, i: number) => (
                  <div key={i} className="mt-3 p-3 bg-[#0f172a] rounded-lg">
                    <div className="flex items-center gap-1.5 mb-1">
                      <span className={`text-xs px-1.5 py-0.5 rounded font-mono ${
                        r.priority === 'high' ? 'bg-[#ef4444]/20 text-[#ef4444]' :
                        r.priority === 'medium' ? 'bg-[#eab308]/20 text-[#eab308]' :
                        'bg-[#6366f1]/20 text-[#6366f1]'
                      }`}>{r.priority}</span>
                      <span className="text-sm text-white">{r.title}</span>
                    </div>
                    <p className="text-xs text-[#94a3b8]">{r.description}</p>
                    <div className="text-xs text-[#22c55e] mt-1">{r.potential_savings}</div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {!state && (
          <div className="bg-[#1e293b] rounded-lg p-8 text-center">
            <div className="text-[#94a3b8] font-mono text-sm">No data available. Start the simulation first.</div>
          </div>
        )}
      </div>
    </div>
  )
}
