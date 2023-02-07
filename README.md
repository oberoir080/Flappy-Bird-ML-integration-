  

# **Flappy Bird**

  

This code is a Flappy Bird clone game implemented in Python using Pygame library. The code contains classes for Bird, Pipe, Ground and the main game loop. The game will display a bird that needs to navigate through pipes by jumping, and the player needs to avoid colliding with the pipes. The code uses the Neat library for training the bird to play the game through machine learning.

  

## Table of Contents

1. [Classes](#classes) 
    1. [Bird Class](#birdclass)
    2. [Pipe Class](#pipeclass) 
    3. [Ground Class](#groundclass)
2. [NEAT File](#neatfile)
    1. [NEAT](#neat)
3. Future Implementations
    1. Adding a UI.
    2. Adding option to either play or watch the model learn.
    3. Adding a gamemode where the Player has to beat the score set by the model.
    4. Adding enemies in the game which shoot small projectiles towards the bird and the bird can either dodge or shoot back at the enemies. (Subject to change) 

  

## Classes <a name="classes"></a>
### Bird Class <a name="birdclass"></a>

- **init(self, x, y):** This is the constructor method of the class, which is called when a new instance of the class is created. It takes the x and y position of the bird as input and initializes the bird's attributes such as its position, tilt, tick count, velocity, height, animation count, and the default image.

- **jump(self):** This function is called when the bird is to jump. It sets the velocity to a negative value so that the bird moves upward, sets the tick count to 0, and updates the height of the bird.

- **move(self):** This function updates the position of the bird. It increments the tick count, calculates the velocity based on the tick count, updates the y-coordinate of the bird based on the velocity, and adds a tilt to the bird based on its velocity.

- **draw(self, window):** This function draws the bird on the window. It rotates the bird based on its tilt and updates the image of the bird every *ANIMATION_TIME* ticks to animate the bird's flapping.

- **get_mask(self):** This function returns a mask for the bird's image. The mask is used for collision detection.

- **rotate_bird(self):** This function calculates the tilt of the bird based on its velocity. The tilt is limited to MAX_ROTATION degrees.

  

### Pipe Class <a name="pipeclass"></a>

- **init(self,x):** This is the constructor method for the class. It sets the initial values for the attributes of the class such as position and height of the pipe.

- **set_height(self):** This function sets the height of the bottom and the upper pipe between the range 50 to 450. The range has been created with a little trial and error and best suits the pipe generation between this range.

- **move(self):** This function updates the position of the pipe in each frame, simulating its movement across the screen.

- **draw(self,window):** This function draws the pipes on the screen since the x coordinate is same for both the pipes it is entered as *self.x* in both the window.blit() function *self.top* and *self.bottom* (y coordinates) are updated from the function *set_height*.

- **collide(self,bird):** This function checks whether the bird has collided with the pipe. It calculates the coordinates of the bird and the pipe and checks whether they overlap.

  

### Ground Class <a name="groundclass"></a>

- **init(self,y):** This is the constructor method and is called when an object of the ground class is created. It sets up the initial properties of the ground object such as its position.

- **move(self):** move: This function updates the position of the ground on the screen. It takes the speed at which the ground should move as an argument, and updates the x-coordinate of the ground object to simulate movement.

- **draw(self,window):** This function draws the ground on the screen.

- *Why is it creating two grounds?* Because once the first sprite is off the screen (that is its x coordinate is less than 0), it gets reset and is added just behind the other ground sprite. This makes it look like the bird is moving forward, however it's the whole terrain that is moving and not the bird.



## NEAT File <a name="neatfile"></a> 
### NEAT <a name="neat"></a>

- **fitness_criterion:** Criterion for measuring the fitness of a network {The higher this value, the better is the bird performing}
- **fitness_threshold:** Minimum fitness required for termination {The neural network should be able to progress further without any problems}
- **pop_size:** Size of the population of networks {The number of birds that we start with}
- **reset_on_extinction:** Determines whether to reset the population when all networks go extinct {We don't want this as we want to train the neural network on the previous population of the bird}

## Acknowledgements

*P.S I haven't fiddled around with the other values in the neat_config file, and tried to understand as much as I can by watching the tutorials of TechWithTim and the NEAT documentation*

 - [TechWithTim's Tutorial Playlist](https://www.youtube.com/playlist?list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2s)
 - [NEAT Documentation](https://neat-python.readthedocs.io/en/latest/config_file.html)
 
 
## Screenshots

![App Screenshot](/Assets/Picture1.png)
![App Screenshot](/Assets/Picture2.png)




 
