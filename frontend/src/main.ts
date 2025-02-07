import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { themePlugin } from './plugins/theme';

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(themePlugin);

app.mount('#app')
