
from enum import Enum

# Enum for colors
class Color(Enum):
    colorless = 0
    red = 1
    green = 2
    darkblue = 3
    lightblue = 4
    yellow = 5
    purple = 6

class Direction(Enum):
    up = 1
    right = 2
    down = 3
    left = 4

# Enum for path and "blobs"
class MapObject(Enum):
    empty = 0
    blob = 1
    path = 2
