<template>
  <div class="container">
    <div ref="terminalRef" class="terminal-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { Terminal } from '@xterm/xterm';
import '@xterm/xterm/css/xterm.css';

import emitter from '@/utils/emitter';

const terminalRef = ref<HTMLDivElement | null>(null);
const terminal = ref<Terminal>();
let currentLine = '';
const commandHistory: string[] = [];
let historyIndex = -1;

const writePrompt = () => {
  terminal.value?.write('\n$ ');
};

const handleCommand = async (command: string) => {
  switch (command.trim()) {
    case 'clear':
      terminal.value?.clear();
      break;
    case 'history':
      commandHistory.forEach((cmd, index) => terminal.value?.writeln(`${index + 1}  ${cmd}`));
      break;
    default:
      emitter.emit('terminal', { type: 'command', content: command });
  }
};

onMounted(() => {
  const term = new Terminal({
    cursorBlink: true,
    fontSize: 14,
    fontFamily: 'Menlo, Monaco, "Courier New", monospace'
  });
  terminal.value = term;
  term.open(terminalRef.value!);
  writePrompt();

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
        term.write('\r\x1b[K$ ' + currentLine);
      }
    } else if (domEvent.key === 'ArrowDown') {
      if (historyIndex < commandHistory.length - 1) {
        historyIndex++;
        currentLine = commandHistory[historyIndex];
        term.write('\r\x1b[K$ ' + currentLine);
      } else {
        historyIndex = commandHistory.length;
        currentLine = '';
        term.write('\r\x1b[K$ ');
      }
    } else if (printable) {
      currentLine += key;
      term.write(key);
    }
  });
});
</script>

<style scoped lang="scss">
.container {
  display: flex;
  margin: 10px;
  overflow: hidden;
}

.terminal-container {
  display: flex;
  width: 100%;
  height: 100%;
  transition: height 0.3s ease;
  overflow: hidden;
}
</style>
