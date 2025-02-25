<template>
  <div class="conversations-view">
    <div class="item-list">
      <div style="text-align: center" v-if="conversations.length < 1">
        the history is empty
      </div>
      <div
        v-for="(conversation, index) in conversations"
        :key="index"
        @click="onItemClick(conversation[0])"
      >
        <div class="item-content">
          <div class="item-header">{{ conversation[1] }}</div>
          <p class="gray item-summary">{{ conversation[3] }}</p>
          <div style="display: flex; justify-content: space-between">
            <div></div>
            <p class="light-gray">{{ conversation[2] }}</p>
          </div>
        </div>
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
  display: flex;
  flex-direction: column;
  padding: 20px;
  width: 100%;
  /*text-align: center;*/
}

.item-content {
  width: 100%;
  background: #ffffff;
  padding: 10px;
  margin: 10px 0;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}

.item-content:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.item-header {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
  direction: auto;
  text-align: start;
}

.item-summary{
  font-size: 14px;
  font-weight: 300;
  margin-bottom: 10px;
  direction: auto;
  text-align: start;
}

</style>
