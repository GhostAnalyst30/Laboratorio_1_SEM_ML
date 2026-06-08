export interface ApartmentState {
  timestamp: number
  apartment_id: string
  tower: string
  floor: number
  apartment_number: number
  temperature: number
  humidity: number
  wind_speed: number
  rain: number
  solar_radiation: number
  air_quality: number
  pressure: number
  num_people_present: number
  occupancy_state: 'empty' | 'partial' | 'full'
  activity_type: string
  water_liters: number
  water_cost: number
  electricity_wh: number
  electricity_cost: number
  gas_m3: number
  gas_cost: number
  internet_gb: number
  internet_cost: number
  battery_charge: number
  solar_generation: number
  comfort_score: number
  sustainability_score: number
  scenario: string
}

export interface TowerInfo {
  id: string
  name: string
  floors: number
  apartments_per_floor: number
  total_apartments: number
}

export interface FloorInfo {
  floor: number
  apartments: string[]
}

export interface SimulationStatus {
  is_running: boolean
  is_paused: boolean
  virtual_minute: number
  scenario: string
  apartment_count: number
  speed_multiplier: number
}

export interface Scenario {
  name: string
  description: string
  duration_days: number
}

export interface ForecastPoint {
  timestamp: number
  predicted_value: number
  lower_bound: number
  upper_bound: number
}

export interface Recommendation {
  category: string
  priority: string
  title: string
  description: string
  potential_savings: string
  estimated_impact: number
}

export interface AnomalyPoint {
  timestamp: number
  actual_value: number
  expected_value: number
  anomaly_score: number
  severity: string
  description: string
}

export interface ClusterProfile {
  cluster_id: number
  label: string
  size: number
  avg_electricity_kwh: number
  avg_water_liters: number
  avg_gas_m3: number
  avg_sustainability: number
  description: string
}

export interface CommunitySummary {
  total_apartments: number
  total_towers: number
  total_records: number
  latest_electricity_wh: number
  latest_water_liters: number
  avg_comfort: number
  avg_sustainability: number
}

export interface SustainabilityMetrics {
  overall_score: number
  energy_score: number
  water_score: number
  community_score: number
  self_sufficiency: number
}

export interface WebSocketTick {
  type: 'tick'
  virtual_minute: number
  states: ApartmentState[]
}
