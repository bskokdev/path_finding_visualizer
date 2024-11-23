from queue import PriorityQueue
from typing import List

import pygame

from colors import BLACK, WHITE
from graph.grid_constants import SQUARE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from graph.position import get_eucl_dist
from .node import Node, NodeType


class Grid:
    """
    Grid class that represents the grid of nodes
    Handles the drawing of the grid and path finding
    """

    def __init__(self, width: int, window):
        self.window = window
        self.height: int = width
        self.width: int = width
        self.data: [[Node]] = self._create_node_grid()
        # start and end position are represented as lists, so they are mutable
        self.start_position: List[int] = [0, 0]
        self.end_position: List[int] = [0, 0]
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        ]

    def _create_node_grid(self) -> [[Node]]:
        """
        Creates a grid of nodes
        :return: 2d array of nodes
        """

        grid: [[Node]] = [
            [Node(row, col, NodeType.BLANK, SQUARE_SIZE) for col in range(self.width)]
            for row in range(self.height)
        ]
        self._make_edges_barriers(grid)
        return grid

    def _make_edges_barriers(self, grid: [[Node]]):
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

        start_node = self.data[self.start_position[0]][self.start_position[1]]
        open_list, closed_list = PriorityQueue(), set()
        open_list.put(start_node)

        came_from = {}
        while open_list:
            curr = open_list.get()
            closed_list.add(curr)

            row, col = curr.row, curr.col

            # check if coordinates are in bounds and not a barrier
            if not self._is_in_bounds(row, col) or curr.is_barrier():
                continue

            # found the path
            if self._is_end(row, col):
                self._create_path(came_from, curr)
                return True

            # traverse all the neighbours nodes to the current one
            for dx, dy in self.directions:
                new_row, new_col = row + dy, col + dx
                neighbour = self.data[new_row][new_col]

                # invalid neighbour node
                if neighbour in closed_list or neighbour.is_barrier():
                    continue

                temp_g_cost = curr.g_cost + 1
                # look for a better path
                if temp_g_cost > neighbour.g_cost:
                    neighbour.g_cost = temp_g_cost
                    neighbour.h_cost = get_eucl_dist(
                        new_row, self.end_position[0],
                        new_col, self.end_position[1]
                    )
                    neighbour.total_cost = neighbour.g_cost + neighbour.h_cost
                    neighbour.open()

                    # update the parent of neighbour to the current node
                    came_from[neighbour] = curr
                if neighbour not in open_list.queue:
                    open_list.put(neighbour)

            # re-render the grid
            self._draw_grid_with_nodes()
            if curr != start_node:
                curr.close()

        return False

    def _is_end(self, row: int, col: int) -> bool:
        """
        Checks if the given position is the end position
        :param row: x position
        :param col: y position
        """

        return row == self.end_position[0] and col == self.end_position[1]

    def _is_in_bounds(self, row: int, col: int) -> bool:
        """
        Checks if the given position is in bounds
        :param row: x position
        :param col: y position
        """

        return 0 <= row < self.height and 0 <= col < self.width

    def _create_path(self, came_from, current: Node):
        """
        Reconstructs the path
        :param came_from: dictionary of nodes and their parents
        :param current: current node
        """

        while current in came_from:
            current = came_from[current]
            current.make_path()
            self._draw_grid_with_nodes()

    def _draw_grid_with_nodes(self):
        """
        Draws nodes and lines on the screen
        """

        self.window.fill(WHITE)
        for row in self.data:
            for node in row:
                node.draw(self.window)

        self._draw_grid_lines(self.window)
        pygame.display.update()

    def _draw_grid_lines(self, window):
        """
        Draws lines on the screen
        :param window: pygame window
        """

        for row in range(self.height):
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

    def _clear_grid(self):
        """
        Resets the grid to the initial state
        """

        self.data = self._create_node_grid()
