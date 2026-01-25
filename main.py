import pygame
import settings
from diffraction_calc import calculate_diffraction
import math

class DraggablePoint:
    def __init__(self,x,h,color, name, is_obstacle=False):
        self.x = x
        self.h = h
        self.color = color
        self.name = name
        self.is_obstacle = is_obstacle
        self.radius = 10
        self.dragging = False

    def draw (self,screen):
        screen_y = settings.GROUND - self.h

        #BTS drawing
        pygame.draw.line(screen, self.color, (self.x,settings.GROUND), (self.x, screen_y))
        pygame.draw.circle(screen, self.color, (self.x,screen_y), self.radius)

        #description
        font = pygame.font.SysFont('Arial', 14)
        text = font.render(f'{self.name}: x={self.x}, y={self.h}',True, settings.WHITE)
        screen.blit(text,(self.x - 20, screen_y - 25))

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen_y = settings.GROUND - self.h

            #check antenna is clicked
            if math.hypot(mouse_x - self.x, mouse_y - screen_y) < self.radius * 2:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if mouse_y < settings.GROUND:
                self.h = settings.GROUND - mouse_y
            elif self.h < 0:
                self.h = 0
            self.x = mouse_x


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption('Diffraction_calc - Radiocomunication revision')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Consolas', 20)

    #create objects
    tx = DraggablePoint(100,100, settings.BLUE, 'TX')
    rx = DraggablePoint(400,100, settings.GREEN, "RX")
    obs = DraggablePoint(200,150, settings.RED, 'WALL', is_obstacle=True)

    freq = 900e6

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            tx.handle(event)
            rx.handle(event)
            obs.handle(event)

            #change frequency
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: freq += 50e6
                if event.key == pygame.K_DOWN and freq > 50e6: freq -= 50e6

        loss, v, h_param, los_h = calculate_diffraction(tx,rx,obs,freq)

        screen.fill(settings.BLACK)
        pygame.draw.rect(screen, (50, 50, 50), (0, settings.GROUND, settings.WIDTH, settings.HEIGHT))

        tx.draw(screen)
        rx.draw(screen)
        obs.draw(screen)

        #LOS point obstacle
        pygame.draw.circle(screen, settings.YELLOW, (obs.x, settings.GROUND - los_h), 5)
        if v>0:
            pygame.draw.line(screen,settings.GRAY,(tx.x,settings.GROUND - tx.h),(obs.x,settings.GROUND - obs.h),3)
            pygame.draw.line(screen,settings.GRAY, (obs.x, settings.GROUND - obs.h), (rx.x, settings.GROUND - rx.h),3)
            pygame.draw.line(screen, settings.YELLOW,(tx.x, settings.GROUND - tx.h), (rx.x, settings.GROUND - rx.h),3)
        else:
            pygame.draw.line(screen, settings.YELLOW,(tx.x, settings.GROUND - tx.h), (rx.x, settings.GROUND - rx.h),3)

        #parameters info
        info_texts = [
        f"Częstotliwość: {freq/1e6:.0f} MHz",
        f"Parametr h: {h_param:.2f} m",
        f"Parametr v: {v:.2f}",
        f"--- STRATA DYFRAKCYJNA ---",
        f"{loss:.2f} dB"
        ]

        for i, txt in enumerate(info_texts):
            color = settings.WHITE
            if "STRATA" in txt: color = settings.YELLOW
            if "dB" in txt: color = settings.RED if loss > 0 else settings.GREEN
            
            label = font.render(txt, True, color)
            screen.blit(label, (20, 20 + i * 30))

        pygame.display.flip()
        clock.tick(settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()