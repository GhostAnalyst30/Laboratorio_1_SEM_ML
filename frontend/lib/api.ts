import type {
  ApartmentState, TowerInfo, FloorInfo, SimulationStatus, Scenario,
  ForecastPoint, Recommendation, AnomalyPoint, ClusterProfile,
  CommunitySummary, SustainabilityMetrics,
} from './types'

const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function fetchJson<T>(url: string, opts?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    headers: { 'Content-Type': 'application/json', ...opts?.headers },
    ...opts,
  })
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`)
  return res.json()
}

export const api = {
  // Community
  communitySummary: () => fetchJson<CommunitySummary>('/api/community/summary'),
  communityTimeseries: (params?: string) => fetchJson(`/api/community/timeseries?${params || ''}`),
  communitySustainability: () => fetchJson<SustainabilityMetrics>('/api/community/sustainability'),
  communityEmergence: () => fetchJson('/api/community/emergence'),

  // Towers
  listTowers: () => fetchJson<{ towers: TowerInfo[] }>('/api/towers'),
  getTower: (id: string) => fetchJson(`/api/towers/${id}`),
  getTowerTimeseries: (id: string, params?: string) => fetchJson(`/api/towers/${id}/timeseries?${params || ''}`),
  getTowerFloors: (id: string) => fetchJson<{ tower: string; floors: FloorInfo[] }>(`/api/towers/${id}/floors`),

  // Apartments
  listApartments: (params?: string) => fetchJson(`/api/apartments?${params || ''}`),
  getApartment: (id: string) => fetchJson(`/api/apartments/${id}`),
  getApartmentTimeseries: (id: string, params?: string) => fetchJson(`/api/apartments/${id}/timeseries?${params || ''}`),
  getApartmentRealtime: (id: string) => fetchJson(`/api/apartments/${id}/realtime`),
  getApartmentHourly: (id: string) => fetchJson(`/api/apartments/${id}/hourly`),
  getApartmentDaily: (id: string) => fetchJson(`/api/apartments/${id}/daily`),

  // Simulation
  simulationStart: (scenario?: string) => fetchJson<{ status: string }>('/api/simulation/start', {
    method: 'POST',
    body: JSON.stringify({ scenario: scenario || 'baseline' }),
  }),
  simulationPause: () => fetchJson('/api/simulation/pause', { method: 'POST' }),
  simulationResume: () => fetchJson('/api/simulation/resume', { method: 'POST' }),
  simulationStop: () => fetchJson('/api/simulation/stop', { method: 'POST' }),
  simulationReset: () => fetchJson('/api/simulation/reset', { method: 'POST' }),
  simulationStatus: () => fetchJson<SimulationStatus>('/api/simulation/status'),
  listScenarios: () => fetchJson<{ scenarios: Scenario[] }>('/api/simulation/scenarios'),
  setSpeed: (speed: number) => fetchJson('/api/simulation/speed', {
    method: 'POST',
    body: JSON.stringify({ speed }),
  }),

  // Analytics
  forecast: (aptId: string, variable?: string, horizon?: number) =>
    fetchJson(`/api/analytics/forecast/${aptId}?variable=${variable || 'electricity_wh'}&horizon=${horizon || 72}`),
  anomalies: (aptId: string, variable?: string) =>
    fetchJson(`/api/analytics/anomalies/${aptId}?variable=${variable || 'electricity_wh'}`),
  clusters: (n?: number) => fetchJson(`/api/analytics/clusters?n_clusters=${n || 4}`),
  recommendations: (aptId: string) => fetchJson(`/api/analytics/recommendations/${aptId}`),
  insights: (aptId: string) => fetchJson(`/api/analytics/insights/${aptId}`),

  // Export
  exportUrl: (type: 'apartment' | 'tower' | 'community', id?: string, format?: string) => {
    if (type === 'apartment') return `${BASE}/api/export/apartment/${id}?format=${format || 'csv'}`
    if (type === 'tower') return `${BASE}/api/export/tower/${id}?format=${format || 'csv'}`
    return `${BASE}/api/export/community?format=${format || 'csv'}`
  },
}
