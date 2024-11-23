import pygame


def get_mouse_pos(square_size: int) -> tuple[int, int]:
    """
    Gets current position mouse position in the grid
    :param square_size: size of the square
    """

    y, x = pygame.mouse.get_pos()
    row = y // square_size
    col = x // square_size
    return row, col


def get_eucl_dist(x1: int, x2: int, y1: int, y2: int) -> int:
    """
    Gets the Euclidean distance
    :param x1: x position of the first node
    :param x2: x position of the second node
    :param y1: y position of the first node
    :param y2: y position of the second node
    """

    return ((x1 - x2) ** 2) + ((y1 - y2) ** 2)


def get_manh_distance(x1: int, x2: int, y1: int, y2: int) -> int:
    """
    Gets the Manhattan distance
    :param x1: x position of the first node
    :param x2: x position of the second node
    :param y1: y position of the first node
    :param y2: y position of the second node
    """

    return abs(x2 - x1) + abs(y2 - y1)
