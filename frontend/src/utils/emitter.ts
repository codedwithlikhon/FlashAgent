import mitt from 'mitt';

type Events = {
  terminal: { type: 'command' | 'observation'; content: string };
  'terminal-visible': boolean;
  'vscode-visible': boolean;
  'file-path': string;
};

const emitter = mitt<Events>();
export default emitter;
