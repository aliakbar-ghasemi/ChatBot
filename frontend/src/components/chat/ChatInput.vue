<template>
  <div class="chat-input-container">
    <div v-if="!hasMessages" style="text-align: center; margin-bottom: 1rem">
      <h1>What can I help with?</h1>
    </div>
    <div class="input-wrapper">
      <textarea
        ref="textareaRef"
        v-model="localInput"
        class="auto-grow-textarea"
        :rows="textareaRows"
        placeholder="Send a message..."
        @keydown.enter.prevent="handleEnter"
        @input="autoResize"
      />

      <div class="actions-bar">
        <div class="left-actions">
          <button class="action-btn" @click="toggleFileUpload">
            <i class="fa fa-paperclip"></i>
          </button>
          <input
            type="file"
            ref="fileInput"
            class="hidden"
            @change="handleFileUpload"
            multiple
          />
        </div>

        <div class="right-actions">
          <span v-if="isTyping" class="typing-indicator"> Typing... </span>
          <button class="send-button" :disabled="!canSend" @click="sendMessage">
            <i class="fa fa-paper-plane" :class="{ rotating: loading }"></i>
          </button>
        </div>
      </div>
    </div>

    <div v-if="attachments.length" class="attachments-preview">
      <div v-for="(file, index) in attachments" :key="index" class="attachment">
        <span>{{ file.name }}</span>
        <button @click="removeAttachment(index)">×</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useDebounceFn } from "@vueuse/core";

const props = defineProps<{
  modelValue: string;
  loading?: boolean;
  hasMessages?: boolean;
  maxLength?: number;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
  send: [content: string, files: File[]];
}>();

const textareaRef = ref<HTMLTextAreaElement>();
const fileInput = ref<HTMLInputElement>();
const attachments = ref<File[]>([]);
const textareaRows = ref(1);
const isTyping = ref(false);
const localInput = ref(props.modelValue);

const canSend = computed(() => {
  return (
    (localInput.value.trim().length > 0 || attachments.value.length > 0) && !props.loading
  );
});

// Handle v-model sync
watch(
  () => props.modelValue,
  (newValue) => {
    if (localInput.value !== newValue) {
      localInput.value = newValue;
    }
  }
);

watch(localInput, (newValue) => {
  emit("update:modelValue", newValue);

  // Handle typing indicator
  isTyping.value = true;
  debouncedResetTyping();
});

const debouncedResetTyping = useDebounceFn(() => {
  isTyping.value = false;
}, 1000);

onMounted(() => {
  autoResize();
});
//Auto-resize textarea
const autoResize = () => {
  const textarea = textareaRef.value;
  if (textarea) {
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  }
};

const handleEnter = (e: KeyboardEvent) => {
  if (e.shiftKey) return;
  sendMessage();
};

const sendMessage = () => {
  if (!canSend.value) return;

  emit("send", localInput.value);
  localInput.value = "";
  attachments.value = [];
  textareaRows.value = 1;

  if (textareaRef.value) {
    textareaRef.value.style.height = "auto";
  }
};

const toggleFileUpload = () => {
  fileInput.value?.click();
};

const handleFileUpload = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    attachments.value = [...attachments.value, ...Array.from(input.files)];
  }
};

const removeAttachment = (index: number) => {
  attachments.value.splice(index, 1);
};
</script>

<style scoped>
.chat-input-container {
  justify-content: center;
  display: flex;
  flex-direction: column;
  width: 100%;
  padding-bottom: 0.6rem;
}

.input-wrapper {
  width: 100%;
  margin: 0 auto;
  padding-top: 1rem;
  background: #fff;
  border-top: 1px solid #e5e7eb;
  border-radius: 20px 20px 20px 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

.auto-grow-textarea {
  width: 100%;
  min-height: 70px;
  max-height: 300px; /* Optional limit */
  /*overflow-y: hidden; /* Hide scrollbar */
  resize: none; /* Prevent manual resizing */
  border: none;
  font-size: 1.2rem;
  line-height: 1.5;
  align-items: center;
  transition: border-color 0.2s;
}

.auto-grow-textarea:focus {
  border: none;
  outline: none;
}

.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.action-btn {
  width: 50px;
  height: 50px;
  padding: 0.5rem;
  border-radius: 50%;
  font-size: 20px;
  border: none;
  cursor: pointer;
  color: #0e2c4b;
  transition: color 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.action-btn:hover {
  background-color: #0056b3;
  color: white;
}

.send-button {
  padding: 0.5rem;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 22px;
  background-color: #d5e1ec;
  color: rgb(88, 88, 88);
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.send-button:hover {
  background-color: #0056b3;
  color: white;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.rotating {
  animation: rotate 1s linear infinite;
}

.attachments-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.attachment {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: #f3f4f6;
  border-radius: 4px;
  font-size: 0.875rem;
}

.hidden {
  display: none;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
