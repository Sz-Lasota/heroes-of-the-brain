from dataclasses import dataclass
import random
import pygame

from game.player import Player
from game.enemy import Enemy

pygame.init()

@dataclass
class Assets:
    screen_size = (704, 896)
    white = (200, 200, 200)
    black = (0, 0, 0)
    tracks = 161, 411

    background_path = "../game/assets/background.png"
    background = bg = pygame.image.load(background_path)

    surface_color = (0, 0, 0)

    player_settings = {
        "width": 160,
        "height": 300,
        "color": (255, 100, 98),
        "pos": (tracks[0], screen_size[1] - 350),
        "tracks": tracks,
    }

    enemy_colors = {False: (79, 79, 79), True: (57, 29, 190)}
    enemy_settings = {
        "width": 20,
        "height": 30,
        "pos": (343, 506),
    }

    score = 0
    font = pygame.font.SysFont("Arial", 24)


class Game:

    def __init__(self, move) -> None:
        # Pygame
        self.assets = Assets()
        self.screen = pygame.display.set_mode(self.assets.screen_size)

        self.screen.fill(self.assets.surface_color)
        self.move = move

        # Runtime
        self.running = True
        self.counter = 0

        # Sprites
        self.player = Player(**self.assets.player_settings)
        self.player_group = pygame.sprite.Group()

        self._enemy = None

        pygame.display.flip()

    def draw_text(self, text, font, color, x, y):
        label = font.render(text, True, color)
        self.screen.blit(label, (x, y))

    def _parse_input(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        if self.counter > 30:
            self.counter =0
            self.move()
        self.counter += 1

    def player_left(self) -> None:
        print("Left")
        self.player.change_track(0)

    def player_right(self) -> None:
        print("Right")
        self.player.change_track(1)

    def player_shoot(self) -> None:
        print("Shoot")
        if (
            self._enemy is not None
            and self._enemy.track == self.player.track
            and self._enemy.destroyable
        ):
            self._enemy = None
            self.assets.score += 1

    def _draw(self) -> None:
        self.screen.blit(self.assets.background, (0, 0))

        if self._enemy is not None:
            self._enemy.draw(self.screen)

        self.player.draw(self.screen)
        self.draw_text(f"Score: {self.assets.score}", self.assets.font, self.assets.white, 10, 10)
        pygame.display.flip()

    def _provide_enemy(self, probability: float) -> None:
        if random.random() > probability:
            return
        destr = random.choice([True, False])
        self._enemy = Enemy(**self.assets.enemy_settings, 
                            track=random.choice([0, 1]), destroyable=destr, 
                            color=self.assets.enemy_colors[destr])

    def run(self) -> None:
        clock = pygame.time.Clock()
        enemy_prb = 0.05

        while self.running:
            clock.tick(60)

            self._parse_input(pygame.event.get())

            self.player.update()

            if self._enemy is not None:
                enemy_prb = 0.05
                self._enemy.update(fasten=self._enemy.rect.y + self._enemy.rect.height > self.assets.screen_size[1] - 255)

                if (
                    self._enemy.rect.y + self._enemy.rect.height
                    > self.assets.screen_size[1] - 190
                    and self._enemy.track == self.player.track
                ):
                    
                    self.running = False
                    pass

                if (
                    self._enemy.rect.y + self._enemy.rect.height
                    > self.assets.screen_size[1] - 55
                ):
                    self._enemy = None

            self._draw()
            if self._enemy is None:
                self._provide_enemy(enemy_prb / 100)
                enemy_prb += 0.05
        self._exit()

    def _exit(self) -> None:
        self.screen.fill(self.assets.black)
        self.draw_text(f"Game Over! Final Score: {self.assets.score}", self.assets.font, self.assets.white, self.assets.screen_size[0] // 2 - 100, self.assets.screen_size[1] // 2)
        pygame.display.flip()

        pygame.time.wait(3000)

        pygame.quit()
