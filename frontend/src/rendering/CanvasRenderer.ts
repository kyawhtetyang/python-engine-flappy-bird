import type { GameSnapshot } from '../state/GameSnapshot';
import { SpriteRenderer } from './SpriteRenderer';

const BACKGROUND_SRC = new URL('../../assets/images/background.png', import.meta.url).href;
const BIRD_SRC = new URL('../../assets/images/bird.png', import.meta.url).href;
const BASE_SRC = new URL('../../assets/images/base.png', import.meta.url).href;
const PIPE_SRC = new URL('../../assets/images/pipe-green.png', import.meta.url).href;
const GAME_OVER_SRC = new URL('../../assets/images/gameover.png', import.meta.url).href;

export class CanvasRenderer {
  private readonly context: CanvasRenderingContext2D;
  private readonly width: number;
  private readonly height: number;
  private readonly birdWidth = 34;
  private readonly birdHeight = 24;
  private readonly groundHeight = 112;
  private readonly background = new SpriteRenderer(BACKGROUND_SRC);
  private readonly bird = new SpriteRenderer(BIRD_SRC);
  private readonly base = new SpriteRenderer(BASE_SRC);
  private readonly pipe = new SpriteRenderer(PIPE_SRC);
  private readonly gameOver = new SpriteRenderer(GAME_OVER_SRC);

  constructor(private readonly canvas: HTMLCanvasElement) {
    const context = canvas.getContext('2d');
    if (!context) {
      throw new Error('2D canvas context not available');
    }

    this.context = context;
    this.width = canvas.width;
    this.height = canvas.height;
  }

  render(snapshot: GameSnapshot): void {
    const drewBackground = this.background.draw(this.context, 0, 0, this.width, this.height);
    if (!drewBackground) {
      this.context.fillStyle = '#70c5ce';
      this.context.fillRect(0, 0, this.width, this.height);
    }

    const groundY = this.height - this.groundHeight;
    const drewBase = this.base.draw(this.context, 0, groundY, this.width, this.groundHeight);
    if (!drewBase) {
      this.context.fillStyle = '#ded895';
      this.context.fillRect(0, groundY, this.width, this.groundHeight);
    }

    const drewBird = this.bird.draw(
      this.context,
      snapshot.bird.x,
      snapshot.bird.y,
      this.birdWidth,
      this.birdHeight,
    );
    if (!drewBird) {
      this.context.fillStyle = '#f7d84a';
      this.context.fillRect(
        snapshot.bird.x,
        snapshot.bird.y,
        this.birdWidth,
        this.birdHeight,
      );
    }

    if ('pipes' in snapshot && Array.isArray(snapshot.pipes)) {
      for (const pipe of snapshot.pipes) {
        const topHeight = pipe.gapY;
        const bottomY = pipe.gapY + pipe.gapSize;
        const bottomHeight = groundY - bottomY;

        const drewTop = this.pipe.draw(this.context, pipe.x, 0, pipe.width, topHeight);
        if (!drewTop) {
          this.context.fillStyle = '#54b547';
          this.context.fillRect(pipe.x, 0, pipe.width, topHeight);
        }

        const drewBottom = this.pipe.draw(
          this.context,
          pipe.x,
          bottomY,
          pipe.width,
          bottomHeight,
        );
        if (!drewBottom) {
          this.context.fillStyle = '#54b547';
          this.context.fillRect(pipe.x, bottomY, pipe.width, bottomHeight);
        }
      }
    }

    this.context.fillStyle = '#1f2937';
    this.context.font = '20px monospace';
    this.context.fillText(`Score: ${snapshot.score}`, 16, 112);
    this.context.fillText(`Status: ${snapshot.status}`, 16, 28);
    this.context.fillText(`Y: ${snapshot.bird.y.toFixed(2)}`, 16, 56);
    this.context.fillText(`VY: ${snapshot.bird.velocityY.toFixed(2)}`, 16, 84);

    if (snapshot.status === 'GAME_OVER') {
      const overlayWidth = 192;
      const overlayHeight = 42;
      const overlayX = (this.width - overlayWidth) / 2;
      const overlayY = 140;
      const drewGameOver = this.gameOver.draw(
        this.context,
        overlayX,
        overlayY,
        overlayWidth,
        overlayHeight,
      );
      if (!drewGameOver) {
        this.context.fillStyle = '#111827';
        this.context.fillRect(overlayX, overlayY, overlayWidth, overlayHeight);
        this.context.fillStyle = '#ffffff';
        this.context.fillText('GAME OVER', overlayX + 18, overlayY + 28);
      }
    }
  }
}
