<template>
  <div class="streaming-message" :class="{ 'is-streaming': isStreaming }">
    <div class="message-content">
      {{ content }}
      <span v-if="isStreaming" class="cursor">▋</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  content: string
  isStreaming: boolean
}>()
</script>

<style scoped>
.streaming-message {
  padding: 0;
  line-height: 1.5;
}

.cursor {
  display: inline-block;
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  50% { opacity: 0; }
}
</style>
