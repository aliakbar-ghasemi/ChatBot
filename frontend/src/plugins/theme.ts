import type { Theme } from '@/types/theme';
import type { App } from 'vue';

export const themePlugin = {
  install: (app: App) => {
    app.config.globalProperties.$theme = {
      applyTheme: (theme: Theme) => {
        Object.entries(theme.colors).forEach(([key, value]) => {
          document.documentElement.style.setProperty(`--color-${key}`, value);
        });
      }
    };
  }
};
