'''
Author: Rajish Wagh
Start Date: 14 September 2017
End Date: Still working on it...

This is a game called Ball Catcher. The objective is to catch all the balls
falling from the top using the bat given.
There are 10 Lives available for this.
Once the lives are over, the game finishes and the user is asked if they
want to play again.

The user can close the game by clicking the x any time.
'''

import pygame
import time
import random
import math
random.seed(int(time.time()))

WIDTH = 1300
HEIGHT = 700
FPS = 60
COLORS = [(0,0,255), (0,255,0), (0,255,255), (255,255,0), (255,0,255)]
ALLOWED_MISSES = 10
Path = '/home/rajishjw/Documents/PyGame/'
SoundsDict = {}
class Glove:
    def __init__(self):
        self.w = 50
        self.x = (WIDTH-self.w)/2
        self.p_x = self.x   # Previous value of x
        self.y = HEIGHT - 30
        self.h = 10
        self.color = (255, 0, 0) # Always red
        self.misses = 0
        self.create()
    def moveleft(self):
        self.p_x = self.x
        if self.x < 5:
            self.x = WIDTH - self.w
        else:
            self.x -= 5
        self.create()
    def moveright(self):
        self.p_x = self.x
        if self.x > WIDTH - self.w + 5:
            self.x = 0
        else:
            self.x += 5
        self.create()
    def create(self):
        # Clear the surface once it gets new value...
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.p_x,self.y,WIDTH,10))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x,self.y,self.w,self.h))
    def reposition(self):
        self.x = (WIDTH-self.w)/2
        self.create()
    def sizeinc(self):
        if self.w < 100:
            self.w += 2

class Star:
    global posn
    def __init__(self):
        self.radius = 20
        self.color = (255,255,255)   #Gets a white
        self.num_points = random.randint(3,8)

        self.center_x = random.randint(self.radius, WIDTH-self.radius)
        intgr = random.randint(0,len(posn)-1)
        self.center_y = posn[intgr]

        self.point_list = []
        self.create_point_list(self.radius)
        self.p_point_list = self.point_list
        self.value = self.num_points
        self.create()
        self.yspeed = (random.randint(1,2))
        self.xspeed = (random.randint(-3,3))


    def create_point_list(self,r):
        self.p_point_list = self.point_list
        self.point_list = []
        for i in range(self.num_points * 2):
            radius = r
            if i % 2 == 0:
                radius = radius // 4
            ang = i * 3.14159 / (self.num_points)
            x = self.center_x + int(math.cos(ang) * radius)
            y = self.center_y + int(math.sin(ang) * radius)
            self.point_list.append((x, y))

    def movedown(self):
        if self.center_x <= self.radius/2 or self.center_x >= WIDTH - self.radius/2:
            self.xspeed = -1 * self.xspeed
        self.center_x += self.xspeed
        self.center_y += self.yspeed # What number needs to be added????
        self.create()

    def create(self):
        self.create_point_list(self.radius)
        pygame.draw.polygon(screen, (0,0,0), self.p_point_list)
        pygame.draw.polygon(screen, self.color, self.point_list)

    def re_init(self):
        self.num_points = random.randint(3,8)
        self.center_x = random.randint(self.radius, WIDTH-self.radius)
        intgr = random.randint(0,len(posn)-1)
        self.center_y = posn[intgr]
        self.create()
        self.yspeed = (random.randint(1,2))
        self.xspeed = (random.randint(-3,3))

    def destroy(self):
        pygame.draw.polygon(screen, (0,0,0), self.point_list)

class Ball: # Currently all balls begin at the same time. They need to be separated.
    global COLORS
    global posn
    def __init__(self):
        self.radius = 10
        self.x = random.randint(10, WIDTH-10)
        intgr = random.randint(0,len(posn)-1)
        self.y = posn[intgr]
        del posn[intgr]
        self.p_y = self.y   # Previous y value
        self.p_x = self.x   # Previous x value
        self.color = COLORS[random.randint(0,4)]
        self.create()
        self.yspeed = (random.randint(1,2))
        self.xspeed = (random.randint(-5,5))

    def create(self):
        pygame.draw.circle(screen, (0,0,0), (self.p_x, self.p_y), self.radius)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def movedown(self):
        self.p_x = self.x
        if self.x <= self.radius/2 or self.x >= WIDTH - self.radius/2:
            self.xspeed = -1 * self.xspeed
        self.x += self.xspeed
        self.p_y = self.y
        self.y += self.yspeed # What number needs to be added????
        self.create()
    def re_init(self):
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), self.radius)
        self.x = random.randint(self.radius, WIDTH-self.radius)
        self.y = self.radius
        self.p_y = self.y
        self.color = COLORS[random.randint(0,4)]
        self.yspeed = (random.randint(1,2))
        self.xspeed = (random.randint(-5,5))
        self.create()

    def destroy(self):
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), self.radius)

def caught(bx, by, gx, w):
    if (bx >= (gx-5)) and (bx <= (gx + w + 5)) and (by >= HEIGHT - 45) and (by <= HEIGHT - 35):
        return True
    else:
        return False

def missed(by):
    if by > HEIGHT - 35: return True
    else: return False

def new_level(l):
    font = pygame.font.Font(None, 75)
    sss = 'Level No: ' + str(l)
    text = font.render(sss, True, (0, 255, 125))
    screen.blit(text,((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
    pygame.display.flip()
    time.sleep(2)
    screen.fill((0, 0, 0))

def display(score, hs, level):
    font = pygame.font.Font(None, 60)
    s = 'Your Score: ' + str(score)
    text1 = font.render(s, True, (255, 255, 0))
    s = 'Highest Score: ' + str(hs)
    text2 = font.render(s, True, (255, 255, 0))
    s = 'Level Reached: ' + str(level)
    text3 = font.render(s, True, (255, 255, 0))
    screen.fill((0, 0, 0))
    screen.blit(text1,((WIDTH - text1.get_width()) // 2, (HEIGHT - text1.get_height()) // 2 - text1.get_height()))
    screen.blit(text2,((WIDTH - text2.get_width()) // 2, (HEIGHT - text2.get_height()) // 2))
    screen.blit(text3,((WIDTH - text3.get_width()) // 2, (HEIGHT - text3.get_height()) // 2 + text3.get_height()))
    pygame.display.flip()
    time.sleep(4)
    screen.fill((0, 0, 0))

def askformore():
    font = pygame.font.Font(None, 60)
    done = False
    s = "Hit Key  'Y'  to play again"
    text1 = font.render(s, True, (255, 255, 255))
    s = "Hit Key  'N'  to Quit"
    text2 = font.render(s, True, (255, 255, 255))
    screen.blit(text1,((WIDTH - text1.get_width()) // 2, (HEIGHT - text1.get_height()) // 2 - text1.get_height()))
    screen.blit(text2,((WIDTH - text2.get_width()) // 2, (HEIGHT - text2.get_height()) // 2 ))
    while not done:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leveldone = True
                gamedone = True
                finished = True
                break
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_y]:
            screen.fill((0, 0, 0))
            done = True
            return True
        elif pressed[pygame.K_n]:
            done = True
            return False

def scorecard(score, misses, hs, l):
    font = pygame.font.Font(None, 45)
    pygame.draw.rect(screen, (90, 0, 0), pygame.Rect(0, 0, WIDTH, 100))
    s = "Score: " + str(score)
    text1 = font.render(s, True, (255, 125, 0))
    screen.blit(text1,(10,(100 - text1.get_height()) // 2))
    s = "Lives: " + str(ALLOWED_MISSES - misses)
    text1 = font.render(s, True, (255, 125, 0))
    screen.blit(text1,(WIDTH/4 + 10,(100 - text1.get_height()) // 2))
    s = "Level: " + str(l)
    text1 = font.render(s, True, (255, 125, 0))
    screen.blit(text1,(2*WIDTH/4 + 10,(100 - text1.get_height()) // 2))
    s = "High Score: " + str(hs)
    text1 = font.render(s, True, (255, 125, 0))
    screen.blit(text1,(3*WIDTH/4 + 10,(100 - text1.get_height()) // 2))

def firstscreen():
    screen.fill((20, 0, 20))
    font = pygame.font.Font(None, 30)
    done = False
    s = "Welcome to 'Ball Catcher' created by Rajish Wagh"
    text1 = font.render(s, True, (255, 255, 255))
    screen.blit(text1,((WIDTH-text1.get_width())//2,(HEIGHT - text1.get_height()) // 2 - int((7)*text1.get_height())))
    s = "Use Left and Right keys to control the bat."
    text1 = font.render(s, True, (255, 255, 255))
    screen.blit(text1,((WIDTH-text1.get_width())//2,(HEIGHT - text1.get_height()) // 2 - int((4)*text1.get_height())))
    s = "The objective is to catch as many BALLS and STARS possible using the bat"
    text1 = font.render(s, True, (255, 255, 255))
    screen.blit(text1,((WIDTH-text1.get_width())//2,(HEIGHT - text1.get_height()) // 2 - int((3)*text1.get_height())))
    s = "Catching a STAR gives you a life and increases the score by value equal to it's vertices"
    text1 = font.render(s, True, (255, 255, 255))
    screen.blit(text1,((WIDTH-text1.get_width())//2,(HEIGHT - text1.get_height()) // 2 - int((2)*text1.get_height())))
    s = "Please send your review to rjw0028@auburn.edu"
    text1 = font.render(s, True, (255, 255, 255))
    screen.blit(text1,((WIDTH-text1.get_width())//2,(HEIGHT - text1.get_height()) // 2 + int((2)*text1.get_height())))
    s = "Hit SPACE to continue..."
    text1 = font.render(s, True, (255, 255, 255))
    screen.blit(text1,((WIDTH-text1.get_width())//2,(HEIGHT - text1.get_height()) // 2 + int((6)*text1.get_height())))

    while not done:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                return False
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            done = True
            screen.fill((0, 0, 0))
            return True

def Play_Sound(S):  # Make such a dictionary to play during the game.
    global SoundsDict, Path
    sound = SoundsDict.get(S)
    if sound == None:
        canonpath = Path + S
        sound = pygame.mixer.Sound(canonpath)
        SoundsDict[S] = sound
    sound.play()

def main_loop():
    global WIDTH, HEIGHT, FPS, screen, posn
    pygame.init()
    pygame.mixer.music.load('"C:\Users\rajis\Music\Komiku_-_35_-_The_True_Last_Boss(chosic.com).mp3"')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    levels = [x for x in range(1,11)]
    High_Score = 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Ball Catcher')
    finished = False
    while not finished:
        if not firstscreen():
            finished = True
            break
        else:
            clock = pygame.time.Clock()
            gamedone = False
            glove = Glove()
            while not gamedone:
                Score = 0
                levelcounter = 4    # So the first level changes at 10
                for level in levels:
                    levelscore = 0
                    levelcounter += level + 1
                    if level == levels[-1]:
                        gamedone = True
                    new_level(level)
                    glove.reposition()
                    posn = [0, -50 , -100, -150, -200, -300, -350, -450, -400, -500, -550]
                    t = time.time()
                    leveldone = False
                    balls = [None for x in range(level)]
                    stars = [None for x in range(int(level/2))]
                    #screen.fill((0, 0, 0))
                    for i in range(int(level/2)):
                        stars[i] = Star()
                    for i in range(level):
                        balls[i] = Ball()
                    while not leveldone:
                        for b in balls:
                            b.movedown()
                        for s in stars:
                            s.movedown()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                leveldone = True
                                gamedone = True
                                finished = True
                                break
                        if (levelscore) and (levelscore)%(levelcounter) == 0:   # Changes levels at 5,11,17... points
                            leveldone = True
                            for b in balls: #Destroy all balls in the level before moving to next
                                b.destroy()
                            for s in stars:
                                s.destroy()

                        for b in balls:
                            if missed(b.y):     # Event: Ball Missed...
                                b.re_init()
                                Play_Sound('Miss.wav')
                                glove.misses += 1
                                if glove.misses > ALLOWED_MISSES:
                                    leveldone = True
                                    gamedone = True

                            elif caught(b.x, b.y, glove.x, glove.w):
                                b.re_init()
                                Play_Sound('Caught-Ball.wav')
                                glove.sizeinc()
                                Score += 1
                                levelscore += 1
                                if High_Score < Score:
                                    High_Score = Score
                        for s in stars:
                            if missed(s.center_y):
                                s.re_init()
                            elif caught(s.center_x, s.center_y, glove.x, glove.w):
                                s.re_init()
                                Play_Sound('Caught-Star.wav')
                                glove.misses -= 1
                                Score += s.value
                                levelscore += s.value
                                if High_Score < Score:
                                    High_Score = Score


                        pressed = pygame.key.get_pressed()
                        if pressed[pygame.K_LEFT]: glove.moveleft()
                        if pressed[pygame.K_RIGHT]: glove.moveright()
                        #screen.fill((0, 0, 0))
                        #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(20, 20, 60, 60))
                        scorecard(Score, glove.misses, High_Score, level)
                        pygame.display.flip()

                        clock.tick(FPS)
                    if gamedone:
                        display(Score, High_Score, level)
                        if (not finished) and askformore():
                            finished = False
                        else:
                            finished = True
                        break
            # print("Do you wish to play again?")
            # if pressed[pygame.K_y]:
            #     finished = False
            # else:
            #     finished = True



main_loop()
