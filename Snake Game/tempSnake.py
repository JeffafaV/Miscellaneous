import pygame
import sys
from enum import Enum
from collections import deque
import random
from itertools import islice
import time

# enum used to help in steering the snake
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Snake():
    # initializes variables for snake
    def __init__(self, bounds):
        self.color = (0, 0, 255) # snake color
        self.body_part_dims = (20, 20) # snake width(x) and height(y)
        self.reset(bounds) # resets snake to its default
        self.velocity = 20 # move 1 tile or 20 pixels per second (240 pixels per second)

    # resets snake to a default position, size, and direction
    def reset(self, bounds):
        self.head_x = bounds[0] - 300
        self.head_y = bounds[1] - 200
        # default position of snake within bounds of game window
        default_pos = (self.head_x, self.head_y)
        # creates a rectangle object for the head of the snake
        snake_head = pygame.Rect(default_pos, self.body_part_dims)
        # insert snake head to the snake queue
        self.snake_body = deque([snake_head])
        # sets default direction to the right
        self.current_dir = Direction.RIGHT
        self.user_dirs = deque([])
    
    # displays snake to the game window
    def draw(self, game_window):
        # loop through each rectangle object in the snake body
        for body_part in self.snake_body:
            # draws body part to the window
            pygame.draw.rect(game_window, self.color, body_part)
    
    # changes movement direction of snake
    def steer(self, keys):
        # the steering logic would act strange if multiple movement keys are pressed
        # at once so I disabled steering unless one movement key is pressed at a time
        
        # change snake direction to the left only if the left key is pressed
        # and snake isn't moving to the right
        if (keys[pygame.K_LEFT] and self.current_dir != Direction.RIGHT and 
        not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]):
            
            if (len(self.user_dirs) == 0):
                self.user_dirs.appendleft(Direction.LEFT)
            elif len(self.user_dirs) != 0 and self.user_dirs[0] != Direction.LEFT:
                self.user_dirs.appendleft(Direction.LEFT)
        
        # change snake direction to the right only if the right key is pressed
        # and snake isn't moving to the left
        elif (keys[pygame.K_RIGHT] and self.current_dir != Direction.LEFT and 
        not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]):
            
            if (len(self.user_dirs) == 0):
                self.user_dirs.appendleft(Direction.RIGHT)
            elif len(self.user_dirs) != 0 and self.user_dirs[0] != Direction.RIGHT:
                self.user_dirs.appendleft(Direction.RIGHT)
        
        # change snake direction to up only if the up key is pressed
        # and snake isn't moving down
        elif (keys[pygame.K_UP] and self.current_dir != Direction.DOWN and 
        not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN]):
            
            if (len(self.user_dirs) == 0):
                self.user_dirs.appendleft(Direction.UP)
            elif len(self.user_dirs) != 0 and self.user_dirs[0] != Direction.UP:
                self.user_dirs.appendleft(Direction.UP)
        
        # change snake direction to down only if the down key is pressed
        # and snake isn't moving up
        elif (keys[pygame.K_DOWN] and self.current_dir != Direction.UP and 
        not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP]):
            
            if (len(self.user_dirs) == 0):
                self.user_dirs.appendleft(Direction.DOWN)
            elif len(self.user_dirs) != 0 and self.user_dirs[0] != Direction.DOWN:
                self.user_dirs.appendleft(Direction.DOWN)

    # turns the snake within the game window
    def turn(self, fruit, bounds, delta_time, calibrated_fps):
        # get the head of the snake from the queue
        snake_head = self.snake_body[0]
        user_dir = self.user_dirs[-1]

        # instead of shifting every part of the snake by 1 position we can just 
        # add a new segment at the front with the next position and delete the
        # last segment of the snake to mimic the snake moving
        
        # create a tuple to store the new body part's position
        new_part_pos = ()

        if user_dir == Direction.UP:
            self.head_y = self.head_y - self.velocity * delta_time * calibrated_fps
            rounded_y = round(self.head_y / self.body_part_dims[1]) * self.body_part_dims[1]
            
            new_part_pos = (snake_head.x, rounded_y)
            
        elif user_dir == Direction.DOWN:
            self.head_y = self.head_y + self.velocity * delta_time * calibrated_fps
            rounded_y = round(self.head_y / self.body_part_dims[1]) * self.body_part_dims[1]
            
            new_part_pos = (snake_head.x, rounded_y)
            
        elif user_dir == Direction.LEFT:
            self.head_x = self.head_x - self.velocity * delta_time * calibrated_fps
            rounded_x = round(self.head_x / self.body_part_dims[0]) * self.body_part_dims[0]
            
            new_part_pos = (rounded_x, snake_head.y)
            
        elif user_dir == Direction.RIGHT:
            self.head_x = self.head_x + self.velocity * delta_time * calibrated_fps
            rounded_x = round(self.head_x / self.body_part_dims[0]) * self.body_part_dims[0]
            
            new_part_pos = (rounded_x, snake_head.y)
        
        print(self.current_dir)
        if new_part_pos != snake_head.topleft:
            print(self.user_dirs)
            self.current_dir = self.user_dirs.pop()
            # append new body part to the front of the body queue
            self.snake_body.appendleft(pygame.Rect(new_part_pos, self.body_part_dims))
            
            # after moving check if the head of snake is not touching food
            if not self.collides_with_food(fruit):
                # since there is no food, we pop the last segment of the snake
                self.snake_body.pop()
            else:
                # note we don't pop here since the snake should grow by 1 part from eating
                # eat fruit and spawn new fruit
                fruit.spawn(bounds)
    
    
    # moves the snake within the game window
    def move(self, fruit, bounds, delta_time, calibrated_fps):
        # get the head of the snake from the queue
        snake_head = self.snake_body[0]

        # instead of shifting every part of the snake by 1 position we can just 
        # add a new segment at the front with the next position and delete the
        # last segment of the snake to mimic the snake moving
        
        # create a tuple to store the new body part's position
        new_part_pos = ()

        if self.current_dir == Direction.UP:
            self.head_y = self.head_y - self.velocity * delta_time * calibrated_fps
            rounded_y = round(self.head_y / self.body_part_dims[1]) * self.body_part_dims[1]
            
            new_part_pos = (snake_head.x, rounded_y)
            
        elif self.current_dir == Direction.DOWN:
            self.head_y = self.head_y + self.velocity * delta_time * calibrated_fps
            rounded_y = round(self.head_y / self.body_part_dims[1]) * self.body_part_dims[1]
            
            new_part_pos = (snake_head.x, rounded_y)
            
        elif self.current_dir == Direction.LEFT:
            self.head_x = self.head_x - self.velocity * delta_time * calibrated_fps
            rounded_x = round(self.head_x / self.body_part_dims[0]) * self.body_part_dims[0]
            
            new_part_pos = (rounded_x, snake_head.y)
            
        elif self.current_dir == Direction.RIGHT:
            self.head_x = self.head_x + self.velocity * delta_time * calibrated_fps
            rounded_x = round(self.head_x / self.body_part_dims[0]) * self.body_part_dims[0]
            
            new_part_pos = (rounded_x, snake_head.y)
        
        print(self.current_dir)
        if new_part_pos != snake_head.topleft:
            
            # append new body part to the front of the body queue
            self.snake_body.appendleft(pygame.Rect(new_part_pos, self.body_part_dims))
            
            # after moving check if the head of snake is not touching food
            if not self.collides_with_food(fruit):
                # since there is no food, we pop the last segment of the snake
                self.snake_body.pop()
            else:
                # note we don't pop here since the snake should grow by 1 part from eating
                # eat fruit and spawn new fruit
                fruit.spawn(bounds)
    
    # checks if snake is touching food
    def collides_with_food(self, fruit):
        # get the head of the snake from the queue
        snake_head = self.snake_body[0]

        # check if the snake head is touching food
        if snake_head.topleft == fruit.fruit_rec.topleft:
            return True

        # snake isn't touching food
        return False
    
    # check if the snake is out of bounds
    def out_of_bounds(self, bounds):
        # get the head of the snake from the queue
        snake_head = self.snake_body[0]
        
        # check if snake is out of bounds in the x direction
        if snake_head.left < 0 or snake_head.left >= bounds[0]:
            return True
        
        # check if snake is out of bounds in the y direction
        if snake_head.top < 0 or snake_head.top >= bounds[1]:
            return True
        
        # snake isn't out of bounds
        return False

    # check if snake collides with itself
    def collides_with_tail(self):
        # snake can't collide with itself if it is only a head
        if len(self.snake_body) == 1:
            return False
        
        # get the head of the snake from the queue
        snake_head = self.snake_body[0]

        # deque doesn't support bracket slicing and indexing is inefficient so this is a workaround
        # sets body to the snake body queue excluding the head
        body = deque(islice(self.snake_body, 1, len(self.snake_body)))

        x = 1
        print(f'{x} {snake_head.topleft}')
        
        # loop through entire body
        for body_part in body:
            x += 1
            print(f'{x} {body_part.topleft}')
            # check if head and body part are colliding
            if body_part.topleft == snake_head.topleft:
                pygame.time.delay(1000)
                sys.exit()
                return True
        
        # head isn't colliding with body
        return False

class Fruit():
    # initialize variables for fruit
    def __init__(self, bounds):
        self.color = (0, 255, 0) # fruit color
        self.fruit_dims = (20, 20) # fruit width and height
        self.spawn(bounds) # spawns a new fruit

    # creates a fruit at a random location
    def spawn(self, bounds):
        # tuple that calculates random position of fruit
        # note that we use 20 since each position is 20 pixels
        fruit_pos = (random.randint(0, (bounds[0] // 20)-1) * 20, random.randint(0, (bounds[1] // 20)-1) * 20)
        # creates a fruit rectangle at a random position
        self.fruit_rec = pygame.Rect(fruit_pos, self.fruit_dims)

    # displays the fruit to the game window
    def draw(self, game_window):
        # draws the fruit with the given color and rectangle object
        pygame.draw.rect(game_window, self.color, self.fruit_rec)

def main_game_loop():
    # window setup
    size_x = 720 # width of window
    size_y = 480 # height of window

    # tuple for the dimensions of the game window
    bounds = (size_x, size_y)

    # initializes all necessary pygame modules
    pygame.init()
    
    # set the dimensions of game window and title
    game_window = pygame.display.set_mode(bounds)
    pygame.display.set_caption("Snake")

    # creates a snake and fruit object
    snake = Snake(bounds)
    fruit = Fruit(bounds)
    #fruit.spawn(bounds)

    prev_time = time.time()
    fps = 60
    calibrated_fps = 12

    # game states
    run = True
    pause = False

    # game continues to run until both states are false
    while run or pause:
        
        # pause state is true
        while pause:
            # loops through events (i.e. clicks, keystrokes, etc.)
            for event in pygame.event.get():
                # check if user exits game window
                if event.type == pygame.QUIT:
                    # sets both states to false to terminate game
                    pause = False
                    run = False
                
                # check if user presses key
                if event.type == pygame.KEYDOWN:
                    # check if key pressed is the Esc key
                    if event.key == pygame.K_ESCAPE:
                        # changes to run state
                        pause = False
                        run = True
        
        # run state is true
        while run:
            curr_time = time.time()
            delta_time = curr_time - prev_time
            prev_time = curr_time

            # loops through events
            for event in pygame.event.get():
                # check if user exits game window
                if event.type == pygame.QUIT:
                    # sets run state to false to terminate game
                    run = False
                
                # check if user presses key
                if event.type == pygame.KEYDOWN:
                    # check if key pressed is the Esc key
                    if event.key == pygame.K_ESCAPE:
                        # changes to pause state
                        pause = True
                        run = False
            
            # contains a collection of all keys pressed and not pressed as booleans
            keys = pygame.key.get_pressed()
            
            # update direction of snake based on key press
            snake.steer(keys)

            # reset the game window to black
            # we do this so that whatever was drawn last frame doesn't stay
            # on the game window when we draw for the current frame
            game_window.fill((0, 0, 0))
            
            if len(snake.user_dirs) > 0:
                snake.turn(fruit, bounds, delta_time, calibrated_fps)
            else:
                # moves the snake
                snake.move(fruit, bounds, delta_time, calibrated_fps)
            
            # checks if the snake is out of bounds or colliding with itself
            if snake.out_of_bounds(bounds) or snake.collides_with_tail():
                # reset snake to its default position and size
                snake.reset(bounds)
                # move the snake
                snake.move(fruit, bounds, delta_time, calibrated_fps)
            
            # draw the fruit and snake
            fruit.draw(game_window)
            snake.draw(game_window)
            
            # display everything that was done to the game window
            # note that any visual manipulation that was done won't
            # be displayed until it reaches this line of code
            pygame.display.update()

            # FIXED
            # a note on this line of code and programming movement. this is the fps 
            # of the game and the lower I set it, the slower the snake becomes. I find 
            # that I have to lower the fps because if I don't then the snake is too 
            # fast. it is not ideal to set movement speed based on the fps. movement 
            # should be based on real time, more specifically delta time. delta time 
            # is the time between two frames or two iterations of the game loop. By 
            # using delta time the movement will always be the same no matter the fps.
            pygame.time.Clock().tick(fps)

    # terminates pygame and python
    pygame.quit()
    sys.exit()

# runs if we're running the script itself
# this won't run if this script is imported to another script
if __name__ == "__main__":
    main_game_loop()