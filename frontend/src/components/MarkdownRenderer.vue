<template>
  <div v-if="thinkTags" v-html="thinkTags"></div>
  <div class="mark-down-renderer" v-html="formattedResponse"></div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { marked } from "marked";

const props = defineProps<{
  content: string;
}>();

// Configure marked to preserve raw HTML (including <think> tags)
marked.use({
  breaks: true, // Optional: Convert line breaks to <br>
});

const formattedResponse = computed(() => {
  // Wrap parsed content in a div to ensure <think> is nested
  var processedContent = props.content.replace(
    /<think>([\s\S]*?)<\/think>/gi,
    ""
    //'<span class="think-text">$1</span>'
  );

  return `<div>${marked.parse(processedContent)}</div>`;
});

// Extract the full <think> tags
const thinkTags = computed(
  () => props.content.match(/<think>.*?<\/think>/gs) || []
);
</script>

<style scoped>
/* Target ONLY the <think> tag */
:deep(think) {
  display: block; /* or inline-block */
  color: #b3b3b3;
  font-style: normal;
  position: relative;
  padding-left: 1rem;
  margin-bottom: 1.5rem;
}

:deep(think)::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: #e2e2e2;
  opacity: 0.7;
}
</style>
