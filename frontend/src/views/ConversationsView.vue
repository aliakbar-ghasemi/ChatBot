<template>
  <div class="conversations-view">
    <div class="item-list">
      <div style="text-align: center" v-if="conversations.length < 1">
        the history is empty
      </div>
      <div
        v-for="(conversation, index) in conversations"
        :key="index"
        class="item"
        @click="onItemClick(conversation[0])"
      >
        {{ conversation[1] }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useConversation } from "../composables/useConversation";
import { useRouter } from "vue-router";

const { conversations, getAllConversations } = useConversation();
const router = useRouter();

onMounted(() => {
  getAllConversations();
});

const onItemClick = (id: string) => {
  router.push(`/chat/${id}`);
};
</script>

<style scoped>
.conversations-view {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.item-list {
  padding: 20px;
  width: 100%;
  /*text-align: center;*/
}

.item {
  background: #ffffff;
  padding: 10px;
  margin: 10px 0;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
