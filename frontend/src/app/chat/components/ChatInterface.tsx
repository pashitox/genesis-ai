'use client'
import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { useChatStore } from '../stores/chatStore'
import { v4 as uuidv4 } from 'uuid'

export default function ChatInterface() {
  const { messages, addMessage, setLastRun } = useChatStore()
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [connectionError, setConnectionError] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const messagesContainerRef = useRef<HTMLDivElement>(null)

  // Scroll suave solo cuando se agregan nuevos mensajes
  useEffect(() => {
    if (messages.length > 0) {
      // Pequeño delay para asegurar que el DOM se haya actualizado
      setTimeout(() => {
        messagesEndRef.current?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'nearest'
        })
      }, 100)
    }
  }, [messages.length]) // Solo dependemos del length, no de todo el array

  // Verificar conexión al backend al cargar el componente
  useEffect(() => {
    checkBackendConnection()
  }, [])

  const checkBackendConnection = async () => {
    try {
      console.log('🔍 Verificando conexión con backend...')
      const response = await axios.get('http://localhost:8002/health', { timeout: 5000 })
      console.log('✅ Backend conectado:', response.data)
      setConnectionError(false)
    } catch (error) {
      console.error('❌ Backend connection failed:', error)
      setConnectionError(true)
    }
  }

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    
    const id = uuidv4()
    const userMsg = { id, role: 'user', text: input }
    addMessage(userMsg)
    setInput('')
    setLoading(true)

    try {
      console.log('Enviando mensaje al backend:', input)
      const response = await axios.post(
        'http://localhost:8002/chat', 
        { message: input },
        { timeout: 30000 }
      )

      const data = response.data
      console.log('Respuesta del backend:', data)
      
      // Actualizar lastRun para que los otros componentes se actualicen
      setLastRun(data)
      setConnectionError(false)

      const assistantMsg = { 
        id: uuidv4(), 
        role: 'assistant', 
        text: data.final_response,
        response: data
      }
      addMessage(assistantMsg)

    } catch (error: any) {
      console.error('Chat error:', error)
      
      let errorMessage = 'Error desconocido'
      
      if (error.code === 'ECONNREFUSED') {
        errorMessage = '❌ Backend no disponible. Verifica que el servidor esté ejecutándose en puerto 8002.'
        setConnectionError(true)
      } else if (error.response?.status === 500) {
        errorMessage = `⚠️ Error del servidor: ${error.response.data.detail || 'Error interno'}`
      } else if (error.response?.status === 404) {
        errorMessage = '🔍 Endpoint no encontrado. Verifica la URL del backend.'
      } else if (error.code === 'NETWORK_ERROR') {
        errorMessage = '🌐 Error de red. Verifica tu conexión.'
      } else if (error.code === 'TIMEOUT') {
        errorMessage = '⏰ Timeout. El servidor está tardando demasiado en responder.'
      } else {
        errorMessage = `❌ Error: ${error.message}`
      }
      
      const errorMsg = { 
        id: uuidv4(), 
        role: 'system', 
        text: errorMessage,
        error: true 
      }
      addMessage(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const retryConnection = async () => {
    setConnectionError(false)
    await checkBackendConnection()
  }

  // Función para formatear el texto con markdown básico
  const formatMessage = (text: string) => {
    return text.split('\n').map((line, index) => {
      // Negrita
      line = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Código inline
      line = line.replace(/`(.*?)`/g, '<code class="inline-code">$1</code>')
      return <div key={index} dangerouslySetInnerHTML={{ __html: line }} />
    })
  }

  return (
    <div className="flex flex-col h-full">
      {/* Banner de error de conexión */}
      {connectionError && (
        <div className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
              <span className="text-sm text-red-200 font-medium">
                Backend no conectado
              </span>
            </div>
            <button
              onClick={retryConnection}
              className="px-3 py-1 text-xs bg-red-500/30 hover:bg-red-500/40 text-red-100 rounded-lg transition-colors border border-red-500/50"
            >
              Reintentar
            </button>
          </div>
          <p className="text-xs text-red-300 mt-1">
            Ejecuta: <code className="bg-red-900/30 px-1 rounded">python main.py</code> en el backend
          </p>
        </div>
      )}

      {/* Messages Container */}
      <div 
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto space-y-3 p-3 rounded-xl bg-slate-800/20 border border-slate-700/30 mb-3"
      >
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center py-8">
            <div className="w-12 h-12 rounded-2xl gradient-bg flex items-center justify-center text-xl mb-3 shadow-lg">
              {connectionError ? '⚠️' : '🤖'}
            </div>
            <h3 className="text-base font-bold text-white mb-2 leading-tight">
              {connectionError ? 'Backend Desconectado' : 'Welcome to GENESIS AI'}
            </h3>
            <p className="text-slate-300 text-sm mb-4 max-w-md leading-relaxed">
              {connectionError 
                ? 'El servidor backend no está disponible. Inicia el servidor para comenzar.'
                : 'Ask me about Docker, Kubernetes, FastAPI, or Python development'
              }
            </p>
            {!connectionError && (
              <div className="flex flex-wrap gap-2 justify-center">
                {['Docker containers', 'Kubernetes pods', 'FastAPI routes', 'Python async'].map((topic) => (
                  <button
                    key={topic}
                    onClick={() => setInput(topic)}
                    className="px-3 py-2 bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 rounded-lg text-xs transition-colors border border-slate-600/50 hover:border-slate-500/50"
                  >
                    {topic}
                  </button>
                ))}
              </div>
            )}
            {connectionError && (
              <div className="text-xs text-slate-400 mt-2">
                <p>Backend esperado en: <code className="bg-slate-700/50 px-1 rounded">http://localhost:8002</code></p>
              </div>
            )}
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`p-3 max-w-[85%] ${
                message.role === 'user' 
                  ? 'chat-message-user' 
                  : message.role === 'system'
                  ? 'bg-red-500/20 text-red-200 border border-red-500/30 rounded-xl'
                  : message.error
                  ? 'bg-orange-500/20 text-orange-200 border border-orange-500/30 rounded-xl'
                  : 'chat-message-assistant'
              }`}>
                <div className="flex items-center space-x-2 mb-2">
                  <div className={`w-2 h-2 rounded-full ${
                    message.role === 'user' ? 'bg-white' : 
                    message.role === 'system' ? 'bg-red-400' :
                    message.error ? 'bg-orange-400' : 'bg-cyan-400'
                  }`}></div>
                  <span className="text-xs font-semibold opacity-90">
                    {message.role === 'user' ? 'You' : 
                     message.role === 'system' ? 'System' : 
                     message.error ? 'Warning' : 'GENESIS AI'}
                  </span>
                </div>
                <div className="text-sm leading-relaxed break-words message-content">
                  {formatMessage(message.text)}
                </div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - Fijo en la parte inferior */}
      <div className="flex space-x-2 items-end bg-slate-900/50 rounded-xl p-2 border border-slate-700/30">
        <div className="flex-1 relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={
              connectionError 
                ? "Backend no disponible - Inicia el servidor primero"
                : "Ask about Docker, Kubernetes, FastAPI, Python..."
            }
            className="input-field w-full px-4 py-3 text-sm placeholder-slate-400/60 focus:outline-none transition-all duration-300 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={loading || connectionError}
          />
          {loading && (
            <div className="absolute right-3 top-3">
              <div className="w-4 h-4 border-2 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
          )}
        </div>
        <button
          onClick={sendMessage}
          disabled={loading || !input.trim() || connectionError}
          className="btn-primary px-4 py-3 font-semibold text-sm whitespace-nowrap flex items-center space-x-2 transition-all duration-300 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed min-w-[80px] justify-center"
        >
          {loading ? (
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <>
              <span>Send</span>
              <span className="text-xs">⚡</span>
            </>
          )}
        </button>
      </div>

      <style jsx>{`
        .message-content :global(strong) {
          font-weight: 600;
          color: #f8fafc;
        }
        .message-content :global(.inline-code) {
          background: rgba(255, 255, 255, 0.1);
          padding: 0.1rem 0.3rem;
          border-radius: 0.25rem;
          font-family: 'Monaco', 'Consolas', monospace;
          font-size: 0.875em;
          border: 1px solid rgba(255, 255, 255, 0.2);
        }
      `}</style>
    </div>
  )
}