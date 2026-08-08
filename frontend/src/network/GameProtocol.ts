export type ClientMessageType = 'START' | 'FLAP' | 'RESTART';

export interface ClientMessage {
  type: ClientMessageType;
}
