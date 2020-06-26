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
            # self.y = newy
            self.show(pygame.Color("white"))
            
    def update_ai(self, newy):
    # newy = pygame.mouse.get_pos()[1]
        if newy - self.HEIGHT // 2 > BORDER and newy + self.HEIGHT // 2 < HEIGHT - BORDER:
            self.show(pygame.Color("black"))
            # self.y = pygame.mouse.get_pos()[1]
            self.y = newy
            self.show(pygame.Color("white"))

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

start_time = time.time()
clock = pygame.time.Clock()

if mode == 'train':

# get data
    sample = open("game.csv", "w")
    print("x,y,vx,vy,Paddle.y", file=sample)
    df_train = pd.DataFrame(columns=['x', 'y', 'vx', 'vy', 'py'])

if mode == 'ai':

    # prepare data
    pong = pd.read_csv("game.csv")
    pong = pong.drop_duplicates()
    
    # train model
    
         # X = pong.drop(columns="Paddle.y")
    # X = pong.loc[:, ['x', 'y', 'vx', 'vy']]
    # y = pong['Paddle.y']
    
    clf = KNeighborsRegressor(n_neighbors=3)
    clf = clf.fit(X, y)
    
    df = pd.DataFrame(columns=['x', 'y', 'vx', 'vy'])
    

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break

    clock.tick(FRAMERATE)
    pygame.display.flip()
    
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
        paddle.update()
        print("{},{},{},{},{}".format(ball.x, ball.y, ball.vx, ball.vy, paddle.y), file=sample)
        df_train = df_train.append({'x': ball.x, 'y': ball.y, 'vx': ball.vx, 'vy': ball.vy, 'py': paddle.y}, ignore_index=True)
        print(df_train)
        
    if mode == 'ai':
        to_predict = df.append({'x': ball.x, 'y': ball.y, 'vx': ball.vx, 'vy': ball.vy}, ignore_index=True)
        should_move = clf.predict(to_predict)
        paddle.update_ai(should_move)
    

    ball.update()

pygame.quit()
