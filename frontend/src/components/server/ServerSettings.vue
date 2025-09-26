<template>
  <div class="mcp-server-content" v-if="server">
    <div class="mcp-server-content-header">
      <div class="header-left">
        <span class="mcp-server-content-header-title">{{ server.name }}</span>
        <DeleteOutlined class="mcp-server-content-header-delete-button" @click="showDeleteConfirm(server.id)" />
      </div>
      <div class="header-right">
        <a-switch v-model:checked="server.activate" class="mcp-server-content-header-activate-switch" :loading="loading" @change="handleActivateChange" />
        <div class="mcp-server-content-header-save-button-container">
          <a-button type="primary" @click="$emit('save')" class="mcp-server-content-header-save-button">
            <SaveOutlined />
            {{ $t('setting.mcpService.save') }}
          </a-button>
        </div>
      </div>
    </div>

    <div class="mcp-server-content-main">
      <div class="mcp-server-content-main-name mcp-server-content-main-item">
        <span>{{ $t('setting.mcpService.name') }}</span>
        <a-input v-model:value="server.name" :placeholder="$t('setting.mcpService.namePlaceholder')" class="text-item input" />
      </div>
      <div class="mcp-server-content-main-description mcp-server-content-main-item">
        <span>{{ $t('setting.mcpService.description') }}</span>
        <a-textarea v-model:value="server.description" :rows="4" :placeholder="$t('setting.mcpService.descriptionPlaceholder')" class="text-item" />
      </div>
      <div class="mcp-server-content-main-type mcp-server-content-main-item">
        <span>{{ $t('setting.mcpService.type') }}</span>
        <a-radio-group v-model:value="server.type" name="radioGroup" class="input radio">
          <a-radio value="stdio">{{ $t('setting.mcpService.stdio') }}</a-radio>
          <a-radio value="sse">{{ $t('setting.mcpService.sse') }}</a-radio>
          <a-radio value="streamableHttp">{{ $t('setting.mcpService.streamableHttp') }}</a-radio>
        </a-radio-group>
      </div>
      <div class="mcp-server-content-main-command mcp-server-content-main-item" v-if="server.type === 'stdio'">
        <span>{{ $t('setting.mcpService.command') }}</span>
        <a-input v-model:value="server.command" :placeholder="$t('setting.mcpService.commandPlaceholder')" class="text-item input" />
      </div>
      <div class="mcp-server-content-main-url mcp-server-content-main-item" v-if="server.type === 'sse' || server.type === 'streamableHttp'">
        <span>{{ $t('setting.mcpService.url') }}</span>
        <a-input
          v-model:value="server.url"
          :placeholder="$t('setting.mcpService.url')"
          class="text-item input"
          @update:value="handleUpdateServer({ url: $event })"
        />
      </div>
      <div class="mcp-server-content-main-args mcp-server-content-main-item">
        <span>{{ $t('setting.mcpService.args') }}</span>
        <a-textarea v-model:value="argsText" :rows="4" :placeholder="$t('setting.mcpService.argsPlaceholder')" class="text-item" @update:value="handleArgsChange" />
      </div>
      <div class="mcp-server-content-main-env mcp-server-content-main-item">
        <span>{{ $t('setting.mcpService.env') }}</span>
        <a-textarea v-model:value="envText" :rows="4" :placeholder="$t('setting.mcpService.envPlaceholder')" class="text-item" @update:value="handleEnvChange" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DeleteOutlined, SaveOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue';
import { message, Modal } from 'ant-design-vue';
import { h, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

import type { McpServer } from '@/store/modules/server';
import * as mcpService from '@/services/mcp';

const emit = defineEmits<{
  (event: 'update:server', server: McpServer): void;
  (event: 'save'): void;
  (event: 'delete', serverId: string): void;
}>();

const props = defineProps<{ server: McpServer }>();

const { t } = useI18n();
const argsText = ref('');
const envText = ref('');
const loading = ref(false);

const validateServerConnection = async () => {
  try {
    loading.value = true;
    const result = await mcpService.connect(props.server);
    return result.ok;
  } catch (error: unknown) {
    const err = error as Error;
    message.error(err.message || t('mcpService.connectionFailed'));
    return false;
  } finally {
    loading.value = false;
  }
};

const updateServer = (data: Partial<McpServer>) => {
  emit('update:server', { ...props.server, ...data });
};

const handleActivateChange = async (checked: boolean) => {
  if (checked) {
    const isValid = await validateServerConnection();
    if (!isValid) {
      message.error(t('mcpService.connectionFailed'));
      updateServer({ activate: false });
      return;
    }
  }
  updateServer({ activate: checked });
  emit('save');
};

const handleArgsChange = (value: string) => {
  const args = value
    .split('\n')
    .map((arg) => arg.trim())
    .filter(Boolean);
  updateServer({ args });
};

const handleEnvChange = (value: string) => {
  const envEntries = value
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => line.split('='));

  const env: Record<string, string> = {};
  envEntries.forEach(([key, ...rest]) => {
    const trimmedKey = key?.trim();
    const trimmedValue = rest.join('=').trim();
    if (trimmedKey && trimmedValue) {
      env[trimmedKey] = trimmedValue;
    }
  });
  updateServer({ env });
};

const formatArgsText = (args: string[]) => args.join('\n');

const formatEnvText = (env: Record<string, string>) =>
  Object.entries(env)
    .map(([key, value]) => `${key}=${value}`)
    .join('\n');

const showDeleteConfirm = (serverId: string) => {
  Modal.confirm({
    title: t('setting.mcpService.deleteConfirmTitle'),
    icon: () => h(ExclamationCircleOutlined, { style: 'color: #ff4d4f' }),
    content: t('setting.mcpService.deleteConfirmContent'),
    okText: t('common.yes'),
    okType: 'danger',
    cancelText: t('common.cancel'),
    onOk() {
      emit('delete', serverId);
    }
  });
};

const handleUpdateServer = (data: Partial<McpServer>) => {
  updateServer(data);
};

watch(
  () => props.server,
  (newServer) => {
    argsText.value = formatArgsText(newServer.args || []);
    envText.value = formatEnvText(newServer.env || {});
  },
  { immediate: true, deep: true }
);
</script>

<style scoped>
.mcp-server-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.mcp-server-content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: white;
  border-radius: 8px;
  margin-bottom: 16px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-right {
  display: flex;
  align-items: center;
}

.mcp-server-content-header-title {
  font-size: 16px;
  font-weight: 500;
  margin-right: 16px;
}

.mcp-server-content-header-delete-button {
  color: #ff4d4f;
  font-size: 16px;
  cursor: pointer;
}

.mcp-server-content-header-save-button-container {
  margin-left: 16px;
}

.mcp-server-content-main {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
}

.mcp-server-content-main-item {
  margin-bottom: 24px;
}

.mcp-server-content-main-item > span {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
}

.text-item {
  width: 100%;
}

.radio {
  display: block;
  line-height: 32px;
}
</style>
