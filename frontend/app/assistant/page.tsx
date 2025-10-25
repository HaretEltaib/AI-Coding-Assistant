"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Send } from "lucide-react"

interface Message {
  role: "user" | "assistant"
  content: string
}

export default function AssistantPage() {
  const [input, setInput] = useState("")
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi, I'm your AI programming assistant. How can I help you with coding today?",
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      role: "user",
      content: input,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // إرسال الطلب إلى API الباكيند
    try {
      const response = await fetch("http://localhost:8000/api/v1/llm/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input }),
      })

      if (!response.ok) throw new Error("Error with the backend API.")

      const data = await response.json()

      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <header className="border-b border-gray-200 py-3 px-4 flex items-center justify-between bg-white">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-[#1a365d] rounded-lg flex items-center justify-center text-white font-bold text-sm mr-2">
            AI
          </div>
          <h1 className="text-lg font-medium text-[#1a365d]">AI Programming Assistant</h1>
        </div>
        <a href="/" className="text-sm text-gray-600 hover:text-gray-900">
          Sign Out
        </a>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[80%] rounded-lg px-4 py-3 ${
                  message.role === "user" ? "bg-[#1a365d] text-white" : "bg-white border border-gray-200 text-gray-800"
                }`}
              >
                <pre
                  className={`whitespace-pre-wrap font-sans text-sm ${
                    message.role === "user" ? "text-white" : "text-gray-800"
                  }`}
                  style={{ fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}
                  dangerouslySetInnerHTML={{
                    __html: message.content.replace(
                      /```([\s\S]*?)```/g,
                      '<div class="bg-gray-100 p-2 rounded-md my-2 overflow-x-auto text-gray-800">$1</div>',
                    ),
                  }}
                />
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-[80%] rounded-lg px-4 py-3 bg-white border border-gray-200">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: "0ms" }} />
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: "150ms" }} />
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a programming question..."
            className="flex-1 border border-gray-300 rounded-l-md py-2 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            className={`bg-[#1a365d] text-white px-4 rounded-r-md flex items-center justify-center ${
              !input.trim() || isLoading ? "opacity-50 cursor-not-allowed" : "hover:bg-[#152c4a]"
            }`}
            disabled={!input.trim() || isLoading}
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  )
}
