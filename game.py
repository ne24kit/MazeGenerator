import pygame
from solve import *
from maze import Maze, Cell, alg_DFS, alg_Prim


class Globals():
    START_COLOR = (255, 255, 0)
    END_COLOR = (100, 194, 237)
    COLOR = (255, 100, 98) 
    SURFACE_COLOR = (167, 255, 100) 
    PATH_COLOR = (80, 200, 120) 
    CELL_SIZE = 20
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
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 1.25 * Globals.CELL_SIZE, 1.25 * Globals.CELL_SIZE
    
    
    def update(self, walls_sprites_list, group_players):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        
        
        if keystate[pygame.K_LEFT]:
            self.speedx = -2
        if keystate[pygame.K_RIGHT]:
            self.speedx = 2
        if keystate[pygame.K_DOWN]:
            self.speedy = 2
        if keystate[pygame.K_UP]:
            self.speedy = -2
        
        #как - нибудь .copy()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        hits = pygame.sprite.groupcollide(walls_sprites_list, group_players,  False, False)
        for hit in hits.keys():
            if hit.rect.right >= self.rect.left or hit.rect.left <= self.rect.right:
                self.rect.x += -self.speedx
            if hit.rect.top <= self.rect.bottom or hit.rect.bottom >= self.rect.top:
                self.rect.y += -self.speedy
        
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)


def start_game(alg, width, height, filename, solution):
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
    

    player = Player()
    group_players = pygame.sprite.Group()
    group_players.add(player)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()  
                quit()

        walls_sprites_list.update() 
        solution_sprites_list.update()
        group_players.update(walls_sprites_list, group_players)
        start_end_cells.update()


        screen.fill(Globals.SURFACE_COLOR)
        walls_sprites_list.draw(screen)
        solution_sprites_list.draw(screen)
        start_end_cells.draw(screen)
        group_players.draw(screen)
        
        pygame.display.flip() 
        clock.tick(60)
