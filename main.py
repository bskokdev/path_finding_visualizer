import pygame

from constants import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    NODE_GRID_SIDE_SIZE,
    RUNTIME_ARGS_COUNT,
)
from io_module import handle_input
from graph import Grid


def run() -> None:
    """
    The function which runs the program.
    """

    window = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    pygame.display.set_caption("Path finding visualizer")
    canvas = Grid(NODE_GRID_SIDE_SIZE, window)

    # [0] = is_start
    # [1] = is_end
    # [2] = is_running
    runtime = [False] * RUNTIME_ARGS_COUNT
    while True:
        canvas.draw_grid_with_nodes()
        for event in pygame.event.get():
            handle_input(
                event, canvas, runtime,
                canvas.start_position, canvas.end_position
            )


if __name__ == "__main__":
    run()
