'use client'

import { motion } from 'framer-motion'
import { TOWERS } from '@/lib/constants'
import Tower2D from './Tower2D'

export default function Community2D() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="w-full max-w-4xl mx-auto px-4"
    >
      <div className="flex items-start justify-center gap-8 md:gap-16">
        {TOWERS.map((id, i) => (
          <div key={id} className="flex-1 min-w-0 max-w-sm">
            <Tower2D towerId={id} index={i} />
          </div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.6 }}
        className="mt-8 text-center"
      >
        <div className="inline-flex items-center gap-4 px-4 py-2 rounded-full bg-white/[0.02] border border-white/[0.04]">
          <div className="flex items-center gap-1.5 text-[9px] font-mono text-white/30 tracking-wider">
            <span className="w-2 h-2 rounded-full bg-green-500/50" />
            EFFICIENT
          </div>
          <div className="w-px h-3 bg-white/[0.06]" />
          <div className="flex items-center gap-1.5 text-[9px] font-mono text-white/30 tracking-wider">
            <span className="w-2 h-2 rounded-full bg-red-500/50" />
            HIGH CONSUMPTION
          </div>
          <div className="w-px h-3 bg-white/[0.06]" />
          <span className="text-[9px] font-mono text-white/20">
            {TOWERS.length * 4} FLOORS · {TOWERS.length * 16} APARTMENTS
          </span>
        </div>
      </motion.div>
    </motion.div>
  )
}
