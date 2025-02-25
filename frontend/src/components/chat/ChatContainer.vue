<template>
  <div v-if="messages.length > 0" class="chat-container" ref="containerRef" @scroll="handleScroll">
    <div v-for="(message, index) in messages" :key="message.id" class="message-wrapper" :ref="index === currentQuestionIndex ? 'currentQuestionRef' : ''">
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

const currentQuestionIndex = ref<number | null>(null); // Index of the current question
const isAtTop = ref(false); // To track if the container is at the top

// Refs
const containerRef = ref<HTMLElement | null>(null); // Ref for the content container
const currentQuestionRef = ref<HTMLElement | null>(null); // Ref for the current question

// Handle the scroll event
const handleScroll = () => {
  const container = containerRef.value;
  // Check if we're at the top
  isAtTop.value = container.scrollTop === 0;
};

const lastMessageId = computed(() => {
  const lastMessage = props.messages[props.messages.length - 1]
  return lastMessage?.id
})

// Function to handle the new stream of data (new messages)
const onMessagesReceived = () => {
  const container = containerRef.value;

  // If the new message is a question, set it as the current question
  // (for now, we will assume that the role 'user' is a question)
  if (props.messages[props.messages.length - 1].role === 'user') {
    currentQuestionIndex.value = props.messages.length - 1;
  }

  // Scroll to the current question
  if (currentQuestionIndex.value !== null) {
    scrollToCurrentQuestion();
  }
};

// Scroll to the current question
const scrollToCurrentQuestion = () => {
  const container = containerRef.value;
  const currentQuestion = currentQuestionRef.value;

  // Only scroll if the current question exists and we're not at the top
  if (currentQuestion && !isAtTop.value) {
    currentQuestion.scrollIntoView({
      behavior: 'smooth',
      block: 'start', // Scroll to the top of the current question
    });
  }
};

const scrollToBottom = () => {
  nextTick(() => {
    if (containerRef.value) {
      containerRef.value.scrollTop = containerRef.value.scrollHeight
    }
  })
}

watch(
  () => props.messages,
  (newMessages) => {
    if(newMessages.length === 0) return;

    if(!props.isStreaming){
      scrollToBottom();
      return;
    }

    // Check if the new message is a question and update the current question index
    const lastMessage: Message = newMessages[newMessages.length - 1];
    if (lastMessage['role'] === 'user') {
      currentQuestionIndex.value = newMessages.length - 1;
      scrollToCurrentQuestion();
    }
  },
  { immediate: true, deep:true } // Make sure it checks on component mount as well
);
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
