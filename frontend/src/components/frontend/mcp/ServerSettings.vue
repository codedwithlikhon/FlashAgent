<template>
  <div class="mcp-server-content" v-if="server">
    <div class="mcp-server-content-header">
      <div class="header-left">
        <span class="mcp-server-content-header-title">{{ server.name }}</span>
        <DeleteOutlined class="mcp-server-content-header-delete-button" @click="emit('delete', server.id)" />
      </div>
      <div class="header-right">
        <a-switch v-model:checked="server.activate" class="mcp-server-content-header-activate-switch" />
        <div class="mcp-server-content-header-save-button-container">
          <a-button type="primary" @click="emit('save')" class="mcp-server-content-header-save-button">
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
        <a-textarea
          v-model:value="server.description"
          :rows="4"
          :placeholder="$t('setting.mcpService.descriptionPlaceholder')"
          class="text-item"
        />
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
      <div class="mcp-server-content-main-url mcp-server-content-main-item" v-if="server.type !== 'stdio'">
        <span>{{ $t('setting.mcpService.url') }}</span>
        <a-input v-model:value="server.url" :placeholder="$t('setting.mcpService.url')" class="text-item input" />
      </div>
      <div class="mcp-server-content-main-args mcp-server-content-main-item">
        <span>{{ $t('setting.mcpService.args') }}</span>
        <a-textarea
          v-model:value="argsText"
          :rows="4"
          :placeholder="$t('setting.mcpService.argsPlaceholder')"
          class="text-item"
          @update:value="handleArgsChange"
        />
      </div>
      <div class="mcp-server-content-main-env mcp-server-content-main-item">
        <span>{{ $t('setting.mcpService.env') }}</span>
        <a-textarea
          v-model:value="envText"
          :rows="4"
          :placeholder="$t('setting.mcpService.envPlaceholder')"
          class="text-item"
          @update:value="handleEnvChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DeleteOutlined, SaveOutlined } from '@ant-design/icons-vue';
import { computed, ref, watch } from 'vue';

const props = defineProps<{ server: any }>();
const emit = defineEmits(['update:server', 'save', 'delete']);

const argsText = ref('');
const envText = ref('');

watch(
  () => props.server,
  (server) => {
    if (!server) return;
    argsText.value = Array.isArray(server.args) ? server.args.join('\n') : '';
    envText.value = Object.entries(server.env ?? {})
      .map(([key, value]) => `${key}=${value}`)
      .join('\n');
  },
  { immediate: true, deep: true }
);

function handleArgsChange(value: string) {
  emit('update:server', { ...props.server, args: value ? value.split('\n').filter(Boolean) : [] });
}

function handleEnvChange(value: string) {
  const env: Record<string, string> = {};
  value
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
    .forEach((line) => {
      const [key, ...rest] = line.split('=');
      if (key && rest.length) {
        env[key] = rest.join('=').trim();
      }
    });
  emit('update:server', { ...props.server, env });
}
</script>

<style scoped lang="scss">
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

.mcp-server-content-header-title {
  font-size: 16px;
  font-weight: 500;
  margin-right: 16px;
}

.mcp-server-content-header-delete-button {
  color: #ff4d4f;
  font-size: 16px;
  cursor: pointer;
  margin-left: 8px;
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
