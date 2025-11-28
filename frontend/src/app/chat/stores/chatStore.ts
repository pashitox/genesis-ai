'use client'

import { create } from 'zustand'

type Msg = { 
  id: string
  role: string
  text: string
  response?: any
  error?: boolean
}

type ChatState = {
  messages: Msg[]
  lastRun: any
  addMessage: (msg: Msg) => void
  updateMessage: (id: string, data: Partial<Msg>) => void
  setLastRun: (run: any) => void
  clear: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  lastRun: null,

  addMessage: (msg) =>
    set((state) => ({
      messages: [...state.messages, msg],
    })),

  updateMessage: (id, data) =>
    set((state) => ({
      messages: state.messages.map((m) =>
        m.id === id ? { ...m, ...data } : m
      ),
    })),

  setLastRun: (run) => 
    set({ lastRun: run }),

  clear: () => set({ messages: [], lastRun: null }),
}))