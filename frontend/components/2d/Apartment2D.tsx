'use client'

import { motion } from 'framer-motion'
import { useSelectionStore } from '@/stores/selectionStore'
import { useUIStore } from '@/stores/uiStore'

interface Props {
  apartmentId: string
  floor: number
  towerId: string
  index: number
}

const COLORS = {
  default: '#1a1d2e',
  hover: '#2a2e45',
  selected: '#818cf8',
  border: '#3d4160',
  borderSelected: '#818cf8',
}

export default function Apartment2D({ apartmentId, towerId, floor, index }: Props) {
  const selectedApartment = useSelectionStore((s) => s.selectedApartment)
  const hoveredApartment = useSelectionStore((s) => s.hoveredApartment)
  const setSelectedApartment = useSelectionStore((s) => s.setSelectedApartment)
  const setHoveredApartment = useSelectionStore((s) => s.setHoveredApartment)
  const setActivePanel = useUIStore((s) => s.setActivePanel)

  const isSelected = selectedApartment === apartmentId
  const isHovered = hoveredApartment === apartmentId

  return (
    <motion.button
      onMouseEnter={() => setHoveredApartment(apartmentId)}
      onMouseLeave={() => setHoveredApartment(null)}
      onClick={(e) => {
        e.stopPropagation()
        setSelectedApartment(apartmentId)
        setActivePanel('info')
      }}
      layout
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{
        opacity: 1,
        scale: 1,
        backgroundColor: isSelected ? COLORS.selected : isHovered ? COLORS.hover : COLORS.default,
        borderColor: isSelected ? COLORS.borderSelected : COLORS.border,
      }}
      transition={{ duration: 0.15 }}
      whileHover={{ scale: 1.08 }}
      whileTap={{ scale: 0.95 }}
      className="relative flex items-center justify-center rounded border cursor-pointer"
      style={{
        width: '100%',
        aspectRatio: '1.3 / 1',
        borderWidth: 1,
      }}
    >
      <motion.span
        className="text-[8px] font-mono select-none"
        animate={{ color: isSelected ? '#ffffff' : isHovered ? '#e2e8f0' : '#475569' }}
        transition={{ duration: 0.15 }}
      >
        {(index + 1).toString().padStart(2, '0')}
      </motion.span>

      {isSelected && (
        <motion.div
          layoutId="selected-glow"
          className="absolute inset-0 rounded"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          style={{
            boxShadow: 'inset 0 0 12px rgba(129,140,248,0.3), 0 0 8px rgba(129,140,248,0.2)',
          }}
        />
      )}
    </motion.button>
  )
}
