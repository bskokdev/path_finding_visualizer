import pygame

"""
This function gets current position of user's mouse in the 2d array
"""


def get_mouse_pos(square_size: int) -> tuple[int, int]:
    y, x = pygame.mouse.get_pos()
    row = y // square_size
    col = x // square_size
    return row, col


"""
Euclidean distance
"""


def get_eucl_dist(x1: int, x2: int, y1: int, y2: int) -> int:
    return ((x1 - x2) ** 2) + ((y1 - y2) ** 2)


"""
Manhattan distance
"""


def get_manh_distance(x1: int, x2: int, y1: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)
