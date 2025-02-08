import { ref, computed } from 'vue'
import { useChatStore } from '../stores/chat'

export function useChat() {
  const store = useChatStore()
  
  const sendStreamingMessage = async (content: string, conversationId?: string) => {
    if (!content.trim()) return
    await store.streamMessage(content, conversationId)
  }

  const clearMessages = () => {
    console.log("clearMessages");
    store.clearMessages()
  }

  return {
    messages: computed(() => store.messages),
    isStreaming: computed(() => store.isStreaming),
    sendStreamingMessage,
    clearMessages
  }
}
