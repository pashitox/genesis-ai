'use client'

export default function SystemStatus() {
  return (
    <div className="flex items-center space-x-6 text-sm">
      <div className="flex items-center space-x-2">
        <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
        <span className="text-gray-300">System Online</span>
      </div>
      <div className="hidden md:flex items-center space-x-4">
        <div className="text-gray-400">Multi-Agent</div>
        <div className="text-gray-400">RAG Enabled</div>
        <div className="text-gray-400">Auto-Critic</div>
      </div>
    </div>
  )
}