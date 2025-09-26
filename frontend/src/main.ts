import { createApp } from 'vue';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';

import App from './App.vue';
import { createI18nInstance } from './services/i18n';
import { createPiniaInstance } from './store/pinia';

const app = createApp(App);

app.use(createPiniaInstance());
app.use(createI18nInstance());
app.use(Antd);

app.mount('#app');
