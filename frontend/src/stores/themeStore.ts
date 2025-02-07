import { defineStore } from 'pinia';
import { ref } from 'vue';
import { lightTheme, darkTheme } from '../themes/themes';
import type { Theme } from '@/types/theme';

export const useThemeStore = defineStore('theme', () => {
  const currentTheme = ref<Theme>(lightTheme);

  function isDarkTheme(): boolean {
    return currentTheme.value === darkTheme;
  }
  function toggleTheme() {
    currentTheme.value = currentTheme.value === lightTheme ? darkTheme : lightTheme;
    applyTheme();
  }

  function applyTheme() {
    const shouldUseDark = currentTheme.value === darkTheme
    
    document.documentElement.classList.toggle('dark', shouldUseDark);

    const colors = currentTheme.value.colors;
    Object.entries(colors).forEach(([key, value]) => {
      document.documentElement.style.setProperty(`--color-${key}`, value);
    });
  }

  return {
    currentTheme,
    toggleTheme,
    isDarkTheme
  };
});
