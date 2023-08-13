from queue import PriorityQueue
from typing import List

import pygame

from constants import BLACK, SQUARE_SIZE, WHITE, WINDOW_WIDTH, WINDOW_HEIGHT
from utils import get_eucl_dist
from . import NodeType
from .node import Node


class Grid:
    """
    Grid class that represents the grid of nodes
    Handles the drawing of the grid and path finding
    """

    def __init__(self, width: int, window):
        self.window = window
        self.height: int = width
        self.width: int = width
        self.data: [[Node]] = self.create_node_grid()
        # start and end position are represented as lists, so they are mutable
        self.start_position: List[int, int] = [0, 0]
        self.end_position: List[int, int] = [0, 0]

    def create_node_grid(self) -> [[Node]]:
        """
        Creates a grid of nodes
        :return: 2d array of nodes
        """

        grid: [[Node]] = [
            [Node(row, col, NodeType.BLANK) for col in range(self.width)]
            for row in range(self.height)
        ]
        self.make_edges_barriers(grid)
        return grid

    def make_edges_barriers(self, grid: [[Node]]):
        """
        Makes the edges of the grid barriers
        """

        # top and bottom edges
        for i in range(self.height):
            grid[0][i].make_barrier()
            grid[self.width - 1][i].make_barrier()

        # left and right edges
        for i in range(self.width):
            grid[i][0].make_barrier()
            grid[i][self.height - 1].make_barrier()

    def find_path_between_start_end(self) -> bool:
        """
        Finds the path between start and end position
        Looks in eight directions
        :return: True if the path is found, False otherwise
        """

        # move directions
        directions = [
            [-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]
        ]

        start_node = self.data[self.start_position[0]][self.start_position[1]]
        open_list, closed_list = PriorityQueue(), set()
        open_list.put(start_node)

        came_from = {}
        while open_list:
            curr: Node = open_list.get()
            closed_list.add(curr)

            row, col = curr.row, curr.col
            # bounds check
            if not self.is_in_bounds(row, col) or curr.is_barrier():
                continue

            # found the path
            if self.is_end(row, col):
                self.create_path(came_from, curr)
                return True

            for dx, dy in directions:
                nr, nc = row + dx, col + dy
                nei: Node = self.data[nr][nc]

                # invalid node
                if nei in closed_list or nei.is_barrier():
                    continue
                temp_g_cost = curr.g_cost + 1
                # looking for a better path
                if temp_g_cost > nei.g_cost:
                    nei.g_cost = temp_g_cost
                    nei.h_cost = get_eucl_dist(
                        nr, self.end_position[0],
                        nc, self.end_position[1]
                    )
                    nei.total_cost = nei.g_cost + nei.h_cost
                    nei.make_open()

                    # update the parent of nei to the current node
                    came_from[nei] = curr
                if nei not in open_list.queue:
                    open_list.put(nei)

            # re-render the grid
            self.draw_grid_with_nodes()
            if curr != start_node:
                curr.make_closed()
        return False

    def is_end(self, row: int, col: int) -> bool:
        """
        Checks if the given position is the end position
        :param row: x position
        :param col: y position
        """

        return row == self.end_position[0] and col == self.end_position[1]

    def is_in_bounds(self, row: int, col: int) -> bool:
        """
        Checks if the given position is in bounds
        :param row: x position
        :param col: y position
        """

        return 0 <= row < self.height and 0 <= col < self.width

    def create_path(self, came_from, current: Node):
        """
        Reconstructs the path
        :param came_from: dictionary of nodes and their parents
        :param current: current node
        """

        while current in came_from:
            current = came_from[current]
            current.make_path()
            self.draw_grid_with_nodes()

    def draw_grid_with_nodes(self):
        """
        Draws nodes and lines on the screen
        """

        self.window.fill(WHITE)
        for row in self.data:
            for node in row:
                node.draw(self.window)
        self.draw_grid(self.window)
        pygame.display.update()

    def draw_grid(self, window):
        """
        Draws lines on the screen
        :param window: pygame window
        """

        for row in range(self.width):
            pygame.draw.line(
                window,
                BLACK,
                (0, row * SQUARE_SIZE),
                (WINDOW_HEIGHT, row * SQUARE_SIZE),
            )
            for col in range(self.width):
                pygame.draw.line(
                    window,
                    BLACK,
                    (col * SQUARE_SIZE, 0),
                    (col * SQUARE_SIZE, WINDOW_WIDTH),
                )

    def clear_grid(self):
        """
        Resets the grid to the initial state
        """

        self.data = self.create_node_grid()
