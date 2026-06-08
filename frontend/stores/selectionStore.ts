import { create } from 'zustand'

interface SelectionStore {
  selectedTower: string | null
  selectedFloor: number | null
  selectedApartment: string | null
  hoveredApartment: string | null
  setSelectedTower: (t: string | null) => void
  setSelectedFloor: (f: number | null) => void
  setSelectedApartment: (a: string | null) => void
  setHoveredApartment: (a: string | null) => void
  clearSelection: () => void
}

export const useSelectionStore = create<SelectionStore>((set) => ({
  selectedTower: null,
  selectedFloor: null,
  selectedApartment: null,
  hoveredApartment: null,
  setSelectedTower: (selectedTower) => set({ selectedTower, selectedFloor: null, selectedApartment: null }),
  setSelectedFloor: (selectedFloor) => set({ selectedFloor, selectedApartment: null }),
  setSelectedApartment: (selectedApartment) => set({ selectedApartment }),
  setHoveredApartment: (hoveredApartment) => set({ hoveredApartment }),
  clearSelection: () => set({ selectedTower: null, selectedFloor: null, selectedApartment: null }),
}))
