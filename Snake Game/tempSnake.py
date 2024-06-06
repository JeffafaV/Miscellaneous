import pygame
import sys
from enum import Enum
from collections import deque
import random
from itertools import islice

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Snake():
    def __init__(self, bounds):
        self.color = (0, 0, 255)
        self.body_part_dims = (20, 20)
        self.reset(bounds)

    def reset(self, bounds):
        default_pos = (bounds[0]-300, bounds[1]-200)
        snake_head = pygame.Rect(default_pos, self.body_part_dims)
        # instead of a queue of positions we can have a queue of rects which also hold positions
        self.snake_body = deque([snake_head])
        self.current_dir = Direction.RIGHT
    
    def draw(self, game_window):
        for body_part in self.snake_body:
            pygame.draw.rect(game_window, self.color, body_part)
    
    def steer(self, keys):
        # uncomment
        if (keys[pygame.K_LEFT] and self.current_dir != Direction.RIGHT and 
                not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]):
            self.current_dir = Direction.LEFT
        
        elif (keys[pygame.K_RIGHT] and self.current_dir != Direction.LEFT and 
                not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]):
            self.current_dir = Direction.RIGHT
        
        elif (keys[pygame.K_UP] and self.current_dir != Direction.DOWN and 
                not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN]):
            self.current_dir = Direction.UP
        
        elif (keys[pygame.K_DOWN] and self.current_dir != Direction.UP and 
                not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP]):
            self.current_dir = Direction.DOWN

    
    def move(self, fruit, bounds):
        snake_head = self.snake_body[0]

        # we move by appending a new segment of the snake and popping the last segment
        new_part = None

        if self.current_dir == Direction.UP:
            new_part = (snake_head.left, snake_head.top - self.body_part_dims[1])
            
        elif self.current_dir == Direction.DOWN:
            new_part = (snake_head.left, snake_head.top + self.body_part_dims[1])
            
        elif self.current_dir == Direction.LEFT:
            new_part = (snake_head.left - self.body_part_dims[0], snake_head.top)
            
        elif self.current_dir == Direction.RIGHT:
            new_part = (snake_head.left + self.body_part_dims[0], snake_head.top)
        
        self.snake_body.appendleft((pygame.Rect(new_part, self.body_part_dims)))

        if not self.collides_with_food(fruit):
            self.snake_body.pop()
        else:    
            fruit.spawn(bounds)
    
    def collides_with_food(self, fruit):
        snake_head = self.snake_body[0]

        #print(fruit.fruit_pos[0])

        if snake_head.topleft == fruit.fruit_rec.topleft:
            return True

        return False
    
    def out_of_bounds(self, bounds):
        snake_head = self.snake_body[0]
        # x
        if snake_head.left < 0 or snake_head.left >= bounds[0]:
            return True
        # y
        if snake_head.top < 0 or snake_head.top >= bounds[1]:
            return True
        
        return False

    def collides_with_tail(self):
        if len(self.snake_body) == 1:
            return False
        
        snake_head = self.snake_body[0]

        # deque doesn't support slicing and indexing is inefficient so this is a workaround
        body = deque(islice(self.snake_body, 1, len(self.snake_body)))
        for body_part in body:
            if body_part.topleft == snake_head.topleft:
                return True
        
        return False

class Fruit():
    def __init__(self, bounds):
        self.color = (0, 255, 0)
        self.fruit_dims = (20, 20)
        self.spawn(bounds)

    def spawn(self, bounds):
        fruit_pos = (random.randint(0, (bounds[0] // 20)-1) * 20, random.randint(0, (bounds[1] // 20)-1) * 20)
        self.fruit_rec = pygame.Rect(fruit_pos, self.fruit_dims)

    def draw(self, game_window):
        pygame.draw.rect(game_window, self.color, self.fruit_rec)

def main_game_loop():
    # window setup
    size_x = 720 # width of window
    size_y = 480 # height of window

    # tuple for the dimensions of the game window
    bounds = (size_x, size_y)

    # initializes all necessary pygame modules
    pygame.init()
    
    game_window = pygame.display.set_mode(bounds)
    pygame.display.set_caption("Snake")

    snake = Snake(bounds)
    fruit = Fruit(bounds)
    #fruit.spawn(bounds)

    # game states
    run = True
    pause = False

    # game continues to run until both states are false
    while run or pause:
        
        # pause state is true
        while pause:
            #print('Paused')
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
            #print('Running')
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
            
            keys = pygame.key.get_pressed()
            snake.steer(keys)
            
            game_window.fill((0, 0, 0))
            snake.move(fruit, bounds)
            
            # might put this in the move function
            if snake.out_of_bounds(bounds) or snake.collides_with_tail():
                snake.reset(bounds)
            fruit.draw(game_window)
            snake.draw(game_window)
            
            pygame.display.update()
            pygame.time.Clock().tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_game_loop()