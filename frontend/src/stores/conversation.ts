import { defineStore } from "pinia";
import { useChatStore } from "./chat";

export const useConversationStore = defineStore("conversation", {
  state: () => ({
    conversations: [],
  }),

  actions: {
    async getAllConversations() {
      try {
        const response = await fetch(
          "http://localhost:8072/api/v1/conversations"
        );

        await response.json().then((data) => {
          //console.log(data);
          this.conversations = data;
        });
      } catch (error) {
        console.error("Failed to fetch conversations:", error);
      }
    },

    async getConversationById(conversationId: string) {
      try {
        const response = await fetch(
          `http://localhost:8072/api/v1/conversations/${conversationId}`
        );
        await response.json().then((data) => {
          console.log(data.messages);
          const chatStore = useChatStore();
          const messages = data.messages.map((message: any) => ({
            id: message.id,
            content: message.message,
            role: message.role,
            timestamp: message.timestamp,
          }));
          chatStore.setMessages(messages);
          //this.conversations = data;
        });
      } catch (error) {
        console.error("Failed to fetch conversations:", error);
      }
    },
  },
});
