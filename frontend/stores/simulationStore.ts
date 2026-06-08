import { create } from 'zustand'

interface VirtualTime {
  virtual_minute: number
  minute_of_day: number
  day_of_month: number
  day_of_week: number
  month: number
  year: number
}

interface SimulationStore {
  status: 'idle' | 'running' | 'paused'
  virtualTime: VirtualTime
  scenario: string
  speedMultiplier: number
  setStatus: (s: 'idle' | 'running' | 'paused') => void
  setVirtualTime: (t: Partial<VirtualTime>) => void
  setScenario: (s: string) => void
  setSpeedMultiplier: (s: number) => void
  advanceOneMinute: () => void
}

export const useSimulationStore = create<SimulationStore>((set, get) => ({
  status: 'idle',
  virtualTime: {
    virtual_minute: 0,
    minute_of_day: 0,
    day_of_month: 1,
    day_of_week: 0,
    month: 1,
    year: 2026,
  },
  scenario: 'baseline',
  speedMultiplier: 1.0,

  setStatus: (status) => set({ status }),
  setVirtualTime: (t) => set((s) => ({ virtualTime: { ...s.virtualTime, ...t } })),
  setScenario: (scenario) => set({ scenario }),
  setSpeedMultiplier: (speedMultiplier) => set({ speedMultiplier }),

  advanceOneMinute: () => {
    const { virtualTime } = get()
    const newVM = virtualTime.virtual_minute + 1
    const newMOD = (virtualTime.minute_of_day + 1) % 1440
    let newDOM = virtualTime.day_of_month
    let newDOW = virtualTime.day_of_week
    let newMonth = virtualTime.month
    let newYear = virtualTime.year

    if (newMOD === 0) {
      newDOM += 1
      newDOW = (virtualTime.day_of_week + 1) % 7
      if (newDOM > 30) {
        newDOM = 1
        newMonth += 1
        if (newMonth > 12) {
          newMonth = 1
          newYear += 1
        }
      }
    }

    set({
      virtualTime: {
        virtual_minute: newVM,
        minute_of_day: newMOD,
        day_of_month: newDOM,
        day_of_week: newDOW,
        month: newMonth,
        year: newYear,
      },
    })
  },
}))
