'use client'

import { useEffect, useRef, useCallback } from 'react'
import type { WebSocketTick } from '@/lib/types'

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'

export function useWebSocket(onTick: (data: WebSocketTick) => void) {
  const wsRef = useRef<WebSocket | null>(null)
  const cbRef = useRef(onTick)
  cbRef.current = onTick

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return

    const ws = new WebSocket(`${WS_URL}/api/simulation/stream`)
    wsRef.current = ws

    ws.onopen = () => console.log('[WS] Connected')

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as WebSocketTick
        cbRef.current(data)
      } catch { }
    }

    ws.onclose = () => {
      console.log('[WS] Disconnected, reconnecting in 3s...')
      setTimeout(connect, 3000)
    }

    ws.onerror = () => ws.close()
  }, [])

  useEffect(() => {
    connect()
    return () => {
      wsRef.current?.close()
      wsRef.current = null
    }
  }, [connect])

  return wsRef
}
