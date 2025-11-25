'use client'

import ChatInterface from './chat/components/ChatInterface'
import AgentPipeline from './chat/components/AgentPipeline'
import RAGResults from './chat/components/RAGResults'
import { useState, useEffect } from 'react'

export default function Home() {
  const [activeTab, setActiveTab] = useState('chat')
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 1024)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900/10 to-slate-900">
      {/* Header Elegante y Minimalista */}
      <header className="w-full bg-slate-900/80 backdrop-blur-2xl border-b border-slate-700/20 sticky top-0 z-50">
        <div className="responsive-container">
          <div className="flex items-center justify-between py-4">
            {/* Logo y Branding */}
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 rounded-lg gradient-bg flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-sm">G</span>
              </div>
              <div className="flex flex-col">
                <h1 className="text-lg font-bold text-white tracking-tight">
                  GENESIS AI
                </h1>
                <p className="text-xs text-slate-400">
                  Autonomous Chat Engine
                </p>
              </div>
            </div>
            
            {/* Status Elegante */}
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-1.5 text-xs text-green-400">
                <div className="status-dot"></div>
                <span>System Online</span>
              </div>
            </div>
          </div>

          {/* Navigation Elegante sin bordes */}
          <div className="flex justify-center pb-3">
            <div className="flex space-x-6">
              {[
                { id: 'chat', label: 'Chat', icon: '💬' },
                { id: 'agents', label: 'Agents', icon: '🔄' },
                { id: 'rag', label: 'Knowledge', icon: '📚' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex flex-col items-center space-y-1 transition-all duration-300 group ${
                    activeTab === tab.id
                      ? 'text-purple-400'
                      : 'text-slate-500 hover:text-slate-300'
                  }`}
                >
                  <div className={`text-lg transition-transform duration-300 ${
                    activeTab === tab.id ? 'scale-110' : 'group-hover:scale-105'
                  }`}>
                    {tab.icon}
                  </div>
                  <span className="text-xs font-medium tracking-wide">
                    {tab.label}
                  </span>
                  <div className={`h-0.5 w-6 bg-gradient-to-r from-purple-500 to-cyan-500 transition-all duration-300 ${
                    activeTab === tab.id ? 'opacity-100' : 'opacity-0'
                  }`}></div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="responsive-container py-6">
        <div className="main-grid">
          
          {/* Chat Section */}
          <div className={`fade-in ${!isMobile || activeTab === 'chat' ? 'block' : 'hidden'} lg:block`}>
            <div className="glass-panel glass-panel-hover p-5 shadow-xl h-full">
              <div className="text-center mb-6">
                <h2 className="text-lg font-bold text-white mb-2 flex items-center justify-center space-x-2">
                  <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
                  <span>Chat Interface</span>
                  <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
                </h2>
                <p className="text-slate-400 text-sm">
                  Real-time conversation with AI agents
                </p>
              </div>
              <div className="h-[520px]">
                <ChatInterface />
              </div>
            </div>
          </div>

          {/* Sidebar Sections */}
          <div className={`space-y-5 ${!isMobile || activeTab !== 'chat' ? 'block' : 'hidden'} lg:block`}>
            
            {/* Agents Panel */}
            <div className={`fade-in ${!isMobile || activeTab === 'agents' ? 'block' : 'hidden'} lg:block`}>
              <div className="glass-panel glass-panel-hover p-5">
                <div className="text-center mb-5">
                  <h2 className="text-base font-bold text-white mb-1 flex items-center justify-center space-x-2">
                    <span className="text-lg">🔄</span>
                    <span>Agent Pipeline</span>
                  </h2>
                  <p className="text-slate-400 text-xs">
                    Multi-stage AI processing workflow
                  </p>
                </div>
                <div className="component-spacing">
                  <AgentPipeline />
                </div>
              </div>
            </div>

            {/* RAG Panel */}
            <div className={`fade-in ${!isMobile || activeTab === 'rag' ? 'block' : 'hidden'} lg:block`}>
              <div className="glass-panel glass-panel-hover p-5">
                <div className="text-center mb-5">
                  <h2 className="text-base font-bold text-white mb-1 flex items-center justify-center space-x-2">
                    <span className="text-lg">📚</span>
                    <span>Knowledge Base</span>
                  </h2>
                  <p className="text-slate-400 text-xs">
                    Semantic search results & context
                  </p>
                </div>
                <div className="component-spacing">
                  <RAGResults />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer Profesional con Botones */}
      <footer className="responsive-container py-6 border-t border-slate-700/20 mt-8 bg-slate-900/40">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          {/* Información de la compañía */}
          <div className="text-center md:text-left">
            <div className="flex items-center space-x-2 justify-center md:justify-start">
              <div className="w-5 h-5 rounded gradient-bg flex items-center justify-center">
                <span className="text-white font-bold text-xs">G</span>
              </div>
              <span className="text-sm font-semibold text-white">GENESIS AI</span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Autonomous Chat Engine v1.0
            </p>
          </div>

          {/* Botones de acción */}
          <div className="flex space-x-3">
            <button className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white transition-colors border border-slate-600/50 rounded-lg hover:border-slate-500/50">
              Documentation
            </button>
            <button className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white transition-colors border border-slate-600/50 rounded-lg hover:border-slate-500/50">
              API Reference
            </button>
            <button className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white transition-colors border border-slate-600/50 rounded-lg hover:border-slate-500/50">
              Support
            </button>
          </div>

          {/* Información técnica */}
          <div className="text-center md:text-right">
            <p className="text-xs text-slate-500">
              Powered by Multi-Agent Architecture
            </p>
            <p className="text-xs text-slate-600 mt-1">
              © 2024 GENESIS AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}