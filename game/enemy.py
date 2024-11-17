import pygame as pg


class Enemy(pg.sprite.Sprite):

    def __init__(
        self, 
        width: int,
        height: int,
        color: tuple[int, int, int],
        pos: tuple[int, int],
        track: int,
        destroyable: bool = True
    ) -> None:
        super().__init__()
        if track == 0 and not destroyable:
            path = "../game/assets/ufo_lewy.png"
        if track == 1 and not destroyable:
            path = "../game/assets/ufo_prawe.png"
        if track == 0 and destroyable:
            path = "../game/assets/szarak_lewy.png"
        if track == 1 and destroyable:
            path = "../game/assets/szarak_prawo.png"
        self.path = path
        print(path, track, destroyable)
        self.png = pg.image.load(path).convert_alpha()
        self.image = pg.transform.scale(self.png, (width, height))

        # self.image = pg.Surface([width, height])

        self.size: list[float] = [width, height]


        pg.draw.rect(self.image, color, pg.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()
        self.image.blit(self.png, self.rect)

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.destroyable = destroyable
        self.track = track
        self._x_offset = 0
        self.now = True

    def _scale_size(self, fasten: bool) -> None:
        self._x_offset += 0.05

        if fasten:
            self.rect.x += 1 if self.track == 1 else -2
            self.rect.y += 1


        self.size[0] += 0.15
        self.size[1] = self.size[0] * 2

        self.image = pg.transform.scale(self.image, self.size)
        self.rect.width = int(self.size[0])
        self.rect.height = int(self.size[1])

        

        if self._x_offset >= 1 and self.track == 0:
            self.rect.x -= 4
            self._x_offset = 0
        
        if self._x_offset >= 1 and self.track == 1:
            self.rect.x += 2
            self._x_offset = 0
        



    def update(self, fasten: bool = True) -> None:
        super().update()

        self._scale_size(fasten)
        

    def draw(self, screen: pg.Surface) -> None:
        self.png = pg.image.load(self.path).convert_alpha()
        self.image = pg.transform.scale(self.png, self.size)
        screen.blit(self.image, self.rect)
