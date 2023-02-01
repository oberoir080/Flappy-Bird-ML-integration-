import neat
import time
import random
import pygame
import os

WIDTH = 480
HEIGHT = 800


os.chdir(os.path.dirname(os.path.abspath(__file__))) #Changing the directory to current working directory

BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","bird1.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","bird2.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","bird3.png")))]

BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","bg.png")))
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","pipe.png")))
GROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","base.png")))

class Bird:
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        self.x = x  #Spawning coordinates of the bird
        self.y = y
        self.tilt = 0  #Tilt when it spawns
        self.tick_count = 0 
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = BIRD[0]

    def jump(self):
        self.vel = -10.5 #pygame uses (0,0) from the top left corner therefore negative value points upwards
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count +=1

        #Everytime it ticks it decreases the y axis [-10.5 + 1.5 = 9]
        down = self.vel*self.tick_count + 1.5*self.tick_count**2 

        if down>= 16:
            down = 16

        if down<0:
            down -= 2

        self.y = self.y + down #Updating the y-axis of the bird

        if down < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:  #Once the bird starts falling down it starts facing downwards
                self.tilt -= self.ROTATION_VELOCITY 

    def draw(self,window):
        self.img_count +=1
        
        #Adding animation
        if self.img_count<self.ANIMATION_TIME:
            self.img = BIRD[0]

        elif self.img_count<self.ANIMATION_TIME*2:
            self.img = BIRD[1]

        elif self.img_count<self.ANIMATION_TIME*3:
            self.img = BIRD[2]
        
        elif self.img_count<self.ANIMATION_TIME*4:
            self.img = BIRD[1]

        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = BIRD[0]
            self.img_count=0 #Resetting the value to zero so that it runs again while the game is running

        if self.tilt <= -80:
            self.img = BIRD[1] #No animation is required when the bird is falling downwards
            self.img_count = self.ANIMATION_TIME*2 #Once it jumps back up it shouldn't look like there was a frame skip

        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        window.blit(rotated_image,new_rect.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

def draw_window(window,bird):
    window.blit(BACKGROUND,(0,0)) #Drawing the background
    bird.draw(window)
    pygame.display.update() #Updating for each frame

def main():
    bird = Bird(210,320)
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    
    run = True
    
    while run:
        clock.tick(30) #30 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

        bird.move()
        draw_window(window,bird)

    pygame.quit()
    quit()

main()

        