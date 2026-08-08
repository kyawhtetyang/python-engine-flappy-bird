export type GameStatus = 'START' | 'PLAYING' | 'GAME_OVER';

export interface BirdSnapshot {
  x: number;
  y: number;
  velocityY: number;
}

export interface PipeSnapshot {
  id: number;
  x: number;
  gapY: number;
  gapSize: number;
  width: number;
}

export interface GameSnapshot {
  type: 'STATE';
  status: GameStatus;
  score: number;
  bird: BirdSnapshot;
  pipes: PipeSnapshot[];
}
