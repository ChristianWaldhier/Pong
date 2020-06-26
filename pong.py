import pygame
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
import time
# Variables

WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELOCITY = 15
FRAMERATE = 35
mode = "train"

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

        # if newx < BORDER+self.RADIUS:
        #    self.vx = -self.vx

        if newx-Ball.RADIUS/2 < Paddle.WIDTH and abs(newy-paddle_left.y) < Paddle.HEIGHT//2:
            self.vx = - self.vx

        elif newy < BORDER+self.RADIUS or newy > HEIGHT-BORDER-self.RADIUS:
            self.vy = -self.vy
        elif newx+Ball.RADIUS > WIDTH-Paddle.WIDTH and abs(newy-paddle_right.y) < Paddle.HEIGHT//2:
            self.vx = - self.vx

        else:
            self.show(bg_color)
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            self.show(fg_color)


class Paddle:
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, x, y):
        self.x = x       
        self.y = y

    def show(self, color):
        # global screen
        pygame.draw.rect(screen, color,
                         pygame.Rect(self.x-self.WIDTH,
                                     self.y-self.HEIGHT//2,
                                     self.WIDTH,
                                     self.HEIGHT))

    def update(self):
        newy = pygame.mouse.get_pos()[1]
        if newy - self.HEIGHT // 2 > BORDER and newy + self.HEIGHT // 2 < HEIGHT - BORDER:
            self.show(pygame.Color("black"))
            self.y = pygame.mouse.get_pos()[1]
            # self.y = newy
            self.show(pygame.Color("white"))

    def update_ai(self, newy):
        if newy - self.HEIGHT // 2 > BORDER and newy + self.HEIGHT // 2 < HEIGHT - BORDER:
            self.show(pygame.Color("black"))
            # self.y = pygame.mouse.get_pos()[1]
            self.y = newy
            self.show(pygame.Color("white"))

# Draw the scenario


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg_color = pygame.Color("black")
fg_color = pygame.Color("green")

screen.fill(bg_color)

pygame.draw.rect(screen, fg_color, pygame.Rect(0, 0, WIDTH, BORDER))  # Top Border
# pygame.draw.rect(screen, fg_color, pygame.Rect(0, 0, BORDER, HEIGHT))  # Left Border
pygame.draw.rect(screen, fg_color, pygame.Rect(0, HEIGHT-BORDER, WIDTH, HEIGHT))  # Bottom Border

ball = Ball(WIDTH-Ball.RADIUS*5, HEIGHT//2, -VELOCITY, -VELOCITY)
ball.show(fg_color)
paddle_right = Paddle(WIDTH, HEIGHT//2)
paddle_left = Paddle(Paddle.WIDTH, HEIGHT//2)
paddle_right.show(fg_color)
paddle_left.show(fg_color)

# paddle_left = Paddle()

start_time = time.time()
clock = pygame.time.Clock()

if mode == 'train':  # get data
    sample = open("game.csv", "w")
    print("x,y,vx,vy,Paddle.y", file=sample)
    df_train = pd.DataFrame(columns=['x', 'y', 'vx', 'vy', 'py'])

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break

    clock.tick(FRAMERATE)
    pygame.display.flip()

    if ball.x > WIDTH+ball.RADIUS:
        ball.x = (WIDTH-Ball.RADIUS*10)
        ball.y = (HEIGHT//2)

    print(time.time()-start_time)

    if time.time()-start_time > 60:
        if mode == 'train':
            X = df_train.loc[:, ['x', 'y', 'vx', 'vy']]
            y = df_train['py']

            clf = KNeighborsRegressor(n_neighbors=3)
            clf = clf.fit(X, y)

            df = pd.DataFrame(columns=['x', 'y', 'vx', 'vy'])

        mode = 'ai'

    if mode == 'train':
        paddle_right.update()

        df_train = df_train.append({'x': ball.x, 'y': ball.y, 'vx': ball.vx, 'vy': ball.vy, 'py': paddle_right.y}, ignore_index=True)
        if time.time()-start_time > 1:
            X = df_train.loc[:, ['x', 'y', 'vx', 'vy']]
            y = df_train['py']

            clf = KNeighborsRegressor(n_neighbors=3)
            clf = clf.fit(X, y)

            df = pd.DataFrame(columns=['x', 'y', 'vx', 'vy'])

            to_predict = df.append({'x': ball.x, 'y': ball.y, 'vx': ball.vx, 'vy': ball.vy}, ignore_index=True)
            should_move = clf.predict(to_predict)

            paddle_left.update_ai(should_move)

    if mode == 'ai':
        to_predict = df.append({'x': ball.x, 'y': ball.y, 'vx': ball.vx, 'vy': ball.vy}, ignore_index=True)
        should_move = clf.predict(to_predict)
        paddle_right.update_ai(should_move)

    ball.update()

pygame.quit()
