from enum import Enum
from typing import List, Tuple, Union
import pygame

Color = tuple[int, int, int] # Color type 
Point = Tuple[int, int] # Point type
class CubeState(Enum):
    EMPTY = 0
    FILLED = 1
    # SELECTED = 2


class Cube():
    def __init__(self, value: CubeState, row: int, col: int, width: float, height: float, win):
        self.value: CubeState = value
        self.row = row
        self.col = col
        # y,x mapping in pygame
        self.rect = pygame.Rect(col*width,row*height, width, height)
        self._color: Color = (200,50,120)
        self.centerFactor = 10
        self.win = win
    
    @property
    def color(self)-> Color:
        return self._color if self.value == CubeState.EMPTY else (0,0,0)

    def draw(self, win=None)-> None:
        win = self.win if win is None else win
        pygame.draw.rect(win, self.color , self.rect)


class Grid():

    def __init__(self,WIN, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400):
        self.rows, self.cols = rows, cols

        cube_height = height/self.rows
        cube_width = width/self.cols 

        self.surface = pygame.Surface((width,height))
        self.surface.fill((255,255,255))
        self.cubes = [
            [Cube(value=CubeState.EMPTY,row=i, col=j, width=cube_width, height=cube_height, win=self.surface)
                for j in range(self.cols)]
            for i in range(self.rows)
        ]

        self.width, self.height = width, height

        self.win = WIN
        self.blit()
        self.draw() if self.win is not None else 0
    
    @property 
    def cube_height(self) -> float:
        return self.height/self.rows
    
    @property
    def cube_width(self) -> float:
        return self.width/self.cols
    
    def draw_grid(self, win=None)-> None:
        '''Draw the grid'''
        # win = win if win is not None else self.win
        win = self.surface
        thick = 1
        BLACK = (0, 0, 0)

        # horizontal lines -----
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*self.cube_height),(self.width, self.cube_height*i), thick)
        # vertical lines |||
        for i in range(self.cols+1):
            pygame.draw.line(win, BLACK, (i*self.cube_width, 0), (self.cube_width*i, self.height))

    def draw(self, win = None)-> None:
        win = self.win if win is None else win
        win.blit(self.surface,(0,0))

    def blit(self):
        # Draw Cubes
        win = self.surface
        for row in self.cubes:
            for cube in row:
                cube.draw(win)

        # drawing grid
        self.draw_grid(win)
    
    def click(self,pos=None)-> None or Union[Cube, None]:
        '''
            Returns the Cube object based on the pos of mouse or given pos
        '''

        col, row = pos if pos is not None else pygame.mouse.get_pos()

        cube_height = self.height/self.rows
        cube_width = self.width/self.cols 
        
        col//= cube_width
        row//= cube_height
        # to remove the trailing zero
        col, row= int(col), int(row)

        if col >= self.cols or col < 0 or row >= self.rows or row < 0:
            return None
        
        return self[row, col]

    def reset(self) -> None:
        self.surface.fill((255,255,255))
        # change the value of the cubes 
        for row in self.cubes:
            for cube in row:
                cube.value = CubeState.EMPTY
        self.blit()
        self.draw()

    def update(self)-> None:
        if pygame.mouse.get_pressed()[0]:
            cube = self.click()
            if cube is not None:
                for i in range(cube.row-1, cube.row+2):
                    for j in range(cube.col-1, cube.col+2):
                        if i >= 0 and i < self.rows and j >= 0 and j < self.cols:
                            self[i,j].value = CubeState.FILLED
                            self[i,j].draw()
        self.draw()

    def __getitem__(self, pos:tuple[int, int])-> Cube:
        x = pos[0]
        y = pos[1]
        return self.cubes[x][y]
    
    def __setitem__(self, pos:tuple[int, int], value:CubeState)-> None:
        self.__getitem__(pos).value = value
    
    def __iter__(self):
        for row in self.cubes:
            for cube in row:
                yield cube
    
    # def get(self, x:int, y:int)-> Cube:
    #     return self.cubes[x][y]
    
    # def set(self, x:int, y:int, value:CubeState)-> None:


def get_points(grid: Grid) -> List[Point]:
    """ Gets the points from the grid """
    arr: List[Point] = []
    for cell in grid:
        if cell.value == CubeState.FILLED:
            arr.append((cell.row, cell.col))
    return arr