'use client'

import { useCommunitySummary, useClusters } from '@/hooks/useSimulation'
import { TOTAL_APARTMENTS, TOWERS } from '@/lib/constants'

export default function CommunityOverview() {
  const { data: summary } = useCommunitySummary()
  const { data: clusters } = useClusters()

  return (
    <div className="bg-[#0c0e1a]/90 backdrop-blur-md border border-white/[0.04] rounded-lg p-4 space-y-3">
      <div className="text-[10px] font-mono text-indigo-400/70 uppercase tracking-[0.2em]">
        Community Overview
      </div>

      <div className="grid grid-cols-2 gap-2">
        <KPI label="Apartments" value={String(TOTAL_APARTMENTS)} />
        <KPI label="Towers" value={String(TOWERS.length)} />
        <KPI label="Comfort" value={summary ? `${(summary.avg_comfort * 100).toFixed(0)}%` : '--'} color="#22d3ee" />
        <KPI label="Sustainability" value={summary ? `${(summary.avg_sustainability * 100).toFixed(0)}%` : '--'} color="#22c55e" />
      </div>

      <div>
        <div className="text-[9px] font-mono text-white/20 uppercase tracking-wider mb-1.5">Tower Archetypes</div>
        <div className="flex gap-1.5">
          {TOWERS.map((id, i) => {
            const archetype = i === 0 ? 'eco' : 'high'
            const colors = {
              eco: 'bg-green-500/10 text-green-400 border-green-500/20',
              high: 'bg-red-500/10 text-red-400 border-red-500/20',
            }
            return (
              <div key={id} className={`flex-1 text-center text-[10px] font-mono py-1 rounded border ${colors[archetype]}`}>
                Tower {id}
              </div>
            )
          })}
        </div>
      </div>

      {clusters?.clusters?.length > 0 && (
        <div>
          <div className="text-[9px] font-mono text-white/20 uppercase tracking-wider mb-1.5">Profiles</div>
          {clusters.clusters.map((c: any) => (
            <div key={c.cluster_id} className="flex items-center justify-between py-0.5 text-[10px] font-mono">
              <span className="text-white/70">{c.label}</span>
              <span className="text-white/30">{c.size} apts</span>
            </div>
          ))}
        </div>
      )}

      {summary && (
        <div className="text-[9px] font-mono text-white/15 text-center pt-1 border-t border-white/[0.04]">
          {(summary?.total_records ?? 0).toLocaleString()} records generated
        </div>
      )}
    </div>
  )
}

function KPI({ label, value, color = '#818cf8' }: { label: string; value: string; color?: string }) {
  return (
    <div className="bg-white/[0.03] border border-white/[0.04] rounded-lg p-2.5">
      <div className="text-[9px] font-mono uppercase tracking-wider" style={{ color: `${color}80` }}>{label}</div>
      <div className="text-base font-bold font-mono" style={{ color }}>{value}</div>
    </div>
  )
}
