<template>
  <div class="files-container">
    <div class="file-tree-container">
      <div v-for="item in items" :key="item" class="file-item">
        <div :class="['file-entry', { 'is-directory': isDirectory(item) }]" @click.stop="handleClick(item)">
          <span class="file-icon">{{ getFileIcon(item) }}</span>
          <span class="file-name">{{ getFileName(item) }}</span>
        </div>
        <div v-if="isDirectory(item) && expandedDirs[fullPath(item)]" class="subdirectory">
          <FileTree
            :items="subDirectories[fullPath(item)] || []"
            :base-path="fullPath(item)"
            :conversation-id="conversationId"
            @item-click="$emit('item-click', $event)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';

import * as service from '@/services/workspace';
import emitter from '@/utils/emitter';

const props = defineProps({
  items: {
    type: Array as () => string[],
    default: () => []
  },
  basePath: {
    type: String,
    default: ''
  },
  conversationId: {
    type: String,
    required: true
  }
});

const expandedDirs = reactive<Record<string, boolean>>({});
const subDirectories = reactive<Record<string, string[]>>({});

function isDirectory(path: string) {
  return path.endsWith('/');
}

function getFileName(path: string) {
  const cleanPath = path.replace(/\/$/, '');
  const parts = cleanPath.split('/');
  return parts[parts.length - 1] || cleanPath;
}

function fullPath(item: string) {
  return item;
}

function getFileIcon(path: string) {
  if (isDirectory(path)) {
    return expandedDirs[fullPath(path)] ? '📂' : '📁';
  }
  const extension = path.split('.').pop()?.toLowerCase();
  switch (extension) {
    case 'js':
      return '📜';
    case 'vue':
      return '🟢';
    case 'html':
      return '🌐';
    case 'css':
      return '🎨';
    case 'json':
      return '⚙️';
    case 'md':
      return '📝';
    default:
      return '📄';
  }
}

async function handleClick(item: string) {
  const path = fullPath(item);
  if (isDirectory(item)) {
    if (!expandedDirs[path]) {
      expandedDirs[path] = true;
      await loadSubDirectory(path);
    } else {
      expandedDirs[path] = false;
    }
  } else {
    emitter.emit('file-path', path);
    emit('item-click', path);
  }
}

async function loadSubDirectory(dirPath: string) {
  if (dirPath in subDirectories) {
    return;
  }
  const result = await service.getFiles(props.conversationId, dirPath);
  subDirectories[dirPath] = Array.isArray(result) ? result : [];
}

const emit = defineEmits<{
  (event: 'item-click', path: string): void;
}>();
</script>

<style scoped>
.files-container {
  display: flex;
  flex-direction: column;
}

.file-entry {
  display: flex;
  align-items: center;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  padding: 4px 6px;
}

.file-entry:hover {
  background-color: #646464;
  color: #fff;
}

.file-icon {
  margin-right: 6px;
  width: 16px;
  text-align: center;
}

.subdirectory {
  margin-left: 16px;
  border-left: 1px dashed #ccc;
  padding-left: 8px;
}
</style>
