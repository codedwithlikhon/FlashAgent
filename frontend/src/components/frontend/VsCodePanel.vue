<template>
  <div class="vscode-container">
    <div class="vscode-header">
      <span>Workspace Explorer</span>
      <a-button size="small" @click="openVsCode">Open in VS Code</a-button>
    </div>
    <div class="vscode-body">
      <file-tree class="file-menu" :items="files" @select="handleSelect" />
      <div class="file-preview">
        <pre><code ref="codeRef" :class="codeLanguage" v-html="highlighted"></code></pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import hljs from 'highlight.js/lib/core';
import javascript from 'highlight.js/lib/languages/javascript';
import typescript from 'highlight.js/lib/languages/typescript';
import python from 'highlight.js/lib/languages/python';
import FileTree from './vscode/FileTree.vue';

hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('typescript', typescript);
hljs.registerLanguage('python', python);

const files = [
  'README.md',
  'examples/advanced_browser_use_playwright.py',
  'frontend/src/components/frontend/TerminalPanel.vue',
];

const codeRef = ref<HTMLElement | null>(null);
const codeLanguage = ref('plaintext');
const highlighted = ref('Select a file to preview.');

const fileContents: Record<string, { language: string; content: string }> = {
  'README.md': {
    language: 'markdown',
    content: '# FlashAgent\nBrowser automation examples with Browser-Use and Playwright.',
  },
  'examples/advanced_browser_use_playwright.py': {
    language: 'python',
    content: 'async def main():\n    print("Demo")',
  },
  'frontend/src/components/frontend/TerminalPanel.vue': {
    language: 'xml',
    content: '<template>\n  <div>Terminal</div>\n</template>',
  },
};

function openVsCode() {
  window.open('http://localhost:3000', '_blank');
}

function handleSelect(file: string) {
  const info = fileContents[file];
  if (!info) {
    highlighted.value = 'No preview available';
    return;
  }
  codeLanguage.value = info.language;
  const { value } = hljs.highlight(info.content, { language: info.language });
  highlighted.value = value;
}
</script>

<style scoped lang="scss">
.vscode-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.vscode-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #1f2937;
  color: #fff;
}

.vscode-body {
  display: flex;
  flex: 1;
  background: #e5e7eb;
}

.file-menu {
  width: 200px;
  border-right: 1px solid #d1d5db;
  background: #f3f4f6;
}

.file-preview {
  flex: 1;
  padding: 1rem;
  overflow: auto;
  background: #fff;
}

pre {
  margin: 0;
}
</style>
