from enum import Enum

from constants import GREEN, RED, BLACK, WHITE, BLUE


class NodeType(Enum):
    """
    This class represents the type of each square in the grid
    """

    END = RED
    BARRIER = BLACK
    BLANK = WHITE
    OPEN = GREEN
    CLOSED = RED
    PATH = BLUE
