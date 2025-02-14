<template>
  <div class="streaming-message" :class="{ 'is-streaming': isStreaming }">
    <div class="response-container">
      <div v-html="formattedResponse" dir="auto"></div>
      <span v-if="isStreaming" class="cursor">▋</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { marked } from "marked";
import { computed } from "vue";

const props = defineProps<{
  content: string;
  isStreaming: boolean;
}>();

const formattedResponse = computed(() => marked.parse(props.content || ""));
</script>

<style scoped>
.streaming-message {
  padding: 0;
  line-height: 1.7;
}

.cursor {
  display: inline-block;
  animation: blink 1s step-end infinite;
}

.response-container {
  line-height: 1.6;
  word-wrap: break-word; /* Ensures long words break properly */
  white-space: pre-wrap; /* Preserves formatting while allowing wrapping */
  overflow-wrap: break-word; /* Ensures text breaks to the next line */
  direction: auto;
}

.response-container pre {
  background: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
  white-space: pre-wrap; /* Allows code to wrap inside <pre> */
  word-wrap: break-word;
}

.response-container code {
  direction: ltr;
  unicode-bidi: embed;
  font-family: monospace;
  background: #f5f5f5;
  padding: 2px 4px;
  border-radius: 4px;
  white-space: pre-wrap; /* Ensures long code snippets wrap */
  word-break: break-word; /* Prevents overflow */
}
@keyframes blink {
  50% {
    opacity: 0;
  }
}
</style>
