export class SpriteRenderer {
  private readonly image: HTMLImageElement;
  private loaded = false;

  constructor(src: string) {
    this.image = new Image();
    this.image.src = src;
    this.image.addEventListener('load', () => {
      this.loaded = true;
    });
  }

  draw(
    context: CanvasRenderingContext2D,
    x: number,
    y: number,
    width: number,
    height: number,
  ): boolean {
    if (!this.loaded) {
      return false;
    }

    context.drawImage(this.image, x, y, width, height);
    return true;
  }
}
