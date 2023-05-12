
from typing import List
from grid import Point


def save_points(arr: List[Point], file_name: str):
    """ Saves the array of points to a file in guestures folder in the same directory
        [ (x1, y1), (x2, y2), ... ] -> guestures/{file_name}.txt
            x1 y1
            x2 y2
            ...
    """
    with open(f'guestures/{file_name}.txt', 'w') as f:
        for point in arr:
            f.write(f'{point[0]} {point[1]}\n')


def load_points(file_name: str) -> List[Point]:
    """ Loads the array of points from a file in guestures folder in the same directory
        guestures/{file_name}.txt -> [ (x1, y1), (x2, y2), ... ]
    """
    arr = []
    with open(f'guestures/{file_name}.txt', 'r') as f:
        for line in f.readlines():
            x, y = line.split()
            arr.append((int(x), int(y)))
    return arr
