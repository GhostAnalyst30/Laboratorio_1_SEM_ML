import type { Metadata } from 'next'
import '@/styles/globals.css'

export const metadata: Metadata = {
  title: 'LAB-SEM-ML | Digital Twin Smart Community',
  description: 'Synthetic Multi-Variable Time-Series Generation and AI-Driven Energy Analytics for Smart Residential Communities',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
