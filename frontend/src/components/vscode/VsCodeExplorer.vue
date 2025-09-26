<template>
  <div class="vscode-container" v-show="visible">
    <div class="vscode-header">
      <span>File Explorer</span>
      <CloseOutlined @click="visible = false" />
    </div>
    <div class="vscode-explorer">
      <div class="file-list">
        <FileTree class="file-menu" :items="files" :conversation-id="conversationId" @item-click="handleFileClick" />
        <div class="vscode-show">
          <a-button class="vscode-button" type="primary" @click="handleOpenVsCode">
            <template #icon>
              <AlignLeftOutlined />
            </template>
            Open in VSCode
          </a-button>
        </div>
      </div>
      <div class="file-content">
        <pre><code :class="codeLanguage" v-html="highlightedCode"></code></pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AlignLeftOutlined, CloseOutlined } from '@ant-design/icons-vue';
import hljs from 'highlight.js';
import 'highlight.js/styles/vs2015.css';
import { onMounted, ref } from 'vue';

import FileTree from './FileTree.vue';
import emitter from '@/utils/emitter';
import * as workspaceService from '@/services/workspace';
import { useChatStore } from '@/store/modules/chat';

const chatStore = useChatStore();
const conversationId = ref(chatStore.conversationId);
const files = ref<string[]>([]);
const visible = ref(false);
const vscodeUrl = ref('');
const highlightedCode = ref('');
const codeLanguage = ref('');

function getLanguageFromPath(path: string) {
  const ext = path.split('.').pop()?.toLowerCase();
  const map: Record<string, string> = {
    js: 'javascript',
    jsx: 'javascript',
    ts: 'typescript',
    tsx: 'typescript',
    html: 'html',
    css: 'css',
    scss: 'scss',
    less: 'less',
    json: 'json',
    md: 'markdown',
    py: 'python',
    java: 'java',
    cpp: 'cpp',
    c: 'c',
    go: 'go',
    rs: 'rust',
    sh: 'bash',
    yaml: 'yaml',
    yml: 'yaml',
    xml: 'xml',
    sql: 'sql',
    php: 'php',
    rb: 'ruby',
    kt: 'kotlin',
    swift: 'swift',
    dart: 'dart',
    vue: 'javascript'
  };
  return map[ext ?? ''] || 'plaintext';
}

async function loadRootFiles() {
  const result = await workspaceService.getFiles(conversationId.value, '');
  files.value = Array.isArray(result) ? result : [];
}

const handleOpenVsCode = () => {
  if (vscodeUrl.value) {
    window.open(vscodeUrl.value, '_blank');
  }
};

const handleFileClick = async (path: string) => {
  const response = await workspaceService.getFile(conversationId.value, path);
  codeLanguage.value = getLanguageFromPath(path);
  try {
    highlightedCode.value = hljs.highlight(response.code, { language: codeLanguage.value }).value;
  } catch (error) {
    console.error('Highlighting failed', error);
    highlightedCode.value = response.code;
  }
};

emitter.on('vscode-visible', (value) => {
  visible.value = value;
  if (value) {
    void refreshExplorer();
  }
});

emitter.on('file-path', (path) => {
  void handleFileClick(path);
});

async function refreshExplorer() {
  await loadRootFiles();
  const { vscode_url } = await workspaceService.getVsCodeUrl(conversationId.value);
  vscodeUrl.value = vscode_url;
}

onMounted(async () => {
  await refreshExplorer();
});
</script>

<style scoped>
.vscode-container {
  flex: 2;
  height: 100%;
  width: 100%;
  margin-bottom: 20px;
}

.vscode-header {
  margin: 15px;
  padding: 5px;
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  border-radius: 5px;
  background-color: #595959;
  color: #fff;
}

.vscode-explorer {
  display: flex;
  flex-direction: row;
  margin-bottom: 10px;
  background-color: #dbdbdb;
  margin: 15px;
  border-radius: 5px;
  padding: 5px;
  height: calc(100% - 60px);
}

.file-list {
  display: flex;
  flex-direction: column;
  width: 220px;
  background-color: #c9c9c9;
  border-radius: 4px;
  overflow: hidden;
}

.file-content {
  flex: 1;
  background-color: #ffffff;
  padding: 10px;
  border-radius: 5px;
  overflow: auto;
  margin-left: 12px;
}

.file-content pre {
  margin: 0;
}

.file-content code {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre;
}

.vscode-show {
  display: flex;
  justify-content: center;
  padding: 8px;
}

.vscode-button {
  width: 100%;
}
</style>
