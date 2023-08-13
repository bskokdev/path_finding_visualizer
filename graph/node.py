from typing import List

import pygame.draw

from constants import SQUARE_SIZE
from .node_type import NodeType


class Node:
    """
    This class represents a single square in the grid
    """

    def __init__(self, row: int, col: int, node_type: NodeType):
        self.row = row
        self.col: int = col
        self.type: NodeType = node_type
        self.neighbors: List[Node] = []
        self.g_cost: int = 0
        self.h_cost: int = 0
        self.total_cost: int = 0

    def draw(self, window) -> None:
        """
        Draws the node on the screen
        :param window: The pygame window
        """

        pygame.draw.rect(
            window,
            self.type.value,
            (self.row * SQUARE_SIZE, self.col * SQUARE_SIZE,
             SQUARE_SIZE, SQUARE_SIZE)
        )

    def make_end(self) -> None:
        self.type = NodeType.END

    def make_barrier(self) -> None:
        self.type = NodeType.BARRIER

    def make_open(self):
        self.type = NodeType.OPEN

    def make_closed(self):
        self.type = NodeType.CLOSED

    def make_path(self):
        self.type = NodeType.PATH

    def reset(self) -> None:
        self.type = NodeType.BLANK

    def is_barrier(self) -> bool:
        return self.type == NodeType.BARRIER

    def is_end(self) -> bool:
        return self.type == NodeType.END

    def is_blank(self):
        return self.type == NodeType.BLANK

    def get_pos(self) -> tuple[int, int]:
        return self.row, self.col

    def __lt__(self, other):
        return self.total_cost < other.total_cost
