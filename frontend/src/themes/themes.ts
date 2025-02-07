import type { Theme } from "@/types/theme";

export const lightTheme: Theme = {
  colors: {
    primary: '#007AFF',
    background: '#FFFFFF',
    text: '#000000',
    secondary: '#6C757D',
    accent: '#5856D6'
  },
  spacing: {
    small: '8px',
    medium: '16px',
    large: '24px'
  },
  typography: {
    h1: '2.5rem',
    h2: '2rem',
    body: '1rem'
  }
};

export const darkTheme: Theme = {
    colors: {
        primary: '#0A84FF',
        background: '#000000',
        text: '#FFFFFF',
        secondary: '#86868B',
        accent: '#5E5CE6'
      },
      spacing: {
        small: '8px',
        medium: '16px',
        large: '24px'
      },
      typography: {
        h1: '2.5rem',
        h2: '2rem',
        body: '1rem'
      }
};
