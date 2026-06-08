import { create } from 'zustand'

interface UIStore {
  sidebarOpen: boolean
  activePanel: 'info' | 'charts' | 'analytics' | 'family' | 'none'
  theme: 'dark'
  setSidebarOpen: (o: boolean) => void
  setActivePanel: (p: UIStore['activePanel']) => void
  toggleSidebar: () => void
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: false,
  activePanel: 'none',
  theme: 'dark',
  setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
  setActivePanel: (activePanel) => set({ activePanel, sidebarOpen: true }),
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}))
