import pygame
from solve import *
from maze import Maze, Cell, alg_DFS, alg_Prim
from time import time


class Globals():
    START_COLOR   = (255, 255, 0)
    END_COLOR     = (100, 194, 237)
    COLOR         = (255, 100, 98) 
    SURFACE_COLOR = (167, 255, 100) 
    PATH_COLOR    = (80,  200, 120) 
    CELL_SIZE = 20
    END_GAME_TIME = [False, True]
# TODO: use this function in more places
def size_convert(value):
    return (2 * value + 1) * Globals.CELL_SIZE


class MazeElementWithGraphics(Cell, pygame.sprite.Sprite):
    def __init__(self, x, y, value):
        Cell.__init__(self, x, y)
        pygame.sprite.Sprite.__init__(self)
        self.value = value
        self.image = pygame.Surface([Globals.CELL_SIZE, Globals.CELL_SIZE])
        color = [Globals.SURFACE_COLOR, Globals.COLOR, Globals.PATH_COLOR, Globals.START_COLOR, Globals.END_COLOR]
        self.image.fill(color[value])
        pygame.draw.rect(self.image, color[value], pygame.Rect(x * Globals.CELL_SIZE, y * Globals.CELL_SIZE, Globals.CELL_SIZE, Globals.CELL_SIZE)) 
        self.rect = self.image.get_rect()
        self.rect.x = x * Globals.CELL_SIZE
        self.rect.y = y * Globals.CELL_SIZE


class MazeWithGraphics(Maze):
    def __init__(self, algorithm, size, run_alg=True, sol=False):
        super().__init__(algorithm, size, run_alg)
        if sol:
            self.solve()
        self.elems_to_draw = [[MazeElementWithGraphics(i, j, self.maze[j][i]) for i in range(2 * self.width + 1)] for j in range(2 * self.height + 1)]


    @classmethod        
    def upload(cls, path, algorithm, solution):
        new = super().upload(path, algorithm)
        if solution:
            new.solve()
        new.elems_to_draw = [[MazeElementWithGraphics(i, j, new.maze[j][i]) for i in range(2 * new.width + 1)] for j in range(2 * new.height + 1)]
        return new
    

    def add_start_end_to_group(self):
        start_end_cells = pygame.sprite.Group()
        self.maze[1][1] = 3
        self.maze[2 * self.height - 1][2 * self.width - 1] = 4
        self.elems_to_draw[1][1] = MazeElementWithGraphics(1, 1, self.maze[1][1])
        self.elems_to_draw[2 * self.height - 1][2 * self.width - 1] = MazeElementWithGraphics(2 * self.width - 1, 2 * self.height - 1, self.maze[2 * self.height - 1][2 * self.width - 1])
        start_end_cells.add(self.elems_to_draw[1][1], self.elems_to_draw[2 * self.height - 1][2 * self.width - 1])
        return start_end_cells


    def add_walls_to_group(self):
        walls_sprites_list = pygame.sprite.Group() 
        [[walls_sprites_list.add(self.elems_to_draw[j][i]) for i in range(2 * self.width + 1) if self.maze[j][i]  == 1 ] for j in range(2 * self.height + 1)]
        return walls_sprites_list
    

    def add_solution_to_group(self):
        solution_sprites_list = pygame.sprite.Group() 
        [[solution_sprites_list.add(self.elems_to_draw[j][i]) for i in range(2 * self.width + 1) if self.maze[j][i]  == 2 ] for j in range(2 * self.height + 1)]
        return solution_sprites_list



class Player(pygame.sprite.Sprite):
    def __init__(self, num=0):
        super().__init__() 
        self.num = num
        self.image = pygame.image.load("Player_blue.png")
        if self.num:
            self.image = pygame.image.load("Player_red.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 1.25 * Globals.CELL_SIZE, 1.25 * Globals.CELL_SIZE
    
    
    def update(self, walls_sprites_list, end_cell):
        global end_flag
        self.speedx = 0
        self.speedy = 0
        old_x, old_y = self.rect.topleft
        
        keystate = pygame.key.get_pressed()
        keys = {'left':  (pygame.K_LEFT,  pygame.K_a),
                'right': (pygame.K_RIGHT, pygame.K_d),
                'down':  (pygame.K_DOWN,  pygame.K_s),
                'up':    (pygame.K_UP,    pygame.K_w)}

        if keystate[keys['left'][self.num]]:
            self.speedx = -2
        if keystate[keys['right'][self.num]]:
            self.speedx = 2
        if keystate[keys['down'][self.num]]:
            self.speedy = 2
        if keystate[keys['up'][self.num]]:
            self.speedy = -2

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        for wall in walls_sprites_list:
            if self.rect.colliderect(wall.rect):
                self.rect.x = old_x
                self.rect.y = old_y

        # TODO: Add check on end cell
        if self.rect.colliderect(end_cell.rect) and not Globals.END_GAME_TIME[self.num]:
            Globals.END_GAME_TIME[self.num] = time()
            
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)


def start_game(alg, width, height, filename, solution, players_count):
    pygame.init()
    if filename:
        my_maze = MazeWithGraphics.upload(filename, alg, solution)
    else:
        my_maze = MazeWithGraphics(alg, (width, height), sol=solution)

    screen = pygame.display.set_mode((size_convert(my_maze.width), size_convert(my_maze.height)))

    pygame.display.set_caption("Try to solve!")
    pygame_icon = pygame.image.load('icon.png')
    pygame.display.set_icon(pygame_icon)
    clock = pygame.time.Clock() 
    

    walls_sprites_list = my_maze.add_walls_to_group()
    solution_sprites_list = my_maze.add_solution_to_group()
    start_end_cells = my_maze.add_start_end_to_group()  

    player_0 = Player(0)
    group_players = pygame.sprite.Group()
    group_players.add(player_0)

    if players_count == 2:
        player_1 = Player(1)
        group_players.add(player_1)
        Globals.END_GAME_TIME[1] = False
    start_time = time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("You couldn't solve it!")
                pygame.quit()  
                quit()

            if Globals.END_GAME_TIME[0] and Globals.END_GAME_TIME[1]: 
                print(f"BLUE TIME: {Globals.END_GAME_TIME[0] - start_time:.2f} sec")
                if players_count == 2:
                    print(f"RED TIME: {Globals.END_GAME_TIME[1] - start_time:.2f} sec")
                    print(f"WINNER: {'RED' if Globals.END_GAME_TIME[1] < Globals.END_GAME_TIME[0] else 'BLUE'}")
                pygame.quit()  
                quit()

        walls_sprites_list.update() 
        solution_sprites_list.update()
        group_players.update(walls_sprites_list, start_end_cells.sprites()[1])

        start_end_cells.update()


        screen.fill(Globals.SURFACE_COLOR)
        walls_sprites_list.draw(screen)
        solution_sprites_list.draw(screen)
        start_end_cells.draw(screen)
        group_players.draw(screen)
        
        pygame.display.flip() 
        clock.tick(60)


