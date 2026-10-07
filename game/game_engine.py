import pygame
import random
from game.player import Player
from game.world import generate_platforms, draw_lava, PLATFORM_COLOR

WIDTH,HEIGHT=500,640
FPS=60
BG=(20,15,30)
GROUND_Y=HEIGHT+200

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Lava Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",42,bold=True)
        self.reset()

    def reset(self):
        self.platforms=generate_platforms(WIDTH,GROUND_Y)
        self.player=Player(WIDTH//2-16,GROUND_Y-50)
        self.cam_y=0
        self.lava_y=GROUND_Y+200

        # Normal lava speed
        self.lava_rise=0.4

        # Lava burst/surge state
        self.surge_active=False
        self.surge_timer=0
        self.next_surge=600+random.randint(0,300)

        self.score=0
        self.game_over=False
        self.won=False
        self.top_y=self.platforms[-1].rect.y
        self.frame=0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def update(self):
        if self.game_over or self.won: return

        keys=pygame.key.get_pressed()
        self.player.update(keys,self.platforms,WIDTH)

        # Update crumbling platforms
        for p in self.platforms[:]:
            if p.crumbling:
                p.crumble_timer -= 1

                if p.crumble_timer <= 0:
                    self.platforms.remove(p)

        target=self.player.rect.centery-HEIGHT//2
        if target<self.cam_y: self.cam_y=target

        # Gradually increase normal lava speed
        self.lava_rise=min(1.2,self.lava_rise+0.0003)

        # Start an occasional lava burst
        if not self.surge_active:
            self.next_surge-=1

            if self.next_surge<=0:
                self.surge_active=True
                self.surge_timer=120

        # Apply temporary surge speed
        if self.surge_active:
            current_lava_rise=self.lava_rise*2.0
            self.surge_timer-=1

            if self.surge_timer<=0:
                self.surge_active=False
                self.next_surge=600+random.randint(0,300)
        else:
            current_lava_rise=self.lava_rise

        # Move the lava
        self.lava_y-=current_lava_rise

        self.score=max(0,(GROUND_Y-self.player.rect.y)//10)
        self.frame+=1

        if self.player.rect.bottom>=self.lava_y:
            self.game_over=True

        if self.player.rect.top<=self.top_y-20:
            self.won=True

    def draw(self):
        self.screen.fill(BG)

        for p in self.platforms:
            dr=p.rect.move(0,-int(self.cam_y))

            # Crumbling platforms shake before disappearing
            if p.crumbling:
                shake_x=random.choice([-3,-2,-1,0,1,2,3])
                shake_y=random.choice([-2,-1,0,1,2])
                dr.x+=shake_x
                dr.y+=shake_y

            if p.platform_type=="spring":
                color=(80,180,80)
            elif p.platform_type=="crumbling":
                color=(180,120,60)
            else:
                color=PLATFORM_COLOR

            pygame.draw.rect(self.screen,color,dr,border_radius=4)

        self.player.draw(self.screen,self.cam_y)
        draw_lava(
            self.screen,
            self.lava_y,
            self.cam_y,
            WIDTH,
            HEIGHT,
            self.frame
        )

        # Height HUD
        sc=self.font.render(
            f"Height: {self.score}m  R=Restart",
            True,
            (220,200,180)
        )
        self.screen.blit(sc,(8,10))

        # Rising danger indicator
        danger=int(min(100,(self.lava_rise/1.2)*100))

        hud_x=8
        hud_y=42
        bar_width=220
        bar_height=18

        pygame.draw.rect(
            self.screen,
            (60,60,60),
            (hud_x,hud_y,bar_width,bar_height)
        )

        pygame.draw.rect(
            self.screen,
            (220,70,40),
            (hud_x,hud_y,int(bar_width*danger/100),bar_height)
        )

        danger_text=self.font.render(
            f"Lava Danger: {danger}%",
            True,
            (240,220,200)
        )

        self.screen.blit(
            danger_text,
            (hud_x+bar_width+10,hud_y-4)
        )

        # Show warning during a surge
        if self.surge_active:
            surge_text=self.font.render(
                "LAVA SURGE!",
                True,
                (255,100,50)
            )
            self.screen.blit(
                surge_text,
                (WIDTH-surge_text.get_width()-10,10)
            )

        if self.game_over:
            self._msg("LAVA GOT YOU!",(220,80,40))

        if self.won:
            self._msg("ESCAPED!",(80,220,100))

        pygame.display.flip()

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,150))
        self.screen.blit(ov,(0,0))

        m=self.big_font.render(text,True,color)
        s=self.font.render(
            "Press R to Play Again",
            True,
            (200,200,200)
        )

        self.screen.blit(
            m,
            (WIDTH//2-m.get_width()//2,HEIGHT//2-40)
        )

        self.screen.blit(
            s,
            (WIDTH//2-s.get_width()//2,HEIGHT//2+20)
        )

    def run(self):
        running=True

        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()