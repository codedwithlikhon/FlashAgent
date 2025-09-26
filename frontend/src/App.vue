<template>
  <div class="layout">
    <main-header />
    <div class="content">
      <mcp-manager class="panel" />
      <search-results class="panel" :search-results="searchResults" />
      <terminal-panel class="panel" />
      <vscode-panel class="panel" />
    </div>
  </div>
</template>

<script setup lang="ts">
import MainHeader from './components/frontend/MainHeader.vue';
import McpManager from './components/frontend/mcp/McpManager.vue';
import SearchResults from './components/frontend/SearchResultList.vue';
import TerminalPanel from './components/frontend/TerminalPanel.vue';
import VsCodePanel from './components/frontend/VsCodePanel.vue';

const searchResults = [
  {
    title: 'FlashAgent – Browser automation experiments',
    url: 'https://example.com/flashagent',
    content: 'A curated workspace showing how Browser-Use agents combine with Playwright and MCP tooling.',
  },
  {
    title: 'Manus AI sandboxing patterns',
    url: 'https://example.com/manus',
    content: 'Sandbox each conversation with isolated containers and enforce least privilege policies.',
  },
];
</script>

<style scoped lang="scss">
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  padding: 1.5rem;
}

.panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  min-height: 260px;
  display: flex;
  flex-direction: column;
}
</style>
