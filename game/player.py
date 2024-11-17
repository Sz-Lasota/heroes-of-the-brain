import pygame as pg

COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)


class Player(pg.sprite.Sprite):

    def __init__(self, width: int, height: int, color: tuple[int, int, int], pos: tuple[int, int], tracks = (161, 411)) -> None:
        super().__init__()
        self.png = pg.image.load("../game/assets/player.png").convert_alpha()
        self.size = width, height
        self.path = "../game/assets/player.png"
        self.image = pg.transform.scale(self.png, (width, height))

        pg.draw.rect(self.image, color, pg.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()
        self.image.blit(self.png, self.rect)

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.track = 0
        self._tracks = tracks

    def change_track(self, direction: int) -> None:
        if self.track == direction:
            return

        self.track = direction
        self.rect.x = self._tracks[self.track]

    
    def update(self) -> None:
        super().update()

    def draw(self, screen: pg.Surface) -> None:
        self.png = pg.image.load(self.path).convert_alpha()
        self.image = pg.transform.scale(self.png, self.size)
        screen.blit(self.image, self.rect)

    