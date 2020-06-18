import pygame

# Variables

WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELOCITY = 15
FRAMERATE = 35

# Define my classes


class Ball:

    RADIUS = 20

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def show(self, color):
        # global screen
        pygame.draw.circle(screen, color, (self.x,  self.y), self.RADIUS)

    def update(self):
        # global bg_color, fg_color

        newx = self.x + self.vx
        newy = self.y + self.vy

        if newx < BORDER+self.RADIUS:
            self.vx = -self.vx
        elif newy < BORDER+self.RADIUS or newy > HEIGHT-BORDER-self.RADIUS:
            self.vy = -self.vy
        elif newx+Ball.RADIUS > WIDTH-Paddle.WIDTH and abs(newy-paddle.y) < Paddle.HEIGHT//2:
            self.vx = - self.vx

        else:
            self.show(bg_color)
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            self.show(fg_color)


class Paddle:
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, y):
        self.y = y

    def show(self, color):
        # global screen
        pygame.draw.rect(screen, color,
                         pygame.Rect(WIDTH-self.WIDTH,
                                     self.y-self.HEIGHT//2,
                                     self.WIDTH, self.HEIGHT))

    def update(self):
        newy = pygame.mouse.get_pos()[1]
        if newy - self.HEIGHT // 2 > BORDER and newy + self.HEIGHT // 2 < HEIGHT - BORDER:
            self.show(pygame.Color("black"))
            self.y = pygame.mouse.get_pos()[1]
            self.show(pygame.Color("white"))


# create objects


# Draw the scenario

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg_color = pygame.Color("black")
fg_color = pygame.Color("white")

screen.fill(bg_color)

pygame.draw.rect(screen, fg_color, pygame.Rect(0, 0, WIDTH, BORDER))
pygame.draw.rect(screen, fg_color, pygame.Rect(0, 0, BORDER, HEIGHT))
pygame.draw.rect(screen, fg_color, pygame.Rect(0, HEIGHT-BORDER, WIDTH, HEIGHT))

ball = Ball(WIDTH-Ball.RADIUS, HEIGHT//2, -VELOCITY, -VELOCITY)
ball.show(fg_color)
paddle = Paddle(HEIGHT//2)
paddle.show(fg_color)

clock = pygame.time.Clock()

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break

    clock.tick(FRAMERATE)
    pygame.display.flip()

    paddle.update()

    ball.update()

pygame.quit()
