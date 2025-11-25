'use client'
import { useChatStore } from '../stores/chatStore'

export default function RAGResults() {
  const { lastRun } = useChatStore()
  const results = lastRun?.rag_context?.results || []

  const getSimilarityColor = (similarity: number) => {
    if (similarity > 0.6) return 'badge-success'
    if (similarity > 0.4) return 'badge-warning'
    return 'badge-error'
  }

  const getSimilarityText = (similarity: number) => {
    if (similarity > 0.6) return 'High relevance'
    if (similarity > 0.4) return 'Medium relevance'
    return 'Low relevance'
  }

  return (
    <div>
      {results.length === 0 ? (
        <div className="text-center py-6 text-slate-400">
          <div className="text-3xl mb-2 opacity-60">🔍</div>
          <p className="text-sm font-medium mb-1">No context retrieved</p>
          <p className="text-xs opacity-75">Send a message to see RAG results</p>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="flex justify-between items-center text-xs text-slate-400 mb-2">
            <span>Found {results.length} results</span>
            <span>Max similarity: {lastRun?.rag_context?.max_similarity ? Math.round(lastRun.rag_context.max_similarity * 100) : 0}%</span>
          </div>
          
          {results.map((result: any, index: number) => (
            <div key={index} className="agent-card p-3 border border-slate-700/50 transition-all duration-300">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 rounded-full bg-cyan-400 shadow-md shadow-cyan-400/50"></div>
                  <span className="text-xs font-semibold text-white capitalize">
                    {result.category || 'Technical'}
                  </span>
                </div>
                <div className={`badge ${getSimilarityColor(result.similarity)}`}>
                  {Math.round(result.similarity * 100)}%
                </div>
              </div>
              
              <p className="text-xs text-slate-300 line-clamp-3 leading-relaxed mb-2">
                {result.content}
              </p>
              
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-500">
                  {getSimilarityText(result.similarity)}
                </span>
                <div className="w-16 bg-slate-700/50 rounded-full h-1">
                  <div 
                    className={`h-1 rounded-full transition-all duration-500 ${
                      result.similarity > 0.6 ? 'bg-green-500' :
                      result.similarity > 0.4 ? 'bg-yellow-500' :
                      'bg-red-500'
                    }`}
                    style={{ width: `${result.similarity * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}