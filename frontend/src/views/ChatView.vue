<template>
  <div class="chat-view">
    <ChatContainer :messages="messages" :is-streaming="isStreaming" />
    <ChatInput
      v-model="userInput"
      @send="sendMessage"
      :loading="isStreaming"
      :hasMessages="messages.length > 0"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import ChatContainer from "../components/chat/ChatContainer.vue";
import ChatInput from "../components/chat/ChatInput.vue";
import { useChat } from "../composables/useChat";
import { useRoute } from "vue-router";
import { useConversation } from "@/composables/useConversation";

const { messages, sendStreamingMessage, isStreaming, clearMessages } =
  useChat();
const { getConversationById } = useConversation();
const userInput = ref("");

const route = useRoute();

const getCoversationId = (_id: string | string[]) => {
  var id = Array.isArray(_id) ? _id[0] : _id || "";

  if (id === null || id === undefined || id === "" || !id || id.trim() === "") {
    const timestamp = Math.floor(Date.now() / 1000);
    id = timestamp.toString();
    console.log("ID had no value:"+id);
  }
  return id;
};

var itemId = getCoversationId(route.params.id); /*Array.isArray(route.params.id)
  ? route.params.id[0]
  : route.params.id || "";*/

const sendMessage = (content: string) => {
  sendStreamingMessage(content, itemId);
};

onMounted(() => {
  clearMessages();
  itemId = getCoversationId(route.params.id)
  if (itemId) {
    getConversationById(itemId);
  }
});

watch(
  () => route.params.id,
  (newId, oldId) => {
    clearMessages();
    itemId = getCoversationId(newId) 
    if (newId) {
      getConversationById(itemId);
    }
  }
);
</script>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
}
</style>
