<template>
  <div class="files-container">
    <div v-for="item in items" :key="item" class="file-item" @click="$emit('select', item)">
      <span class="file-icon">{{ getIcon(item) }}</span>
      <span class="file-name">{{ item }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ items: string[] }>();
const emit = defineEmits<{ select: [file: string] }>();

function getIcon(path: string) {
  if (path.endsWith('.py')) return '🐍';
  if (path.endsWith('.vue')) return '🟢';
  if (path.endsWith('.md')) return '📄';
  return '📁';
}
</script>

<style scoped lang="scss">
.files-container {
  display: flex;
  flex-direction: column;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 0.4rem 0.6rem;
  cursor: pointer;
  gap: 0.5rem;
  border-radius: 6px;
}

.file-item:hover {
  background: rgba(59, 130, 246, 0.1);
}
</style>
