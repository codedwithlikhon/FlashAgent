<template>
  <a-layout class="app-layout">
    <a-layout-header class="app-header">FlashAgent Workspace</a-layout-header>
    <a-layout-content class="app-content">
      <div class="content-grid">
        <section class="server-panel">
          <ServerManager />
        </section>
        <section class="workspace-panel">
          <a-row :gutter="[16, 16]">
            <a-col :xs="24" :md="12">
              <SearchResultList :search-results="searchResults" />
            </a-col>
            <a-col :xs="24" :md="12">
              <ImageDisplay :content="imageContent" />
            </a-col>
          </a-row>
          <a-row :gutter="[16, 16]" class="terminal-row">
            <a-col :span="24">
              <TerminalConsole />
            </a-col>
          </a-row>
          <VsCodeExplorer />
        </section>
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';

import ImageDisplay from './components/ImageDisplay.vue';
import SearchResultList from './components/SearchResultList.vue';
import ServerManager from './components/server/ServerManager.vue';
import TerminalConsole from './components/terminal/TerminalConsole.vue';
import VsCodeExplorer from './components/vscode/VsCodeExplorer.vue';
import emitter from './utils/emitter';

interface SearchResult {
  title: string;
  url: string;
  content: string;
}

const searchResults = ref<SearchResult[]>([
  {
    title: 'FlashAgent Documentation',
    url: 'https://example.com/docs',
    content: 'Learn how to operate Browser-Use agents with Ant Design Vue dashboards.'
  },
  {
    title: 'Model Context Protocol Overview',
    url: 'https://example.com/mcp',
    content: 'Integrate MCP services directly into the FlashAgent control plane.'
  },
  {
    title: 'Playwright Integration Tips',
    url: 'https://example.com/playwright',
    content: 'Share CDP sessions between Browser-Use and Playwright for precision automation.'
  }
]);

const imageContent = ref<string[]>([
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/w8AAn0B9oQgVcsAAAAASUVORK5CYII='
]);

onMounted(() => {
  emitter.emit('terminal-visible', true);
  emitter.emit('vscode-visible', true);
});
</script>

<style scoped lang="scss">
.app-layout {
  min-height: 100vh;
}

.app-header {
  color: #fff;
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.app-content {
  padding: 24px;
  background-color: #f5f5f5;
}

.content-grid {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 24px;
}

.server-panel {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.workspace-panel {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.terminal-row {
  min-height: 280px;
}

@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
