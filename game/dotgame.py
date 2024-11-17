import pygame
import math
import random
from time import sleep

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pentagon with Radial Lines")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 70  


class Dot:

    def __init__(self, x, y, vec, idx, r=5) -> None:
        self.x, self.y = x, y
        self.vec = vec
        self.radius = r
        self.idx = idx

    def rotate(self, angle, center):
        angle = math.radians(angle)
        vec = [self.x - center[0], self.y - center[1]]
        vec[0], vec[1] = vec[0] * math.cos(angle) - vec[1] * math.sin(angle), vec[0] * math.sin(angle) + vec[1] * math.cos(angle)
        self.x, self.y = vec[0] + center[0], vec[1] + center[1]

    def update(self):
        self.x += self.vec[0]
        self.y += self.vec[1]
        self.radius += 0.05

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), int(self.radius))


class Game:

    def __init__(self) -> None:
        pass

def get_screen_edges():
    
    edges = [
        (WIDTH // 2, 0),            
        (WIDTH, HEIGHT // 2),       
        (WIDTH // 2, HEIGHT),       
        (0, HEIGHT // 2),           
    ]
    return edges

def calc_ref(edges: list[tuple[int, int]], idx: int) -> tuple[int, int]:
    ref1, ref2 = edges[(idx + 2) % len(edges)], edges[(idx + 3) % len(edges)]
    return (ref1[0] + ref2[0]) // 2, (ref1[1] + ref2[1]) // 2



def draw_line(start, ref):
    vec = [start[0] - ref[0], start[1] - ref[1]]
    vec = list(map(lambda it: 10*it, vec))
    ref = (start[0] + vec[0], start[1] + vec[1])
    pygame.draw.line(screen, BLACK, start, ref, 2)


def calc_vec(start, ref):
    vec = [start[0] - ref[0], start[1] - ref[1]]
    vec = list(map(lambda it: -0.01*it, vec))
    return vec


def get_pentagon_points(center, radius, start_angle=0):
    points = []
    for i in range(5):
        angle = math.radians(i * 72 + start_angle)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    return points

def rotate_dots(angl, dots, points):
    for i, dot in enumerate(dots):
        line_idx = dot.idx
        ref = calc_ref(points, line_idx)

        dot.rotate(-angl, CENTER)

        dots[i] = Dot(dot.x, dot.y, calc_vec(points[line_idx], ref), line_idx, dot.radius)        


running = True
assigned_edges = random.sample(get_screen_edges(), 4)  
clock = pygame.time.Clock()
ang = 54

dots = [

]

screen.fill(WHITE)

while running:
    clock.tick(60)


    screen.fill(WHITE)

    pentagon_points = get_pentagon_points(CENTER, RADIUS, ang)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                ang += 72
                pentagon_points = get_pentagon_points(CENTER, RADIUS, ang)
                rotate_dots(-72, dots, pentagon_points)
            if event.key == pygame.K_a:
                ang -= 72
                rotate_dots(+72, dots, pentagon_points)
            if event.key == pygame.K_SPACE:
                line_idx = random.randrange(0, len(pentagon_points))
                ref = calc_ref(pentagon_points, line_idx)
                dots.append(Dot(ref[0], ref[1], calc_vec(pentagon_points[line_idx], ref), line_idx))
            

    
    pygame.draw.polygon(screen, RED, pentagon_points, width=3)

    for dot in dots:
        dot.update()
        dot.draw()
    
    for i, point in enumerate(pentagon_points):
        draw_line(point, calc_ref(pentagon_points, i))


    
    pygame.display.flip()



pygame.quit()
