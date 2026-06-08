'use client'

import { motion } from 'framer-motion'
import { useSelectionStore } from '@/stores/selectionStore'
import { FLOORS_PER_TOWER } from '@/lib/constants'
import Floor2D from './Floor2D'

interface Props {
  towerId: string
  index: number
}

const TOWER_META: Record<string, { label: string; accent: string; desc: string }> = {
  A: {
    label: 'EFFICIENT',
    accent: '#22c55e',
    desc: 'Low consumption profile',
  },
  B: {
    label: 'HIGH CONSUMPTION',
    accent: '#ef4444',
    desc: 'High consumption profile',
  },
}

export default function Tower2D({ towerId, index }: Props) {
  const selectedTower = useSelectionStore((s) => s.selectedTower)
  const setSelectedTower = useSelectionStore((s) => s.setSelectedTower)
  const isSelected = selectedTower === towerId
  const meta = TOWER_META[towerId] || { label: towerId, accent: '#6366f1', desc: '' }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.15, ease: 'easeOut' }}
      onClick={() => setSelectedTower(towerId)}
      className="flex flex-col"
    >
      <div className="flex items-center gap-3 mb-3 px-1">
        <motion.div
          animate={{ scale: isSelected ? 1.05 : 1 }}
          transition={{ duration: 0.2 }}
          className="flex items-center gap-2"
        >
          <span className="text-sm font-bold font-mono tracking-[0.15em] text-white/90">
            TOWER {towerId}
          </span>
          <span
            className="text-[9px] font-mono tracking-[0.2em] px-1.5 py-0.5 rounded"
            style={{
              color: meta.accent,
              backgroundColor: `${meta.accent}15`,
              border: `1px solid ${meta.accent}25`,
            }}
          >
            {meta.label}
          </span>
        </motion.div>
      </div>

      <motion.div
        layout
        animate={{
          borderColor: isSelected
            ? `${meta.accent}50`
            : 'rgba(255,255,255,0.04)',
          boxShadow: isSelected
            ? `0 0 20px ${meta.accent}08`
            : 'none',
        }}
        transition={{ duration: 0.3 }}
        className="rounded-xl border bg-white/[0.02] overflow-hidden"
        style={{ borderWidth: 1 }}
      >
        <div className="px-3 py-3">
          <div className="flex flex-col gap-0.5">
            {Array.from({ length: FLOORS_PER_TOWER }, (_, i) => {
              const floorNum = FLOORS_PER_TOWER - i
              return (
                <Floor2D
                  key={floorNum}
                  towerId={towerId}
                  floorNumber={floorNum}
                  index={i}
                />
              )
            })}
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: isSelected ? 1 : 0.4 }}
        transition={{ duration: 0.3 }}
        className="mt-2 text-[9px] font-mono text-center tracking-wider"
        style={{ color: isSelected ? meta.accent : 'rgba(148,163,184,0.3)' }}
      >
        {meta.desc} · {FLOORS_PER_TOWER * 4} apts
      </motion.div>
    </motion.div>
  )
}
