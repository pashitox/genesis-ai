import { ReactNode } from 'react'
import './globals.css'

export const metadata = {
  title: 'GENESIS AI — Autonomous Chat Engine',
  description: 'Self-Improving AI System with Multi-Agent Architecture',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es">
      <body className="min-h-screen bg-dark-900 text-white font-sans">
        {children}
      </body>
    </html>
  )
}