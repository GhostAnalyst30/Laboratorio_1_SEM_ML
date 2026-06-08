'use client'

import { useParams } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export default function TowerPage() {
  const { towerId } = useParams()
  const { data: tower } = useQuery<any>({
    queryKey: ['tower', towerId],
    queryFn: () => api.getTower(towerId as string),
  })

  return (
    <div className="min-h-screen bg-[#0f172a] p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold font-mono text-white mb-6">Tower {towerId}</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {tower?.floors?.map((floor: any) => (
            <div key={floor.floor} className="bg-[#1e293b] rounded-lg p-4">
              <div className="text-sm font-mono text-[#6366f1] mb-2">Floor {floor.floor}</div>
              <div className="flex flex-wrap gap-1.5">
                {floor.apartments.map((apt: string) => (
                  <a
                    key={apt}
                    href={`/apartments/${apt}`}
                    className="px-2 py-1 text-xs font-mono text-[#94a3b8] bg-[#0f172a] rounded hover:bg-[#6366f1] hover:text-white transition-colors"
                  >
                    {apt}
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>

        <a href="/" className="inline-block mt-6 text-sm text-[#6366f1] hover:text-[#818cf8] font-mono">
          ← Back to Community
        </a>
      </div>
    </div>
  )
}
