import neat
import time
import random
import pygame
import os
pygame.font.init()

WIDTH = 480
HEIGHT = 800

GEN = 0


os.chdir(os.path.dirname(os.path.abspath(__file__))) #Changing the directory to current working directory

BIRD = [pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","bird1.png"))), #Loading up the images
pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","bird2.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","bird3.png")))]

BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","bg.png")))
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","pipe.png")))
GROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets","base.png")))
FONT = pygame.font.SysFont("arial", 30)

class Pipe:
    PIPE_GAP = 200 #Defining the gap between the pipes  
    TERRAIN_VELOCITY = 5 #Defining the velocity of the terrain (This is the speed at which the terrain moves towards the left hand side)

    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.UPPER_PIPE = pygame.transform.flip(PIPE, False,True) #Flipping the image 
        self.BELOW_PIPE = PIPE

        self.passed = False 
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450) #The height of the pipe is randomly generated using this random function between the range(50,450)
        self.top =  self.height - self.UPPER_PIPE.get_height() #The height of the upper pipe is stored in self.top (The value is subtracted because in pygame y increases with negative values)
        self.bottom = self.height + self.PIPE_GAP #The height of the pipe below is determined by adding (that is decreasing the y axis by PIPE_GAP) self.PIPE_GAP

    def move(self):
        self.x -= self.TERRAIN_VELOCITY

    def draw(self,window):  
        window.blit(self.UPPER_PIPE, (self.x ,self.top))
        window.blit(self.BELOW_PIPE, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()  #Calling the bird's hitbox 
        upper_mask = pygame.mask.from_surface(self.UPPER_PIPE) 
        below_mask = pygame.mask.from_surface(self.BELOW_PIPE)

        upper_offset = (self.x - bird.x, self.top - round(bird.y))
        below_offset = (self.x - bird.x, self.bottom - round(bird.y))

        point_of_collision_upper = bird_mask.overlap(upper_mask, upper_offset) #If the hitbox of the bird and pipe overlap, it means there is a collision
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
    MAX_ROTATION = 25  #Once the bird jumps, it can tilt by 25 units (above or below)
    ROTATION_VELOCITY = 20  #Speed at which the bird rotates
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
        return pygame.mask.from_surface(self.img) #Creating the mask of the bird

def draw_window(window, birds, pipes, ground, score, gen):
    window.blit(BACKGROUND,(0,0)) #Drawing the background

    for pipe in pipes:
        pipe.draw(window) #Drawing the pipes

    text = FONT.render("Score:" + str(score), 1, (255,255,255))  #Rendering the score, anti-aliasing=1, 255,255,255 is white colour
    window.blit(text,(WIDTH - 10 - text.get_width(),10)) #Drawing the text at the (x,y) coordinates

    gentext = FONT.render("Gen:" + str(gen), 1, (255,255,255)) 
    window.blit(gentext,(10 ,10))

    for bird in birds: #Drawing the birds
        bird.draw(window)

    ground.draw(window)  #Drawing the ground
    
    pygame.display.update() #Updating for each frame

def main(genomes, config):
    global GEN
    GEN +=1
    nets = []
    ge = []
    birds = []
    ground = Ground(730)
    pipes = [Pipe(480)]

    for _,i in genomes:
        net = neat.nn.FeedForwardNetwork.create(i,config)
        nets.append(net)
        birds.append(Bird(210,320))
        i.fitness = 0
        ge.append(i)


    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    
    score = 0

    run = True
    
    while run:  #This is the main game loop
        clock.tick(30) #30 frames per second

        for event in pygame.event.get(): #This loop is used to quit the game
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].UPPER_PIPE.get_width():
                pipe_index = 1
        else:
            run = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1 

            #This is acting as an input to the neural network as a tuple of 3 values and based on the output it decides whether the bird should jump or not
            output = nets[i].activate((bird.y,abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom))) 

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        removed = []
        for pipe in pipes:
            for i,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1 #If the bird collides with the pipe, the fitness of that mutation should decrease
                    birds.pop(i) #Remove the bird if it collides from the array
                    nets.pop(i) #Remove the instance of neural network from the array
                    ge.pop(i) #Remove the state of that bird so that better population of bird can be generated in the next generations
                    

                if not pipe.passed and pipe.x < bird.x: #If the pipe has not been passed by the bird and the x coordinate of the bird is less than
                    pipe.passed = True                  #the x coordinate of the pipe then generate another pipe
                    add_pipe = True

            if pipe.x + pipe.UPPER_PIPE.get_width() < 0:
                removed.append(pipe)

            pipe.move()

        if add_pipe: #This condition is satisfied when the bird passes the pipe and is awarded with +5 fitness and the score is increased by 1
            score+=1
            for i in ge:
                i.fitness += 5
            pipes.append(Pipe(480)) #Add another pipe to be generated 

        for i in removed:
            pipes.remove(i)

        for i,bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:  #If the bird touches the top of the screen or the ground then remove it
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        ground.move()
        
        draw_window(window, birds, pipes, ground,score, GEN)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True)) #Detailed view of stats
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main,50)

if __name__ == "__main__":
    config_file = os.path.join("neat_config.txt")
    run(config_file)
