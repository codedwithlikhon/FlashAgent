import type { McpServer } from '@/store/modules/server';

export async function connect(server: McpServer) {
  console.debug('Attempting to connect to MCP server', server);
  await new Promise((resolve) => setTimeout(resolve, 300));
  const ok = Boolean(server.url || server.command);
  if (!ok) {
    throw new Error('Server configuration is incomplete.');
  }
  return { ok };
}
