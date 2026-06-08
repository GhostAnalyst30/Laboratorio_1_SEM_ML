'use client'

import { useState } from 'react'
import { api } from '@/lib/api'
import { TOWERS } from '@/lib/constants'
import { Download } from 'lucide-react'

export default function ExportPage() {
  const [type, setType] = useState<'apartment' | 'tower' | 'community'>('apartment')
  const [apartmentId, setApartmentId] = useState('A1-1')
  const [towerId, setTowerId] = useState('A')
  const [format, setFormat] = useState<'csv' | 'json' | 'parquet'>('csv')

  const towers = TOWERS

  const getUrl = () => {
    if (type === 'apartment') return api.exportUrl('apartment', apartmentId, format)
    if (type === 'tower') return api.exportUrl('tower', towerId, format)
    return api.exportUrl('community', undefined, format)
  }

  return (
    <div className="min-h-screen bg-[#0f172a] p-8">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold font-mono text-white">Dataset Export</h1>
            <p className="text-sm text-[#94a3b8] font-mono">Download generated synthetic data for research</p>
          </div>
          <a href="/" className="text-sm text-[#6366f1] hover:text-[#818cf8] font-mono">
            ← Back
          </a>
        </div>

        <div className="bg-[#1e293b] rounded-xl p-6 space-y-6">
          {/* Export Type */}
          <div>
            <label className="block text-xs font-mono text-[#94a3b8] mb-2">Export Type</label>
            <div className="flex gap-2">
              {(['apartment', 'tower', 'community'] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => setType(t)}
                  className={`px-4 py-2 text-sm font-mono rounded-lg transition-colors ${
                    type === t
                      ? 'bg-[#6366f1] text-white'
                      : 'bg-[#0f172a] text-[#94a3b8] hover:text-white'
                  }`}
                >
                  {t.charAt(0).toUpperCase() + t.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Apartment/Tower Selection */}
          {type === 'apartment' && (
            <div>
              <label className="block text-xs font-mono text-[#94a3b8] mb-2">Apartment ID</label>
              <input
                type="text"
                value={apartmentId}
                onChange={(e) => setApartmentId(e.target.value.toUpperCase())}
                placeholder="e.g., A2-3"
                className="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white font-mono text-sm focus:outline-none focus:border-[#6366f1]"
              />
              <div className="mt-2 flex flex-wrap gap-1.5">
                {['A1-1', 'B3-2', 'C5-4', 'D2-1', 'E7-3', 'F4-2'].map((ex) => (
                  <button
                    key={ex}
                    onClick={() => setApartmentId(ex)}
                    className="text-xs text-[#64748b] hover:text-white font-mono px-1.5 py-0.5 bg-[#0f172a] rounded"
                  >
                    {ex}
                  </button>
                ))}
              </div>
            </div>
          )}

          {type === 'tower' && (
            <div>
              <label className="block text-xs font-mono text-[#94a3b8] mb-2">Tower</label>
              <div className="flex gap-2">
                {towers.map((t) => (
                  <button
                    key={t}
                    onClick={() => setTowerId(t)}
                    className={`px-4 py-2 text-sm font-mono rounded-lg transition-colors ${
                      towerId === t
                        ? 'bg-[#6366f1] text-white'
                        : 'bg-[#0f172a] text-[#94a3b8] hover:text-white'
                    }`}
                  >
                    Tower {t}
                  </button>
                ))}
              </div>
            </div>
          )}

          {type === 'community' && (
            <div className="bg-[#0f172a] rounded-lg p-4">
              <p className="text-sm text-[#94a3b8] font-mono">
                Download data for both towers, 4 floors, 32 apartments.
              </p>
              <p className="text-xs text-[#64748b] font-mono mt-1">
                A full month generates ~1.38M records
              </p>
            </div>
          )}

          {/* Format */}
          <div>
            <label className="block text-xs font-mono text-[#94a3b8] mb-2">Format</label>
            <div className="flex gap-2">
              {(['csv', 'json', 'parquet'] as const).map((f) => (
                <button
                  key={f}
                  onClick={() => setFormat(f)}
                  className={`px-4 py-2 text-sm font-mono rounded-lg transition-colors ${
                    format === f
                      ? 'bg-[#6366f1] text-white'
                      : 'bg-[#0f172a] text-[#94a3b8] hover:text-white'
                  }`}
                >
                  .{f}
                </button>
              ))}
            </div>
          </div>

          {/* Download */}
          <a
            href={getUrl()}
            className="flex items-center justify-center gap-2 w-full py-3 bg-[#6366f1] hover:bg-[#4f46e5] text-white font-mono text-sm rounded-lg transition-colors"
          >
            <Download size={16} />
            Download Dataset
          </a>
        </div>

        <div className="mt-6 bg-[#1e293b] rounded-xl p-4">
          <h3 className="text-xs font-mono text-[#94a3b8] mb-2">Research Notes</h3>
          <ul className="text-xs text-[#64748b] font-mono space-y-1">
            <li>• Data generated by Multi-Agent System simulation</li>
            <li>• Each record contains 36 variables per apartment per minute</li>
            <li>• Variables are physically coherent (activity-driven, not random)</li>
            <li>• Parquet format uses Snappy compression</li>
            <li>• Suitable for AI training, forecasting, anomaly detection research</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
