import enum


class Colors(tuple[int, int, int], enum.Enum):
    white = (255, 255, 255)
    red = (255, 0, 0)
