import { defineStore } from 'pinia';
import { nanoid } from 'nanoid';

interface ServerRecord {
  id: string;
  name: string;
  description?: string;
  activate: boolean;
  type: 'stdio' | 'sse' | 'streamableHttp';
  command?: string;
  url?: string;
  args: string[];
  env: Record<string, string>;
}

const mockServers: ServerRecord[] = [
  {
    id: nanoid(),
    name: 'Local Browser-Use',
    description: 'Runs MCP server via stdio',
    activate: true,
    type: 'stdio',
    command: 'uvx browser-use',
    args: ['--port=9000'],
    env: { OPENAI_API_KEY: 'sk-demo' },
  },
  {
    id: nanoid(),
    name: 'Maps SSE',
    description: 'Streaming server example',
    activate: false,
    type: 'sse',
    url: 'https://mcp.example.com/sse',
    args: [],
    env: {},
  },
];

export const useServerStore = defineStore('servers', {
  state: () => ({ servers: [] as ServerRecord[] }),
  actions: {
    fetchServers() {
      if (!this.servers.length) {
        this.servers = [...mockServers];
      }
    },
    addServer(server: Partial<ServerRecord>) {
      const record: ServerRecord = {
        id: nanoid(),
        name: server.name ?? 'New MCP Server',
        description: server.description ?? '',
        activate: server.activate ?? false,
        type: server.type ?? 'stdio',
        command: server.command ?? '',
        url: server.url ?? '',
        args: server.args ?? [],
        env: server.env ?? {},
      };
      this.servers.push(record);
      return record;
    },
    updateServer(server: ServerRecord) {
      const index = this.servers.findIndex((item) => item.id === server.id);
      if (index >= 0) {
        this.servers[index] = { ...server };
      }
    },
    deleteServer(id: string) {
      this.servers = this.servers.filter((server) => server.id !== id);
    },
  },
});
