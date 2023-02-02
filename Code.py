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

class Pipe:
    PIPE_GAP = 200
    TERRAIN_VELOCITY = 5

    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.UPPER_PIPE = pygame.transform.flip(PIPE, False,True)
        self.BELOW_PIPE = PIPE

        self.passed = False 
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top =  self.height - self.UPPER_PIPE.get_height()
        self.bottom = self.height + self.PIPE_GAP

    def move(self):
        self.x -= self.TERRAIN_VELOCITY

    def draw(self,window):
        window.blit(self.UPPER_PIPE, (self.x ,self.top))
        window.blit(self.BELOW_PIPE, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        upper_mask = pygame.mask.from_surface(self.UPPER_PIPE)
        below_mask = pygame.mask.from_surface(self.BELOW_PIPE)

        upper_offset = (self.x - bird.x, self.top - round(bird.y))
        below_offset = (self.x - bird.x, self.bottom - round(bird.y))

        point_of_collision_upper = bird_mask.overlap(upper_mask, upper_offset)
        point_of_collision_below = bird_mask.overlap(below_mask, below_offset)

        if point_of_collision_upper or point_of_collision_below:
            return True

        return False


class Ground:
    TERRAIN_VELOCITY = 5
    WIDTH = GROUND.get_width()
    
    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.TERRAIN_VELOCITY
        self.x2 -= self.TERRAIN_VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(GROUND, (self.x1, self.y))
        window.blit(GROUND, (self.x2, self.y))
        
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

def draw_window(window, bird, pipes, ground):
    window.blit(BACKGROUND,(0,0)) #Drawing the background

    for pipe in pipes:
        pipe.draw(window)

    ground.draw(window)
    bird.draw(window)
    pygame.display.update() #Updating for each frame

def main():
    bird = Bird(210,320)
    ground = Ground(730)
    pipes = [Pipe(700)]

    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    
    score = 0

    run = True
    
    while run:
        clock.tick(30) #30 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

        # bird.move()
        add_pipe = False
        removed = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.UPPER_PIPE.get_width() < 0:
                removed.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score+=1
            pipes.append(Pipe(700))

        for i in removed:
            pipes.remove(i)

        ground.move()

        draw_window(window, bird, pipes, ground)

    pygame.quit()
    quit()

main()

        