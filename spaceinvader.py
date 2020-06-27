import pygame
import random
import math
from pygame import mixer
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="mysql123",
  database="mydatabase"
)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("select name,score from mydatabase.participants order by score desc;")
result=mycursor.fetchone()


highest = "Highest Score -> "+result[0]+" : " + str(result[1])
print(highest)



pygame.init()
welcomescreen = pygame.display.set_mode((800,600))
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
text1 = ''
user = ''

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
userscore_updated = 0
font=pygame.font.Font("freesansbold.ttf",32)
textbox_font= pygame.font.Font("freesansbold.ttf",20)
welcome_font=pygame.font.Font("freesansbold.ttf",40)
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
    global userscore_updated
    global text1
    global score_value
    if userscore_updated == 0:
        mycursor1 = mydb.cursor(buffered=True)
        query = "INSERT INTO participants (name,score) VALUES (%s,%s))"
        print(query)
        val = (text1,str(score_value))

        print(val)
        mycursor1.execute("INSERT INTO participants (name,score) VALUES (%s,%s)",val)
        mydb.commit()
        print(mycursor1.rowcount,"value inserted")
        userscore_updated = 1
    


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
welcome = 0
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
text = welcome_font.render('Space Invader', True, (214, 240, 19), (0,0,0))
textRect = text.get_rect()
textRect.center = (800 // 2, 120)
display_surface = pygame.display.set_mode((800, 600 ))

#Highest Score
text_highest = textbox_font.render(highest, True, (255,255,255), (0,0,0))
textRect2 = text_highest.get_rect()
textRect2.center = (600, 20)

input_box = pygame.Rect(270, 300, 290, 32)
color_inactive = pygame.Color('white')
color_active = pygame.Color('green')
color_current = color_inactive
active = False
 #uname
done = False

while running:

    if welcome == 0:
        welcomescreen.fill((0,0,0))
        welcomescreen.blit(background,(0,0))
        '''welcomescreen.blit(back)'''
        
        display_surface.blit(text, textRect)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color_current = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text1)
                        welcome = 1
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
        text_uname = textbox_font.render('Username', True, (255,255,255), (0,0,0))
        textRect1 = text_uname.get_rect()
        textRect1.center = (320, 280)
        display_surface.blit(text_uname, textRect1)
        display_surface.blit(text_highest, textRect2)

        txt_surface = textbox_font.render(text1, True, color_current)
        welcomescreen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(welcomescreen, color_current, input_box, 2)
        pygame.display.update()
    else:    
        screen.fill((0,0,0))
        screen.blit(background,(0,0))
        display_surface.blit(text_highest, textRect2)
        



        
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
