import pygame

SPEED = 4

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vel_y = 0
        self.on_ground = False
        self.color = (60,160,220)

    def update(self, keys, platforms, width):
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -13
            self.on_ground = False
            for p in platforms:
                if (
                    self.rect.colliderect(p.rect)
                    and self.vel_y > 0
                    and self.rect.bottom <= p.rect.top + self.vel_y
                ):
                    self.rect.bottom = p.rect.top

                    if p.platform_type == "spring":
                     self.vel_y = -20
                    self.on_ground = False

            else:
                    self.vel_y = 0
                    self.on_ground = True

                    if p.platform_type == "crumbling" and not p.crumbling:
                        p.crumbling = True
                        p.crumble_timer = 45
    def draw(self, screen, cam_y):
        dr = self.rect.move(0, -int(cam_y))
        pygame.draw.rect(screen, self.color, dr, border_radius=6)
        pygame.draw.circle(screen,(255,220,180),(dr.centerx, dr.top+8),7)
