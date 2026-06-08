'use client'

import { useSimulationStore } from '@/stores/simulationStore'
import { useCommunitySummary } from '@/hooks/useSimulation'
import { useSelectionStore } from '@/stores/selectionStore'
import { useUIStore } from '@/stores/uiStore'
import { TOTAL_APARTMENTS, TOWERS } from '@/lib/constants'
import { LayoutGrid, Download, Eye } from 'lucide-react'

export default function Header() {
  const { virtualTime, status } = useSimulationStore()
  const setActivePanel = useUIStore((s) => s.setActivePanel)
  const clearSelection = useSelectionStore((s) => s.clearSelection)

  const timeStr = `${String(Math.floor(virtualTime.minute_of_day / 60)).padStart(2, '0')}:${String(virtualTime.minute_of_day % 60).padStart(2, '0')}`
  const dateStr = `${virtualTime.year}-${String(virtualTime.month).padStart(2, '0')}-${String(virtualTime.day_of_month).padStart(2, '0')}`

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-12 bg-[#0c0e1a]/80 backdrop-blur-md border-b border-white/[0.04] flex items-center justify-between px-5">
      <div className="flex items-center gap-3">
        <div className="text-indigo-400 font-bold font-mono text-sm tracking-[0.2em]">
          LAB-SEM-ML
        </div>
        <div className="h-3 w-px bg-white/[0.06]" />
        <div className="text-white/30 text-[10px] font-mono tracking-wider hidden sm:block">
          DIGITAL TWIN · {TOWERS.length} TOWERS · {TOTAL_APARTMENTS} APARTMENTS
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-[11px] font-mono">
          <span className="text-white/40">{dateStr}</span>
          <span className="text-white/80 font-semibold">{timeStr}</span>
          <span className={`inline-block w-1.5 h-1.5 rounded-full ${
            status === 'running' ? 'bg-green-400 shadow-[0_0_6px_rgba(34,197,94,0.5)]' :
            status === 'paused' ? 'bg-yellow-400' : 'bg-white/20'
          }`} />
        </div>

        <nav className="flex items-center gap-1">
          <button
            onClick={() => { clearSelection(); setActivePanel('none') }}
            className="px-2.5 py-1.5 text-[11px] font-mono text-white/40 hover:text-white/80 transition-colors"
          >
            <Eye size={14} className="inline mr-1.5" />
            2D
          </button>
          <a
            href="/dashboard"
            className="px-2.5 py-1.5 text-[11px] font-mono text-white/40 hover:text-white/80 transition-colors"
          >
            <LayoutGrid size={14} className="inline mr-1.5" />
            Dashboard
          </a>
          <a
            href="/export"
            className="px-2.5 py-1.5 text-[11px] font-mono text-white/40 hover:text-white/80 transition-colors"
          >
            <Download size={14} className="inline mr-1.5" />
            Export
          </a>
        </nav>
      </div>
    </header>
  )
}
