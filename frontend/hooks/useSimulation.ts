'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function useSimulationStatus() {
  return useQuery<any>({
    queryKey: ['simulation', 'status'],
    queryFn: api.simulationStatus,
    refetchInterval: 3000,
  })
}

export function useCommunitySummary() {
  return useQuery<any>({
    queryKey: ['community', 'summary'],
    queryFn: api.communitySummary,
    refetchInterval: 5000,
  })
}

export function useApartmentRealtime(id: string) {
  return useQuery<any>({
    queryKey: ['apartment', id, 'realtime'],
    queryFn: () => api.getApartmentRealtime(id),
    refetchInterval: 5000,
    enabled: !!id,
  })
}

export function useApartmentTimeseries(id: string, params?: string) {
  return useQuery<any>({
    queryKey: ['apartment', id, 'timeseries', params],
    queryFn: () => api.getApartmentTimeseries(id, params),
    enabled: !!id,
  })
}

export function useForecast(id: string, variable?: string) {
  return useQuery<any>({
    queryKey: ['analytics', 'forecast', id, variable],
    queryFn: () => api.forecast(id, variable),
    enabled: !!id,
  })
}

export function useAnomalies(id: string, variable?: string) {
  return useQuery<any>({
    queryKey: ['analytics', 'anomalies', id, variable],
    queryFn: () => api.anomalies(id, variable),
    enabled: !!id,
  })
}

export function useClusters(n?: number) {
  return useQuery<any>({
    queryKey: ['analytics', 'clusters', n],
    queryFn: () => api.clusters(n),
  })
}

export function useRecommendations(id: string) {
  return useQuery<any>({
    queryKey: ['analytics', 'recommendations', id],
    queryFn: () => api.recommendations(id),
    enabled: !!id,
  })
}

export function useStartSimulation() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (scenario?: string) => api.simulationStart(scenario),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['simulation'] })
    },
  })
}

export function usePauseSimulation() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: api.simulationPause,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['simulation'] }),
  })
}

export function useResumeSimulation() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: api.simulationResume,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['simulation'] }),
  })
}

export function useStopSimulation() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: api.simulationStop,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['simulation'] }),
  })
}
