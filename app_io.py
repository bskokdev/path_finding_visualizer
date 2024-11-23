import sys

import pygame
from pygame.event import Event

from graph import Grid, Node, NodeType
from graph.grid_constants import SQUARE_SIZE
from graph.position import get_mouse_pos

"""
This module handles all the input from the user.
"""


def handle_input(
        event: Event, grid: Grid, runtime: [bool],
        start_position, end_position
) -> None:
    """
    Handles all the input.
    :param event: Pygame event
    :param grid: the grid
    :param runtime: runtime arguments
    :param start_position: start position
    :param end_position: end position
    """

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    # current mouse position
    row, col = get_mouse_pos(SQUARE_SIZE)
    _handle_mouse_click(grid.data, row, col)
    _handle_keyboard_input(
        event, grid, row, col,
        runtime, start_position, end_position
    )


def _handle_mouse_click(data_grid: [[Node]], row: int, col: int) -> None:
    """
    Handles mouse clicks.
    Left click = barrier
    right click = reset

    :param data_grid: The grid
    :param row: x position
    :param col: y position
    """

    square: Node = data_grid[row][col]
    if pygame.mouse.get_pressed()[0]:
        square.make_barrier()
    if pygame.mouse.get_pressed()[2]:
        square.reset()


def _handle_keyboard_input(
        event, grid: Grid, row: int, col: int,
        runtime: [bool],
        start_position, end_position
) -> None:
    """
    Handles keyboard input.

    S = select start position
    E = select end position
    P = find the shortest path
    R = reset grid

    :param event: pygame event
    :param grid: the grid
    :param row: x position
    :param col: y position
    :param runtime: runtime arguments
    :param start_position: start position
    :param end_position: end position
    """

    # do not allow any strokes during path finding
    if event.type == pygame.KEYDOWN and not runtime[2]:
        if grid.data[row][col].type != NodeType.BARRIER:
            # Mark as the start position
            if event.key == pygame.K_s:
                _check_position(
                    "start",
                    runtime[0],
                    grid.data[row][col].make_path,
                    start_position,
                    row,
                    col,
                )
                runtime[0] = True
            # Mark as the end position
            if event.key == pygame.K_e:
                _check_position(
                    "end",
                    runtime[1],
                    grid.data[row][col].make_end,
                    end_position,
                    row,
                    col,
                )
                runtime[1] = True
        # Reset grid
        if event.key == pygame.K_r:
            grid._clear_grid()
            runtime[0], runtime[1] = False, False
        # Find path
        if event.key == pygame.K_p:
            if runtime[0] and runtime[1]:
                runtime[2] = True
                if grid.find_path_between_start_end():
                    print("Path found")
                else:
                    print("No path")
                runtime[2] = False
            else:
                print("no start or end position!")


def _check_position(
        position_type: str, is_taken: bool,
        modify_node, coordinates,
        row: int, col: int,
) -> None:
    """
    Checks for valid position in the grid.
    The position is then modified in the grid if valid.

    :param position_type: Start or end
    :param is_taken: is the position already taken
    :param modify_node: function to modify the node
    :param coordinates: mutable coordinates list of the grid position
    :param row: x position
    :param col: y position
    """

    if position_type == "start" and is_taken:
        print("Only one starting position!")
    elif position_type == "end" and is_taken:
        print("Only one end position!")
    else:
        modify_node()
        # updates coordinates to the selected ones
        coordinates[0] = row
        coordinates[1] = col
