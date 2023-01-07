from queue import PriorityQueue

import pygame

from constants import BLACK, SQUARE_SIZE, WHITE, WINDOW_WIDTH, WINDOW_HEIGHT
from utils import get_eucl_dist
from . import NodeType
from .node import Node


class Grid:
    def __init__(self, width: int, window):
        self.window = window
        self.height: int = width
        self.width: int = width
        self.data: [[Node]] = self.create_node_grid()
        # start and end position are represented as lists so they are mutable
        self.start_position: list[int, int] = [0, 0]
        self.end_position: list[int, int] = [0, 0]

    """
    This function marks the edge nodes as barriers
    """

    def make_edges_barriers(self, grid: [[Node]]):
        for i in range(self.height):
            grid[0][i].make_barrier()
            grid[self.width - 1][i].make_barrier()
        for i in range(self.width):
            grid[i][0].make_barrier()
            grid[i][self.height - 1].make_barrier()

    """
    This function creates and returns 2d array of Nodes from height and width
    """

    def create_node_grid(self) -> [[Node]]:
        grid: [[Node]] = [
            [Node(row, col, NodeType.BLANK) for col in range(self.width)]
            for row in range(self.height)
        ]
        self.make_edges_barriers(grid)
        return grid

    """
    This function visualizes A* search from start to end node
    node has 8 neighbors
    node can also have just 4 neighbors - Manhattan distance
    open list is represented as PriorityQueue (min heap)
    """

    def find_path_between_start_end(self) -> bool:
        # connected nodes directions
        dRow = [-1, -1, -1, 0, 0, 1, 1, 1]
        dCol = [-1, 0, 1, -1, 1, -1, 0, 1]

        # use this for only 4 directions
        # dRow = [-1, 1, 0, 0]
        # dCol = [0, 0, 1, -1]

        start: Node = self.data[self.start_position[0]][self.start_position[1]]
        open_list = PriorityQueue()
        closed_list = set()
        open_list.put(start)
        came_from = {}
        while open_list:
            current_node: Node = open_list.get()
            closed_list.add(current_node)

            row: int = current_node.row
            col: int = current_node.col
            # found path
            if (
                current_node.row == self.end_position[0]
                and current_node.col == self.end_position[1]
            ):
                self.create_path(came_from, current_node)
                return True
            # bounds check
            if (
                row <= 0
                or col <= 0
                or row >= self.height
                or col >= self.width
                or current_node.type == NodeType.BARRIER
            ):
                continue
            # traversal through connected nodes
            for offsetRow, offsetCol in zip(dRow, dCol):
                # calc offset for row and col = coordinates of each neighbor
                adj_x, adj_y = (row + offsetRow), (col + offsetCol)
                neighbor: Node = self.data[adj_x][adj_y]
                if neighbor in closed_list or neighbor.is_barrier():
                    continue
                temp_g_cost = current_node.g_cost + 1
                # looking for better path
                if temp_g_cost > neighbor.g_cost:
                    neighbor.g_cost = temp_g_cost
                    neighbor.h_cost = get_eucl_dist(
                        adj_x, self.end_position[0], adj_y, self.end_position[1]
                    )
                    neighbor.total_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.make_open()
                    came_from[neighbor] = current_node
                if neighbor not in open_list.queue:
                    open_list.put(neighbor)

            # updating the grid
            self.draw_grid_with_nodes()
            if current_node != start:
                current_node.make_closed()
        return False

    """
    This function reconstructs the found path from A* algorithm
    """

    def create_path(self, came_from, current: Node):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            self.draw_grid_with_nodes()

    """
    Draws nodes and grid over them
    """

    def draw_grid_with_nodes(self):
        self.window.fill(WHITE)
        for row in self.data:
            for node in row:
                node.draw(self.window)
        self.draw_grid(self.window)
        pygame.display.update()

    """
    Draws only lines
    """

    def draw_grid(self, window):
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
        self.data = self.create_node_grid()
