<template>
  <div class="container">
    <div class="terminal-header">
      <span>Command Terminal</span>
    </div>
    <div ref="terminalRef" class="terminal-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from 'xterm-addon-fit';
import '@xterm/xterm/css/xterm.css';

const terminalRef = ref<HTMLDivElement | null>(null);

onMounted(() => {
  const terminal = new Terminal({
    cursorBlink: true,
    fontSize: 13,
    fontFamily: 'Geist Mono, Menlo, Monaco, "Courier New", monospace',
    theme: {
      background: '#1e1e1e',
      foreground: '#f9fafb',
      cursor: '#22d3ee',
    },
  });
  const fitAddon = new FitAddon();
  terminal.loadAddon(fitAddon);

  terminal.open(terminalRef.value!);
  fitAddon.fit();
  terminal.writeln('FlashAgent terminal ready. Type `help` for options.');
  terminal.write('$ ');
});
</script>

<style scoped lang="scss">
.container {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  background-color: #1e1e1e;
  overflow: hidden;
}

.terminal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: #111827;
  color: #fff;
}

.terminal-container {
  flex: 1;
  padding: 0.75rem;
}
</style>
