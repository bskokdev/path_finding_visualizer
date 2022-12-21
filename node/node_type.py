from enum import Enum

from constants import GREEN, RED, BLACK, WHITE, BLUE

"""
This class represents type of each square in the grid
"""
class NodeType(Enum):
    END = RED
    BARRIER = BLACK
    BLANK = WHITE
    OPEN = GREEN
    CLOSED = RED
    PATH = BLUE

