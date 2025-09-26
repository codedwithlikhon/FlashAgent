import { createApp } from 'vue';
import Antd from 'ant-design-vue';
import { createPinia } from 'pinia';
import { createI18n } from 'vue-i18n';

import App from './App.vue';
import enUS from './locales/en-US.json';

import 'ant-design-vue/dist/reset.css';
import './style.scss';

const pinia = createPinia();
const i18n = createI18n({
  legacy: false,
  locale: 'en-US',
  messages: {
    'en-US': enUS,
  },
});

createApp(App).use(Antd).use(pinia).use(i18n).mount('#app');
