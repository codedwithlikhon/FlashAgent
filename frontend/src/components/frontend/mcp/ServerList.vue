<template>
  <div class="mcp-server-menu">
    <div v-if="!servers.length" class="no-servers-info">{{ $t('setting.mcpService.noServersAvailable') }}</div>
    <div
      v-else
      v-for="server in servers"
      :key="server.id"
      class="menu-item"
      :class="{ 'menu-item-selected': server.id === selectedServerId }"
      @click="$emit('select', server)"
    >
      <CodeOutlined />
      <span class="menu-item-label">{{ server.name }}</span>
      <span class="menu-item-status" :class="server.activate ? 'menu-item-status-on' : 'menu-item-status-off'" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { CodeOutlined } from '@ant-design/icons-vue';

const props = defineProps<{ servers: any[]; selectedServerId: string | number | null }>();
const emit = defineEmits<{ select: [server: any] }>();
</script>

<style scoped lang="scss">
.mcp-server-menu {
  padding: 16px 8px;
  height: 100%;
}

.no-servers-info {
  padding: 20px;
  text-align: center;
  color: #888;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  font-size: 14px;
  border-radius: 4px;
  margin-bottom: 8px;
}

.menu-item:hover {
  background: #f0f0f0;
}

.menu-item-label {
  margin-left: 10px;
  font-size: 14px;
  flex-grow: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.menu-item-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-left: 16px;
  flex-shrink: 0;
}

.menu-item-status-on {
  background-color: #52c41a;
}

.menu-item-status-off {
  background-color: #d9d9d9;
}

.menu-item-selected {
  background-color: #e6f7ff;
  color: #1890ff;
}
</style>
