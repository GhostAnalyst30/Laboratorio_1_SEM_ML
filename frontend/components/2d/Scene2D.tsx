'use client'

import { motion } from 'framer-motion'
import Community2D from './Community2D'

export default function Scene2D() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="w-full h-full flex items-center justify-center overflow-auto"
    >
      <div className="py-8 md:py-12 w-full">
        <Community2D />
      </div>
    </motion.div>
  )
}
