<template>
  <aside :class="['sidebar', { 'collapsed': isCollapsed }]">
    <div class="sidebar-toggle" @click="toggleSidebar">
      <span class="toggle-icon">{{ isCollapsed ? '→' : '←' }}</span>
    </div>
    
    <nav class="sidebar-nav">
      <ul>
        <li>
          <router-link to="/chat" class="nav-item">
            <span class="icon">🏠</span>
            <span class="label" v-show="!isCollapsed">Home</span>
          </router-link>
        </li>
        <li>
          <router-link to="/conversations" class="nav-item">
            <span class="icon">💬</span>
            <span class="label" v-show="!isCollapsed">Chat</span>
          </router-link>
        </li>
        <li>
          <router-link to="/settings" class="nav-item">
            <span class="icon">⚙️</span>
            <span class="label" v-show="!isCollapsed">Settings</span>
          </router-link>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isCollapsed = ref(false)

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #f5f5f5;
  position: fixed;
  left: 0;
  top: 0;
  transition: all 0.3s ease;
  border-right: 1px solid #e0e0e0;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar-toggle {
  padding: 1rem;
  cursor: pointer;
  text-align: right;
}

.toggle-icon {
  font-size: 1.2rem;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  text-decoration: none;
  color: #333;
  gap: 1rem;
}

.nav-item:hover {
  background-color: #e0e0e0;
}

.nav-item.router-link-active {
  color: #42b883;
  background-color: #e8f5e9;
}

.icon {
  font-size: 1.2rem;
}

.label {
  white-space: nowrap;
}
</style>
