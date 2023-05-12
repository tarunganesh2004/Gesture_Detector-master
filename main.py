from typing import Tuple
import pygame
import pygame_gui
from components import CallbackButton, get_text

from grid import Grid, CubeState, Point, get_points
from pygame_gui.elements import UITextEntryLine, UILabel
from guesture_handler.gusser import predict
from save_load_points import load_points, save_points

def save_button_fn(grid: Grid, text_box: UITextEntryLine) -> None:
    """ Saves the points from the grid """
    file_name = text_box.get_text().strip()
    file_name = file_name if file_name != "" else 'gesture' 
    arr = get_points(grid)
    save_points(arr, file_name)
    print(f'Saved {file_name}.txt')

def load_point_fn(grid: Grid, file_name: str) -> None:
    """ Loads the points from the file_name """
    arr = load_points(file_name)
    for point in arr:
        grid[point] = CubeState.FILLED

    grid.blit()
    grid.draw()

def run_prediction(grid: Grid, label: UILabel) -> None:
    arr = get_points(grid)
    prediction =  predict(arr) 

    label.set_text(f'The guesture predicted is: {prediction}')


def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Guesture Recognition')
    FPS = 60
    manager = pygame_gui.UIManager(
        (WIN.get_width(), WIN.get_height()))
    
    grid = Grid(WIN, cols=100, rows=100,
                width=SCREEN_WIDTH, height=SCREEN_HEIGHT-100)
    
    # create a surface for the manager with white color 
    manager_screen = pygame.Surface((600, 100))
    
    # create a label for showing the result 
    label = UILabel(relative_rect=pygame.Rect((0, 500), (600, 40)),
                                        text="Result: ", manager=manager)
    
    # create a textbox for the file name
    text_box = UITextEntryLine(relative_rect=pygame.Rect((0, 545), (200, 40)), manager=manager)
    text_box.placeholder_text = "Enter the gesture name: "

    CallbackButton(relative_rect=pygame.Rect((200, 545), (100, 40)), text="Save",
                   manager=manager, tool_tip_text=None,
                   func=lambda: save_button_fn(grid, text_box))
    
    # add a clear button
    CallbackButton(relative_rect=pygame.Rect((300, 545), (100, 40)), text="Clear",
                     manager=manager, tool_tip_text=None,
                     func=lambda: grid.reset())

    # add a predict button
    CallbackButton(relative_rect=pygame.Rect((400, 545), (100, 40)), text="Predict",
                        manager=manager, tool_tip_text=None,
                        func=  lambda: run_prediction(grid, label) )
    
    # add a load button
    CallbackButton(relative_rect=pygame.Rect((500, 545), (100, 40)), text="Load",
                        manager=manager, tool_tip_text=None,
                        func=lambda: load_point_fn(grid, text_box.get_text().strip()) )


    run = True
    while run:
        clock.tick(FPS)
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            manager.process_events(event)
        grid.update()
        WIN.blit(manager_screen, ( 0, 500 ))

        manager.update(time_delta=time_delta)
        manager.draw_ui(WIN)
        pygame.display.update() 
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()