# Saurabh Vashisth

import pygame   #importing modules

pygame.init()

import time
import random
from images import *
from const import *




class person:
    pass


class dragon(person):
    dragonx =  300
    dragony = 0
    dragonxchange = 0


class player(person):
    leadx = PLAYERX #SCREENWIDTH/10
    leady = PLAYERY #SCREENHEIGHT - PLAYERHEIGHT + 15
    xchange = 0
    ychange = 0

class princess(person):
    princessx = SCREENWIDTH*0.1
    princessy = SCREENHEIGHT*0.03

class fireball:
    ballx = 0
    bally = 0
    ballxchange = BALLXCHANGE
    ballychange = 0
    level = 0


class coins:
        COINS = []
        NUMCOINS = []
        BOOLARRAY = []


class board(player,princess,coins,fireball,dragon):
    
    def __init__(self):
        pygame.display.set_caption("Donkey Kong")
        self.screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        self.cur = pygame.mouse.get_pos()
        self.recent = None
        self.NUMLEVEL = 0
        self.CONTINUE = True
        self.RANDBOOL = True
        self.index = 0
        self.NUMBALLS = 0
        self.BALLS = []
        self.BOOL = []
        self.JUMP = False
        self.LIVES = 3
        self.SCORE = 0
        self.COINS=[]
        self.BOOLARRAY = []
        self.NUMCOINS = []

    def message(self,msg, clr, x = SCREENWIDTH/2, y = SCREENHEIGHT/2, size = 25):
        font = pygame.font.SysFont("comicsansms",size)
        text = font.render(msg,True,clr)
        self.screen.blit(text,[x,y])

    def intro(self):         
        START=True
        while START:
            self.message("Donkey Kong",BLUE,SCREENWIDTH*0.38,SCREENHEIGHT*0.1,60)
            self.message("Push <Enter> to Play",BLUE,SCREENWIDTH*0.35,SCREENHEIGHT*0.2,50)
            
            pygame.draw.rect(self.screen,(84,84,84) , [SCREENWIDTH* 0.38,SCREENHEIGHT*0.4,300,200])
            
            self.message("Controls",BLUE,SCREENWIDTH*0.45,SCREENHEIGHT*0.42,40)
            self.message("Use w to move up",BLACK,SCREENWIDTH*0.43,SCREENHEIGHT*0.5,30)
            self.message("Use a to move left",BLACK,SCREENWIDTH*0.43,SCREENHEIGHT*0.55,30)
            self.message("Use s to move down" ,BLACK,SCREENWIDTH*0.43,SCREENHEIGHT*0.6,30)
            self.message("Use d to move right",BLACK,SCREENWIDTH*0.43,SCREENHEIGHT*0.65,30)
             

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        START = False
                        self.LIVES = 3
                        self.gameloop()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        qui()
            self.clock.tick(5)
    
    
    def makegrid(self):
        i=0
        while i<SCREENHEIGHT:
            self.screen.blit(wall_img,(0,i))
            self.screen.blit(wall_img,(SCREENWIDTH-WALLWIDTH,i))
            i+=WALLHEIGHT-3
        i=0
        while i<SCREENWIDTH:
            self.screen.blit(wall_rotate_img,(i,0))     
            self.screen.blit(wall_rotate_img,(i,SCREENHEIGHT-WALLWIDTH))
            i+=WALLHEIGHT-3


    def makecage(self):

        self.screen.blit(princess_img,(self.princessx,self.princessy))
        i = WALLWIDTH
        j = self.princessx*0.8
        while i < PRINCESSHEIGHT + WALLWIDTH:
            self.screen.blit(brick_img,(self.princessx*0.8,i))
            self.screen.blit(brick_img,(self.princessx*1.8,i))
            i+=BRICKHEIGHT
        i-=BRICKHEIGHT

        while j < self.princessx*1.8:
            self.screen.blit(brick_img,(j,i))
            j+=BRICKWIDTH
        return i


    def makefloor(self,startx,starty,endx):
        
        i = startx
        while i < endx:
            self.screen.blit(floor_img,(i,starty))
            i+=15


    def makeladder(self, x, y1, y2):
        y1-=LADDERHEIGHT
        while y1>=y2:
            self.screen.blit(ladder_img,(x,y1))
            y1-=LADDERHEIGHT


    def makeballs(self,toplevel,LEVEL,dragonx):
        obj = fireball()
        obj.bally = toplevel + FLOORGAP - 20
        obj.ballx = dragonx + DRAGONWIDTH   #round(random.randrange(LEVEL[0][1],LEVEL[0][2])/10.0)*10
        obj.ballxchange = BALLXCHANGE
        self.BALLS.append(obj)
        self.NUMBALLS += 1
        self.BOOL.append(1)

    def checkexit(self,event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.CONTINUE = False
            while not self.CONTINUE:
                pygame.draw.rect(self.screen, RED,[ SCREENWIDTH*0.3,SCREENHEIGHT*0.3,570,100])
                self.message("Press <Enter> to Quit or C to continue",BLACK, SCREENWIDTH*0.35,SCREENHEIGHT*0.35)
                for event in pygame.event.get():
                    if event.key == pygame.K_RETURN or event.type ==  pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        self.CONTINUE = True
                pygame.display.update()

    def collectCoins(self,LEVEL):
        for i in range(self.NUMLEVEL):
            for j in range(self.NUMCOINS[i]):
                if self.BOOLARRAY[i][j] == 0 and (self.leadx == self.COINS[i][j] or self.leadx + 20 == self.COINS[i][j] )and self.leady + 40 == LEVEL[i][0]:
                    self.BOOLARRAY[i][j] = 1
                    self.SCORE+=5
                    pygame.mixer.Sound.play(coinsound)
                elif self.BOOLARRAY[i][j] == 0:
                    self.screen.blit(star_img,(self.COINS[i][j],LEVEL[i][0] -20))


    def checkCollision(self,HEIGHTS,LEVEL):
            for i in range(self.NUMBALLS):
                if self.leadx > self.BALLS[i].ballx - 20 and self.leadx < self.BALLS[i].ballx + 20:
                    if (self.leady  <= self.BALLS[i].bally + 10 and self.leady >= self.BALLS[i].bally - 20) or \
                        (self.leady == PLAYERY and self.BALLS[i].bally == GROUNDHEIGHT - 20):
                            self.leadx = PLAYERX 
                            self.leady = PLAYERY
                            self.xchange = 0
                            self.ychange = 0
                            self.LIVES-=1
                            self.SCORE-=25
                            pygame.mixer.Sound.play(explodesound)
                if self.BALLS[i].ballx < WALLWIDTH and self.BALLS[i].bally == GROUNDHEIGHT - 20 :
                    pass
                else:
                    if self.BALLS[i].level<self.NUMLEVEL:
                        if self.BALLS[i].bally == HEIGHTS[self.BALLS[i].level+1] - 20 :
                            self.BALLS[i].ballxchange = ((-1)**random.randrange(0,2))*BALLXCHANGE
                            self.BALLS[i].ballychange = 0
                            self.BALLS[i].level +=1
                    if self.BALLS[i].ballx  <  WALLWIDTH or self.BALLS[i].ballx + BALLWIDTH> SCREENWIDTH - WALLWIDTH:
                        self.BALLS[i].ballxchange *=-1
                    elif self.BALLS[i].level<self.NUMLEVEL:
                        if self.BALLS[i].ballx > LEVEL[self.BALLS[i].level][2] or self.BALLS[i].ballx < LEVEL[self.BALLS[i].level][1]:
                            self.BALLS[i].ballychange = 2*BALLXCHANGE
                            self.BALLS[i].ballxchange = 0
                    self.BALLS[i].ballx += self.BALLS[i].ballxchange
                    self.BALLS[i].bally += self.BALLS[i].ballychange
                    self.screen.blit(ball_img,(self.BALLS[i].ballx,self.BALLS[i].bally))



    def checkWall(self):
        if self.leady > PLAYERY:
            self.leady= PLAYERY
        if self.leadx > SCREENWIDTH - WALLWIDTH - PLAYERWIDTH:
            self.leadx = SCREENWIDTH - WALLWIDTH - PLAYERWIDTH
        elif self.leadx < WALLWIDTH:
            self.leadx = WALLWIDTH 




    def gameover(self):
        var = True
        while var:
            self.screen.fill(BLACK)

            if self.LIVES > 0:
                pygame.draw.rect(self.screen, BLUE, [SCREENWIDTH* 0.4,SCREENHEIGHT*0.2,300,100])
                self.message("Hurray!! You Won!",WHITE,SCREENWIDTH*0.43,SCREENHEIGHT*0.25,40)
            
            
            if self.LIVES==0:
                pygame.draw.rect(self.screen, RED, [SCREENWIDTH* 0.4,SCREENHEIGHT*0.4,300,100])
                self.message("Game Over",BLACK,SCREENWIDTH*0.46,SCREENHEIGHT*0.45,40)
            pygame.draw.rect(self.screen, GREEN, [SCREENWIDTH* 0.4,SCREENHEIGHT*0.6,300,100])
            self.message("Your score: " +str(self.SCORE),BLACK,SCREENWIDTH*0.45,SCREENHEIGHT*0.65,40)
            pygame.draw.rect(self.screen, YELLOW, [SCREENWIDTH* 0.34,SCREENHEIGHT*0.8,450,100])
            self.message("Press <Enter> to Play Continue or Q to Quit",BLACK,SCREENWIDTH*0.35,SCREENHEIGHT*0.85,30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_RETURN:
                        if self.LIVES == 0:
                            self.SCORE = 0
                        var = False
            pygame.display.update()
            self.clock.tick(FPS)

                    
        

    def gameloop(self):


        self.screen.fill(BLACK)
        self.makegrid()
        toplevel = self.makecage()
        curlevel = toplevel + FLOORGAP   #FIRST LADDER FROM TOP
        LEVEL=[]    # LEVEL STORES [ Y AXIS , LEFT_X , RIGHT_X , UPLADDER , DOWNLADDER ]
       

        # CREATING THE Y AXIS AND LEFT_X AND RIGHT_X OF FLOORS
        state = 0

        while curlevel + FLOORGAP < GROUNDHEIGHT:
            if state == 0 :
                LEVEL.append([curlevel,WALLWIDTH,round(random.randrange(SCREENWIDTH*0.6,SCREENWIDTH*0.8)/10.0)*10,0,0])
                state = 1
            elif state == 1 :
                LEVEL.append([curlevel,round(random.randrange(SCREENWIDTH*0.2,SCREENWIDTH*0.4)/10.0)*10,SCREENWIDTH - WALLWIDTH,0,0])
                state = 0
            curlevel+=FLOORGAP
            self.NUMLEVEL+=1
        
        
        
        
        HEIGHTS = []
        i = 0 
        for i in range(self.NUMLEVEL):
            HEIGHTS.append(LEVEL[i][0])
        
        HEIGHTS.append(GROUNDHEIGHT)

        LEVEL[0][3] = self.princessx*1.5    # PRINCESS LADDER
        
    
        # GROUND LADDER X AXIS
        GROUNDLADDERX = int(random.randrange(LEVEL[self.NUMLEVEL-1][1],LEVEL[self.NUMLEVEL-1][2]))
        
        
        # CREATING UPPER LADDER X AXIS 
        state = 1
        s = 1
        while s < self.NUMLEVEL:
            if state == 1:
                LEVEL[s][3] = round(random.randrange(LEVEL[s][1],LEVEL[s-1][2])/10.0)*10
                state = 0
            elif state == 0:
                LEVEL[s][3] = round(random.randrange(LEVEL[s-1][1],LEVEL[s][2])/10.0)*10
                state = 1
            s+=1

        # CREATING DOWN LADDER X AXIS
        s = 0
        while s < self.NUMLEVEL - 1:
            LEVEL[s][4]=LEVEL[s+1][3]
            s+=1

        self.BOOLARRAY.append([])
        self.COINS.append([])
        
        for i in range(self.NUMLEVEL):
            s = 0
            last = int(random.randrange(8,13))
            self.BOOLARRAY.append([])
            self.COINS.append([])
        
            for j in range(1,last):      ################################################################################ rotate coins 
                self.COINS[i].append(round(random.randrange(LEVEL[i][1],LEVEL[i][2]-30)/10.0)*10)
                self.BOOLARRAY[i].append(0)
                s+=1
            self.NUMCOINS.append(s)




        self.dragony = toplevel + FLOORGAP -DRAGONHEIGHT + 20


        # DOWNLADDER OF BOTTOM MOST LEVEL
        LEVEL[self.NUMLEVEL-1][4] = GROUNDLADDERX


        #self.ballx = round(random.randrange(LEVEL[0][1],LEVEL[0][2])/10.0)*10
        #self.bally = LEVEL[0][0]
        for i in range(self.NUMLEVEL):
            print LEVEL[i][0],LEVEL[i][1],LEVEL[i][2]

        v = 10
        randdragon = round(random.randrange(LEVEL[0][1],LEVEL[0][2])/10.0)*10
        if randdragon > self.dragonx:
            self.dragonxchange = 5
        elif randdragon < self.dragonx:
            self.dragonxchange = -5
        self.LIVES = 3
        realindex = 0 
        
        
        ##########################################################################
        ######################### GAME LOOP #################################
        
        freefall = 0
        while True:


            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen,(84,84,84), [SCREENWIDTH* 0.8,SCREENHEIGHT*0.05,180,120])
            
            self.message("LEVEL: " + str(LEVELNUMBER),BLACK,SCREENWIDTH*0.82,SCREENHEIGHT*0.06,40)
            self.message("SCORE: " + str(self.SCORE),BLACK,SCREENWIDTH*0.82,SCREENHEIGHT*0.12,40)
            self.message("LIVES: " + str(self.LIVES),BLACK,SCREENWIDTH*0.82,SCREENHEIGHT*0.16,40)

            if self.LIVES == 0:
                break
            self.makegrid()
            toplevel = self.makecage()
           
            
            if self.dragonx == randdragon:
                self.makeballs(toplevel,LEVEL,randdragon)
                randdragon = round(random.randrange(LEVEL[0][1] ,LEVEL[0][2])/10.0)*10
                if self.dragonx == randdragon:
                    randdragon+=20
                if randdragon > self.dragonx:
                    self.dragonxchange = DRAGONMOVE
                elif randdragon < self.dragonx:
                    self.dragonxchange = -DRAGONMOVE



            i = 0
            for i in range(self.NUMLEVEL):
                self.makefloor(LEVEL[i][1],LEVEL[i][0],LEVEL[i][2])
           
            
            i = 1
            while i < self.NUMLEVEL:
                self.makeladder(LEVEL[i][3],LEVEL[i][0]+20,LEVEL[i-1][0])
                i+=1

            self.makeladder(LEVEL[0][3],LEVEL[0][0]+20,toplevel-5)                   # PRINCESS LADDER
            self.makeladder(GROUNDLADDERX,GROUNDHEIGHT,LEVEL[self.NUMLEVEL-1][0])    #BOTTOM MOST LADDER
        
            ################################################################################

            ####################################################################
            ############## GAME QUIT, PLAYER MOVEMENTS FOR ALL LEVELS ##########

            self.RANDBOOL = True 
            for self.index in range(self.NUMLEVEL):
                if LEVEL[self.index][0] == self.leady + 40:
                    realindex = self.index
                    freefall = 0
                    self.ychange = 0
                    self.RANDBOOL = False
                    for event in pygame.event.get():
                        self.checkexit(event)
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.JUMP =True
                                v  = 10
                                self.leady -=v
                                v-=1
                            if (self.leadx >= LEVEL[self.index][3] - 20) and (self.leadx <= LEVEL[self.index][3] +10):
                                if event.key == pygame.K_w:
                                    self.recent = pygame.K_w
                                    self.ychange = -5
                                    self.xchange = 0
                            if (self.leadx >= LEVEL[self.index][4] - 20) and ( self.leadx <= LEVEL[self.index][4]):
                                if event.key == pygame.K_s:
                                    self.recent = pygame.K_s
                                    self.ychange = 5
                                    self.xchange = 0
                            if event.key == pygame.K_a:
                                    self.xchange = -10
                                    self.recent = pygame.K_a
                            elif event.key == pygame.K_d:
                                    self.recent = pygame.K_d
                                    self.xchange = 10
                        elif event.type == pygame.KEYUP and event.key == self.recent:
                            self.xchange = 0
                            self.ychange = 0
                    break


            #########################################################
            ######### PLAYER MOVEMENTS FOR GROUNDLEVEL ##############
                

            if self.leady == PLAYERY:
                freefall =0 
                for event in pygame.event.get():
                    self.checkexit(event)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.JUMP = True
                            v = 10
                            self.leady -=v
                            v-=1

                        if (self.leadx  >= GROUNDLADDERX -20) and (self.leadx <= GROUNDLADDERX + 10):
                            if event.key == pygame.K_w:
                                self.recent = pygame.K_w
                                self.ychange =-5
                                self.xchange = 0
                        if event.key == pygame.K_a :
                            self.recent = pygame.K_a     #ADD CONDITIONS
                            self.xchange = -10
                            self.ychange = 0
                        elif event.key == pygame.K_d:
                            self.recent = pygame.K_d
                            self.xchange = 10
                            self.ychange = 0
                    elif event.type == pygame.KEYUP and event.key == self.recent:
                        self.xchange=0
                        self.ychange =0

            ##########################################################
            ########## PLAYER MOVEMENTS FOR QUEEN'S CAGE ###########
            elif self.leady + 45 == toplevel:
                for event in pygame.event.get():
                    self.checkexit(event)
                    if event.type == pygame.KEYDOWN:
                        if (self.leadx >= LEVEL[0][3] - 20) and (self.leadx <= LEVEL[0][3] +10):
                            if event.key == pygame.K_s:
                                self.recent = pygame.K_s
                                self.ychange = 5
                                self.xchange = 0
                        if event.key == pygame.K_a:
                                self.recent = pygame.K_a     #ADD CONDITIONS
                                self.xchange = -10
                                self.ychange = 0
                        elif event.key == pygame.K_d:
                            self.recent = pygame.K_d
                            self.xchange = 10
                            self.ychange =0
                    if event.type == pygame.KEYUP and event.key == self.recent:
                        self.xchange=0
            elif self.RANDBOOL:
                if self.JUMP and not freefall :
                    if v == 0:
                        v=-1
                    self.leady -=v
                    v-=1
                    if v == -11:
                        self.JUMP =False

                else:
                    for event in pygame.event.get():
                        self.checkexit(event)
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_w:
                                self.recent = pygame.K_w     #ADD CONDITIONS
                                self.ychange = -5
                                self.xchange = 0
                            elif event.key == pygame.K_s:
                                self.recent = pygame.K_s
                                self.ychange = 5
                                self.xchange = 0
                        if event.type == pygame.KEYUP and event.key == self.recent:
                            self.ychange=0
            
            if self.leady +40 == LEVEL[0][0]:
                if self.leadx == self.dragonx or (self.dragonx + DRAGONWIDTH >self.leadx and self.leadx > self.dragonx):
                    self.leadx = PLAYERX
                    self.leady = PLAYERY
                    self.xchange = self.ychange = 0
                    self.LIVES-=1
                    self.SCORE-=25
                    pygame.mixer.Sound.play(explodesound)


            
            if not self.RANDBOOL and not self.JUMP:
                if (self.leadx < LEVEL[self.index][1] or self.leadx + PLAYERWIDTH/2 > LEVEL[self.index][2] )and not self.JUMP:
                    freefall = 10
            if self.leady + 45 <= toplevel:
                self.leady = toplevel - 45



            if freefall and not self.JUMP:
                self.leady+=freefall
                self.xchange = 0
            

            self.leadx += self.xchange
            self.leady += self.ychange
            self.dragonx+=self.dragonxchange
            
            self.checkCollision(HEIGHTS,LEVEL)
            self.collectCoins(LEVEL) 
            
            if self.leady + 45 == toplevel:
                if self.leadx < self.princessx+ 25:
                    self.leadx = self.princessx + 25
                    self.SCORE+=50
                    break
                if self.leadx + 30 > self.princessx*1.8:
                    self.leadx = self.princessx*1.8-30
            
            self.checkWall()
            
            self.screen.blit(player_img,(self.leadx,self.leady))
            self.screen.blit(dragon_img,(self.dragonx,self.dragony))
            pygame.display.update()
            self.clock.tick(FPS)

        self.gameover()



def main():
    global FLOORGAP
    global BALLXCHANGE
    global LEVELNUMBER 
    templist = range(100000) 
    i = 0
    templist[i]= board()
    templist[i].intro()
    nextlevel = False
    counter = 0
    while i<5:
        if templist[i].LIVES<=0:
            nextlevel = False
        if templist[i].LIVES >0:
            nextlevel = True
        if nextlevel:
            counter+=1
            FLOORGAP -=20
            LEVELNUMBER+=1
            if counter >1:
                BALLXCHANGE = 10
                
        templist[i+1]=board()
        templist[i+1].SCORE= templist[i].SCORE
        templist[i+1].gameloop()
        i+=1




if __name__ == "__main__":
    main()


