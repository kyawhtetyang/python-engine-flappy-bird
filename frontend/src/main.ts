import { GAME_WIDTH, GAME_HEIGHT } from './config/constants';
import { GameSocket } from './network/GameSocket';
import { CanvasRenderer } from './rendering/CanvasRenderer';
import type { GameSnapshot } from './state/GameSnapshot';

const canvas = document.getElementById('game') as HTMLCanvasElement | null;

if (!canvas) {
  throw new Error('Canvas element not found');
}

canvas.width = GAME_WIDTH;
canvas.height = GAME_HEIGHT;

const renderer = new CanvasRenderer(canvas);

const controls = document.createElement('div');
controls.id = 'controls';

const startButton = document.createElement('button');
startButton.textContent = 'START';

const flapButton = document.createElement('button');
flapButton.textContent = 'FLAP';

const restartButton = document.createElement('button');
restartButton.textContent = 'RESTART';

controls.append(startButton, flapButton, restartButton);
document.body.appendChild(controls);

const status = document.createElement('pre');
status.id = 'snapshot-status';
status.textContent = 'Connecting to ws://127.0.0.1:8000/ws';
document.body.appendChild(status);

const socket = new GameSocket('ws://127.0.0.1:8000/ws');
socket.onSnapshot = (snapshot: GameSnapshot) => {
  status.textContent = JSON.stringify(snapshot, null, 2);
  renderer.render(snapshot);
};
socket.connect();

startButton.addEventListener('click', () => {
  socket.sendMessage('START');
});

flapButton.addEventListener('click', () => {
  socket.sendMessage('FLAP');
});

restartButton.addEventListener('click', () => {
  socket.sendMessage('RESTART');
});

canvas.addEventListener('click', () => {
  socket.sendMessage('FLAP');
});

window.addEventListener('keydown', (event) => {
  if (event.code === 'Space') {
    event.preventDefault();
    socket.sendMessage('FLAP');
  }
});
