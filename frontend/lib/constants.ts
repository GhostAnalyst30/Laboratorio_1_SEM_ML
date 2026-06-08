export const TOWERS = ['A', 'B'] as const

export const FLOORS_PER_TOWER = 4
export const APARTMENTS_PER_FLOOR = 4
export const TOTAL_APARTMENTS = TOWERS.length * FLOORS_PER_TOWER * APARTMENTS_PER_FLOOR

export const UTILITY_COLORS: Record<string, string> = {
  electricity_wh: '#6366f1',
  water_liters: '#22d3ee',
  gas_m3: '#f59e0b',
  internet_gb: '#a855f7',
  solar_generation: '#22c55e',
  temperature: '#ef4444',
  humidity: '#3b82f6',
}

export const UTILITY_LABELS: Record<string, string> = {
  electricity_wh: 'Electricity (Wh)',
  water_liters: 'Water (L)',
  gas_m3: 'Gas (m³)',
  internet_gb: 'Internet (GB)',
  solar_generation: 'Solar (Wh)',
  temperature: 'Temperature (°C)',
  humidity: 'Humidity (%)',
}

export const SCENARIO_LABELS: Record<string, string> = {
  baseline: 'Baseline',
  solar_panels: 'Solar Panels',
  battery_storage: 'Battery Storage',
  power_outages: 'Power Outages',
  water_restriction: 'Water Restriction',
  heat_wave: 'Heat Wave',
  price_increase: 'Price Increase',
}

export const ACTIVITY_EMOJIS: Record<string, string> = {
  sleeping: '🌙',
  waking: '☀️',
  morning_routine: '🚿',
  away: '🚶',
  working: '💻',
  studying: '📚',
  cooking: '🍳',
  eating: '🍽️',
  leisure: '📺',
  cleaning: '🧹',
  night_routine: '🌃',
  entertainment: '🎮',
}
