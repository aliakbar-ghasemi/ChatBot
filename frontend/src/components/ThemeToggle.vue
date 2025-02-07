<template>
  <button class="theme-toggle" @click="toggleTheme" :title="buttonTitle">
    <IconSun v-if="isDark" class="icon" />
    <IconMoon v-else class="icon" />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useThemeStore } from '@/stores/themeStore';
import IconSun from '@/components/icons/IconSun.vue';
import IconMoon from '@/components/icons/IconMoon.vue';

const themeStore = useThemeStore();

const isDark = computed(() => themeStore.isDarkTheme());
const buttonTitle = computed(() => isDark.value ? 'Switch to light mode' : 'Switch to dark mode');

const toggleTheme = () => {
  themeStore.toggleTheme();
};
</script>

<style scoped lang="scss">
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: var(--color-surface);
  }

  .icon {
    width: 24px;
    height: 24px;
    color: var(--color-text);
  }
}
</style>
