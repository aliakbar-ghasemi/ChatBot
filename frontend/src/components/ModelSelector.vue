<template>
  <div class="model-selector">
    <select :value="chatStore.currentModel" @change="handleModelChange">
      <option v-for="model in chatStore.models" :key="model.name" :value="model.name">
        {{ model.displayName }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useChatStore } from '../stores/chat'
import type { Model } from '../types/chat';

const chatStore = useChatStore()

const handleModelChange = (event: Event) => {
  const target = event.target as HTMLSelectElement
  chatStore.setModel(target.value)
}


const fetchModels = async () => {
  try {
    const response = await fetch("http://localhost:8072/api/v1/models");
    const data = await response.json();
    console.log(data.models);
    
    var models: Model[] = [];
    data.models.forEach((model: string) => {
      models.push({
        name: model,
        displayName: model,
      });
    });
    chatStore.setModelList(models);
  } catch (error) {
    console.error("Error fetching models:", error);
  }
};

onMounted(() => {
  fetchModels();
});
</script>

<style scoped>
.model-selector { }

select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  background-color: white;
  width: 200px;
}
</style>
