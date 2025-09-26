import { defineStore } from 'pinia';
import { ref } from 'vue';

import emitter from '@/utils/emitter';

type ActionOptions = {
  action: string;
  args: {
    command: string;
    is_input: boolean;
    thought: string;
    blocking: boolean;
    hidden: boolean;
    confirmation_state: string;
  };
};

class MockSocket {
  emit(event: string, options: ActionOptions) {
    if (event !== 'oh_user_action') {
      return;
    }

    const command = options.args.command || '';
    if (command) {
      emitter.emit('terminal', { type: 'command', content: `$ ${command}` });
    }

    const response = command
      ? `Executed command: ${command}`
      : 'No command provided.';

    emitter.emit('terminal', { type: 'observation', content: response });
  }
}

export const useChatStore = defineStore('chat', () => {
  const conversationId = ref('demo-conversation');
  const socket = new MockSocket();

  return { conversationId, socket };
});
