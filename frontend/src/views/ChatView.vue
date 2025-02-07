
<template>
  <div class="chat-view">
    <ChatContainer :messages="messages" :is-streaming="isStreaming"/>
    <ChatInput 
      :model-value="userInput"
      @send="sendStreamingMessage"
      :loading="isStreaming"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ChatContainer from '../components/chat/ChatContainer.vue'
import ChatInput from '../components/chat/ChatInput.vue'
import { useChat } from '../composables/useChat'

const { messages, sendStreamingMessage, isStreaming } = useChat()
const userInput = ref('')
</script>

<style scoped>
.chat-view {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
