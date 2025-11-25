'use client'
import { useChatStore } from '../stores/chatStore'
import { useEffect } from 'react'

export default function AgentPipeline() {
  const { lastRun } = useChatStore()

  // Agregar este useEffect para debuggear
  useEffect(() => {
    console.log('🔄 AgentPipeline - lastRun actualizado:', lastRun)
  }, [lastRun])

  const agents = [
    { 
      name: "RAG Agent", 
      description: "Semantic Search & Context",
      score: lastRun?.rag_context?.max_similarity,
      icon: "🔍",
      color: "from-purple-500 to-pink-500",
      status: lastRun?.rag_context ? "active" : "idle"
    },
    { 
      name: "Reasoner", 
      description: "Generates Response",
      score: lastRun?.rag_context?.max_similarity,
      icon: "🧠",
      color: "from-blue-500 to-cyan-500",
      status: lastRun?.final_response ? "active" : "idle"
    },
    { 
      name: "Critic", 
      description: "Quality Analysis",
      score: lastRun?.critic_review?.score,
      icon: "⭐",
      color: "from-yellow-500 to-orange-500",
      status: lastRun?.critic_review ? "active" : "idle"
    },
    { 
      name: "Improver", 
      description: "Optimization",
      score: lastRun?.critic_review?.score,
      icon: "⚡",
      color: "from-green-500 to-emerald-500",
      status: lastRun?.critic_review ? "active" : "idle"
    }
  ]

  const getScoreColor = (score: number) => {
    if (!score) return 'bg-slate-700/50 text-slate-400 border-slate-600/50'
    if (score > 0.7) return 'badge-success'
    if (score > 0.5) return 'badge-warning'
    return 'badge-error'
  }

  const getScoreText = (score: number) => {
    if (!score) return '—'
    if (score > 0.7) return 'Excellent'
    if (score > 0.5) return 'Good'
    return 'Needs Work'
  }

  const getStatusColor = (status: string) => {
    return status === 'active' ? 'bg-green-400' : 'bg-slate-500'
  }

  const getDisplayScore = (score: number) => {
    if (!score) return '—'
    return Math.round(score * 100) + '%'
  }

  return (
    <div className="space-y-3">
      {agents.map((agent, index) => (
        <div key={agent.name} className="agent-card p-3 border border-slate-700/50 transition-all duration-300">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className={`flex-shrink-0 w-8 h-8 rounded-lg bg-gradient-to-br ${agent.color} flex items-center justify-center text-white font-bold text-sm shadow-md`}>
                {agent.icon}
              </div>
              <div className={`absolute -top-1 -right-1 w-3 h-3 rounded-full border-2 border-slate-800 ${getStatusColor(agent.status)}`}></div>
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-1">
                <h3 className="font-semibold text-white text-sm truncate">{agent.name}</h3>
                <div className={`badge ${getScoreColor(agent.score)}`}>
                  {getDisplayScore(agent.score)}
                </div>
              </div>
              <p className="text-xs text-slate-400 mb-2 truncate">{agent.description}</p>
              
              {agent.score && (
                <>
                  <div className="w-full bg-slate-700/50 rounded-full h-1.5 mb-1">
                    <div 
                      className={`h-1.5 rounded-full transition-all duration-500 ${
                        agent.score > 0.7 ? 'bg-green-500' :
                        agent.score > 0.5 ? 'bg-yellow-500' :
                        'bg-red-500'
                      }`}
                      style={{ width: `${agent.score * 100}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-slate-500">
                    {getScoreText(agent.score)}
                  </p>
                </>
              )}
            </div>
          </div>
        </div>
      ))}
      
      {/* Estado del sistema */}
      <div className="text-center pt-2 border-t border-slate-700/30">
        <p className="text-xs text-slate-500">
          {lastRun ? 'Last run completed' : 'Ready for first query'}
        </p>
        {lastRun && (
          <p className="text-xs text-slate-600 mt-1">
            Context: {lastRun.rag_context?.results_count || 0} results
          </p>
        )}
      </div>
    </div>
  )
}