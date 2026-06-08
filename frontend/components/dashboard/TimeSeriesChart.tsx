'use client'

import { useMemo } from 'react'
import type { ForecastPoint } from '@/lib/types'

interface TimeSeriesChartProps {
  title: string
  data: ForecastPoint[]
  color?: string
}

export default function TimeSeriesChart({ title, data, color = '#6366f1' }: TimeSeriesChartProps) {
  const maxVal = useMemo(() => Math.max(...data.map(d => d.upper_bound), 1), [data])
  const minVal = useMemo(() => Math.min(...data.map(d => d.lower_bound), 0), [data])
  const range = maxVal - minVal || 1
  const width = 320
  const height = 140
  const pad = { top: 15, right: 15, bottom: 25, left: 40 }
  const plotW = width - pad.left - pad.right
  const plotH = height - pad.top - pad.bottom

  const points = useMemo(() => {
    if (data.length === 0) return ''
    return data.map((d, i) => {
      const x = pad.left + (i / (data.length - 1 || 1)) * plotW
      const y = pad.top + plotH - ((d.predicted_value - minVal) / range) * plotH
      return `${x},${y}`
    }).join(' ')
  }, [data, plotW, plotH, minVal, range])

  const upperPoints = useMemo(() => {
    if (data.length === 0) return ''
    return data.map((d, i) => {
      const x = pad.left + (i / (data.length - 1 || 1)) * plotW
      const y = pad.top + plotH - ((d.upper_bound - minVal) / range) * plotH
      return `${x},${y}`
    }).join(' ')
  }, [data, plotW, plotH, minVal, range])

  const lowerPoints = useMemo(() => {
    if (data.length === 0) return ''
    return data.map((d, i) => {
      const x = pad.left + (i / (data.length - 1 || 1)) * plotW
      const y = pad.top + plotH - ((d.lower_bound - minVal) / range) * plotH
      return `${x},${y}`
    }).join(' ')
  }, [data, plotW, plotH, minVal, range])

  const areaPath = useMemo(() => {
    if (!upperPoints || !lowerPoints) return ''
    const upper = upperPoints.split(' ')
    const lower = lowerPoints.split(' ').reverse()
    return upper.join(' ') + ' ' + lower.join(' ')
  }, [upperPoints, lowerPoints])

  return (
    <div className="bg-[#1e293b] rounded-lg p-3">
      <div className="text-xs font-mono text-[#94a3b8] mb-2">{title}</div>
      <svg width={width} height={height} className="w-full">
        {/* Grid */}
        {[0, 0.25, 0.5, 0.75, 1].map((frac) => {
          const y = pad.top + plotH * (1 - frac)
          return (
            <g key={frac}>
              <line
                x1={pad.left} y1={y} x2={pad.left + plotW} y2={y}
                stroke="#334155" strokeWidth={0.5}
              />
              <text x={pad.left - 4} y={y + 3} textAnchor="end" fill="#64748b" fontSize={8} fontFamily="monospace">
                {(minVal + range * frac).toFixed(0)}
              </text>
            </g>
          )
        })}

        {/* Confidence band */}
        {areaPath && (
          <polygon
            points={areaPath}
            fill={color}
            fillOpacity={0.1}
          />
        )}

        {/* Prediction line */}
        {points && (
          <polyline
            points={points}
            fill="none"
            stroke={color}
            strokeWidth={1.5}
          />
        )}

        {/* Axes */}
        <line x1={pad.left} y1={pad.top} x2={pad.left} y2={pad.top + plotH} stroke="#334155" strokeWidth={1} />
        <line x1={pad.left} y1={pad.top + plotH} x2={pad.left + plotW} y2={pad.top + plotH} stroke="#334155" strokeWidth={1} />
      </svg>
    </div>
  )
}
