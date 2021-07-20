import sys, random, time, os
import random
import pygame
import tkinter as tk
from tkinter import messagebox

#CONSTANTS SCREEN WIDTH AND HEIGHT
WIDTH = 500
HEIGHT = 500
ROWS = 20
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
FPS = 20 # FPS for the game
CLOCK = pygame.time.Clock()
FRUIT_WIDTH = 50
FRUIT_HEIGHT = 50
SNAKE_SIZE = 10

#FRUIT
BANANA = pygame.transform.scale(pygame.image.load(os.path.join('assets','banana.jpg')),(30,30))

# INITIATE PYGAME
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')


def draw_window():
    global snake, fruit
    WIN.fill(BLACK)
    draw_grid(WIDTH,ROWS)
    snake.draw_snake()
    fruit.draw(WIN)
    pygame.display.update()

def draw_grid(width, row):
    size_between = WIDTH//ROWS
    x = 0
    y=0
    for i in range(ROWS):
        x = x + size_between
        y = y + size_between
        pygame.draw.line(WIN,(255,255,255), (x,0),(x,WIDTH))
        pygame.draw.line(WIN,(255,255,255), (0,y),(WIDTH, y))


def randomize_fruit(rows, snake):
    # print(positions)
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos==(x,y),positions))) > 0:
            continue
        else:
            break
    return (x,y)

def message_box(subject,content):
    root = tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass


class Cube: # use to represent the snake
    rows = 20
    w = 500
    def __init__(self, start, _dirnx=1, _dirny=0, color=RED):
        self.pos = start
        self._dirnx = _dirnx
        self._dirny = _dirny
        self.color = color

    def move(self, _dirnx, _dirny):
        self._dirnx = _dirnx
        self._dirny = _dirny
        self.pos = (self.pos[0]+ self._dirnx, self.pos[1]+self._dirny)

    def draw(self, surface=WIN, eyes= False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color,(i*dis+1, j*dis+1,dis-2,dis-2) )
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(WIN, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(WIN, (0,0,0), circleMiddle2, radius)

class Snake:
    body = []
    turns = {} #REMEMBER THE POSITION WHERE THE SNAKE TURNS
    def __init__(self,color,pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        #SETTING THE DIRECTION OF THE SNAKE
        self._dirnx = 0
        self._dirny = 0
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


            key_pressed = pygame.key.get_pressed()
            for key in key_pressed:
                if key_pressed[pygame.K_a]:
                    self._dirnx = -1
                    self._dirny = 0
                    self.turns[self.head.pos[:]] = [self._dirnx, self._dirny]
                elif key_pressed[pygame.K_s]:
                    self._dirnx = 0
                    self._dirny = 1
                    self.turns[self.head.pos[:]] = [self._dirnx, self._dirny]
                elif key_pressed[pygame.K_d]:
                    self._dirnx = 1
                    self._dirny = 0
                    self.turns[self.head.pos[:]] = [self._dirnx, self._dirny]
                elif key_pressed[pygame.K_w]:
                    self._dirnx = 0
                    self._dirny = -1
                    self.turns[self.head.pos[:]] = [self._dirnx, self._dirny]

        #MAKE OTHER PART OF THE SNAKE TURN AT THE INDICATED POSITION
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c._dirnx == -1 and c.pos[0]<=0 : c.pos = (c.rows-1, c.pos[1])
                elif c._dirnx == 1 and c.pos[0]>=c.rows-1:c.pos=(0,c.pos[1])
                elif c._dirny == 1 and c.pos[1]>=c.rows-1:c.pos=(c.pos[0],0)
                elif c._dirny == -1 and c.pos[1] <= 0: c.pos=(c.pos[0],c.rows-1)
                else:
                    c.move(c._dirnx,c._dirny )
    def draw_snake(self):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(WIN,eyes=True)
            else:
                c.draw(WIN)
    def addCube(self):
        tail = self.body[-1]
        dx,dy = tail._dirnx, tail._dirny
        if dx ==1 and dy ==0:
            self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
        elif dx==-1 and dy==0:
            self.body.append(Cube((tail.pos[0]+1,tail.pos[1])))
        elif dx==0 and dy==1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]-1)))
        elif dx==0 and dy==-1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1]._dirnx = dx
        self.body[-1]._dirny = dy
    def reset(self,pos):
        self.head = Cube(pos)
        self.body=[]
        self.body.append(self.head)
        self.turns = {}
        self._dirnx = 1
        self._dirny = 0

def main():

    global snake, fruit
    game = True
    fruit_rec = pygame.Rect(50,50, FRUIT_WIDTH, FRUIT_WIDTH)
    snake = Snake((255,0,0),(10,10))
    fruit = Cube(randomize_fruit(ROWS,snake), color=GREEN)
    direction = "right"
    while game:
        pygame.time.delay(80)
        CLOCK.tick(FPS)
        snake.move()
        if snake.body[0].pos == fruit.pos:
            snake.addCube()
            fruit = Cube(randomize_fruit(ROWS,snake),color=(0,255,0))
        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos,snake.body[x+1:])):
                print("Score: ",len(snake.body))
                message_box('You Lost!', 'Play Again')
                snake.reset((10,10))
                break

        draw_window()




if __name__ == "__main__":
    main()
