<template>
  <div v-if="messages.length > 0" class="chat-container" ref="containerRef">
    <div v-for="message in messages" :key="message.id" class="message-wrapper">
      <div :class="['message', message.role]">
        <StreamingMessage
          :content="message.content"
          :is-streaming="isStreaming && message.id === lastMessageId"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import StreamingMessage from './StreamingMessage.vue'
import type { Message } from '@/types/chat'

const props = defineProps<{
  messages: Message[]
  isStreaming: boolean
}>()

const containerRef = ref<HTMLElement>()
const lastMessageId = computed(() => {
  const lastMessage = props.messages[props.messages.length - 1]
  return lastMessage?.id
})

// Watch both the messages array and individual message content
watch(
  () => props.messages,
  () => {
    scrollToBottom()
  },
  { deep: true }
)

const scrollToBottom = () => {
  nextTick(() => {
    if (containerRef.value) {
      containerRef.value.scrollTop = containerRef.value.scrollHeight
    }
  })
}
</script>

<style scoped>
.chat-container {
  flex: 1;
  overflow-y: auto; /* Add scroll if content overflows */
  padding: 1rem;
}

.message-wrapper {
  margin-bottom: 1rem;
}

.message {
  padding: 1rem;
  border-radius: 8px;
}

.message.user {
  max-width: 80%;
  margin-left: auto;
  background-color: #6366f1;
  color: white;
}

.message.assistant {
  margin-right: auto;
  background-color: #f3f4f6;
}
</style>
