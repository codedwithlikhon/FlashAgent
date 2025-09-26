import { createI18n } from 'vue-i18n';

import en from '../locales/en.json';

type MessageSchema = typeof en;

export function createI18nInstance() {
  return createI18n<{ message: MessageSchema }, 'en'>({
    legacy: false,
    locale: 'en',
    fallbackLocale: 'en',
    messages: { en }
  });
}
