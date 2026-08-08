import type { ClientMessage, ClientMessageType } from './GameProtocol';
import type { GameSnapshot } from '../state/GameSnapshot';

export class GameSocket {
  private socket: WebSocket | null = null;
  onSnapshot: ((snapshot: GameSnapshot) => void) | null = null;

  constructor(private readonly url: string) {}

  connect(): void {
    this.socket = new WebSocket(this.url);
    this.socket.addEventListener('message', (event) => {
      const snapshot = JSON.parse(event.data) as GameSnapshot;
      this.onSnapshot?.(snapshot);
    });
  }

  sendMessage(type: ClientMessageType): void {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      return;
    }

    const message: ClientMessage = { type };
    this.socket.send(JSON.stringify(message));
  }
}
