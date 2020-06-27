import pygame
import random
import math
from pygame import mixer

pygame.init()
screen=pygame.display.set_mode((800,600))

#background
background=pygame.image.load('background.png')
#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
#caption and icon 
pygame.display.set_caption('Space Invader')
icon=pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#player
playerimg=pygame.image.load("space-invaders.png")
playerx=450
playery=480
playerx_change=0

#enemy
enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
num_of_enemies=5

for i in range(num_of_enemies):
    alien_identity  = random.randint(0,2)
    enemyimg.append(pygame.image.load("alien"+str(alien_identity)+".png"))
    enemyx.append(random.randint(0,735))
    enemyy.append(random.randint(20,150))
    enemyx_change.append(4)
    enemyy_change.append(40)

#bullet
bulletimg=pygame.image.load("005-bullet.png")
bulletx=20
bullety=480
bulletx_change=0
bullety_change=15
bullet_state="ready"

#score
score_value=0
font=pygame.font.Font("freesansbold.ttf",32)
textx=10
texty=10

#game over
game_over_font=pygame.font.Font("freesansbold.ttf",64)

def show_text(x,y):
    score=font.render("Score: "+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over():
    over_text=game_over_font.render("GAME OVER !",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletimg,(x+16,y+10))

def iscollision(enemyx,enemyy,bulletx,bullety):
    distance=math.sqrt((math.pow(enemyx-bulletx,2))+(math.pow(enemyy-bullety,2)))
    if distance<27:
        return True
    else:
        return False

running=True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        #checking key stroke
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerx_change=-5
            if event.key==pygame.K_RIGHT:
                playerx_change=5
            if event.key==pygame.K_SPACE:
                bullet_sound=mixer.Sound("laser.wav")
                bullet_sound.play()
                if bullet_state is "ready":
                    bulletx=playerx+12
                    bullet(bulletx,bullety)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerx_change=0
    #checking boundaries for player
    playerx+=playerx_change 
    if playerx<=0:
        playerx=0
    elif playerx>=736:
        playerx=736  

    #movement of invader
    for i in range(num_of_enemies):
        if enemyy[i]>440:
            for j in range(num_of_enemies):
                enemyy[j]=2000
            game_over()
            break

        enemyx[i]+=enemyx_change[i]
        if enemyx[i]<=0:
            enemyx_change[i]=4
            enemyy[i]+=enemyy_change[i]
        elif enemyx[i]>=736:
            enemyx_change[i]=-4
            enemyy[i]+=enemyy_change[i]
        collision=iscollision(enemyx[i],enemyy[i],bulletx,bullety)
        if collision:
            collision_sound=mixer.Sound("explosion.wav")
            collision_sound.play()
            bullety=480
            bullet_state="ready"
            score_value=score_value+1
            enemyx[i]=random.randint(0,735)
            enemyy[i]=random.randint(20,150)
        enemy(enemyx[i],enemyy[i],i)
    #reseting bullet
    if bullety<=0:
        bullety=480
        bullet_state="ready"
    # movement of bullet
    if bullet_state is "fire":
        bullet(bulletx,bullety)
        bullety-=bullety_change

    player(playerx,playery)
    show_text(textx,texty)
    pygame.display.update()
