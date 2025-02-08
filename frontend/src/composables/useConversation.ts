import { ref, computed } from 'vue'
import { useConversationStore } from '../stores/conversation'

export function useConversation() {
  const store = useConversationStore()
  
  const getAllConversations = async () => {
    await store.getAllConversations()
  }

  const getConversationById = async (conversationId: string) => {
    await store.getConversationById(conversationId)
  }

  return {
    conversations: computed(() => store.conversations),
    getAllConversations,
    getConversationById
  }
}
