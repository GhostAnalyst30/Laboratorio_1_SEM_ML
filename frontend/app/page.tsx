'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import Header from '@/components/ui/Header'
import SimulationControls from '@/components/simulation/SimulationControls'
import SidePanel from '@/components/dashboard/SidePanel'
import CommunityOverview from '@/components/dashboard/CommunityOverview'
import Scene2D from '@/components/2d/Scene2D'
import { useSelectionStore } from '@/stores/selectionStore'
import { useUIStore } from '@/stores/uiStore'
import { Layers, Eye, Info, RotateCcw } from 'lucide-react'

const queryClient = new QueryClient()

function HomeContent() {
  const [showOverview, setShowOverview] = useState(true)
  const selectedApartment = useSelectionStore((s) => s.selectedApartment)
  const setSidebarOpen = useUIStore((s) => s.setSidebarOpen)
  const sidebarOpen = useUIStore((s) => s.sidebarOpen)
  const clearSelection = useSelectionStore((s) => s.clearSelection)

  return (
    <div className="relative w-full h-[100dvh] overflow-hidden bg-[#0c0e1a]">
      <Header />

      <main className="absolute inset-0 top-12 bottom-14 overflow-y-auto">
        <Scene2D />
      </main>

      {/* Left toolstrip */}
      <motion.div
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3, delay: 0.8 }}
        className="fixed left-3 top-1/2 -translate-y-1/2 z-30 flex flex-col gap-1.5"
      >
        <button
          onClick={() => setShowOverview(!showOverview)}
          className={`p-2 rounded-lg border transition-all ${
            showOverview
              ? 'bg-indigo-500/20 border-indigo-500/30 text-indigo-300'
              : 'bg-white/[0.03] border-white/[0.04] text-white/30 hover:text-white/60'
          }`}
        >
          <Layers size={14} />
        </button>
        <button
          onClick={() => {
            if (selectedApartment) {
              setSidebarOpen(!sidebarOpen)
            }
          }}
          className={`p-2 rounded-lg border transition-all ${
            sidebarOpen && selectedApartment
              ? 'bg-indigo-500/20 border-indigo-500/30 text-indigo-300'
              : 'bg-white/[0.03] border-white/[0.04] text-white/30 hover:text-white/60'
          }`}
        >
          <Eye size={14} />
        </button>
        <button
          onClick={clearSelection}
          className="p-2 rounded-lg border border-white/[0.04] bg-white/[0.03] text-white/30 hover:text-white/60 transition-all"
        >
          <RotateCcw size={14} />
        </button>
      </motion.div>

      <AnimatePresence>
        {showOverview && (
          <motion.div
            initial={{ opacity: 0, x: -20, scale: 0.95 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: -20, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="fixed left-12 top-16 z-30 w-72"
          >
            <CommunityOverview />
          </motion.div>
        )}
      </AnimatePresence>

      <SidePanel />
      <SimulationControls />

      {/* Bottom hint */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 1.2 }}
        className="fixed bottom-20 left-1/2 -translate-x-1/2 z-40"
      >
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/[0.02] border border-white/[0.04] text-[9px] font-mono text-white/20 tracking-wider">
          <Info size={10} />
          Click an apartment to view real-time data
        </div>
      </motion.div>
    </div>
  )
}

export default function Home() {
  return (
    <QueryClientProvider client={queryClient}>
      <HomeContent />
    </QueryClientProvider>
  )
}
