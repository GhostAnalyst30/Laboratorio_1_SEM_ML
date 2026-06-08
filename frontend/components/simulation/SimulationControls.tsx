'use client'

import { useState } from 'react'
import { useSimulationStore } from '@/stores/simulationStore'
import { useStartSimulation, usePauseSimulation, useResumeSimulation, useStopSimulation } from '@/hooks/useSimulation'
import { api } from '@/lib/api'
import { useQuery } from '@tanstack/react-query'
import { SCENARIO_LABELS } from '@/lib/constants'
import { Play, Pause, Square, ChevronDown } from 'lucide-react'

export default function SimulationControls() {
  const { status, setStatus, scenario, setScenario, speedMultiplier, setSpeedMultiplier } = useSimulationStore()
  const [showScenarios, setShowScenarios] = useState(false)

  const startSim = useStartSimulation()
  const pauseSim = usePauseSimulation()
  const resumeSim = useResumeSimulation()
  const stopSim = useStopSimulation()

  const { data: scenariosData } = useQuery({
    queryKey: ['scenarios'],
    queryFn: api.listScenarios,
  })

  const handleStart = () => {
    startSim.mutate(scenario, { onSuccess: () => setStatus('running') })
  }
  const handlePause = () => {
    pauseSim.mutate(undefined, { onSuccess: () => setStatus('paused') })
  }
  const handleResume = () => {
    resumeSim.mutate(undefined, { onSuccess: () => setStatus('running') })
  }
  const handleStop = () => {
    stopSim.mutate(undefined, { onSuccess: () => setStatus('idle') })
  }

  return (
    <div className="fixed bottom-5 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 bg-[#0c0e1a]/90 backdrop-blur-md border border-white/[0.06] rounded-lg px-3 py-2">
      {status === 'idle' && (
        <button onClick={handleStart}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 text-[11px] font-mono rounded transition-all"
        >
          <Play size={12} /> START
        </button>
      )}
      {status === 'running' && (
        <button onClick={handlePause}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-yellow-500/20 hover:bg-yellow-500/30 text-yellow-300 text-[11px] font-mono rounded transition-all"
        >
          <Pause size={12} /> PAUSE
        </button>
      )}
      {status === 'paused' && (
        <>
          <button onClick={handleResume}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-green-500/20 hover:bg-green-500/30 text-green-300 text-[11px] font-mono rounded transition-all"
          >
            <Play size={12} /> RESUME
          </button>
          <button onClick={handleStop}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-red-500/20 hover:bg-red-500/30 text-red-300 text-[11px] font-mono rounded transition-all"
          >
            <Square size={12} /> STOP
          </button>
        </>
      )}

      <div className="w-px h-4 bg-white/[0.06]" />

      <div className="relative">
        <button onClick={() => setShowScenarios(!showScenarios)}
          className="flex items-center gap-1.5 px-2.5 py-1.5 text-[11px] font-mono text-white/50 hover:text-white/80 transition-colors"
        >
          {SCENARIO_LABELS[scenario] || scenario}
          <ChevronDown size={10} />
        </button>
        {showScenarios && (
          <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-[#0c0e1a]/95 border border-white/[0.06] rounded-lg py-1 min-w-[140px] shadow-xl backdrop-blur-md">
            {(scenariosData?.scenarios || []).map((s: any) => (
              <button key={s.name} onClick={() => { setScenario(s.name); setShowScenarios(false) }}
                className={`block w-full text-left px-3 py-1.5 text-[11px] font-mono transition-colors ${
                  scenario === s.name ? 'text-indigo-300 bg-indigo-500/10' : 'text-white/40 hover:text-white/70'
                }`}
              >
                {SCENARIO_LABELS[s.name] || s.name}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="w-px h-4 bg-white/[0.06]" />

      <div className="flex items-center gap-1.5">
        <button onClick={() => setSpeedMultiplier(Math.max(0.5, speedMultiplier - 0.5))}
          className="text-white/30 hover:text-white/70 text-xs px-1"
        >−</button>
        <span className="text-[11px] font-mono text-white/50 min-w-[2.5ch] text-center">{speedMultiplier}x</span>
        <button onClick={() => setSpeedMultiplier(Math.min(5, speedMultiplier + 0.5))}
          className="text-white/30 hover:text-white/70 text-xs px-1"
        >+</button>
      </div>
    </div>
  )
}
