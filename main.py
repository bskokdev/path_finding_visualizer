import pygame

from app_io import handle_input
from graph import Grid
from graph.grid_constants import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    GRID_SIDE_SIZE,
)


def run() -> None:
    """
    The function which runs the program.
    """

    window = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    pygame.display.set_caption("Path finding visualizer")
    canvas = Grid(GRID_SIDE_SIZE, window)

    # runtime[0] = is_start
    # runtime[1] = is_end
    # runtime[2] = is_running
    runtime = [False] * 3
    while True:
        canvas._draw_grid_with_nodes()
        for event in pygame.event.get():
            handle_input(
                event, canvas, runtime,
                canvas.start_position, canvas.end_position
            )


if __name__ == "__main__":
    run()
