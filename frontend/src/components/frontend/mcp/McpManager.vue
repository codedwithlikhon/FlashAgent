<template>
  <div class="mcp-manager-container">
    <div class="top-action-bar">
      <h2 class="title">{{ $t('setting.mcpService.title') }}</h2>
      <div class="actions">
        <a-button @click="showImportModal">
          <template #icon>
            <ImportOutlined />
          </template>
          {{ $t('setting.mcpService.importFromJson') }}
        </a-button>
        <a-button type="primary" @click="handleAddServer" style="margin-left: 8px">
          <template #icon>
            <PlusOutlined />
          </template>
          {{ $t('setting.mcpService.addMcpServer') }}
        </a-button>
      </div>
    </div>

    <div class="main-content">
      <div class="server-list-panel">
        <ServerList :servers="servers" :selectedServerId="selectedServer?.id" @select="handleSelect" />
      </div>
      <div class="server-settings-panel">
        <ServerSettings
          v-if="selectedServer"
          :server="selectedServer"
          @update:server="handleUpdateServer"
          @save="handleSave"
          @delete="handleDelete"
        />
        <div v-else class="no-server-placeholder">
          <div class="placeholder-content">
            <div class="placeholder-icon">
              <CodeOutlined />
            </div>
            <p class="placeholder-text">{{ $t('setting.mcpService.noServerSelected') }}</p>
          </div>
        </div>
      </div>
    </div>

    <a-modal v-model:visible="importModalVisible" :title="$t('setting.mcpService.importModalTitle')" @ok="handleImportOk">
      <pre>{{ exampleJson }}</pre>
      <a-textarea v-model:value="importJsonText" :rows="6" />
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { PlusOutlined, CodeOutlined, ImportOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { useI18n } from 'vue-i18n';

import ServerList from './ServerList.vue';
import ServerSettings from './ServerSettings.vue';
import { useServerStore } from '../../../store/modules/server';

const { t } = useI18n();
const serverStore = useServerStore();
const servers = computed(() => serverStore.servers);
const selectedServer = ref(serverStore.servers[0] ?? null);

const importModalVisible = ref(false);
const importJsonText = ref('');

const exampleServer = {
  mcpServers: {
    'amap-amap-sse': {
      url: 'https://mcp.amap.com/sse?key=amap_key',
    },
  },
};
const exampleJson = JSON.stringify(exampleServer, null, 2);

function handleSelect(server: any) {
  selectedServer.value = server;
}

function handleUpdateServer(server: any) {
  selectedServer.value = { ...selectedServer.value, ...server };
}

function handleSave() {
  if (selectedServer.value) {
    serverStore.updateServer(selectedServer.value);
    message.success(t('setting.mcpService.saved'));
  }
}

function handleDelete(id: string) {
  serverStore.deleteServer(id);
  message.success(t('setting.mcpService.deleted'));
}

function handleAddServer() {
  const server = serverStore.addServer({
    name: 'MCP Server',
    activate: false,
    type: 'stdio',
    command: '',
    args: [],
    env: {},
  });
  selectedServer.value = server;
}

function showImportModal() {
  importModalVisible.value = true;
  importJsonText.value = '';
}

function resolveType(server: any) {
  if (server.url?.includes('sse')) return 'sse';
  if (server.command?.startsWith('npx') || server.command?.startsWith('uvx')) return 'stdio';
  if (server.url?.includes('mcp')) return 'streamableHttp';
  return 'stdio';
}

function handleImportOk() {
  try {
    const parsed = JSON.parse(importJsonText.value);
    if (parsed.mcpServers) {
      let added = 0;
      Object.entries(parsed.mcpServers).forEach(([name, config]: any) => {
        const type = resolveType(config);
        serverStore.addServer({
          name,
          activate: false,
          type,
          url: config.url,
          command: type === 'stdio' ? config.command : '',
          args: config.args ?? [],
          env: config.env ?? {},
        });
        added += 1;
      });
      message.success(t('setting.mcpService.importSuccess', { count: added }));
    } else {
      message.warn(t('setting.mcpService.invalidJson'));
    }
    importModalVisible.value = false;
  } catch (error) {
    message.error(t('setting.mcpService.invalidJson'));
  }
}

watch(
  () => serverStore.servers,
  (value) => {
    if (!value.length) {
      selectedServer.value = null;
      return;
    }
    if (!selectedServer.value) {
      selectedServer.value = value[0];
      return;
    }
    const current = value.find((item) => item.id === selectedServer.value?.id);
    if (!current) {
      selectedServer.value = value[0];
    }
  },
  { deep: true }
);

onMounted(() => {
  serverStore.fetchServers();
});
</script>

<style scoped lang="scss">
.mcp-manager-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f0f2f5;
}

.top-action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #fff;
  border-bottom: 1px solid #e8e8e8;
}

.title {
  font-size: 1.1rem;
  margin: 0;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
  padding: 24px;
  gap: 24px;
}

.server-list-panel {
  width: 260px;
  flex-shrink: 0;
  background: #fff;
  border-radius: 8px;
  overflow-y: auto;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.server-settings-panel {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  overflow-y: auto;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.no-server-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 50px;
}

.placeholder-content {
  text-align: center;
  color: rgba(0, 0, 0, 0.25);
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 16px;
}
</style>
