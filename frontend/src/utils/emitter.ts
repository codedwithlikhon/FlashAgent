import mitt from 'mitt';

type Events = {
  'terminal-visible': boolean;
  'vscode-visible': boolean;
  terminal: { type: 'command' | 'observation'; content: string };
  'file-path': string;
};

const emitter = mitt<Events>();

export default emitter;
