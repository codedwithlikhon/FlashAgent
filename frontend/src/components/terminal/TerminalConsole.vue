<template>
  <div class="container" v-show="visible">
    <div class="terminal-header">
      <span>Command Console</span>
      <CloseOutlined @click="visible = false" />
    </div>
    <div ref="terminalRef" class="terminal-container"></div>
  </div>
</template>

<script setup lang="ts">
import { CloseOutlined } from '@ant-design/icons-vue';
import { FitAddon } from '@xterm/addon-fit';
import { Terminal } from '@xterm/xterm';
import '@xterm/xterm/css/xterm.css';
import { onMounted, ref, watch } from 'vue';

import { useChatStore } from '@/store/modules/chat';
import emitter from '@/utils/emitter';

const chatStore = useChatStore();

const props = defineProps<{ content?: string | string[] }>();

const terminalRef = ref<HTMLDivElement | null>(null);
const terminal = ref<Terminal>();
const visible = ref(false);
let currentLine = '';
const commandHistory: string[] = [];
let historyIndex = -1;

const writePrompt = () => {
  terminal.value?.write('\x1b[32mflashagent@workspace:~ $ \x1b[0m');
};

const saveHistory = () => {
  localStorage.setItem('terminalHistory', JSON.stringify(commandHistory));
};

const sendToServer = async (command: string) => {
  chatStore.socket.emit('oh_user_action', {
    action: 'run',
    args: {
      command,
      is_input: false,
      thought: '',
      blocking: false,
      hidden: false,
      confirmation_state: 'confirmed'
    }
  });
};

const handleCommand = async (command: string) => {
  switch (command.trim()) {
    case 'help':
      terminal.value?.writeln('Available commands:');
      terminal.value?.writeln('  help     - Show this help message');
      terminal.value?.writeln('  clear    - Clear the terminal');
      terminal.value?.writeln('  history  - Show command history');
      terminal.value?.writeln('  server   - Send command to server');
      break;
    case 'clear':
      terminal.value?.clear();
      break;
    case 'history':
      commandHistory.forEach((cmd, index) => {
        terminal.value?.writeln(`${index + 1}  ${cmd}`);
      });
      break;
    case '':
      break;
    default:
      await sendToServer(command);
  }
  saveHistory();
};

const bootstrapTerminal = () => {
  const term = new Terminal({
    cursorBlink: true,
    fontSize: 14,
    fontFamily: 'Menlo, Monaco, "Courier New", monospace',
    theme: {
      background: '#1e1e1e',
      foreground: '#ffffff',
      green: 'rgb(0, 187, 0)'
    },
    wordWrap: true
  });

  const addon = new FitAddon();
  term.loadAddon(addon);
  terminal.value = term;

  term.open(terminalRef.value!);
  addon.fit();

  term.write('Welcome to the terminal!\r\n');
  writePrompt();

  window.addEventListener('resize', () => addon.fit());

  term.onKey(({ key, domEvent }) => {
    const printable = !domEvent.altKey && !domEvent.ctrlKey && !domEvent.metaKey;
    if (domEvent.key === 'Enter') {
      term.write('\r\n');
      void handleCommand(currentLine);
      if (currentLine.trim()) {
        commandHistory.push(currentLine);
        historyIndex = commandHistory.length;
      }
      currentLine = '';
      writePrompt();
    } else if (domEvent.key === 'Backspace') {
      if (currentLine.length > 0) {
        currentLine = currentLine.slice(0, -1);
        term.write('\b \b');
      }
    } else if (domEvent.key === 'ArrowUp') {
      if (historyIndex > 0) {
        historyIndex--;
        currentLine = commandHistory[historyIndex];
        term.write(`\r\x1b[K`);
        writePrompt();
        term.write(currentLine);
      }
    } else if (domEvent.key === 'ArrowDown') {
      if (historyIndex < commandHistory.length - 1) {
        historyIndex++;
        currentLine = commandHistory[historyIndex];
      } else {
        historyIndex = commandHistory.length;
        currentLine = '';
      }
      term.write(`\r\x1b[K`);
      writePrompt();
      term.write(currentLine);
    } else if (printable) {
      currentLine += key;
      term.write(key);
    }
  });
};

watch(
  () => props.content,
  (newVal) => {
    if (!terminal.value) {
      return;
    }

    terminal.value.clear();
    if (Array.isArray(newVal)) {
      newVal.forEach((line) => terminal.value?.writeln(line));
    } else if (typeof newVal === 'string' && newVal) {
      terminal.value.writeln(newVal);
    }
    terminal.value.writeln('');
    writePrompt();
  }
);

onMounted(() => {
  bootstrapTerminal();

  emitter.on('terminal-visible', (value) => {
    visible.value = value;
    if (value) {
      terminal.value?.focus();
    }
  });

  emitter.on('terminal', (payload) => {
    if (!terminal.value) return;
    if (payload.type === 'command') {
      terminal.value.writeln(payload.content);
    } else if (payload.type === 'observation') {
      terminal.value.writeln(`${payload.content}\n`);
      writePrompt();
    }
  });
});
</script>

<style scoped lang="scss">
.container {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin: 20px;
  border-radius: 12px;
  background-color: #1e1e1e;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.terminal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #2d2d2d;
  color: #fff;
  cursor: pointer;
  user-select: none;
  border-bottom: 1px solid #3d3d3d;
}

.terminal-container {
  display: flex;
  flex: 1;
  width: 100%;
  padding: 10px;
}
</style>
