# Images
import pygame
from const import *


coinsound = pygame.mixer.Sound('./coin.wav')
explodesound = pygame.mixer.Sound('./explode1.wav')

player_img = pygame.image.load('./boy.png')
player_img = pygame.transform.scale(player_img,(PLAYERWIDTH,PLAYERHEIGHT))

star_img = pygame.image.load('./Star.png')
star_img = pygame.transform.scale(star_img,(STARWIDTH,STARHEIGHT))

wall_img = pygame.image.load('./Wood_Block_Tall.png')
wall_img = pygame.transform.scale(wall_img,(WALLWIDTH,WALLHEIGHT))
wall_rotate_img = pygame.transform.rotate(wall_img,90)

floor_img = pygame.image.load('./Rock.png')
floor_img = pygame.transform.scale(floor_img,(FLOORWIDTH,FLOORHEIGHT))

ladder_img = pygame.image.load('./mock2.png')
ladder_img = pygame.transform.scale(ladder_img,(LADDERWIDTH,LADDERHEIGHT))

princess_img = pygame.image.load('./princess.png')
princess_img = pygame.transform.scale(princess_img,(PRINCESSWIDTH,PRINCESSHEIGHT))

ball_img = pygame.image.load('./fl.png')
ball_img = pygame.transform.scale(ball_img,(BALLWIDTH,BALLHEIGHT))

brick_img = pygame.image.load('./brick2.png')
brick_img = pygame.transform.scale(brick_img,(BRICKWIDTH,BRICKHEIGHT))


dragon_img = pygame.image.load('./dra.png')
dragon_img = pygame.transform.scale(dragon_img,(DRAGONWIDTH,DRAGONHEIGHT))


