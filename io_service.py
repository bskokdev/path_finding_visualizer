import sys

import pygame
from pygame.event import Event

from constants import SQUARE_SIZE
from node import Grid, Node, NodeType
from utils import get_mouse_pos

"""
This function checks for valid start or end position
if the position is valid, coordinates at the given position will be modified
otherwise error message will be printed
"""


def checkPosition(
    position_type: str,
    is_taken: bool,
    modify_node,
    coordinates: list[int, int],
    row: int,
    col: int,
) -> None:
    if position_type == "start" and is_taken:
        print("Only one starting position!")
    elif position_type == "end" and is_taken:
        print("Only one end position!")
    else:
        modify_node()
        # updates coordinates to the selected ones
        coordinates[0] = row
        coordinates[1] = col


"""
this function handles mouse click of the user
left click = barrier
right click = reset
"""


def handle_mouse_click(data_grid: [[Node]], row: int, col: int) -> None:
    square: Node = data_grid[row][col]
    if pygame.mouse.get_pressed()[0]:
        square.make_barrier()
    if pygame.mouse.get_pressed()[2]:
        square.reset()


"""
This function handles keyboard input of the user
S = select start position
E = select end position
P = find the shortest path
"""


def handle_keyboard_input(
    event, grid: Grid, row: int, col: int, runtime: [bool], start_position, end_position
) -> None:
    # doesn't allow any strokes during path finding
    if event.type == pygame.KEYDOWN and not runtime[2]:
        if grid.data[row][col].type != NodeType.BARRIER:
            """Start position"""
            if event.key == pygame.K_s:
                checkPosition(
                    "start",
                    runtime[0],
                    grid.data[row][col].make_path,
                    start_position,
                    row,
                    col,
                )
                runtime[0] = True
            """End position"""
            if event.key == pygame.K_e:
                checkPosition(
                    "end",
                    runtime[1],
                    grid.data[row][col].make_end,
                    end_position,
                    row,
                    col,
                )
                runtime[1] = True
        """Reset grid"""
        if event.key == pygame.K_r:
            grid.clear_grid()
            runtime[0], runtime[1] = False, False
        """Find path"""
        if event.key == pygame.K_p:
            if runtime[0] and runtime[1]:
                runtime[2] = True
                if grid.find_path_between_start_end():
                    runtime[2] = False
            else:
                print("no start or end position!")


"""
This function handles mouse and keyboard input
"""


def handle_input(
    event: Event, grid: Grid, runtime: [bool], start_position, end_position
) -> None:
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    # current mouse position
    row, col = get_mouse_pos(SQUARE_SIZE)
    handle_mouse_click(grid.data, row, col)
    handle_keyboard_input(event, grid, row, col, runtime, start_position, end_position)
