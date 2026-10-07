import pygame
import random

PLATFORM_COLOR = (100,80,50)
LAVA_COLOR = (220,60,20)

class Platform:
    def __init__(self, rect, platform_type="normal"):
        self.rect = rect
        self.platform_type = platform_type
        self.crumbling = False
        self.crumble_timer = 0

def generate_platforms(width, base_y, count=30):
    plats = [Platform(pygame.Rect(0, base_y, width, 20), "normal")]
    y = base_y - 110

    for i in range(count):
        w = random.randint(80, 200)
        x = random.randint(0, width - w)

        # Most platforms are normal.
        # Some are crumbling and some are springs.
        platform_type = random.choices(
            ["normal", "crumbling", "spring"],
            weights=[6, 2, 2],
            k=1
        )[0]

        plats.append(
            Platform(
                pygame.Rect(x, y, w, 16),
                platform_type
            )
        )

        y -= random.randint(80, 130)

    return plats

def draw_lava(screen, lava_y, cam_y, width, height, frame):
    import math

    ly = int(lava_y - cam_y)

    if ly < height:
        # lava surface wave
        pts = [(0, ly)]

        for x in range(0, width + 20, 20):
            pts.append(
                (x, ly + int(math.sin(x * 0.08 + frame * 0.1) * 8))
            )

        pts.append((width, height))
        pts.append((0, height))

        pygame.draw.polygon(screen, LAVA_COLOR, pts)

        # glow
        s = pygame.Surface((width, 30), pygame.SRCALPHA)

        for i in range(15):
            pygame.draw.line(
                s,
                (255, 100, 0, max(0, 60 - i * 4)),
                (0, i),
                (width, i),
                1
            )

        screen.blit(s, (0, ly - 15))