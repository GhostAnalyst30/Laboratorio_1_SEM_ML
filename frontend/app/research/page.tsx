'use client'

import { TOWERS, FLOORS_PER_TOWER, APARTMENTS_PER_FLOOR, TOTAL_APARTMENTS, SCENARIO_LABELS } from '@/lib/constants'

export default function ResearchPage() {
  return (
    <div className="min-h-screen bg-[#0f172a] p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold font-mono text-white">Research Portal</h1>
            <p className="text-sm text-[#94a3b8] font-mono">Digital Twin Dataset Specification</p>
          </div>
          <a href="/" className="text-sm text-[#6366f1] hover:text-[#818cf8] font-mono">
            ← Back
          </a>
        </div>

        {/* Dataset Spec */}
        <div className="bg-[#1e293b] rounded-xl p-6 mb-6">
          <h2 className="text-sm font-mono text-[#6366f1] mb-4">Dataset Overview</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {[
              ['Total Apartments', String(TOTAL_APARTMENTS)],
              ['Towers', String(TOWERS.length)],
              ['Floors', String(FLOORS_PER_TOWER)],
              ['Apts/Floor', String(APARTMENTS_PER_FLOOR)],
              ['Variables', '36 per record'],
              ['Resolution', '1 minute'],
              ['Days/Month', '30'],
              ['Records/Month', '1.38M'],
            ].map(([label, val]) => (
              <div key={label} className="bg-[#0f172a] rounded-lg p-3">
                <div className="text-[10px] text-[#64748b] font-mono">{label}</div>
                <div className="text-lg font-bold font-mono text-white">{val}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Variables */}
        <div className="bg-[#1e293b] rounded-xl p-6 mb-6">
          <h2 className="text-sm font-mono text-[#6366f1] mb-4">Generated Variables (36 per record)</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-xs font-mono">
            {[
              'timestamp', 'apartment_id', 'tower', 'floor', 'apartment_number',
              'temperature', 'humidity', 'wind_speed', 'rain', 'solar_radiation',
              'air_quality', 'pressure', 'num_people_present', 'occupancy_state',
              'activity_type', 'water_liters', 'water_cost', 'electricity_wh',
              'electricity_cost', 'gas_m3', 'gas_cost', 'internet_gb', 'internet_cost',
              'battery_charge', 'solar_generation', 'comfort_score',
              'sustainability_score', 'scenario',
            ].map((v) => (
              <div key={v} className="bg-[#0f172a] rounded px-2 py-1.5 text-[#94a3b8]">
                {v}
              </div>
            ))}
          </div>
        </div>

        {/* Scenarios */}
        <div className="bg-[#1e293b] rounded-xl p-6 mb-6">
          <h2 className="text-sm font-mono text-[#6366f1] mb-4">Experimental Scenarios</h2>
          <div className="space-y-3">
            {Object.entries(SCENARIO_LABELS).map(([key, label], i) => (
              <div key={key} className="bg-[#0f172a] rounded-lg p-3 flex items-start gap-3">
                <div className="text-[#6366f1] font-bold font-mono w-6">M{i + 1}</div>
                <div>
                  <div className="text-sm text-white font-mono">{label}</div>
                  <div className="text-xs text-[#64748b] font-mono mt-0.5">
                    {key === 'baseline' && 'Baseline behavior, normal conditions'}
                    {key === 'solar_panels' && 'Solar panels installed, grid reduction measured'}
                    {key === 'battery_storage' && 'Battery + solar, self-sufficiency measured'}
                    {key === 'power_outages' && 'Scheduled outages, resilience measured'}
                    {key === 'water_restriction' && '70% water supply, adaptation measured'}
                    {key === 'heat_wave' && '+8°C heat wave, cooling demand measured'}
                    {key === 'price_increase' && '3x utility prices, elasticity measured'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Data Generation Engine */}
        <div className="bg-[#1e293b] rounded-xl p-6">
          <h2 className="text-sm font-mono text-[#6366f1] mb-4">Data Generation Engine</h2>
          <div className="space-y-2 text-xs text-[#94a3b8] font-mono">
            <p>• <span className="text-white">Multi-Agent System</span> with 1 Environment Agent + 168 Apartment Agents</p>
            <p>• <span className="text-white">Environment Agent</span>: Fourier components, Perlin noise, Markov weather chains</p>
            <p>• <span className="text-white">Apartment Agents</span>: Family profiles, activity state machines, appliance models</p>
            <p>• <span className="text-white">Memory Module</span>: Agents adapt behavior based on past bills and comfort</p>
            <p>• <span className="text-white">Emergence</span>: Towers naturally differentiate into efficiency archetypes</p>
            <p>• <span className="text-white">Storage</span>: Apache Parquet with Hive partitioning (Snappy compression)</p>
            <p>• <span className="text-white">Analytics</span>: Forecasting, anomaly detection, clustering, recommendations</p>
          </div>
        </div>
      </div>
    </div>
  )
}
