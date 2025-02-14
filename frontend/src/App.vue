<template>
  <div class="app-container">
    <Sidebar />
    <main :class="['main-content', { 'sidebar-collapsed': isSidebarCollapsed }]">
      <div>
        <ModelSelector />
      </div>
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from './components/Sidebar.vue'
import ModelSelector from '@/components/ModelSelector.vue'

const isSidebarCollapsed = ref(false)
</script>

<style>
.app-container {
  display: flex;
  flex-direction: row;
  
}

.main-content {
  display: flex;
  flex-direction: column;
  margin-left: 250px;
  width: calc(100% - 250px);
  height: 100vh;
  padding: 1rem;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

body{
  background: #f8f9fa;
}

.main-content.sidebar-collapsed {
  margin-left: 60px;
  width: calc(100% - 60px);
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 60px;
    width: calc(100% - 60px);
  }
}
</style>
