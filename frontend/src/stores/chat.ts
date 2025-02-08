import { defineStore } from "pinia";
import type { Message, Model } from "../types/chat";
import { StreamService } from "../services/streamService";

export const useChatStore = defineStore("chat", {
  state: () => ({
    messages: [] as Message[],
    currentStreamingMessage: "",
    isStreaming: false,
    models: [
      { name: '', displayName: 'Auto' }
    ] as Model[],
    currentModel: "",
  }),

  actions: {
    setModelList(models: Model[]) {
      this.models = [];
      this.models.push({ name: '', displayName: 'Auto' })
      this.models.push(...models);
    },

    setModel(model: string) {
      this.currentModel = model;
    },
    
    clearMessages() {
      console.log("clearMessages");
      this.messages = [];
    },

    setMessages(messages: Message[]) {
      this.messages = messages;
    },
    async streamMessage(content: string, conversationId?: string | undefined) {
      this.isStreaming = true;
      const streamService = new StreamService();

      try {
        this.messages.push({
          id: Date.now(),
          content: content,
          role: "user",
          timestamp: new Date(),
        });

        const response = await fetch("http://localhost:8072/api/v1/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ 
            prompt: content,
            model: this.currentModel,
            conversation_id: conversationId,
          }),
        });
        console.log(response);

        const messageId = Date.now();
        this.messages.push({
          id: messageId,
          content: "",
          role: "assistant",
          timestamp: new Date(),
        });

        for await (const chunk of streamService.streamResponse(response)) {
          this.updateStreamingMessage(messageId, chunk);
        }
      } finally {
        this.isStreaming = false;
      }
    },

    updateStreamingMessage(messageId: number, chunk: string) {
      const messageIndex = this.messages.findIndex((m) => m.id === messageId);
      if (messageIndex !== -1) {
        this.messages[messageIndex].content += chunk;
      }
    },
  },
});
