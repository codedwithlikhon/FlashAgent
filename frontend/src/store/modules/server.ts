import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

export interface McpServer {
  id: string;
  name: string;
  description: string;
  activate: boolean;
  type: 'stdio' | 'sse' | 'streamableHttp';
  command: string;
  registryUrl: string;
  url: string;
  args: string[];
  env: Record<string, string>;
}

const STORAGE_KEY = 'flashagent.mcpServers';

function createId() {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
    return crypto.randomUUID();
  }
  return Math.random().toString(36).slice(2, 11);
}

function loadFromStorage(): McpServer[] {
  if (typeof window === 'undefined') {
    return [];
  }

  const stored = window.localStorage.getItem(STORAGE_KEY);
  if (!stored) return [];

  try {
    const parsed = JSON.parse(stored) as McpServer[];
    if (Array.isArray(parsed)) {
      return parsed.map((server) => ({
        ...server,
        id: server.id || createId()
      }));
    }
    return [];
  } catch (error) {
    console.error('Failed to parse stored servers', error);
    return [];
  }
}

function persist(servers: McpServer[]) {
  if (typeof window === 'undefined') {
    return;
  }
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(servers));
}

export const useServerStore = defineStore('server', () => {
  const servers = ref<McpServer[]>([]);

  const fetchServers = () => {
    servers.value = loadFromStorage();
  };

  const addServer = (server: Omit<McpServer, 'id'>) => {
    const entry: McpServer = { ...server, id: createId() };
    servers.value.push(entry);
    persist(servers.value);
  };

  const updateServer = (server: McpServer) => {
    const index = servers.value.findIndex((item) => item.id === server.id);
    if (index >= 0) {
      servers.value[index] = { ...server };
      persist(servers.value);
    }
  };

  const deleteServer = (id: string) => {
    servers.value = servers.value.filter((server) => server.id !== id);
    persist(servers.value);
  };

  const activeServers = computed(() => servers.value.filter((server) => server.activate));

  return {
    servers,
    fetchServers,
    addServer,
    updateServer,
    deleteServer,
    activeServers
  };
});
