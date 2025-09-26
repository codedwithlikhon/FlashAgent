import { createPinia } from 'pinia';

let pinia: ReturnType<typeof createPinia> | undefined;

export function createPiniaInstance() {
  if (!pinia) {
    pinia = createPinia();
  }
  return pinia;
}
