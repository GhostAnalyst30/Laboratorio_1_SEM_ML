'use client'

import { motion } from 'framer-motion'
import { useSelectionStore } from '@/stores/selectionStore'
import { APARTMENTS_PER_FLOOR } from '@/lib/constants'
import Apartment2D from './Apartment2D'

interface Props {
  towerId: string
  floorNumber: number
  index: number
}

export default function Floor2D({ towerId, floorNumber, index }: Props) {
  const selectedFloor = useSelectionStore((s) => s.selectedFloor)
  const selectedTower = useSelectionStore((s) => s.selectedTower)
  const setSelectedFloor = useSelectionStore((s) => s.setSelectedFloor)

  const isHighlighted = selectedTower === towerId && selectedFloor === floorNumber

  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: -20 }}
      animate={{
        opacity: 1,
        x: 0,
        backgroundColor: isHighlighted ? 'rgba(99,102,241,0.08)' : 'transparent',
      }}
      transition={{ duration: 0.3, delay: index * 0.08 }}
      onClick={() => setSelectedFloor(floorNumber)}
      className="relative cursor-pointer rounded-lg px-1.5 py-1.5"
      style={{
        border: isHighlighted ? '1px solid rgba(99,102,241,0.25)' : '1px solid transparent',
      }}
    >
      <div className="flex items-center gap-2">
        <motion.span
          className="text-[9px] font-mono select-none shrink-0 w-4 text-right"
          animate={{ color: isHighlighted ? 'rgba(129,140,248,0.6)' : 'rgba(148,163,184,0.25)' }}
          transition={{ duration: 0.2 }}
        >
          {floorNumber}
        </motion.span>

        <div className="flex-1 grid gap-1"
          style={{
            gridTemplateColumns: `repeat(${APARTMENTS_PER_FLOOR}, 1fr)`,
          }}
        >
          {Array.from({ length: APARTMENTS_PER_FLOOR }, (_, i) => {
            const aptId = `${towerId}${floorNumber}-${i + 1}`
            return (
              <Apartment2D
                key={aptId}
                apartmentId={aptId}
                towerId={towerId}
                floor={floorNumber}
                index={i}
              />
            )
          })}
        </div>
      </div>
    </motion.div>
  )
}
