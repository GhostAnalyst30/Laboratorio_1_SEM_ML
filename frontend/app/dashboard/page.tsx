'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useCommunitySummary, useClusters } from '@/hooks/useSimulation'
import { TOWERS, TOTAL_APARTMENTS, UTILITY_COLORS } from '@/lib/constants'

const qc = new QueryClient()

function DashboardContent() {
  const { data: summary } = useCommunitySummary()
  const { data: clusters } = useClusters()

  return (
    <div className="min-h-screen bg-[#0f172a] p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold font-mono text-white">Dashboard</h1>
            <p className="text-sm text-[#94a3b8] font-mono">Community Analytics Overview</p>
          </div>
          <a href="/" className="text-sm text-[#6366f1] hover:text-[#818cf8] font-mono">
            ← 3D View
          </a>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Total Apartments', value: TOTAL_APARTMENTS, color: '#6366f1' },
            { label: 'Total Towers', value: TOWERS.length, color: '#22d3ee' },
            { label: 'Avg Comfort', value: summary ? `${(summary.avg_comfort * 100).toFixed(0)}%` : '--', color: '#22c55e' },
            { label: 'Sustainability', value: summary ? `${(summary.avg_sustainability * 100).toFixed(0)}%` : '--', color: '#a855f7' },
          ].map((kpi) => (
            <div key={kpi.label} className="bg-[#1e293b] rounded-xl p-4">
              <div className="text-xs font-mono" style={{ color: kpi.color }}>{kpi.label}</div>
              <div className="text-3xl font-bold font-mono text-white mt-1">{kpi.value}</div>
            </div>
          ))}
        </div>

        {/* Tower Archetypes */}
        <div className="bg-[#1e293b] rounded-xl p-4 mb-8">
          <h2 className="text-sm font-mono text-[#94a3b8] mb-4">Tower Identities (Emergent Behavior)</h2>
          <div className="grid grid-cols-2 gap-3 max-w-md">
            {TOWERS.map((id, i) => {
              const archetype = i === 0 ? 'Efficient' : 'High Consumption'
              const color = i === 0 ? '#22c55e' : '#ef4444'
              return (
                <div key={id} className="bg-[#0f172a] rounded-lg p-3 text-center">
                  <div className="text-lg font-bold font-mono text-white">Tower {id}</div>
                  <div className="text-xs font-mono mt-1" style={{ color }}>{archetype}</div>
                  <div className="text-[10px] text-[#64748b] mt-1">16 apts</div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Clusters */}
        {clusters?.clusters && (
          <div className="bg-[#1e293b] rounded-xl p-4">
            <h2 className="text-sm font-mono text-[#94a3b8] mb-4">Consumption Archetypes (Clustering)</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
              {clusters.clusters.map((c: any) => (
                <div key={c.cluster_id} className="bg-[#0f172a] rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-mono text-white">{c.label}</span>
                    <span className="text-xs text-[#94a3b8] font-mono">{c.size} apts</span>
                  </div>
                  <div className="space-y-1 text-xs font-mono text-[#64748b]">
                    <div className="flex justify-between">
                      <span>Electricity</span>
                      <span className="text-white">{c.avg_electricity_kwh.toFixed(1)} kWh</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Water</span>
                      <span className="text-white">{c.avg_water_liters.toFixed(0)} L</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Sustainability</span>
                      <span className="text-white">{(c.avg_sustainability * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {summary && (
          <div className="mt-8 text-center text-xs text-[#64748b] font-mono">
            Dataset: {(summary?.total_records ?? 0).toLocaleString()} records generated
          </div>
        )}
      </div>
    </div>
  )
}

export default function DashboardPage() {
  return (
    <QueryClientProvider client={qc}>
      <DashboardContent />
    </QueryClientProvider>
  )
}
