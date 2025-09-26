export interface FileEntry {
  path: string;
  isDirectory: boolean;
}

const sampleFiles: Record<string, string[]> = {
  '': ['src/', 'src/components/', 'src/components/Terminal.vue', 'README.md'],
  'src/': ['src/components/', 'src/main.ts'],
  'src/components/': ['src/components/Terminal.vue'],
};

const fileContents: Record<string, string> = {
  'README.md': '# FlashAgent Workspace\n\nThis is a demo file rendered by the mock workspace service.',
  'src/components/Terminal.vue': '<template>\n  <div>Example component</div>\n</template>\n'
};

export async function getFiles(conversationId: string, dirPath: string) {
  console.debug('getFiles', { conversationId, dirPath });
  return sampleFiles[dirPath] ?? [];
}

export async function getFile(conversationId: string, path: string) {
  console.debug('getFile', { conversationId, path });
  return {
    code: fileContents[path] ?? '// File not found in mock workspace.'
  };
}

export async function getVsCodeUrl(conversationId: string) {
  console.debug('getVsCodeUrl', { conversationId });
  return { vscode_url: 'https://example.com/vscode' };
}
